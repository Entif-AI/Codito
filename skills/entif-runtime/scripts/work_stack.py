#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = "0.1"
TASK_STATES = {
    "planned", "executing", "receipt_observed", "verified", "committed",
    "failed", "safe_hold", "reconciled_retryable", "stale", "cancelled"
}
SIDE_EFFECT_CLASSES = {"none", "idempotent", "reconcile_before_retry", "non_idempotent"}
FAILURE_POLICIES = {"retry", "reconcile", "safe_hold", "abort"}


def now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def atomic_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def stable_digest(obj):
    data = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def load_work(work_dir: Path):
    p = work_dir / "WORK.json"
    if not p.exists():
        raise SystemExit(f"Not a work-stack directory: {work_dir}")
    return read_json(p)


def task_path(work_dir: Path, task_id: str):
    return work_dir / "tasks" / f"{task_id}.json"


def load_task(work_dir: Path, task_id: str):
    p = task_path(work_dir, task_id)
    if not p.exists():
        raise SystemExit(f"Unknown task: {task_id}")
    return read_json(p)


def save_task(work_dir: Path, task):
    task["updated_at"] = now()
    atomic_json(task_path(work_dir, task["task_id"]), task)


def all_tasks(work_dir: Path):
    out = {}
    for p in sorted((work_dir / "tasks").glob("*.json")):
        t = read_json(p)
        out[t["task_id"]] = t
    return out


def append_event(work_dir: Path, event: str, task_id=None, data=None):
    ep = work_dir / "EVENTS.jsonl"
    seq = 1
    prev = None
    if ep.exists() and ep.stat().st_size:
        lines = [x for x in ep.read_text(encoding="utf-8").splitlines() if x.strip()]
        last = json.loads(lines[-1])
        seq = int(last["seq"]) + 1
        prev = last["digest"]
    rec = {
        "seq": seq,
        "ts": now(),
        "work_id": load_work(work_dir)["work_id"],
        "event": event,
        "task_id": task_id,
        "data": data or {},
        "prev_digest": prev,
    }
    rec["digest"] = stable_digest(rec)
    with ep.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, sort_keys=True, ensure_ascii=False) + "\n")
    return rec


def snapshot_files(items):
    snap = {}
    for raw in items:
        p = Path(raw).expanduser().resolve()
        if not p.exists() or not p.is_file():
            snap[str(p)] = {"exists": False, "sha256": None, "bytes": None}
        else:
            snap[str(p)] = {"exists": True, "sha256": sha256_file(p), "bytes": p.stat().st_size}
    return snap


def deps_committed(task, tasks):
    for dep in task.get("depends_on", []):
        if dep not in tasks or tasks[dep].get("state") != "committed":
            return False
    return True


def derived_ready(task, tasks):
    state = task.get("state")
    if state == "planned":
        return deps_committed(task, tasks)
    if state == "reconciled_retryable":
        return deps_committed(task, tasks)
    if state == "failed" and task.get("side_effect_class") in {"none", "idempotent"}:
        return deps_committed(task, tasks)
    return False


def materialize_status(work_dir: Path):
    w = load_work(work_dir)
    tasks = all_tasks(work_dir)
    groups = {}
    for tid, t in tasks.items():
        state = t.get("state", "unknown")
        groups.setdefault(state, []).append(tid)
    ready = [tid for tid, t in tasks.items() if derived_ready(t, tasks)]
    blocked = [tid for tid, t in tasks.items() if t.get("state") == "planned" and tid not in ready]
    status = {
        "schema_version": SCHEMA,
        "work_id": w["work_id"],
        "title": w["title"],
        "parent_work_id": w.get("parent_work_id"),
        "task_count": len(tasks),
        "ready": sorted(ready),
        "blocked": sorted(blocked),
        "states": {k: sorted(v) for k, v in sorted(groups.items())},
        "updated_at": now(),
    }
    atomic_json(work_dir / "STATUS.json", status)
    return status


def cmd_init(a):
    base = Path(a.root).expanduser().resolve()
    work_id = a.work_id or str(uuid.uuid4())
    work_dir = base / work_id
    if work_dir.exists():
        raise SystemExit(f"Work directory already exists: {work_dir}")
    for d in ["tasks", "receipts", "children"]:
        (work_dir / d).mkdir(parents=True, exist_ok=True)
    work = {
        "schema_version": SCHEMA,
        "work_id": work_id,
        "title": a.title,
        "parent_work_id": a.parent_work_id,
        "created_at": now(),
        "state": "active",
    }
    atomic_json(work_dir / "WORK.json", work)
    append_event(work_dir, "work_initialized", data={"title": a.title, "parent_work_id": a.parent_work_id})
    materialize_status(work_dir)
    print(str(work_dir))


def cmd_spawn_child(a):
    parent = Path(a.work).expanduser().resolve()
    pw = load_work(parent)
    child_id = a.work_id or str(uuid.uuid4())
    child_dir = parent / "children" / child_id
    for d in ["tasks", "receipts", "children"]:
        (child_dir / d).mkdir(parents=True, exist_ok=True)
    work = {
        "schema_version": SCHEMA,
        "work_id": child_id,
        "title": a.title,
        "parent_work_id": pw["work_id"],
        "created_at": now(),
        "state": "active",
    }
    atomic_json(child_dir / "WORK.json", work)
    append_event(child_dir, "work_initialized", data={"title": a.title, "parent_work_id": pw["work_id"]})
    append_event(parent, "child_spawned", data={"child_work_id": child_id, "path": str(child_dir)})
    materialize_status(child_dir)
    materialize_status(parent)
    print(str(child_dir))


def parse_csv_arg(raw):
    if not raw:
        return []
    vals = []
    for item in raw:
        vals.extend([x.strip() for x in item.split(",") if x.strip()])
    return vals


def cmd_add_task(a):
    wd = Path(a.work).expanduser().resolve()
    w = load_work(wd)
    tasks = all_tasks(wd)
    tid = a.task_id or f"T{len(tasks)+1:03d}"
    if tid in tasks:
        raise SystemExit(f"Task already exists: {tid}")
    deps = parse_csv_arg(a.depends_on)
    missing = [d for d in deps if d not in tasks]
    if missing:
        raise SystemExit(f"Unknown dependencies: {', '.join(missing)}")
    sec = a.side_effect_class
    if sec not in SIDE_EFFECT_CLASSES:
        raise SystemExit(f"Invalid side-effect class: {sec}")
    if sec != "none" and not a.idempotency_key:
        raise SystemExit("Side-effecting tasks require --idempotency-key")
    task = {
        "schema_version": SCHEMA,
        "work_id": w["work_id"],
        "task_id": tid,
        "title": a.title,
        "state": "planned",
        "depends_on": deps,
        "idempotency_key": a.idempotency_key or f"local:{w['work_id']}:{tid}",
        "side_effect_class": sec,
        "failure_policy": a.failure_policy,
        "success_predicate": a.success_predicate or "explicit verification required",
        "input_files": [str(Path(x).expanduser().resolve()) for x in (a.input_file or [])],
        "output_files": [str(Path(x).expanduser().resolve()) for x in (a.output_file or [])],
        "input_refs": a.input_ref or [],
        "output_refs": a.output_ref or [],
        "attempt_count": 0,
        "latest_attempt_id": None,
        "receipts": [],
        "input_snapshot": {},
        "output_snapshot": {},
        "created_at": now(),
        "updated_at": now(),
    }
    save_task(wd, task)
    append_event(wd, "task_added", tid, {"depends_on": deps, "side_effect_class": sec})
    materialize_status(wd)
    print(tid)


def cmd_start(a):
    wd = Path(a.work).expanduser().resolve()
    tasks = all_tasks(wd)
    t = load_task(wd, a.task)
    if t["state"] == "committed":
        print(json.dumps({"task_id": a.task, "state": "committed", "noop": True}))
        return
    if t["state"] in {"executing", "receipt_observed", "verified", "safe_hold"}:
        raise SystemExit(f"Task {a.task} is {t['state']}; reconcile/finish before replay")
    if not derived_ready(t, tasks):
        raise SystemExit(f"Task {a.task} is not ready; dependencies or replay policy block it")
    t["attempt_count"] += 1
    attempt_id = str(uuid.uuid4())
    t["latest_attempt_id"] = attempt_id
    t["input_snapshot"] = snapshot_files(t.get("input_files", []))
    t["state"] = "executing"
    save_task(wd, t)
    append_event(wd, "task_started", a.task, {"attempt_id": attempt_id, "attempt_count": t["attempt_count"]})
    materialize_status(wd)
    print(attempt_id)


def cmd_receipt(a):
    wd = Path(a.work).expanduser().resolve()
    t = load_task(wd, a.task)
    if t["state"] not in {"executing", "receipt_observed"}:
        raise SystemExit(f"Task {a.task} cannot accept receipt from state {t['state']}")
    rid = a.receipt_id or str(uuid.uuid4())
    rec = {
        "schema_version": SCHEMA,
        "receipt_id": rid,
        "work_id": t["work_id"],
        "task_id": t["task_id"],
        "attempt_id": t.get("latest_attempt_id"),
        "receipt_ref": a.receipt_ref,
        "note": a.note,
        "observed_at": now(),
    }
    rp = wd / "receipts" / f"{t['task_id']}-{rid}.json"
    atomic_json(rp, rec)
    if rid not in t["receipts"]:
        t["receipts"].append(rid)
    t["state"] = "receipt_observed"
    save_task(wd, t)
    append_event(wd, "receipt_observed", a.task, {"receipt_id": rid, "receipt_ref": a.receipt_ref})
    materialize_status(wd)
    print(rid)


def cmd_verify(a):
    wd = Path(a.work).expanduser().resolve()
    t = load_task(wd, a.task)
    if t["state"] not in {"executing", "receipt_observed"}:
        raise SystemExit(f"Task {a.task} cannot verify from state {t['state']}")
    if t["side_effect_class"] != "none" and not t.get("receipts"):
        raise SystemExit("External side-effect task requires a recorded receipt before verification")
    outs = snapshot_files(t.get("output_files", []))
    missing = [p for p, meta in outs.items() if not meta["exists"]]
    if missing:
        raise SystemExit("Missing declared output files: " + ", ".join(missing))
    t["output_snapshot"] = outs
    t["state"] = "verified"
    save_task(wd, t)
    append_event(wd, "task_verified", a.task, {"note": a.note or "", "outputs": outs})
    materialize_status(wd)
    print(json.dumps({"task_id": a.task, "state": "verified"}))


def compare_snapshot(snapshot):
    issues = []
    for raw, old in snapshot.items():
        p = Path(raw)
        exists = p.exists() and p.is_file()
        if exists != bool(old.get("exists")):
            issues.append(f"existence changed: {raw}")
            continue
        if exists:
            current = sha256_file(p)
            if current != old.get("sha256"):
                issues.append(f"sha256 changed: {raw}")
    return issues


def cmd_commit(a):
    wd = Path(a.work).expanduser().resolve()
    tasks = all_tasks(wd)
    t = load_task(wd, a.task)
    if t["state"] == "committed":
        print(json.dumps({"task_id": a.task, "state": "committed", "noop": True}))
        return
    if t["state"] != "verified":
        raise SystemExit(f"Task {a.task} must be verified before commit; state={t['state']}")
    if not deps_committed(t, tasks):
        raise SystemExit(f"Task {a.task} has uncommitted dependencies")
    drift = compare_snapshot(t.get("input_snapshot", {})) + compare_snapshot(t.get("output_snapshot", {}))
    if drift:
        raise SystemExit("Cannot commit with snapshot drift: " + "; ".join(drift))
    t["state"] = "committed"
    t["committed_at"] = now()
    save_task(wd, t)
    append_event(wd, "task_committed", a.task, {"attempt_id": t.get("latest_attempt_id")})
    materialize_status(wd)
    print(json.dumps({"task_id": a.task, "state": "committed"}))


def cmd_fail(a):
    wd = Path(a.work).expanduser().resolve()
    t = load_task(wd, a.task)
    if t["state"] == "committed":
        raise SystemExit("Cannot fail a committed task; invalidate it instead")
    ambiguous = bool(a.ambiguous)
    if ambiguous and t["side_effect_class"] in {"reconcile_before_retry", "non_idempotent"}:
        t["state"] = "safe_hold"
    else:
        t["state"] = "failed"
    t["last_failure"] = {"reason": a.reason, "ambiguous": ambiguous, "at": now()}
    save_task(wd, t)
    append_event(wd, "task_failed", a.task, t["last_failure"])
    materialize_status(wd)
    print(json.dumps({"task_id": a.task, "state": t["state"]}))


def cmd_reconcile(a):
    wd = Path(a.work).expanduser().resolve()
    t = load_task(wd, a.task)
    if t["state"] not in {"safe_hold", "failed", "executing", "receipt_observed"}:
        raise SystemExit(f"Task {a.task} does not require reconciliation from state {t['state']}")
    outcome = a.outcome
    if outcome == "retryable":
        t["state"] = "reconciled_retryable"
    elif outcome == "not_executed":
        t["state"] = "reconciled_retryable"
    elif outcome == "safe_hold":
        t["state"] = "safe_hold"
    elif outcome == "verified_external":
        if not t.get("receipts") and not a.receipt_ref:
            raise SystemExit("verified_external reconciliation requires an existing or supplied receipt")
        if a.receipt_ref:
            rid = str(uuid.uuid4())
            rec = {"schema_version": SCHEMA, "receipt_id": rid, "work_id": t["work_id"], "task_id": t["task_id"], "attempt_id": t.get("latest_attempt_id"), "receipt_ref": a.receipt_ref, "note": a.note, "observed_at": now(), "reconciliation": True}
            atomic_json(wd / "receipts" / f"{t['task_id']}-{rid}.json", rec)
            t["receipts"].append(rid)
        t["state"] = "receipt_observed"
    else:
        raise SystemExit(f"Unknown reconciliation outcome: {outcome}")
    save_task(wd, t)
    append_event(wd, "task_reconciled", a.task, {"outcome": outcome, "note": a.note or ""})
    materialize_status(wd)
    print(json.dumps({"task_id": a.task, "state": t["state"]}))


def dependent_closure(tasks, roots):
    result = set(roots)
    changed = True
    while changed:
        changed = False
        for tid, t in tasks.items():
            if tid not in result and any(dep in result for dep in t.get("depends_on", [])):
                result.add(tid)
                changed = True
    return result


def cmd_invalidate(a):
    wd = Path(a.work).expanduser().resolve()
    tasks = all_tasks(wd)
    if a.task not in tasks:
        raise SystemExit(f"Unknown task: {a.task}")
    targets = dependent_closure(tasks, [a.task]) if a.cascade else {a.task}
    for tid in sorted(targets):
        t = tasks[tid]
        if t["state"] != "cancelled":
            t["state"] = "stale"
            t["stale_reason"] = a.reason
            save_task(wd, t)
            append_event(wd, "task_invalidated", tid, {"reason": a.reason, "cascade_root": a.task})
    materialize_status(wd)
    print(json.dumps({"invalidated": sorted(targets)}))


def validate_events(work_dir: Path, issues):
    ep = work_dir / "EVENTS.jsonl"
    if not ep.exists():
        issues.append("EVENTS.jsonl missing")
        return
    prev = None
    expected = 1
    for line_no, line in enumerate(ep.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except Exception as e:
            issues.append(f"event line {line_no} invalid JSON: {e}")
            continue
        if rec.get("seq") != expected:
            issues.append(f"event sequence mismatch at line {line_no}: expected {expected}, got {rec.get('seq')}")
        if rec.get("prev_digest") != prev:
            issues.append(f"event prev_digest mismatch at line {line_no}")
        digest = rec.get("digest")
        base = dict(rec)
        base.pop("digest", None)
        if digest != stable_digest(base):
            issues.append(f"event digest mismatch at line {line_no}")
        prev = digest
        expected += 1


def cycle_check(tasks, issues):
    visiting, visited = set(), set()
    def dfs(tid):
        if tid in visiting:
            issues.append(f"dependency cycle detected at {tid}")
            return
        if tid in visited:
            return
        visiting.add(tid)
        for dep in tasks[tid].get("depends_on", []):
            if dep in tasks:
                dfs(dep)
        visiting.remove(tid)
        visited.add(tid)
    for tid in tasks:
        dfs(tid)


def validate_work(work_dir: Path):
    issues = []
    w = load_work(work_dir)
    tasks = all_tasks(work_dir)
    validate_events(work_dir, issues)
    keys = {}
    for tid, t in tasks.items():
        if t.get("work_id") != w["work_id"]:
            issues.append(f"{tid}: work_id mismatch")
        if t.get("state") not in TASK_STATES:
            issues.append(f"{tid}: invalid state {t.get('state')}")
        if t.get("side_effect_class") not in SIDE_EFFECT_CLASSES:
            issues.append(f"{tid}: invalid side_effect_class")
        for dep in t.get("depends_on", []):
            if dep not in tasks:
                issues.append(f"{tid}: missing dependency {dep}")
        key = t.get("idempotency_key")
        if key:
            if key in keys and keys[key] != tid:
                issues.append(f"idempotency key collision: {key} on {keys[key]} and {tid}")
            keys[key] = tid
        if t.get("state") == "committed":
            if not deps_committed(t, tasks):
                issues.append(f"{tid}: committed while dependency is not committed")
            for msg in compare_snapshot(t.get("input_snapshot", {})):
                issues.append(f"{tid}: stale committed input: {msg}")
            for msg in compare_snapshot(t.get("output_snapshot", {})):
                issues.append(f"{tid}: committed output drift: {msg}")
            if t.get("side_effect_class") != "none" and not t.get("receipts"):
                issues.append(f"{tid}: committed side effect has no receipt")
    cycle_check(tasks, issues)
    return issues


def cmd_validate(a):
    wd = Path(a.work).expanduser().resolve()
    issues = validate_work(wd)
    status = materialize_status(wd)
    report = {"work_id": load_work(wd)["work_id"], "ok": not issues, "issues": issues, "status": status}
    print(json.dumps(report, indent=2, sort_keys=True))
    if issues:
        raise SystemExit(1)


def cmd_status(a):
    wd = Path(a.work).expanduser().resolve()
    print(json.dumps(materialize_status(wd), indent=2, sort_keys=True))


def build_parser():
    p = argparse.ArgumentParser(description="Durable nested mini-task execution ledger")
    sp = p.add_subparsers(dest="cmd", required=True)
    x = sp.add_parser("init"); x.add_argument("--root", required=True); x.add_argument("--title", required=True); x.add_argument("--work-id"); x.add_argument("--parent-work-id"); x.set_defaults(func=cmd_init)
    x = sp.add_parser("spawn-child"); x.add_argument("--work", required=True); x.add_argument("--title", required=True); x.add_argument("--work-id"); x.set_defaults(func=cmd_spawn_child)
    x = sp.add_parser("add-task"); x.add_argument("--work", required=True); x.add_argument("--title", required=True); x.add_argument("--task-id"); x.add_argument("--depends-on", action="append"); x.add_argument("--side-effect-class", default="none", choices=sorted(SIDE_EFFECT_CLASSES)); x.add_argument("--idempotency-key"); x.add_argument("--failure-policy", default="reconcile", choices=sorted(FAILURE_POLICIES)); x.add_argument("--success-predicate"); x.add_argument("--input-file", action="append"); x.add_argument("--output-file", action="append"); x.add_argument("--input-ref", action="append"); x.add_argument("--output-ref", action="append"); x.set_defaults(func=cmd_add_task)
    x = sp.add_parser("start"); x.add_argument("--work", required=True); x.add_argument("--task", required=True); x.set_defaults(func=cmd_start)
    x = sp.add_parser("receipt"); x.add_argument("--work", required=True); x.add_argument("--task", required=True); x.add_argument("--receipt-id"); x.add_argument("--receipt-ref", required=True); x.add_argument("--note"); x.set_defaults(func=cmd_receipt)
    x = sp.add_parser("verify"); x.add_argument("--work", required=True); x.add_argument("--task", required=True); x.add_argument("--note"); x.set_defaults(func=cmd_verify)
    x = sp.add_parser("commit"); x.add_argument("--work", required=True); x.add_argument("--task", required=True); x.set_defaults(func=cmd_commit)
    x = sp.add_parser("fail"); x.add_argument("--work", required=True); x.add_argument("--task", required=True); x.add_argument("--reason", required=True); x.add_argument("--ambiguous", action="store_true"); x.set_defaults(func=cmd_fail)
    x = sp.add_parser("reconcile"); x.add_argument("--work", required=True); x.add_argument("--task", required=True); x.add_argument("--outcome", required=True, choices=["retryable", "not_executed", "safe_hold", "verified_external"]); x.add_argument("--receipt-ref"); x.add_argument("--note"); x.set_defaults(func=cmd_reconcile)
    x = sp.add_parser("invalidate"); x.add_argument("--work", required=True); x.add_argument("--task", required=True); x.add_argument("--reason", required=True); x.add_argument("--cascade", action="store_true"); x.set_defaults(func=cmd_invalidate)
    x = sp.add_parser("status"); x.add_argument("--work", required=True); x.set_defaults(func=cmd_status)
    x = sp.add_parser("validate"); x.add_argument("--work", required=True); x.set_defaults(func=cmd_validate)
    return p


def main():
    a = build_parser().parse_args()
    a.func(a)


if __name__ == "__main__":
    main()

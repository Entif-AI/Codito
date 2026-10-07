#!/usr/bin/env python3
"""Validate and discover Entif Runtime handoff/recovery state.

This helper chooses a starting recovery source and emits concise narration.
It does not decide semantic correctness or authorize replay of side effects.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

SCHEMA_ID = "entif.runtime.handoff/v1"
KINDS = {"checkpoint", "transfer", "completion", "emergency"}
SURFACES = {"chat", "codex", "unknown"}
REQUIRED = [
    "schema",
    "handoff_id",
    "kind",
    "created_at",
    "runtime_surface",
    "reason",
    "mission",
    "refs",
    "work",
    "checkpoint",
    "completed",
    "negative_knowledge",
    "unresolved",
    "next_safe_operations",
    "hydration",
    "verification",
    "cleanup",
]


def validate(path: Path) -> tuple[int, dict]:
    try:
        data = json.loads(path.read_text())
    except Exception as exc:
        return 1, {"ok": False, "errors": [f"invalid_json: {exc}"]}

    errors = [key for key in REQUIRED if key not in data]
    if data.get("schema") != SCHEMA_ID:
        errors.append("schema")
    if data.get("kind") not in KINDS:
        errors.append("kind")
    if data.get("runtime_surface") not in SURFACES:
        errors.append("runtime_surface")
    hydration = data.get("hydration")
    if isinstance(hydration, dict):
        for key in ("read_first", "read_if_needed", "read_if_condition"):
            if key not in hydration:
                errors.append(f"hydration.{key}")
    else:
        errors.append("hydration")
    for key in ("completed", "negative_knowledge", "unresolved", "next_safe_operations", "verification"):
        if key in data and not isinstance(data[key], list):
            errors.append(key)
    errors = sorted(set(errors))
    return (0 if not errors else 1), {"ok": not errors, "errors": errors, "kind": data.get("kind"), "handoff_id": data.get("handoff_id")}


def latest_checkpoint(root: Path) -> Path | None:
    candidates = []
    for base in [
        root / ".entif/runtime/durability/checkpoints",
        root / ".entif/runtime/checkpoints",
    ]:
        if base.exists():
            candidates.extend(p for p in base.glob("CP*") if p.is_dir())
    return sorted(candidates, key=lambda p: p.name)[-1] if candidates else None


def work_stack_status(root: Path) -> Path | None:
    base = root / ".entif/runtime/work"
    if not base.exists():
        return None
    hits = sorted(base.rglob("STATUS.json"))
    return hits[-1] if hits else None


def discover(repo: Path, explicit_handoff: Path | None, recovery_log: Path | None) -> dict:
    root = repo.resolve()
    narration: list[str] = []

    if explicit_handoff and explicit_handoff.exists():
        narration.append(f"Recovery: explicit handoff found at {explicit_handoff}; validating.")
        return {"route": "handoff", "source": str(explicit_handoff), "narration": narration}

    local_handoff = root / ".entif/runtime/HANDOFF.json"
    if local_handoff.exists():
        narration.append(f"Recovery: runtime handoff found at {local_handoff}; validating.")
        return {"route": "handoff", "source": str(local_handoff), "narration": narration}

    narration.append("Recovery: explicit handoff not found; checking Work Stack.")
    ws = work_stack_status(root)
    if ws:
        narration.append(f"Recovery: Work Stack found at {ws}; validating task and receipt state before replay.")
        return {"route": "work_stack", "source": str(ws), "narration": narration}

    narration.append("Recovery: Work Stack not found; locating latest verified checkpoint.")
    cp = latest_checkpoint(root)
    if cp:
        narration.append(f"Recovery: extracting checkpoint {cp.name}; verifying checkpoint receipt before hydration.")
        return {"route": "checkpoint", "source": str(cp), "narration": narration}

    narration.append("Recovery: structured checkpoint not found; checking feature/Git recovery state.")
    feature_log = root / "FEATURE_LOG.md"
    if feature_log.exists():
        narration.append(f"Recovery: FEATURE_LOG.md found at {feature_log}; reconciling it with live Git/issue/PR state.")
        return {"route": "feature_log", "source": str(feature_log), "narration": narration}

    if recovery_log and recovery_log.exists():
        narration.append("Recovery: no structured runtime state survived; parsing reduced run trace as last-resort evidence.")
        return {"route": "reduced_trace", "source": str(recovery_log), "narration": narration}

    narration.append("Recovery: no handoff, Work Stack, checkpoint, feature log, or supplied reduced trace was found.")
    return {"route": "none", "source": None, "narration": narration}


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("validate")
    v.add_argument("path")

    d = sub.add_parser("discover")
    d.add_argument("--repo", default=".")
    d.add_argument("--handoff")
    d.add_argument("--recovery-log")

    args = parser.parse_args()
    if args.cmd == "validate":
        rc, out = validate(Path(args.path))
    else:
        out = discover(
            Path(args.repo),
            Path(args.handoff) if args.handoff else None,
            Path(args.recovery_log) if args.recovery_log else None,
        )
        rc = 0
    print(json.dumps(out, indent=2, sort_keys=True))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())

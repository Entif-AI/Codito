#!/usr/bin/env python3
import argparse
import csv
import hashlib
import json
import os
import shutil
import sys
import uuid
import zipfile
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = "entif.run-durability/v1"


def now():
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def atomic_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    os.replace(tmp, path)


def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def ensure_run(run: Path):
    for name in ['RUN_START.json', 'STATE.json']:
        if not (run / name).exists():
            raise SystemExit(f"missing {name}: {run}")


def append_event(run: Path, event_type: str, payload: dict):
    p = run / 'EVENTS.jsonl'
    prev_hash = None
    seq = 1
    if p.exists() and p.stat().st_size:
        with p.open('rb') as f:
            lines = [ln for ln in f.read().splitlines() if ln.strip()]
        last = json.loads(lines[-1])
        prev_hash = last['event_hash']
        seq = last['seq'] + 1
    body = {
        'schema': SCHEMA,
        'seq': seq,
        'recorded_at': now(),
        'type': event_type,
        'payload': payload,
        'prev_event_hash': prev_hash,
    }
    encoded = json.dumps(body, sort_keys=True, separators=(',', ':')).encode()
    body['event_hash'] = hashlib.sha256(encoded).hexdigest()
    with p.open('a', encoding='utf-8') as f:
        f.write(json.dumps(body, sort_keys=True) + '\n')
    return body


def iter_files(root: Path, excludes):
    ex = set(excludes or [])
    for p in sorted(root.rglob('*')):
        if not p.is_file():
            continue
        rel = p.relative_to(root).as_posix()
        if any(rel == e or rel.startswith(e.rstrip('/') + '/') for e in ex):
            continue
        yield rel, p


def scan_manifest(root: Path, excludes):
    out = {}
    for rel, p in iter_files(root, excludes):
        out[rel] = {'sha256': sha256_file(p), 'bytes': p.stat().st_size}
    return out


def cp_sort_key(cp):
    try:
        return int(cp[2:])
    except Exception:
        return 10**9


def next_checkpoint_id(run: Path):
    cps = []
    croot = run / 'checkpoints'
    if croot.exists():
        cps = [p.name for p in croot.iterdir() if p.is_dir() and p.name.startswith('CP')]
    n = max([cp_sort_key(x) for x in cps] or [0]) + 1
    return f"CP{n:04d}"


def write_status(run: Path):
    start = load_json(run / 'RUN_START.json')
    state = load_json(run / 'STATE.json')
    cps = state.get('checkpoints', {})
    latest = None
    for cp in sorted(cps, key=cp_sort_key):
        if checkpoint_policy_satisfied(start, state, cp, for_draft=False):
            latest = cp
    pending = []
    for cp, rec in cps.items():
        if not checkpoint_policy_satisfied(start, state, cp, for_draft=False):
            pending.append(cp)
    dc = state.get('draft_complete', {})
    dc_uncovered = []
    for rel, meta in dc.items():
        cp = meta['checkpoint_id']
        if not checkpoint_policy_satisfied(start, state, cp, for_draft=True):
            dc_uncovered.append(rel)
    status = {
        'schema': SCHEMA,
        'run_id': start['run_id'],
        'title': start['title'],
        'updated_at': now(),
        'primary_channel': start['policy']['primary_channel'],
        'witness_mode': start['policy']['witness_mode'],
        'startup_policy_ready': startup_policy_satisfied(start, state),
        'startup_receipts': state.get('startup_receipts', {}),
        'latest_policy_durable_checkpoint': latest,
        'checkpoint_count': len(cps),
        'pending_checkpoints': sorted(pending, key=cp_sort_key),
        'draft_complete_count': len(dc),
        'draft_complete_uncovered': dc_uncovered,
        'latest_freeze': state.get('latest_freeze'),
        'next_action': state.get('next_action'),
        'blocking_condition': state.get('blocking_condition'),
    }
    atomic_json(run / 'STATUS.json', status)
    return status


def channel_receipts(state, cp, channel):
    return state.get('receipts', {}).get(cp, {}).get(channel, [])


def startup_policy_satisfied(start, state):
    primary = start['policy']['primary_channel']
    if not state.get('startup_receipts', {}).get(primary):
        return False
    if start['policy']['witness_mode'] == 'required' and not state.get('startup_receipts', {}).get('witness'):
        return False
    return True


def checkpoint_policy_satisfied(start, state, cp, for_draft=False):
    primary = start['policy']['primary_channel']
    if not channel_receipts(state, cp, primary):
        return False
    if for_draft and start['policy']['witness_mode'] == 'required':
        if not channel_receipts(state, cp, 'witness'):
            return False
    return True


def cmd_init(args):
    base = Path(args.root).resolve()
    base.mkdir(parents=True, exist_ok=True)
    run_id = args.run_id or str(uuid.uuid4())
    run = base / run_id
    if run.exists():
        raise SystemExit(f"run already exists: {run}")
    run.mkdir(parents=True)
    for d in ['checkpoints', 'freezes', 'ExternalPersistence']:
        (run / d).mkdir()
    policy = {
        'primary_channel': args.primary_channel,
        'witness_mode': args.witness_mode,
        'witness_recipient': args.witness_recipient,
        'remote_parent_ref': args.remote_parent_ref,
        'dirty_ceiling_minutes': args.dirty_ceiling_minutes,
        'witness_interval_minutes': args.witness_interval_minutes,
    }
    if args.witness_mode == 'required' and not args.witness_recipient:
        raise SystemExit('required witness mode needs --witness-recipient')
    start = {
        'schema': SCHEMA,
        'run_id': run_id,
        'title': args.title,
        'created_at': now(),
        'project_id': args.project_id,
        'package_version': args.package_version,
        'scope_fingerprint': args.scope_fingerprint,
        'policy': policy,
    }
    state = {
        'schema': SCHEMA,
        'run_id': run_id,
        'checkpoints': {},
        'startup_receipts': {},
        'receipts': {},
        'draft_complete': {},
        'latest_freeze': None,
        'next_action': args.next_action,
        'blocking_condition': None,
    }
    atomic_json(run / 'RUN_START.json', start)
    atomic_json(run / 'STATE.json', state)
    atomic_json(run / 'current-manifest.json', {})
    atomic_json(run / 'ExternalPersistence' / 'remote-index.json', {'schema': SCHEMA, 'run_id': run_id, 'startup_receipts': {}, 'receipts': {}})
    append_event(run, 'run_init', {'run_id': run_id})
    write_status(run)
    print(run)


def cmd_checkpoint(args):
    run = Path(args.run).resolve(); ensure_run(run)
    root = Path(args.track_root).resolve()
    if not root.is_dir():
        raise SystemExit(f"track root not found: {root}")
    old = load_json(run / 'current-manifest.json')
    new = scan_manifest(root, args.exclude)
    changes = []
    for rel in sorted(set(old) | set(new)):
        if rel not in old:
            changes.append(('ADD', rel, new[rel]))
        elif rel not in new:
            changes.append(('DELETE', rel, old[rel]))
        elif old[rel]['sha256'] != new[rel]['sha256']:
            changes.append(('MODIFY', rel, new[rel]))
    if not changes and not args.allow_empty:
        raise SystemExit('no changed files since prior checkpoint')
    cp = next_checkpoint_id(run)
    cpdir = run / 'checkpoints' / cp
    cpdir.mkdir(parents=True)
    delta_dir = cpdir / 'delta'; delta_dir.mkdir()
    rows = []
    for action, rel, meta in changes:
        row = {'action': action, 'logical_path': rel, 'bytes': meta.get('bytes', 0), 'sha256': meta.get('sha256', '')}
        rows.append(row)
        if action != 'DELETE':
            src = root / rel
            dst = delta_dir / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    draft_set = set(args.draft_complete or [])
    for rel in draft_set:
        if rel not in new:
            raise SystemExit(f"draft-complete path is not present in current tree: {rel}")
    checkpoint = {
        'schema': SCHEMA,
        'checkpoint_id': cp,
        'created_at': now(),
        'track_root': str(root),
        'delta_count': len(changes),
        'draft_complete_paths': sorted(draft_set),
        'note': args.note,
    }
    atomic_json(cpdir / 'checkpoint.json', checkpoint)
    atomic_json(cpdir / 'current-manifest.json', new)
    with (cpdir / 'delta-manifest.tsv').open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['action', 'logical_path', 'bytes', 'sha256'], delimiter='\t')
        w.writeheader(); w.writerows(rows)
    bundle = cpdir / f'{cp}.bundle.zip'
    with zipfile.ZipFile(bundle, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for p in sorted(cpdir.rglob('*')):
            if p == bundle or not p.is_file():
                continue
            z.write(p, p.relative_to(cpdir).as_posix())
    bundle_hash = sha256_file(bundle)
    state = load_json(run / 'STATE.json')
    state['checkpoints'][cp] = {
        'bundle_path': str(bundle),
        'bundle_sha256': bundle_hash,
        'bundle_bytes': bundle.stat().st_size,
        'delta_count': len(changes),
        'created_at': checkpoint['created_at'],
    }
    state.setdefault('receipts', {})[cp] = {}
    for rel in draft_set:
        state['draft_complete'][rel] = {'sha256': new[rel]['sha256'], 'checkpoint_id': cp, 'declared_at': now()}
    # Existing draft-complete paths changed without explicit re-declaration are no longer draft-complete.
    for rel in list(state['draft_complete']):
        if rel not in new or state['draft_complete'][rel]['sha256'] != new[rel]['sha256']:
            if rel not in draft_set:
                del state['draft_complete'][rel]
    if args.next_action is not None:
        state['next_action'] = args.next_action
    atomic_json(run / 'STATE.json', state)
    atomic_json(run / 'current-manifest.json', new)
    append_event(run, 'checkpoint_prepared', {'checkpoint_id': cp, 'bundle_sha256': bundle_hash, 'delta_count': len(changes)})
    write_status(run)
    print(json.dumps({'checkpoint_id': cp, 'bundle': str(bundle), 'sha256': bundle_hash, 'delta_count': len(changes)}, indent=2))



def cmd_startup_receipt(args):
    run = Path(args.run).resolve(); ensure_run(run)
    start = load_json(run / 'RUN_START.json')
    state = load_json(run / 'STATE.json')
    local_hash = sha256_file(run / 'RUN_START.json')
    if args.remote_sha256 and args.remote_sha256.lower() != local_hash.lower():
        raise SystemExit('remote SHA-256 does not match local RUN_START.json')
    if args.channel == 'witness' and not args.recipient:
        raise SystemExit('witness startup receipt requires --recipient')
    rec = {
        'schema': SCHEMA,
        'subject': 'RUN_START.json',
        'channel': args.channel,
        'recorded_at': now(),
        'remote_id': args.remote_id,
        'remote_url': args.remote_url,
        'recipient': args.recipient,
        'verification_ref': args.verification_ref,
        'remote_sha256': args.remote_sha256,
        'local_sha256': local_hash,
    }
    state.setdefault('startup_receipts', {}).setdefault(args.channel, []).append(rec)
    atomic_json(run / 'STATE.json', state)
    idxp = run / 'ExternalPersistence' / 'remote-index.json'
    idx = load_json(idxp)
    idx.setdefault('startup_receipts', {}).setdefault(args.channel, []).append(rec)
    atomic_json(idxp, idx)
    append_event(run, 'startup_receipt_recorded', {'channel': args.channel, 'remote_id': args.remote_id})
    write_status(run)
    print(json.dumps(rec, indent=2))

def cmd_receipt(args):
    run = Path(args.run).resolve(); ensure_run(run)
    state = load_json(run / 'STATE.json')
    if args.checkpoint not in state.get('checkpoints', {}):
        raise SystemExit(f"unknown checkpoint: {args.checkpoint}")
    cpmeta = state['checkpoints'][args.checkpoint]
    if args.remote_sha256 and args.remote_sha256.lower() != cpmeta['bundle_sha256'].lower():
        raise SystemExit('remote SHA-256 does not match local checkpoint bundle')
    if args.channel == 'witness' and not args.recipient:
        raise SystemExit('witness receipt requires --recipient')
    rec = {
        'schema': SCHEMA,
        'checkpoint_id': args.checkpoint,
        'channel': args.channel,
        'recorded_at': now(),
        'remote_id': args.remote_id,
        'remote_url': args.remote_url,
        'recipient': args.recipient,
        'verification_ref': args.verification_ref,
        'remote_sha256': args.remote_sha256,
        'local_bundle_sha256': cpmeta['bundle_sha256'],
    }
    state.setdefault('receipts', {}).setdefault(args.checkpoint, {}).setdefault(args.channel, []).append(rec)
    atomic_json(run / 'STATE.json', state)
    idxp = run / 'ExternalPersistence' / 'remote-index.json'
    idx = load_json(idxp)
    idx.setdefault('receipts', {}).setdefault(args.checkpoint, {}).setdefault(args.channel, []).append(rec)
    atomic_json(idxp, idx)
    append_event(run, 'receipt_recorded', {'checkpoint_id': args.checkpoint, 'channel': args.channel, 'remote_id': args.remote_id})
    write_status(run)
    print(json.dumps(rec, indent=2))


def cmd_freeze(args):
    run = Path(args.run).resolve(); ensure_run(run)
    start = load_json(run / 'RUN_START.json')
    state = load_json(run / 'STATE.json')
    missing = []
    mappings = []
    for rel, meta in sorted(state.get('draft_complete', {}).items()):
        cp = meta['checkpoint_id']
        if not checkpoint_policy_satisfied(start, state, cp, for_draft=True):
            missing.append(rel)
        mappings.append({
            'logical_path': rel,
            'sha256': meta['sha256'],
            'checkpoint_id': cp,
            'primary_receipts': channel_receipts(state, cp, start['policy']['primary_channel']),
            'witness_receipts': channel_receipts(state, cp, 'witness'),
        })
    if missing:
        raise SystemExit('draft-complete files lack required receipt coverage: ' + ', '.join(missing))
    freeze_id = args.freeze_id or datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    out = run / 'freezes' / f'PRE_QA_FREEZE-{freeze_id}.json'
    freeze = {
        'schema': SCHEMA,
        'freeze_id': freeze_id,
        'created_at': now(),
        'run_id': start['run_id'],
        'draft_complete': mappings,
        'witness_mode': start['policy']['witness_mode'],
        'startup_policy_ready': startup_policy_satisfied(start, state),
        'startup_receipts': state.get('startup_receipts', {}),
        'note': 'This freeze record still requires ordinary external persistence; its own receipt is recorded outside these bytes.',
    }
    atomic_json(out, freeze)
    state['latest_freeze'] = {'freeze_id': freeze_id, 'path': str(out), 'created_at': freeze['created_at']}
    atomic_json(run / 'STATE.json', state)
    append_event(run, 'pre_qa_freeze_prepared', {'freeze_id': freeze_id, 'path': str(out)})
    write_status(run)
    print(out)


def validate_events(run: Path, errors):
    p = run / 'EVENTS.jsonl'
    if not p.exists():
        errors.append('missing EVENTS.jsonl'); return
    prev = None; expected = 1
    for line in p.read_text(encoding='utf-8').splitlines():
        if not line.strip(): continue
        e = json.loads(line)
        if e.get('seq') != expected: errors.append(f"event sequence gap at {expected}")
        if e.get('prev_event_hash') != prev: errors.append(f"event prev hash mismatch at seq {expected}")
        check = {k:v for k,v in e.items() if k != 'event_hash'}
        encoded = json.dumps(check, sort_keys=True, separators=(',', ':')).encode()
        digest = hashlib.sha256(encoded).hexdigest()
        if digest != e.get('event_hash'): errors.append(f"event hash mismatch at seq {expected}")
        prev = e.get('event_hash'); expected += 1


def cmd_validate(args):
    run = Path(args.run).resolve(); ensure_run(run)
    start = load_json(run / 'RUN_START.json'); state = load_json(run / 'STATE.json')
    errors = []
    validate_events(run, errors)
    for channel, recs in state.get('startup_receipts', {}).items():
        for rec in recs:
            if not rec.get('remote_id'):
                errors.append(f"startup/{channel}: receipt missing remote_id")
            if rec.get('local_sha256') != sha256_file(run / 'RUN_START.json'):
                errors.append(f"startup/{channel}: receipt bound to wrong local RUN_START hash")
            if rec.get('remote_sha256') and rec['remote_sha256'] != rec.get('local_sha256'):
                errors.append(f"startup/{channel}: remote hash mismatch")
    if args.require_policy and not startup_policy_satisfied(start, state):
        errors.append('startup persistence policy is not satisfied')
    cpnums = sorted([cp_sort_key(x) for x in state.get('checkpoints', {})])
    if cpnums and cpnums != list(range(1, max(cpnums)+1)):
        errors.append('checkpoint sequence is not contiguous')
    for cp, meta in state.get('checkpoints', {}).items():
        bundle = Path(meta['bundle_path'])
        if not bundle.exists():
            errors.append(f"{cp}: missing bundle")
        elif sha256_file(bundle) != meta['bundle_sha256']:
            errors.append(f"{cp}: bundle SHA-256 mismatch")
        cpdir = run / 'checkpoints' / cp
        if not (cpdir/'checkpoint.json').exists() or not (cpdir/'delta-manifest.tsv').exists():
            errors.append(f"{cp}: incomplete checkpoint directory")
        for channel, recs in state.get('receipts', {}).get(cp, {}).items():
            for rec in recs:
                if not rec.get('remote_id'):
                    errors.append(f"{cp}/{channel}: receipt missing remote_id")
                if rec.get('local_bundle_sha256') != meta['bundle_sha256']:
                    errors.append(f"{cp}/{channel}: receipt bound to wrong local hash")
                if rec.get('remote_sha256') and rec['remote_sha256'] != meta['bundle_sha256']:
                    errors.append(f"{cp}/{channel}: remote hash mismatch")
    current = load_json(run / 'current-manifest.json')
    for rel, meta in state.get('draft_complete', {}).items():
        if rel not in current:
            errors.append(f"draft-complete path missing from current manifest: {rel}")
        elif current[rel]['sha256'] != meta['sha256']:
            errors.append(f"draft-complete hash stale: {rel}")
        elif args.require_policy and not checkpoint_policy_satisfied(start, state, meta['checkpoint_id'], for_draft=True):
            errors.append(f"draft-complete path lacks required receipts: {rel}")
    if state.get('latest_freeze'):
        fp = Path(state['latest_freeze']['path'])
        if not fp.exists(): errors.append('latest freeze file is missing')
    write_status(run)
    if errors:
        print(json.dumps({'ok': False, 'errors': errors}, indent=2)); raise SystemExit(1)
    print(json.dumps({'ok': True, 'run_id': start['run_id'], 'checkpoints': len(state.get('checkpoints', {})), 'draft_complete': len(state.get('draft_complete', {}))}, indent=2))


def cmd_status(args):
    run = Path(args.run).resolve(); ensure_run(run)
    print(json.dumps(write_status(run), indent=2))


def cmd_recovery(args):
    run = Path(args.run).resolve(); ensure_run(run)
    start = load_json(run / 'RUN_START.json'); state = load_json(run / 'STATE.json')
    latest = None
    for cp in sorted(state.get('checkpoints', {}), key=cp_sort_key):
        if checkpoint_policy_satisfied(start, state, cp, for_draft=False): latest = cp
    report = {
        'schema': SCHEMA,
        'run_id': start['run_id'],
        'startup_policy_ready': startup_policy_satisfied(start, state),
        'highest_verified_checkpoint': latest,
        'next_action': state.get('next_action'),
        'blocking_condition': state.get('blocking_condition'),
        'draft_complete_uncovered': write_status(run)['draft_complete_uncovered'],
        'remote_index': str(run / 'ExternalPersistence' / 'remote-index.json'),
    }
    print(json.dumps(report, indent=2))


def build_parser():
    p = argparse.ArgumentParser(description='Feed-forward external durability ledger')
    sp = p.add_subparsers(dest='cmd', required=True)
    s = sp.add_parser('init'); s.add_argument('--root', required=True); s.add_argument('--title', required=True); s.add_argument('--run-id'); s.add_argument('--project-id'); s.add_argument('--package-version'); s.add_argument('--scope-fingerprint'); s.add_argument('--primary-channel', default='drive'); s.add_argument('--witness-mode', choices=['none','optional','required'], default='none'); s.add_argument('--witness-recipient'); s.add_argument('--remote-parent-ref'); s.add_argument('--dirty-ceiling-minutes', type=int, default=10); s.add_argument('--witness-interval-minutes', type=int, default=10); s.add_argument('--next-action'); s.set_defaults(func=cmd_init)
    s = sp.add_parser('startup-receipt'); s.add_argument('--run', required=True); s.add_argument('--channel', required=True); s.add_argument('--remote-id', required=True); s.add_argument('--remote-url'); s.add_argument('--recipient'); s.add_argument('--verification-ref'); s.add_argument('--remote-sha256'); s.set_defaults(func=cmd_startup_receipt)
    s = sp.add_parser('checkpoint'); s.add_argument('--run', required=True); s.add_argument('--track-root', required=True); s.add_argument('--exclude', action='append', default=[]); s.add_argument('--draft-complete', action='append', default=[]); s.add_argument('--note'); s.add_argument('--next-action'); s.add_argument('--allow-empty', action='store_true'); s.set_defaults(func=cmd_checkpoint)
    s = sp.add_parser('receipt'); s.add_argument('--run', required=True); s.add_argument('--checkpoint', required=True); s.add_argument('--channel', required=True); s.add_argument('--remote-id', required=True); s.add_argument('--remote-url'); s.add_argument('--recipient'); s.add_argument('--verification-ref'); s.add_argument('--remote-sha256'); s.set_defaults(func=cmd_receipt)
    s = sp.add_parser('freeze'); s.add_argument('--run', required=True); s.add_argument('--freeze-id'); s.set_defaults(func=cmd_freeze)
    s = sp.add_parser('validate'); s.add_argument('--run', required=True); s.add_argument('--require-policy', action='store_true'); s.set_defaults(func=cmd_validate)
    s = sp.add_parser('status'); s.add_argument('--run', required=True); s.set_defaults(func=cmd_status)
    s = sp.add_parser('recovery-report'); s.add_argument('--run', required=True); s.set_defaults(func=cmd_recovery)
    return p


def main():
    args = build_parser().parse_args()
    args.func(args)

if __name__ == '__main__':
    main()

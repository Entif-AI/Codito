#!/usr/bin/env python3
"""Small deterministic runtime policy helper for Entif Runtime.

This script classifies explicit runtime surface, reports checkpoint/pressure posture,
and proves the Codex merge candidate is free of branch-local runtime state.
It does not decide semantic correctness or authority.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

RUNTIME_ROOT = Path('.entif/runtime')


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)


def detect_surface(explicit: str) -> dict:
    if explicit != 'auto':
        return {'surface': explicit, 'source': 'explicit'}
    env = os.getenv('ENTIF_RUNTIME_SURFACE', '').strip().lower()
    if env in {'chat', 'codex'}:
        return {'surface': env, 'source': 'ENTIF_RUNTIME_SURFACE'}
    if any(os.getenv(k) for k in ('CODEX_HOME', 'CODEX_THREAD_ID', 'OPENAI_CODEX')):
        return {'surface': 'codex', 'source': 'codex_environment_marker'}
    # Do not infer Codex solely from presence of git; Chat/Desktop may have local files.
    return {'surface': 'unknown', 'source': 'insufficient_host_signal'}


def pressure(args: argparse.Namespace) -> dict:
    states = []
    reasons = []
    occ = args.context_occupancy
    if occ is not None:
        if occ >= 0.90:
            states.append('CRITICAL'); reasons.append('context occupancy >= 90%')
        elif occ >= 0.78:
            states.append('TRANSFER'); reasons.append('context occupancy >= 78%')
        elif occ >= 0.65:
            states.append('PREPARE'); reasons.append('context occupancy >= 65%')
    if args.explicit_warning:
        states.append('TRANSFER'); reasons.append('explicit context/compaction warning')
    if args.tool_events_since_checkpoint >= 250:
        states.append('TRANSFER'); reasons.append('very large tool-event tail')
    elif args.tool_events_since_checkpoint >= 120:
        states.append('PREPARE'); reasons.append('large tool-event tail')
    if args.response_budget_truncations >= 10 and args.tool_events_since_checkpoint >= 60:
        states.append('PREPARE'); reasons.append('repeated response-budget truncation under sustained tool load')
    if args.minutes_since_semantic_checkpoint >= 20:
        states.append('TRANSFER'); reasons.append('semantic checkpoint drought >= 20m')
    elif args.minutes_since_semantic_checkpoint >= 10:
        states.append('PREPARE'); reasons.append('semantic checkpoint drought >= 10m')
    rank = {'SAFE':0,'PREPARE':1,'TRANSFER':2,'CRITICAL':3}
    state = max(states, key=lambda s: rank[s]) if states else 'SAFE'
    return {'state':state,'reasons':reasons,'diagnostic_only':True}


def checkpoint(args: argparse.Namespace) -> dict:
    if not args.dirty:
        return {'due': False, 'state': 'clean'}
    if args.surface == 'codex':
        if args.minutes_since_checkpoint >= 10:
            return {'due': True, 'state': 'OVERDUE', 'action': 'commit_and_push_feature_branch'}
        if args.minutes_since_checkpoint >= 5:
            return {'due': True, 'state': 'DUE', 'action': 'commit_and_push_feature_branch'}
        return {'due': False, 'state': 'FRESH'}
    if args.surface == 'chat':
        if args.minutes_since_checkpoint >= 10:
            return {'due': True, 'state': 'OVERDUE', 'action': 'persist_and_verify_external_checkpoint'}
        return {'due': False, 'state': 'FRESH'}
    return {'due': None, 'state': 'UNKNOWN_SURFACE', 'action': 'resolve_surface_before_durability_policy'}


def merge_check(repo: Path) -> tuple[int, dict]:
    repo = repo.resolve()
    inside = run(['git','rev-parse','--is-inside-work-tree'], repo)
    if inside.returncode != 0 or inside.stdout.strip() != 'true':
        return 2, {'ok':False,'error':'not_a_git_worktree'}
    ignored = run(['git','check-ignore','-q','.entif/runtime/probe'], repo)
    ignored_runtime = ignored.returncode == 0
    tracked = run(['git','ls-tree','-r','--name-only','HEAD','--','.entif/runtime'], repo)
    tracked_paths = [x for x in tracked.stdout.splitlines() if x.strip()] if tracked.returncode == 0 else []
    worktree_exists = (repo / RUNTIME_ROOT).exists()
    ok = (not ignored_runtime) and (not tracked_paths) and (not worktree_exists)
    return (0 if ok else 1), {
        'ok': ok,
        'runtime_root': str(RUNTIME_ROOT),
        'runtime_root_gitignored': ignored_runtime,
        'tracked_runtime_paths_in_HEAD': tracked_paths,
        'runtime_root_exists_in_worktree': worktree_exists,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    sp = p.add_subparsers(dest='cmd', required=True)
    d = sp.add_parser('detect')
    d.add_argument('--surface', choices=['auto','chat','codex'], default='auto')
    pr = sp.add_parser('pressure')
    pr.add_argument('--context-occupancy', type=float)
    pr.add_argument('--explicit-warning', action='store_true')
    pr.add_argument('--tool-events-since-checkpoint', type=int, default=0)
    pr.add_argument('--response-budget-truncations', type=int, default=0)
    pr.add_argument('--minutes-since-semantic-checkpoint', type=float, default=0)
    ck = sp.add_parser('checkpoint')
    ck.add_argument('--surface', choices=['chat','codex'], required=True)
    ck.add_argument('--minutes-since-checkpoint', type=float, required=True)
    ck.add_argument('--dirty', action='store_true')
    mc = sp.add_parser('merge-check')
    mc.add_argument('--repo', default='.')
    args = p.parse_args()
    if args.cmd == 'detect':
        out=detect_surface(args.surface); rc=0
    elif args.cmd == 'pressure':
        out=pressure(args); rc=0
    elif args.cmd == 'checkpoint':
        out=checkpoint(args); rc=0
    else:
        rc,out=merge_check(Path(args.repo))
    print(json.dumps(out, indent=2, sort_keys=True))
    return rc

if __name__ == '__main__':
    raise SystemExit(main())

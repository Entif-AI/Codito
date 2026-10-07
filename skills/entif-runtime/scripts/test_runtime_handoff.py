#!/usr/bin/env python3
import json
import subprocess
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).with_name('runtime_handoff.py')
SCHEMA = Path(__file__).parents[1] / 'references' / 'handoff.schema.json'


def run(*args, cwd=None, expect=0):
    p = subprocess.run(['python', str(SCRIPT), *args], cwd=cwd, text=True, capture_output=True)
    assert p.returncode == expect, (p.returncode, p.stdout, p.stderr)
    return json.loads(p.stdout)


def valid_handoff():
    return {
        'schema': 'entif.runtime.handoff/v1',
        'handoff_id': 'H-001',
        'kind': 'transfer',
        'created_at': '2026-10-06T20:30:00-04:00',
        'runtime_surface': 'codex',
        'reason': 'context pressure',
        'mission': 'Continue feature work safely.',
        'refs': {'repository': 'Entif-AI/Codito', 'branch': 'feature/x', 'issue': '#49'},
        'work': {'work_id': 'W-1', 'location': '.entif/runtime/work/W-1', 'current_task_ids': ['T2']},
        'checkpoint': {'checkpoint_id': 'CP0002', 'adapter': 'git', 'git_sha': 'abc123', 'receipt_refs': ['origin/feature/x@abc123']},
        'completed': ['T1 verified'],
        'negative_knowledge': ['Do not retry operation OP-7 without reconciliation.'],
        'unresolved': [{'id': 'OP-7', 'kind': 'side_effect', 'state': 'executed_ack_unknown', 'summary': 'remote write ack lost'}],
        'next_safe_operations': ['Reconcile OP-7 against the live target.'],
        'hydration': {'read_first': ['.entif/runtime/HANDOFF.json'], 'read_if_needed': ['journal tail'], 'read_if_condition': []},
        'verification': ['Verify branch head before mutation.'],
        'cleanup': {'runtime_root_must_be_removed_before_merge': True},
    }

assert SCHEMA.exists(), 'handoff schema must exist'

with tempfile.TemporaryDirectory() as td:
    root = Path(td)
    (root / '.entif/runtime').mkdir(parents=True)
    h = root / '.entif/runtime/HANDOFF.json'
    h.write_text(json.dumps(valid_handoff()))
    out = run('validate', str(h))
    assert out['ok'] is True

    # Explicit handoff outranks every fallback.
    out = run('discover', '--repo', str(root), '--handoff', str(h))
    assert out['route'] == 'handoff'
    assert out['source'].endswith('HANDOFF.json')
    assert out['narration'][0].startswith('Recovery: explicit handoff found')

with tempfile.TemporaryDirectory() as td:
    root = Path(td)
    ws = root / '.entif/runtime/work/W-2'
    ws.mkdir(parents=True)
    (ws / 'STATUS.json').write_text('{}')
    cp = root / '.entif/runtime/durability/checkpoints/CP0002'
    cp.mkdir(parents=True)
    (cp / 'checkpoint.json').write_text('{}')
    out = run('discover', '--repo', str(root))
    assert out['route'] == 'work_stack'
    assert any('explicit handoff not found' in x.lower() for x in out['narration'])
    assert any('work stack found' in x.lower() for x in out['narration'])

with tempfile.TemporaryDirectory() as td:
    root = Path(td)
    cp = root / '.entif/runtime/durability/checkpoints/CP0002'
    cp.mkdir(parents=True)
    (cp / 'checkpoint.json').write_text('{}')
    out = run('discover', '--repo', str(root))
    assert out['route'] == 'checkpoint'
    assert 'CP0002' in out['source']
    assert any('Work Stack not found' in x for x in out['narration'])
    assert any('checkpoint CP0002' in x for x in out['narration'])

with tempfile.TemporaryDirectory() as td:
    root = Path(td)
    (root / 'FEATURE_LOG.md').write_text('# feature')
    trace = root / 'recovery.skim.md'
    trace.write_text('# Reduced Run Trace\n## Recovery capsule\n')
    out = run('discover', '--repo', str(root), '--recovery-log', str(trace))
    assert out['route'] == 'feature_log'

with tempfile.TemporaryDirectory() as td:
    root = Path(td)
    trace = root / 'recovery.skim.md'
    trace.write_text('# Reduced Run Trace\n## Recovery capsule\n')
    out = run('discover', '--repo', str(root), '--recovery-log', str(trace))
    assert out['route'] == 'reduced_trace'
    assert any('last-resort evidence' in x for x in out['narration'])

with tempfile.TemporaryDirectory() as td:
    root = Path(td)
    bad = root / 'bad.json'
    data = valid_handoff()
    del data['negative_knowledge']
    bad.write_text(json.dumps(data))
    out = run('validate', str(bad), expect=1)
    assert out['ok'] is False
    assert 'negative_knowledge' in out['errors']

print('runtime handoff: PASS')

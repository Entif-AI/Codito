#!/usr/bin/env python3
import json
import subprocess
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).with_name('run_durability.py')

def run(*args, ok=True):
    p = subprocess.run(['python', str(SCRIPT), *args], text=True, capture_output=True)
    if ok and p.returncode != 0:
        raise AssertionError(p.stdout + p.stderr)
    if not ok and p.returncode == 0:
        raise AssertionError('expected failure')
    return p

def main():
    with tempfile.TemporaryDirectory() as td:
        base = Path(td); work = base/'work'; work.mkdir()
        (work/'a.txt').write_text('alpha', encoding='utf-8')
        p = run('init','--root',str(base/'runs'),'--title','test','--run-id','R1','--witness-mode','required','--witness-recipient','w@example.test')
        r = Path(p.stdout.strip())
        start = json.loads((r/'RUN_START.json').read_text())
        assert start['policy']['dirty_ceiling_minutes'] == 10
        assert start['policy']['witness_interval_minutes'] == 10
        assert start['policy']['primary_channel'] == 'drive'
        run('validate','--run',str(r),'--require-policy', ok=False)
        run('startup-receipt','--run',str(r),'--channel','drive','--remote-id','run-start-drive')
        run('validate','--run',str(r),'--require-policy', ok=False)
        run('startup-receipt','--run',str(r),'--channel','witness','--remote-id','run-start-witness','--recipient','w@example.test')
        run('validate','--run',str(r),'--require-policy')
        cp1 = json.loads(run('checkpoint','--run',str(r),'--track-root',str(work),'--draft-complete','a.txt','--next-action','continue').stdout)
        run('validate','--run',str(r),'--require-policy', ok=False)
        run('receipt','--run',str(r),'--checkpoint','CP0001','--channel','drive','--remote-id','drive-1','--remote-sha256',cp1['sha256'])
        run('freeze','--run',str(r), ok=False)
        run('receipt','--run',str(r),'--checkpoint','CP0001','--channel','witness','--remote-id','msg-1','--recipient','w@example.test','--remote-sha256',cp1['sha256'])
        run('validate','--run',str(r),'--require-policy')
        run('freeze','--run',str(r),'--freeze-id','F1')
        (work/'a.txt').write_text('beta', encoding='utf-8')
        cp2 = json.loads(run('checkpoint','--run',str(r),'--track-root',str(work),'--draft-complete','a.txt').stdout)
        run('validate','--run',str(r),'--require-policy', ok=False)
        run('receipt','--run',str(r),'--checkpoint','CP0002','--channel','drive','--remote-id','drive-2','--remote-sha256',cp2['sha256'])
        run('receipt','--run',str(r),'--checkpoint','CP0002','--channel','witness','--remote-id','msg-2','--recipient','w@example.test','--remote-sha256',cp2['sha256'])
        run('validate','--run',str(r),'--require-policy')
        bundle = Path(json.loads((r/'STATE.json').read_text())['checkpoints']['CP0002']['bundle_path'])
        bundle.write_bytes(bundle.read_bytes()+b'corrupt')
        run('validate','--run',str(r), ok=False)
    print('ok')

if __name__ == '__main__':
    main()

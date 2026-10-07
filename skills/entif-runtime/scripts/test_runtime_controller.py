#!/usr/bin/env python3
import json, subprocess, tempfile
from pathlib import Path

SCRIPT=Path(__file__).with_name('runtime_controller.py')

def call(*args, cwd=None, expect=0):
    p=subprocess.run(['python',str(SCRIPT),*args],cwd=cwd,text=True,capture_output=True)
    assert p.returncode==expect,(p.returncode,p.stdout,p.stderr)
    return json.loads(p.stdout)

assert call('detect','--surface','chat')['surface']=='chat'
assert call('checkpoint','--surface','codex','--minutes-since-checkpoint','5','--dirty')['state']=='DUE'
assert call('checkpoint','--surface','codex','--minutes-since-checkpoint','10','--dirty')['state']=='OVERDUE'
assert call('checkpoint','--surface','chat','--minutes-since-checkpoint','10','--dirty')['action']=='persist_and_verify_external_checkpoint'
assert call('pressure','--tool-events-since-checkpoint','250')['state']=='TRANSFER'
assert call('pressure','--context-occupancy','0.91')['state']=='CRITICAL'
with tempfile.TemporaryDirectory() as td:
    r=Path(td)
    subprocess.run(['git','init','-q'],cwd=r,check=True)
    subprocess.run(['git','config','user.email','test@example.com'],cwd=r,check=True)
    subprocess.run(['git','config','user.name','Test'],cwd=r,check=True)
    (r/'a').write_text('x')
    subprocess.run(['git','add','a'],cwd=r,check=True)
    subprocess.run(['git','commit','-qm','init'],cwd=r,check=True)
    assert call('merge-check','--repo',str(r))['ok'] is True
    (r/'.entif/runtime').mkdir(parents=True)
    (r/'.entif/runtime/RUN.json').write_text('{}')
    out=call('merge-check','--repo',str(r),expect=1)
    assert out['runtime_root_exists_in_worktree'] is True
print('ok')

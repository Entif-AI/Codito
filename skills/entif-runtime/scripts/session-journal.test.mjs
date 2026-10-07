#!/usr/bin/env node
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';

const SCRIPT = new URL('./session-journal.mjs', import.meta.url).pathname;
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'entif-session-journal-'));
const file = path.join(tmp, 'journal.jsonl');
const I = ['--session-id','s1','--work-epoch-id','w1','--lease-id','l1'];
const sha = s => crypto.createHash('sha256').update(s).digest('hex');
function run(args, expected=0) {
  const r=spawnSync(process.execPath,[SCRIPT,...args],{encoding:'utf8'});
  if(r.status!==expected) throw new Error(`expected exit ${expected}, got ${r.status}\nstdout=${r.stdout}\nstderr=${r.stderr}`);
  return r;
}
function expectFailure(args, fragment) {
  const r=spawnSync(process.execPath,[SCRIPT,...args],{encoding:'utf8'});
  assert.notEqual(r.status,0,`expected failure for ${args.join(' ')}`);
  assert.match(r.stderr,new RegExp(fragment));
}

try {
  run(['init','--file',file,...I,'--principal','ChatGPT']);
  run(['append-turn','--file',file,...I,'--role','user','--content','hello']);
  run(['append-turn','--file',file,...I,'--role','assistant','--content','world']);
  let v=run(['validate','--file',file]);
  assert.match(v.stdout,/"last_seq": 3/);

  let t=run(['tail','--file',file,'--after','2','--limit','10']);
  const tailLines=t.stdout.trim().split('\n').map(JSON.parse);
  assert.equal(tailLines.length,1);
  assert.equal(tailLines[0].seq,3);

  run(['append-operation','--file',file,...I,'--operation-id','op1','--operation-type','github.update_file','--target-ref','repo:path','--request-digest',sha('request'),'--status','executed_receipt_present','--receipt-ref','commit123']);
  run(['validate','--file',file]);

  expectFailure(['append-operation','--file',file,...I,'--operation-id','op2','--operation-type','github.comment','--target-ref','issue:1','--request-digest',sha('x'),'--status','executed_receipt_present'],'MISSING_RECEIPT');

  run(['append-checkpoint','--file',file,...I,'--materialized-through-seq','4','--feature-log-sha256',sha('featurelog'),'--git-sha','abc123']);
  run(['validate','--file',file]);

  expectFailure(['append-checkpoint','--file',file,...I,'--materialized-through-seq','999','--feature-log-sha256',sha('featurelog'),'--git-sha','abc123'],'INVALID_CURSOR');

  expectFailure(['append-turn','--file',file,'--session-id','s1','--work-epoch-id','w1','--lease-id','OTHER','--role','user','--content','bad'],'IDENTITY_MISMATCH');

  const badSeq=path.join(tmp,'bad-seq.jsonl');
  const records=fs.readFileSync(file,'utf8').trim().split('\n').map(JSON.parse);
  records[2].seq=7;
  fs.writeFileSync(badSeq,records.map(x=>JSON.stringify(x)).join('\n')+'\n');
  expectFailure(['validate','--file',badSeq],'expected seq 3, found 7');

  const tampered=path.join(tmp,'tampered.jsonl');
  const tr=fs.readFileSync(file,'utf8').trim().split('\n').map(JSON.parse);
  tr[1].content='changed-after-recording';
  fs.writeFileSync(tampered,tr.map(x=>JSON.stringify(x)).join('\n')+'\n');
  expectFailure(['validate','--file',tampered],'content digest mismatch');

  const partial=path.join(tmp,'partial.jsonl');
  fs.copyFileSync(file,partial);
  fs.appendFileSync(partial,'{"schema":"entif.session-journal/v1","seq":6');
  expectFailure(['validate','--file',partial],'invalid JSON');
  expectFailure(['append-turn','--file',partial,...I,'--role','user','--content','should not append'],'INVALID_TAIL');

  const report=run(['recovery-report','--file',file,'--after','2','--limit','20']);
  const parsed=JSON.parse(report.stdout);
  assert.equal(parsed.durable_last_seq,5);
  assert.equal(parsed.operation_states.length,1);
  assert.equal(parsed.operation_states[0].status,'executed_receipt_present');
  assert.equal(parsed.checkpoints.length,1);

  console.log('session-journal tests: PASS');
} finally {
  fs.rmSync(tmp,{recursive:true,force:true});
}

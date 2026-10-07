#!/usr/bin/env node
import fs from 'node:fs';
import crypto from 'node:crypto';
import readline from 'node:readline';

const SCHEMA = 'entif.session-journal/v1';
const HEX64 = /^[0-9a-f]{64}$/;
const OP_STATUSES = new Set([
  'requested_not_executed',
  'executed_receipt_present',
  'executed_ack_unknown',
  'retryable_idempotent',
  'non_idempotent_or_ambiguous',
]);

function fail(code, message) {
  console.error(`${code}: ${message}`);
  process.exit(2);
}
function parseArgs(argv) {
  const out = {_: []};
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (!arg.startsWith('--')) { out._.push(arg); continue; }
    const key = arg.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) out[key] = true;
    else { out[key] = next; i++; }
  }
  return out;
}
function required(a, key) {
  const value = a[key];
  if (value === undefined || value === true || value === '') fail('USAGE', `missing --${key}`);
  return String(value);
}
function sha256(value) {
  return crypto.createHash('sha256').update(value).digest('hex');
}
function now(a) {
  const value = a['recorded-at'] ? String(a['recorded-at']) : new Date().toISOString();
  if (Number.isNaN(Date.parse(value))) fail('INVALID_TIMESTAMP', `invalid RFC3339 timestamp: ${value}`);
  return value;
}
function ensureParentPortable(file) {
  const idx = file.lastIndexOf('/');
  if (idx > 0) fs.mkdirSync(file.slice(0, idx), {recursive: true});
}
function readLastCompleteLine(file) {
  if (!fs.existsSync(file)) return null;
  const stat = fs.statSync(file);
  if (stat.size === 0) return null;
  const fd = fs.openSync(file, 'r');
  try {
    const chunkSize = Math.min(stat.size, 65536);
    const start = stat.size - chunkSize;
    const buf = Buffer.alloc(chunkSize);
    fs.readSync(fd, buf, 0, chunkSize, start);
    const text = buf.toString('utf8');
    const lines = text.split('\n');
    if (lines.at(-1) === '') lines.pop();
    const line = lines.at(-1);
    if (!line) return null;
    try { return JSON.parse(line); }
    catch { fail('INVALID_TAIL', 'last durable journal line is not valid JSON'); }
  } finally { fs.closeSync(fd); }
}
function nextSeq(file) {
  const last = readLastCompleteLine(file);
  return last ? Number(last.seq) + 1 : 1;
}
function identityFromArgs(a) {
  return {
    session_id: required(a, 'session-id'),
    work_epoch_id: required(a, 'work-epoch-id'),
    lease_id: required(a, 'lease-id'),
  };
}
function checkIdentityAgainstLast(file, identity) {
  const last = readLastCompleteLine(file);
  if (!last) return;
  for (const key of ['session_id', 'work_epoch_id', 'lease_id']) {
    if (last[key] !== identity[key]) fail('IDENTITY_MISMATCH', `${key} differs from existing journal`);
  }
}
function append(file, record) {
  ensureParentPortable(file);
  fs.appendFileSync(file, `${JSON.stringify(record)}\n`, 'utf8');
  return record;
}
function baseRecord(a, file, type) {
  const identity = identityFromArgs(a);
  checkIdentityAgainstLast(file, identity);
  return {schema: SCHEMA, seq: nextSeq(file), ...identity, type, recorded_at: now(a)};
}
function getContent(a) {
  if (a['content-file']) return fs.readFileSync(String(a['content-file']), 'utf8');
  if (a.content !== undefined && a.content !== true) return String(a.content);
  fail('USAGE', 'provide --content or --content-file');
}

function init(a) {
  const file = required(a, 'file');
  if (fs.existsSync(file) && fs.statSync(file).size > 0) fail('JOURNAL_EXISTS', `${file} already contains data`);
  const record = baseRecord(a, file, 'session_start');
  record.principal = a.principal && a.principal !== true ? String(a.principal) : null;
  append(file, record);
  console.log(JSON.stringify({ok: true, file, seq: record.seq, record_sha256: sha256(JSON.stringify(record))}, null, 2));
}
function appendTurn(a) {
  const file = required(a, 'file');
  const role = required(a, 'role');
  if (!['user', 'assistant'].includes(role)) fail('INVALID_ROLE', 'role must be user or assistant');
  const content = getContent(a);
  const record = baseRecord(a, file, 'turn');
  record.role = role;
  record.content = content;
  record.content_sha256 = sha256(content);
  append(file, record);
  console.log(JSON.stringify({ok: true, seq: record.seq, content_sha256: record.content_sha256}, null, 2));
}
function appendOperation(a) {
  const file = required(a, 'file');
  const status = required(a, 'status');
  if (!OP_STATUSES.has(status)) fail('INVALID_OPERATION_STATUS', status);
  const record = baseRecord(a, file, 'operation');
  record.operation_id = required(a, 'operation-id');
  record.operation_type = required(a, 'operation-type');
  record.target_ref = required(a, 'target-ref');
  record.request_digest = required(a, 'request-digest');
  if (!HEX64.test(record.request_digest)) fail('INVALID_DIGEST', 'request_digest must be lowercase SHA-256 hex');
  record.status = status;
  record.receipt_ref = a['receipt-ref'] && a['receipt-ref'] !== true ? String(a['receipt-ref']) : null;
  if (status === 'executed_receipt_present' && !record.receipt_ref) fail('MISSING_RECEIPT', 'executed_receipt_present requires --receipt-ref');
  append(file, record);
  console.log(JSON.stringify({ok: true, seq: record.seq, operation_id: record.operation_id, status}, null, 2));
}
function appendCheckpoint(a) {
  const file = required(a, 'file');
  const last = readLastCompleteLine(file);
  if (!last) fail('EMPTY_JOURNAL', 'checkpoint requires an existing journal');
  const materialized = Number(a['materialized-through-seq'] ?? last.seq);
  if (!Number.isInteger(materialized) || materialized < 1 || materialized > Number(last.seq)) {
    fail('INVALID_CURSOR', `materialized cursor ${materialized} must be between 1 and ${last.seq}`);
  }
  const digest = required(a, 'feature-log-sha256');
  if (!HEX64.test(digest)) fail('INVALID_DIGEST', 'feature-log SHA-256 must be lowercase hex');
  const record = baseRecord(a, file, 'checkpoint');
  record.materialized_through_seq = materialized;
  record.feature_log_sha256 = digest;
  record.git_sha = required(a, 'git-sha');
  record.checkpoint_kind = a.kind && a.kind !== true ? String(a.kind) : 'semantic';
  append(file, record);
  console.log(JSON.stringify({ok: true, seq: record.seq, materialized_through_seq: materialized}, null, 2));
}

function validateRecord(record, expectedSeq, identity) {
  const errors = [];
  if (record.schema !== SCHEMA) errors.push(`seq ${expectedSeq}: schema mismatch`);
  if (record.seq !== expectedSeq) errors.push(`expected seq ${expectedSeq}, found ${record.seq}`);
  for (const key of ['session_id', 'work_epoch_id', 'lease_id']) {
    if (!record[key]) errors.push(`seq ${expectedSeq}: missing ${key}`);
    else if (identity[key] !== undefined && record[key] !== identity[key]) errors.push(`seq ${expectedSeq}: ${key} changed`);
  }
  if (!record.type) errors.push(`seq ${expectedSeq}: missing type`);
  if (!record.recorded_at || Number.isNaN(Date.parse(record.recorded_at))) errors.push(`seq ${expectedSeq}: invalid recorded_at`);
  if (record.type === 'turn') {
    if (!['user', 'assistant'].includes(record.role)) errors.push(`seq ${expectedSeq}: invalid role`);
    if (typeof record.content !== 'string') errors.push(`seq ${expectedSeq}: missing content`);
    else if (record.content_sha256 !== sha256(record.content)) errors.push(`seq ${expectedSeq}: content digest mismatch`);
  } else if (record.type === 'operation') {
    if (!record.operation_id || !record.operation_type || !record.target_ref) errors.push(`seq ${expectedSeq}: incomplete operation identity`);
    if (!HEX64.test(String(record.request_digest || ''))) errors.push(`seq ${expectedSeq}: invalid request_digest`);
    if (!OP_STATUSES.has(record.status)) errors.push(`seq ${expectedSeq}: invalid operation status`);
    if (record.status === 'executed_receipt_present' && !record.receipt_ref) errors.push(`seq ${expectedSeq}: receipt required`);
  } else if (record.type === 'checkpoint') {
    if (!Number.isInteger(record.materialized_through_seq) || record.materialized_through_seq < 1 || record.materialized_through_seq >= record.seq) errors.push(`seq ${expectedSeq}: invalid materialized cursor`);
    if (!HEX64.test(String(record.feature_log_sha256 || ''))) errors.push(`seq ${expectedSeq}: invalid feature_log_sha256`);
    if (!record.git_sha) errors.push(`seq ${expectedSeq}: missing git_sha`);
  } else if (record.type !== 'session_start') {
    errors.push(`seq ${expectedSeq}: unknown type ${record.type}`);
  }
  return errors;
}
async function scan(file, {collect = false, after = 0, limit = Infinity} = {}) {
  if (!fs.existsSync(file)) fail('NO_JOURNAL', `${file} not found`);
  const stream = fs.createReadStream(file, {encoding: 'utf8'});
  const rl = readline.createInterface({input: stream, crlfDelay: Infinity});
  const identity = {};
  const errors = [];
  const records = [];
  let expected = 1;
  let count = 0;
  for await (const line of rl) {
    if (!line.trim()) continue;
    let record;
    try { record = JSON.parse(line); }
    catch { errors.push(`line/seq ${expected}: invalid JSON`); expected++; continue; }
    if (expected === 1) for (const key of ['session_id', 'work_epoch_id', 'lease_id']) identity[key] = record[key];
    errors.push(...validateRecord(record, expected, identity));
    if (collect && Number(record.seq) > after && count < limit) { records.push(record); count++; }
    expected++;
  }
  return {errors, records, identity, last_seq: expected - 1};
}
async function validateCmd(a) {
  const file = required(a, 'file');
  const result = await scan(file);
  if (result.errors.length) { console.error(result.errors.join('\n')); process.exit(1); }
  console.log(JSON.stringify({ok: true, last_seq: result.last_seq, identity: result.identity}, null, 2));
}
async function tailCmd(a) {
  const file = required(a, 'file');
  const after = Number(a.after || 0);
  const limit = Number(a.limit || 200);
  if (!Number.isInteger(after) || after < 0 || !Number.isInteger(limit) || limit < 1) fail('USAGE', '--after must be >=0 and --limit >=1');
  const result = await scan(file, {collect: true, after, limit});
  if (result.errors.length) fail('INVALID_JOURNAL', result.errors.join('; '));
  for (const record of result.records) process.stdout.write(`${JSON.stringify(record)}\n`);
}
async function recoveryReport(a) {
  const file = required(a, 'file');
  const after = Number(a.after || 0);
  const limit = Number(a.limit || 200);
  const result = await scan(file, {collect: true, after, limit});
  if (result.errors.length) fail('INVALID_JOURNAL', result.errors.join('; '));
  const operations = result.records.filter(r => r.type === 'operation').map(r => ({seq:r.seq, operation_id:r.operation_id, operation_type:r.operation_type, target_ref:r.target_ref, status:r.status, receipt_ref:r.receipt_ref || null}));
  const checkpoints = result.records.filter(r => r.type === 'checkpoint').map(r => ({seq:r.seq, materialized_through_seq:r.materialized_through_seq, git_sha:r.git_sha, feature_log_sha256:r.feature_log_sha256}));
  console.log(JSON.stringify({ok:true, after, durable_last_seq:result.last_seq, returned_records:result.records.length, operation_states:operations, checkpoints}, null, 2));
}

const a = parseArgs(process.argv.slice(2));
const cmd = a._[0];
try {
  switch (cmd) {
    case 'init': init(a); break;
    case 'append-turn': appendTurn(a); break;
    case 'append-operation': appendOperation(a); break;
    case 'append-checkpoint': appendCheckpoint(a); break;
    case 'validate': await validateCmd(a); break;
    case 'tail': await tailCmd(a); break;
    case 'recovery-report': await recoveryReport(a); break;
    default: fail('USAGE', 'commands: init|append-turn|append-operation|append-checkpoint|validate|tail|recovery-report');
  }
} catch (error) {
  if (error?.code === 'ENOENT') fail('NO_FILE', error.message);
  throw error;
}

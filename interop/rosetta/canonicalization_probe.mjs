// Source-extracted construction, not a full repository test.
// Rosetta pin: 1fc05c404d15fa7cc9713e7ee19d87b94316f07a
// packages/rosetta-canon/src/lib/rosetta-canon.ts, lines 20-39.
import assert from 'node:assert/strict';
function sortValue(value) {
  if (Array.isArray(value)) return value.map(entry => sortValue(entry));
  if (value && typeof value === 'object') {
    const entries = Object.entries(value).sort(([left], [right]) => left < right ? -1 : left > right ? 1 : 0);
    return Object.fromEntries(entries.map(([key, entry]) => [key, sortValue(entry)]));
  }
  if (typeof value === 'number' && !Number.isFinite(value)) throw new Error('JCS canonicalization only accepts finite JSON numbers.');
  return value;
}
const actual = JSON.stringify(sortValue({'2': 'two', '10': 'ten'}));
const expected = '{"10":"ten","2":"two"}';
assert.notEqual(actual, expected, 'Expected to reproduce integer-like key ordering discrepancy.');
console.log(JSON.stringify({probe:'source-extracted integer-like key ordering',actual,expected,discrepancy_reproduced:actual !== expected,scope:'isolated construction; repository suite not run'},null,2));
# Work Stack Model

## Purpose

Represent one bounded cluster of correlated operations durably enough that ordering, handoffs, retries, and recovery do not depend on chat memory.

## Directory model

```text
<base>/<work-uuid>/
  WORK.json
  EVENTS.jsonl
  STATUS.json
  tasks/
  receipts/
  children/
```

A child work bucket records `parent_work_id` and lives under the parent's `children/` directory.

## Task identity

Each task has a stable task ID inside one work bucket. The record carries:

- title;
- state;
- dependencies;
- idempotency key when side effects exist;
- side-effect class;
- local input/output files;
- external input/output refs;
- success predicate;
- failure policy;
- attempt count/current attempt;
- receipts;
- committed input/output snapshots.

## States

- `planned`: dependencies or prerequisites are not yet satisfied.
- `ready`: derived status only; task record remains planned until start.
- `executing`: an attempt has been recorded before execution.
- `receipt_observed`: an external receipt exists; verification still required.
- `verified`: declared postcondition/output check has been performed.
- `committed`: task is complete under the recorded contract.
- `failed`: attempt failed with a known state.
- `safe_hold`: external state is ambiguous or replay is unsafe.
- `reconciled_retryable`: live-state reconciliation established that retry is permitted.
- `stale`: previously valid task was invalidated or one of its committed local snapshots drifted.
- `cancelled`: intentionally abandoned.

## Readiness

A task is ready when:

- its state is `planned`, `failed` with idempotent replay, or `reconciled_retryable`; and
- every `depends_on` task is committed and non-stale.

A task may be blocked without blocking unrelated siblings.

## Side-effect classes

### none

No material external side effect. Retry from a known failed state is ordinarily safe.

### idempotent

The operation has a real idempotency contract represented by `idempotency_key`. Reusing the same key may be safe, but do not invent idempotency for an API that lacks it.

### reconcile_before_retry

A failed/unknown attempt requires target-state reconciliation before replay.

### non_idempotent

If execution acknowledgment is ambiguous, safe-hold until reconciliation proves whether the effect occurred.

## Snapshot semantics

At `start`, hash declared local input files. At `verify`, hash declared local output files. At `commit`, confirm both sets still match their snapshots.

Later `validate` compares committed snapshots against current bytes. A mismatch is a stale-result signal, not proof about why the file changed.

## Events

`EVENTS.jsonl` is append-only and hash-chained. Task JSON is the current materialized task record. `STATUS.json` is a disposable/regenerable summary view.

The event journal is operational provenance, not a source of higher semantic or governance authority.

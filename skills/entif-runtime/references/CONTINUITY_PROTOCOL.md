# Session Continuity Protocol

## Purpose

Preserve recoverable work across agent/runtime boundaries without requiring the successor to replay the entire conversation.

## State model

Use three memory temperatures:

| Layer | Artifact | Purpose |
|---|---|---|
| HOT | `FEATURE_LOG.md` | Compact materialized resumability state |
| WARM | session JSONL journal | Append-only chronology and bounded operation evidence |
| COLD | issue, Git, PR, tests/CI, receipts | Canonical contracts and durable objective evidence |

A warmer layer does not outrank a colder authoritative surface merely because it is more detailed.

## Core invariant

Reliability must not depend on the dying agent successfully explaining itself before it dies.

## Active-session lifecycle

```text
remote lease acquired
  -> journal session_start
  -> append material turns/operation envelopes
  -> semantic state changes
  -> materialize FEATURE_LOG checkpoint + journal cursor
  -> checkpoint/push/verify
  -> continue
```

A transcript append and a semantic checkpoint are different operations. The journal may advance several records while the materialized view remains unchanged.

## Crash recovery

```text
replacement execution
  -> inspect FEATURE_LOG
  -> validate recorded cursor
  -> validate journal
  -> read tail after cursor
  -> reconcile operation receipts/live state
  -> recover/acquire lease
  -> materialize new checkpoint
  -> continue
```

Default to bounded replay. Full-transcript hydration is an escalation path, not the first recovery action.

## Graceful transfer

```text
persist final intended journal state
  -> refresh materialized state
  -> checkpoint/push/verify
  -> release lease
  -> emit compact bootstrap pointing to durable state
```

If graceful transfer fails after the journal was durably persisted, crash recovery remains possible.

## Context-pressure states

Use the parent runtime policy in `CONTEXT_PRESSURE.md` and `runtime_controller.py` as the single selected pressure controller. Continuity defines what must survive PREPARE/TRANSFER; it does not maintain a second threshold table.

Reserve enough output/reasoning headroom to complete transfer. Thresholds and heuristics are calibratable operational policy, not platform guarantees or Rosetta semantics. Continuity preservation remains active regardless of pressure state.

# Runtime model

## Canonical execution root

One execution epoch has one `run_id` and may have one `work_id`. Use the same identifiers across adapters where possible.

Logical state classes:

- `authority`: current governing refs and disclosure posture;
- `feature`: issue/spec/plan/branch/lease/PR identity;
- `orchestration`: ready-work binding, selected procedure/executor/runtime surface, and dispatch identity;
- `work`: task DAG, attempts, receipts, idempotency, stale/safe-held state;
- `continuity`: standard handoff, semantic frontier, journal cursor, negative knowledge, next safe step;
- `durability`: checkpoint identity, hashes, remote/branch receipt;
- `pressure`: latest context-pressure state and evidence.

## Ownership law

Do not duplicate canonical facts between modules.

- Work Stack owns task execution/replay facts.
- Feature lifecycle owns branch/lease/checkpoint ownership.
- Durability owns persistence proof.
- Continuity owns semantic resumability and pointers to the others.
- Pressure owns only the decision to checkpoint/transfer, never task truth.
- Work orchestration owns ready-work uptake and dispatch binding, not desired-state authority.
- Feature post-mortem execution owns evidence/evaluator/proposal mechanics; Governance owns institutional adoption/state.

## Shared Work Stack layout

Use bundled `scripts/work_stack.py`. Its schema is shared across Chat and Codex.

A bucket contains `WORK.json`, `EVENTS.jsonl`, `tasks/`, `receipts/`, `children/`, and regenerated `STATUS.json`.

## Shared continuity frontier

Use `entif.runtime.handoff/v1` as the shared checkpoint/transfer/completion/emergency object. Its semantic frontier should contain:

- mission and controlling user instruction;
- authority and governing skill refs;
- work/run IDs and current task states;
- completed outcomes and verification receipts;
- exact live artifact/issue/PR/Sheet/file refs;
- decisions and rationale needed to avoid rediscovery;
- negative knowledge and ruled-out paths;
- unresolved hypotheses/blockers;
- ambiguous side effects requiring reconciliation;
- highest verified checkpoint;
- ordered next safe operations and hydration map.

Raw transcripts are recovery evidence, not execution authority.

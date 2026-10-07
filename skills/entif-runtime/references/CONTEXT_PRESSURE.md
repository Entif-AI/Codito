# Context pressure controller

Context is a finite hot cache. Durable execution state lives elsewhere.

## Signal priority

1. native context-window occupancy telemetry;
2. runtime/API input-token telemetry plus usable limit/output headroom;
3. explicit compaction/context warnings;
4. deterministic local token estimate;
5. operational heuristics.

Never fabricate exact occupancy.

## States

### SAFE
Work normally. Preserve state incrementally through the active adapter.

### PREPARE
Finish the current coherent unit when safe, then materialize the semantic frontier and receipts in the standard handoff. Avoid starting another large retrieval fan-out or non-idempotent multi-step sequence until checkpointed.

### TRANSFER
Persist and verify a `transfer` handoff, reconcile ambiguous side effects, narrate the selected recovery entrypoint, and deliberately continue in a fresh context/session. Do not reduce model/reasoning quality to remain in the old context.

### CRITICAL
Do not begin another non-idempotent operation. Persist the minimum truthful `emergency` handoff immediately and transfer/recover.

## Heuristic evidence

When native telemetry is absent, consider together rather than as universal gates:

- minutes/material changes since last semantic checkpoint;
- tool calls/outputs since checkpoint;
- retrieved bytes/tokens since checkpoint;
- repeated tool-response budget truncations;
- long gap since assistant/user-visible semantic checkpoint;
- number of simultaneously active work items/refs;
- unresolved side effects;
- compaction or degraded-recall symptoms.

Use hysteresis. Thresholds are experimental runtime policy, not Rosetta semantics. The bundled controller supplies conservative defaults only for diagnostics and can be overridden.

# Migration inventory

Target: `entif-runtime` becomes the eager runtime/execution continuity parent under Codito #49.

| Legacy skill | Disposition | Canonical responsibility inside Entif Runtime |
|---|---|---|
| `entif-feature-workflow` | `MERGE_WITH_MODULE` then retire eager entrypoint after parity | feature epoch, lease, branch checkpoint/check-in, stale recovery |
| `entif-work-stack` | `MOVE_TO_MODULE` then retire eager entrypoint after parity | task DAG, attempts, receipts, replay/idempotency, stale derived state |
| `entif-session-continuity` | `MOVE_TO_MODULE` then retire eager entrypoint after parity | journal, semantic frontier, checkpoint/transfer/recover |
| `entif-run-durability` | `MOVE_TO_MODULE` then retire eager entrypoint after parity | adapter-specific persistence proof/checkpoint receipts |

Shared deterministic helpers are bundled rather than reimplemented. Environment adapters select persistence policy without changing Work Stack/journal schemas.

Retire old eager entrypoints only after representative Chat and Codex parity fixtures, rollback confidence, routing telemetry, and governance acceptance pass.

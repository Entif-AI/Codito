# Migration inventory

Target: `entif-runtime` becomes the eager runtime/execution continuity parent under Codito #49.

| Legacy/shared skill | Disposition | Canonical responsibility |
|---|---|---|
| `entif-feature-workflow` | `MERGE_WITH_MODULE` then retire eager entrypoint after parity | feature epoch, lease, branch checkpoint/check-in, stale recovery |
| `entif-work-stack` | `MOVE_TO_MODULE` then retire eager entrypoint after parity | task DAG, attempts, receipts, replay/idempotency, stale derived state |
| `entif-session-continuity` | `MOVE_TO_MODULE` then retire eager entrypoint after parity | journal, semantic frontier, standardized handoff/transfer/recover |
| `entif-run-durability` | `MOVE_TO_MODULE` then retire eager entrypoint after parity | adapter-specific persistence proof/checkpoint receipts |
| `entif-work-orchestrator` | `MOVE_TO_MODULE` then retire/supersede legacy entrypoint after parity | ready-work uptake, procedure/executor/runtime-surface selection, dispatch frontier, execution telemetry |
| `entif-feature-postmortem` | `MOVE_TO_MODULE` then retire eager entrypoint after parity | completed-feature evidence compilation, governed evaluator invocation, separate proposal workstream; institutional outputs hand to Governance |
| `entif-pr-closeout` | `MOVE_TO_MODULE` then retire eager entrypoint after parity | review/finalization, worklog archive/delta, rejected obligations, one-hop parent synopsis, merge-readiness/closeout |
| `entif-postmortem-logger` | `MOVE_TO_MODULE` with temporary eager compatibility veneer until activation parity | immediate qualifying incident logging, canonical ledger reconciliation, Logic-assisted failure triage, and prior-failure/gotcha projection; Governance retains institutional adoption/state |
| `entif-governed-creator` | `KEEP_TOP_LEVEL_EXCEPTION` | governed Skill mutation/validation; Runtime may invoke but does not absorb its authority gate |

Shared deterministic helpers are bundled rather than reimplemented. Capability predicates select persistence policy without changing Work Stack/journal/handoff schemas; Chat/Codex adapters remain common presets rather than the canonical ontology.

Governance (#53) remains the canonical owner of institutional case/pattern/policy/adoption/version/supersession state. Feature post-mortem execution inside Runtime does not create governance authority.

Codito #84 owns the future optional Runtime -> Akasha telemetry/evidence export adapter. It is downstream/compatibility work and is not a first-wave Runtime dependency.

Retire old eager entrypoints only after representative capability-profile parity fixtures, rollback confidence, routing/activation telemetry, and governance acceptance pass. Failure-logging parity MUST include a real abnormal-termination/recovery fixture proving the Runtime-owned path files or enriches the incident before related automation is reused.

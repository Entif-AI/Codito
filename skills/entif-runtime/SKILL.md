---
name: entif-runtime
description: "Govern durable Entif/Rosetta execution with one capability-aware runtime control plane. Use for ready-work orchestration, substantial feature work, long multi-tool runs, dependent operations, branch leases/checkpoints, Work Stack state, crash/context recovery, standardized checkpoint/handoff, context-pressure transfer, immediate failure/incident capture, failure-mode lookback, or feature-level post-mortem execution. Detect the actual execution capabilities first: choose persistence, checkpoint, recovery, and telemetry behavior from what is durable, writable, verifiable, authorized, and available now. Chat and Codex are common profiles, not the ontology."
---

# Entif Runtime

Own the execution epoch. Keep one shared state model and select policy from the actual execution capabilities, using named product adapters only as presets when they fit.

## 1. Resolve authority and execution capabilities

1. Resolve applicable public Rosetta authority and, when authorized, relevant protected Entif authority before material mutation.
2. Classify public/external writes before acting. Accessibility is not disclosure permission.
3. Surface authority conflicts and stop or narrow work rather than silently reconciling incompatible authorities.
4. Determine the execution surface before initializing persistence. Prefer observed capabilities and constraints over product labels or task wording.
5. Read `references/RUNTIME_MODEL.md` and `references/SURFACE_CAPABILITIES.md`.
6. When a common preset fits, read exactly one of `references/CHAT_ADAPTER.md` or `references/CODEX_ADAPTER.md`; otherwise compose policy directly from the capability matrix.
7. Read `references/WORK_ORCHESTRATION.md` when taking up ready work for execution.
8. Read `references/HANDOFF_RECOVERY.md` for checkpoint, transfer, completion, emergency handoff, or resumption.
9. Read `references/FAILURE_INTELLIGENCE.md` after a material failure/near miss, failed handoff, repeated operational trap, or recovery from an abnormal termination.
10. Read `references/CONTEXT_PRESSURE.md` for long or retrieval-heavy work. Read `references/RECOVERY.md` after interruption, stale state, or ambiguous side effects.
11. Read `references/PR_CLOSEOUT.md` for PR/review/finalization or resumed post-finalization work.
12. Read `references/FEATURE_POSTMORTEM.md` only after the full root feature reaches its governing completion/deployment gate.

Never execute a persistence policy merely because the current product usually uses it. A writable, durable Git worktree may justify branch checkpoints on more than one product; a GitHub API connector without a writable worktree does not. A non-persistent sandbox needs an external durability channel even when its host label is unfamiliar.

If an authorized persistence connector is reachable but an expected capability is absent or transiently disappears, use the same-invocation connector recovery protocol in `references/connector-recovery.md`. Only an explicit provider denial counts as `PERMISSION_DENIED`; a missing capability surface is not itself a permission failure. Rebind/reinitialize/restart as prescribed and do **not** require another user prompt merely to continue recovery. Reconcile the target before retrying any ambiguous write.

## 2. Initialize one execution epoch

Use one stable run/work identity across feature lifecycle, Work Stack, continuity journal, durability checkpoints, recovery receipts, and failure-intelligence evidence.

Shared ownership:

- **Work orchestration**: take up already-ready bounded work, bind procedure/executor/runtime surface, and route the legal execution frontier without redefining desired state.
- **Feature lifecycle**: branch/lease/checkpoint/check-in, verification and handoff.
- **Work Stack**: dependent tasks, attempts, idempotency/reconciliation, receipts, safe holds, stale outputs.
- **Continuity**: compact semantic frontier, journal/cursors, transfer/recovery bootstrap.
- **Durability**: proof that valuable bytes/state escaped the disposable execution locus.
- **Pressure controller**: decides when to materialize or evacuate active context. It does not weaken model/reasoning quality.
- **Failure intelligence**: preserve material failure evidence, compose Logic when analysis is non-trivial, file/reconcile incidents promptly, retrieve applicable prior failure patterns, and project bounded gotchas into the active run.
- **PR closeout**: owns review obligations, evidence-bound finalization, candidate cleanup, one-hop synopsis, and merge-readiness proof; merge authority remains separate.
- **Feature post-mortem execution**: compiles completed-feature evidence, invokes governed evaluation, and stages separate improvement proposals; Governance owns institutional adoption/state.

Do not maintain competing handwritten copies of task state. Pointers may be duplicated; authority may not.

## 3. Execute through shared states

For material dependent work:

`planned/ready -> executing -> receipt_observed when external -> verified -> committed`

Before replaying an interrupted side effect, classify it as:

`requested_not_executed | executed_receipt_present | executed_ack_unknown | retryable_idempotent | non_idempotent_or_ambiguous`

A crash is not evidence that an external mutation failed.

Use bundled helpers when applicable:

```bash
python scripts/work_stack.py ...
node scripts/session-journal.mjs ...
python scripts/run_durability.py ...
python scripts/runtime_controller.py ...
python scripts/runtime_handoff.py ...
```

For ready work, apply `references/WORK_ORCHESTRATION.md`: bind the durable objective/readiness refs first, then select procedure/executor/runtime surface. Do not let execution create missing Architecture/specification authority by accident.

## 4. Checkpoint on semantics, risk, and time

Checkpoint at coherent boundaries earlier than the time ceiling. Also enforce the active capability profile's dirty-work ceiling.

- **Durable writable Git worktree profile**: when the repository/branch is the execution durability plane, target a commit + push about every 5 minutes while materially dirty; never exceed 10 minutes without a branch checkpoint unless the current operation cannot be interrupted safely. Track runtime state under `.entif/runtime/` when project policy permits.
- **Disposable local/sandbox profile**: externally persist substantial dirty work/continuity state at semantic boundaries and no later than the configured ceiling, default 10 minutes. Google Drive is a common authorized file-durability channel when available, not a universal requirement.
- **Hybrid profile**: when independent persistence is materially useful, both may be used, but do not duplicate state merely because two tools exist.

At every material checkpoint, refresh the standard `entif.runtime.handoff/v1` state with `kind=checkpoint` unless transfer/completion/emergency applies. A checkpoint is valid only after its active persistence receipt is verified.

## 5. Guard context without shrinking capability

Treat conversation/context as a hot cache, not the durable source of execution truth.

Use `SAFE -> PREPARE -> TRANSFER -> SAFE`, with `CRITICAL` for emergency evacuation. Prefer native occupancy telemetry; otherwise use conservative operational signals. At PREPARE, materialize current mission, decisions, negative knowledge, live refs, unresolved hypotheses, receipts, and next safe operations. At TRANSFER, persist and verify that capsule, reconcile ambiguous side effects, then continue in a fresh context.

Do not solve pressure by switching to a weaker model, lowering reasoning effort, dropping verification, or arbitrarily narrowing the user's requested outcome.

## 6. Recover from evidence and learn before replay

Follow `references/HANDOFF_RECOVERY.md` and narrate each material fallback decision. Recovery order is: explicit handoff -> Runtime/Work Stack -> verified adapter checkpoint -> `FEATURE_LOG.md` plus Git/issue/PR/live receipts -> reduced run trace as last-resort evidence.

After selecting the strongest surviving source:

1. Validate source identity and freshness before trusting prose.
2. Validate Work Stack and the highest verified persistence checkpoint when present.
3. Reconcile executing/receipt-observed/safe-held tasks against live targets before replay.
4. Read only the journal tail/source artifacts required by the hydration map.
5. Reacquire or validate feature-work ownership before mutation.
6. Preserve negative knowledge and distinguish observed/reconciled facts from inference.
7. If the prior run failed, nearly failed, or terminated abnormally, apply `references/FAILURE_INTELLIGENCE.md` before broad new mutation: preserve evidence, assess incident materiality, retrieve relevant prior incidents/patterns, and load only applicable gotchas into the run.
8. Materialize a fresh `entif.runtime.handoff/v1` checkpoint before broad new work when recovery changed or reconstructed state.

If only a reduced run trace survives, read `references/TRACE_RECOVERY.md`.

## 7. File failure evidence while it is fresh

A material failure/near miss MUST NOT wait for feature completion merely because the run can continue.

Runtime owns the execution path to the canonical incident/case ledger. During migration, the existing `entif-postmortem-logger` entrypoint MAY remain eagerly visible as a compatibility trigger, but it delegates to this Runtime-owned failure-intelligence path and is not a separate source of execution truth.

When the failure mechanism is ambiguous, repeated, rhetorically slippery, or likely to influence future authority, compose the `logic` meta-skill before asserting root cause. Keep observations, reconstructions, evaluations, and hypotheses distinct.

Do not block safe containment on exhaustive RCA. Preserve the incident first; enrich it as evidence improves.

## 8. Close the execution epoch

Before completion or merge:

1. Verify actual requested outcomes and validation receipts.
2. Validate Work Stack, continuity, durability, failure-intelligence state, and branch/lease state.
3. Reconcile ambiguous external attempts.
4. For a Git-worktree profile using `.entif/runtime/`, run the runtime merge-cleanliness gate. `.entif/runtime/` MUST NOT exist in the merge candidate tree.
5. Preserve runtime history on the feature branch/PR history; do not merge runtime scratch/journals into `main`.
6. Materialize a `completion` handoff and externalize any needed final runtime evidence before deleting branch-local runtime state.
7. Apply `references/PR_CLOSEOUT.md` for review/finalization, archive, candidate cleanup, and merge-readiness proof; readiness does not create merge authority.
8. After the full root feature reaches its governing completion/deployment gate, route feature-level retrospective execution through `references/FEATURE_POSTMORTEM.md`.
9. Perform postflight validation against the real resulting state after action; helper success or a model-authored claim is not sufficient proof.
10. Update authority maps only when authority relationships actually changed.

## Progressive disclosure

- `references/RUNTIME_MODEL.md` - canonical ownership/state model.
- `references/SURFACE_CAPABILITIES.md` - capability predicates and persistence-profile selection.
- `references/CHAT_ADAPTER.md` - common disposable-sandbox/external-persistence preset.
- `references/CODEX_ADAPTER.md` - common durable Git-worktree preset.
- `references/WORK_ORCHESTRATION.md` - ready-work uptake, procedure/executor selection, and dispatch boundary.
- `references/HANDOFF_RECOVERY.md` - shared checkpoint/transfer/completion/emergency format and recovery ladder.
- `references/handoff.schema.json` - machine-readable handoff v1 shape.
- `references/FAILURE_INTELLIGENCE.md` - incident capture, Logic composition, prior-failure lookback, and gotcha projection.
- `references/TRACE_RECOVERY.md` - last-resort recovery from reduced run traces.
- `references/CONTEXT_PRESSURE.md` - SAFE/PREPARE/TRANSFER/CRITICAL controller.
- `references/RECOVERY.md` - crash, compaction, ambiguity, stale-lease recovery.
- `references/PR_CLOSEOUT.md` - review/finalization, archive, merge-cleanliness, and resume-after-finalization.
- `references/FEATURE_POSTMORTEM.md` - completed-feature evaluation/proposal execution and Governance handoff.
- `references/MIGRATION_INVENTORY.md` - legacy runtime/orchestration/post-mortem dispositions and compatibility.

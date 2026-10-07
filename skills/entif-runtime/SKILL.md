---
name: entif-runtime
description: "Govern durable Entif/Rosetta execution across ChatGPT and Codex with one environment-aware runtime control plane. Use for substantial feature work, long multi-tool runs, dependent operations, branch leases/checkpoints, Work Stack state, crash/context recovery, context-pressure transfer, or any task where progress must survive interruption. Detect the execution surface first: Chat uses verified external persistence such as Google Drive; Codex uses frequent committed/pushed feature-branch checkpoints and tracked branch-local runtime state. Compose shared task, receipt, continuity, durability, and recovery semantics without making either environment imitate the other."
---

# Entif Runtime

Own the execution epoch. Keep one shared state model and select the correct persistence adapter for the actual environment.

## 1. Resolve authority and surface

1. Resolve applicable public Rosetta authority and, when authorized, relevant protected Entif authority before material mutation.
2. Classify public/external writes before acting. Accessibility is not disclosure permission.
3. Surface authority conflicts and stop or narrow work rather than silently reconciling incompatible authorities.
4. Determine the runtime surface before initializing persistence. Prefer explicit host/product identity and actual capabilities over inference from task wording.
5. Read `references/RUNTIME_MODEL.md`, then exactly one of `references/CHAT_ADAPTER.md` or `references/CODEX_ADAPTER.md`.
6. Read `references/CONTEXT_PRESSURE.md` for long or retrieval-heavy work. Read `references/RECOVERY.md` after interruption, stale state, or ambiguous side effects.

Never execute Chat persistence policy in Codex merely because Drive exists. Never treat Chat connector access to GitHub as proof of a Codex writable worktree.

If an authorized persistence connector is reachable but an expected capability is absent or transiently disappears, use the same-invocation connector recovery protocol in `references/connector-recovery.md`. Only an explicit provider denial counts as `PERMISSION_DENIED`; a missing capability surface is not itself a permission failure. Rebind/reinitialize/restart as prescribed and do **not** require another user prompt merely to continue recovery. Reconcile the target before retrying any ambiguous write.

## 2. Initialize one execution epoch

Use one stable run/work identity across feature lifecycle, Work Stack, continuity journal, durability checkpoints, and recovery receipts.

Shared ownership:

- **Feature lifecycle**: issue/plan readiness, branch/lease/checkpoint/check-in, verification and handoff.
- **Work Stack**: dependent tasks, attempts, idempotency/reconciliation, receipts, safe holds, stale outputs.
- **Continuity**: compact semantic frontier, journal/cursors, transfer/recovery bootstrap.
- **Durability**: proof that valuable bytes/state escaped the disposable execution locus.
- **Pressure controller**: decides when to materialize or evacuate active context. It does not weaken model/reasoning quality.

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
```

## 4. Checkpoint on semantics and time

Checkpoint at coherent boundaries earlier than the time ceiling. Also enforce the adapter's dirty-work ceiling.

- **Codex**: target a Git commit + push about every 5 minutes while materially dirty; never exceed 10 minutes without a branch checkpoint unless the current operation cannot be interrupted safely. Track runtime state under `.entif/runtime/` on the feature branch.
- **Chat**: externally persist substantial dirty work/continuity state at semantic boundaries and no later than the configured ceiling, default 10 minutes. Google Drive is the default authorized file-durability channel when available.

A checkpoint is valid only after its adapter-specific receipt is verified.

## 5. Guard context without shrinking capability

Treat conversation/context as a hot cache, not the durable source of execution truth.

Use `SAFE -> PREPARE -> TRANSFER -> SAFE`, with `CRITICAL` for emergency evacuation. Prefer native occupancy telemetry; otherwise use conservative operational signals. At PREPARE, materialize current mission, decisions, negative knowledge, live refs, unresolved hypotheses, receipts, and next safe operations. At TRANSFER, persist and verify that capsule, reconcile ambiguous side effects, then continue in a fresh context.

Do not solve pressure by switching to a weaker model, lowering reasoning effort, dropping verification, or arbitrarily narrowing the user's requested outcome.

## 6. Recover from evidence

After interruption:

1. Load the compact runtime/feature state before transcript history.
2. Validate the Work Stack and highest verified adapter checkpoint.
3. Reconcile executing/receipt-observed/safe-held tasks against live targets.
4. Read only the journal tail after the last trustworthy cursor by default.
5. Reacquire or validate feature-work ownership before mutation.
6. Materialize a new checkpoint before broad new work if recovery changed state.

## 7. Close the execution epoch

Before completion or merge:

1. Verify actual requested outcomes and validation receipts.
2. Validate Work Stack, continuity, durability, and branch/lease state.
3. Reconcile ambiguous external attempts.
4. For Codex, run the runtime merge-cleanliness gate. `.entif/runtime/` MUST NOT exist in the merge candidate tree.
5. Preserve runtime history on the feature branch/PR history; do not merge runtime scratch/journals into `main`.
6. Use the canonical PR closeout capability for merge-ready work; readiness does not create merge authority.
7. Perform postflight validation against the real resulting state after action; helper success or a model-authored claim is not sufficient proof.
8. Update authority maps only when authority relationships actually changed.

## Progressive disclosure

- `references/RUNTIME_MODEL.md` — canonical ownership/state model.
- `references/CHAT_ADAPTER.md` — Chat persistence and recovery policy.
- `references/CODEX_ADAPTER.md` — Codex feature-branch checkpoint/scratch policy.
- `references/CONTEXT_PRESSURE.md` — SAFE/PREPARE/TRANSFER/CRITICAL controller.
- `references/RECOVERY.md` — crash, compaction, ambiguity, stale-lease recovery.
- `references/MIGRATION_INVENTORY.md` — legacy Feature Workflow / Session Continuity / Run Durability / Work Stack disposition and compatibility.

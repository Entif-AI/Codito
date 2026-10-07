# Recovery protocol

Use this when a session, runtime, sandbox, output link, or final-delivery step failed after substantive work may have completed.

1. Read `RUN_START.json`, `STATUS.json`, and `ExternalPersistence/remote-index.json` from the most trustworthy available location.
2. Identify the highest checkpoint satisfying the configured policy.
3. Verify the remote object still exists. Compare hashes when provider/download tooling makes that practical.
4. Rehydrate only the current task's needed files and dependencies.
5. Use checkpoint manifests to distinguish changed, deleted, and unchanged paths.
6. If a connected side effect has ambiguous acknowledgement, do not infer failure from the crash. Reconcile the live target or use Entif Work Stack safe-hold/reconciliation state.
7. Record discrepancies instead of repeatedly rereading the same state.
8. Resume from the recorded next action.

A recovery loop has failed when it repeatedly inspects the same persisted material without either advancing the next required operation or isolating a concrete inconsistency/blocker. Stop that loop and preserve the smallest known failing surface plus the last verified checkpoint.

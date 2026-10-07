# Recovery

Recover from receipts and live state, not remembered intent.

1. Detect environment and locate its highest verified checkpoint.
2. Load compact feature/runtime state first.
3. Validate Work Stack structure and inspect executing, receipt-observed, safe-held, and stale tasks.
4. Reconcile external side effects against the live target before retry.
5. Validate/reacquire feature ownership/lease when repository mutation is involved.
6. Hydrate only the journal tail and source artifacts needed for the recorded next safe operations.
7. Record negative knowledge so searches/failed approaches are not repeated.
8. Materialize a new trustworthy checkpoint if recovery changes state.

Adapter-specific authority:

- Chat: the latest verified external receipt outranks newer sandbox-only bytes for durability claims.
- Codex: the latest verified pushed feature-branch commit is the primary recovery point unless a stronger explicit external checkpoint applies.

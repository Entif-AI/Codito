# Recovery

Recover from receipts and live state, not remembered intent. Use `HANDOFF_RECOVERY.md` as the discovery/handoff contract and narrate each material fallback decision.

Recovery order:

1. explicit supplied handoff/bootstrap;
2. Runtime `HANDOFF.json` + Work Stack;
3. highest verified adapter checkpoint/archive;
4. `FEATURE_LOG.md` + Git/issue/PR/live-target evidence;
5. reduced run trace as last-resort evidence.

After selecting a source:

1. detect environment and verify source identity/freshness;
2. validate Work Stack structure and inspect executing, receipt-observed, safe-held, and stale tasks;
3. reconcile external side effects against the live target before retry;
4. validate/reacquire feature ownership/lease when repository mutation is involved;
5. hydrate only the journal tail/source artifacts named by the handoff or required for the next safe operations;
6. record negative knowledge so searches/failed approaches are not repeated;
7. distinguish observed/reconciled state from inference;
8. after material failure or abnormal termination, apply `FAILURE_INTELLIGENCE.md` before broad mutation so filing and prior-failure lookback happen while evidence is fresh;
9. materialize and verify a new standard handoff/checkpoint if recovery changes or reconstructs state.

Persistence-profile authority:

- Disposable-local profile: the latest verified external receipt outranks newer local-only bytes for durability claims.
- Durable-Git profile: the latest verified pushed feature-branch commit is the primary recovery point unless a stronger explicit external checkpoint applies.

If only a reduced trace survives, apply `TRACE_RECOVERY.md`; the trace is forensic evidence and cannot by itself prove external side-effect failure or platform-level termination cause.

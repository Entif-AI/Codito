# Work Stack Composition

Use Entif Work Stack when a session contains a bounded sequence of operations whose correctness depends on order, payload handoff, side-effect acknowledgment, or replay safety.

## Division of authority

- Session journal: what materially happened in the conversation/session and bounded operation references.
- FEATURE_LOG: compact causal/resumability view for a successor.
- Work Stack: current task dependencies, attempt state, idempotency/reconciliation, receipts, and local input/output snapshots.
- Git/issues/tests/connected targets: stronger truth surfaces in their own domains.

Do not copy the entire Work Stack into FEATURE_LOG. Record only `work_id`, durable location, current/blocked/safe-held task IDs, and the next safe operation.

## Recovery

After interruption, read FEATURE_LOG, then validate the referenced Work Stack before retrying an operation. If Work Stack and session prose disagree about execution state, reconcile against the live external target/receipts rather than choosing whichever narrative is newer.

A Work Stack task becoming stale is a continuation signal: upstream bytes/state changed after the task was committed. It is not proof that the underlying scientific or engineering claim is false.

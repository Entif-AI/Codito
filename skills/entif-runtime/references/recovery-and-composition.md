# Recovery and Composition

## Recovery rule

On interruption:

1. load `WORK.json` and regenerated `STATUS.json`;
2. run `validate` before replaying side effects;
3. inspect executing, receipt-observed, safe-hold, or stale tasks first;
4. reconcile live external state for ambiguous operations;
5. resume only tasks whose dependencies are committed and current;
6. avoid replaying already committed tasks.

## Session Continuity

When Entif Session Continuity is active:

- store the work ID/path and current task IDs in the compact continuation state;
- journal bounded operation events by reference rather than duplicating full task payloads;
- let the Work Stack own dependency/idempotency/attempt state;
- let Session Continuity own conversational context, causal notes, and transfer/recovery guidance.

A session crash does not mutate work-stack task truth.

## Research Factory

Use the Work Stack when Factory execution contains immediate dependencies such as:

- source bytes -> extraction -> evidence window -> crosswalk update;
- manuscript mutation -> regenerated traceability -> manifest -> QA -> persistence;
- experiment config -> execution -> raw results -> aggregation -> interpretation;
- package repack -> remote upload -> readback verification -> receipt update.

Do not make every research thought a task.

## Connected tools

Connected-tool receipts belong to the target system/operator. Store a bounded receipt reference or copy in `receipts/` when it improves recovery.

For ambiguous acknowledgments, reconcile the live target before retrying. Work Stack state cannot turn an attempted external action into a verified external action by declaration.

## Nested work

Spawn a child bucket when a subproblem has several internal dependencies or may proceed/fail independently. Parent tasks may depend on a child completion receipt/reference, but avoid deeply nesting trivial work.

## Persistence

The local work bucket is useful even before external persistence. If sandbox loss would materially harm recovery, externalize the bucket/checkpoint under the governing workflow's persistence contract. Do not infer that local durability is remote durability.

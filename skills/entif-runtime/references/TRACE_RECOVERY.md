# Reduced Trace Recovery

Use this only when stronger structured runtime state is absent or insufficient and a user supplies a reduced run trace such as the output of the `trace-skim` workflow developed for ChatGPT/Astra run exports.

The trace is forensic evidence, not authority and not proof that a side effect did or did not occur.

## Recognized useful structure

Prefer these sections when present:

- source identity/hash and conversation metadata;
- final statistics and unexpected/error/tool-failure census;
- `Recovery capsule`;
- last user message;
- last assistant message;
- last reasoning/analysis summary record;
- recent tool calls;
- execution/tool failure signals;
- timestamped user/assistant/reasoning/tool events.

Do not require every field. Older skimmer versions may omit some of them.

## Last-resort reconstruction procedure

1. **State the fallback.** Narrate that structured state was not found and that the reduced trace is being used as last-resort evidence.
2. **Verify provenance.** Preserve source path/conversation ID/SHA-256 when present. Do not pretend a reduced derivative is the raw export.
3. **Recover the controlling mission.** Start from the latest material user instruction, then the latest assistant checkpoint/reasoning summary.
4. **Recover execution frontier.** Read recent tool calls/outputs and extract durable identifiers: repository, issue, PR, branch, commit, Work ID/task ID, Drive/Doc/Sheet ID, checkpoint ID, external receipt, and target object.
5. **Separate transport success from operation success.** Inspect inner failure signals such as command exit status, traceback, explicit result errors, or ambiguous acknowledgement.
6. **Reconcile live state.** Query GitHub/Drive/other targets for the identifiers found. Never infer that the last attempted side effect failed because the trace ended.
7. **Classify each unfinished side effect** using Runtime's standard recovery states.
8. **Recover negative knowledge.** Preserve failed commands, rejected hypotheses, completed searches, and explicit user corrections that would otherwise be repeated.
9. **Create a fresh handoff.** Materialize `entif.runtime.handoff/v1` with `source_trace` identifying the reduced trace and with reconstructed facts separated from unresolved inference.
10. **Checkpoint before broad work.** Persist/verify the reconstructed handoff and Work Stack state through the active adapter, then resume.

## Confidence discipline

A trace can often prove that the run was still working when it stopped, which operations were attempted, and which receipts were returned. It usually cannot prove the platform-level cause of termination unless an explicit platform error is present.

Use labels such as `observed`, `reconciled_live`, and `inferred` in working notes when reconstruction depends on interpretation. Do not upgrade inference into a receipt.

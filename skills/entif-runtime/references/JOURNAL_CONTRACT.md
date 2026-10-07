# Session Journal Contract

## Location

The journal schema is shared; the active runtime adapter selects the durable location.

- **Codex:** `.entif/runtime/journal/<session-id>.jsonl` on the tracked feature branch.
- **Chat:** keep the local journal in the active run workspace and include it in the verified external continuity/durability checkpoint; do not rely on sandbox lifetime.

Use one file per execution/session epoch. Do not create a second journal merely because the persistence adapter changes.

## Common record fields

Every record contains:

```json
{
  "schema": "entif.session-journal/v1",
  "seq": 1,
  "session_id": "session-id",
  "work_epoch_id": "work-epoch-id",
  "lease_id": "lease-id",
  "type": "session_start",
  "recorded_at": "RFC3339 timestamp"
}
```

`seq` is strictly monotonic and contiguous within a journal. Identity fields remain stable within one journal.

## Turn record

```json
{
  "type": "turn",
  "role": "user",
  "content": "...",
  "content_sha256": "64 lowercase hex chars"
}
```

Allowed roles are `user` and `assistant`.

## Operation record

```json
{
  "type": "operation",
  "operation_id": "op-...",
  "operation_type": "github.update_file",
  "target_ref": "bounded durable target",
  "request_digest": "64 lowercase hex chars",
  "status": "executed_receipt_present",
  "receipt_ref": "commit/comment/object id"
}
```

Allowed structural statuses:

- `requested_not_executed`
- `executed_receipt_present`
- `executed_ack_unknown`
- `retryable_idempotent`
- `non_idempotent_or_ambiguous`

The status records recovery posture. It does not prove the semantic safety of replay.

## Checkpoint record

```json
{
  "type": "checkpoint",
  "materialized_through_seq": 42,
  "feature_log_sha256": "...",
  "git_sha": "...",
  "checkpoint_kind": "semantic"
}
```

`materialized_through_seq` must not exceed the sequence immediately preceding the checkpoint record.

## Privacy and minimization

- Raw journals are private by default.
- Do not copy protected connector payloads or large tool results when a durable pointer/receipt suffices.
- Do not publish raw journals to public Rosetta merely because a branch or conversation is accessible.
- Retention/purge behavior is operational policy and may become stricter than branch lifetime.
- Finalization should remove branch-operational journal files from the merge candidate unless an explicit private retention destination is defined.

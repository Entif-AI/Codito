# Durability model

## State separation

Do not collapse these states:

- `LOCAL_ONLY`: bytes exist only in the current execution locus.
- `CHECKPOINT_PREPARED`: a local immutable checkpoint/delta and hashes exist.
- `PRIMARY_ATTEMPTED`: external primary persistence was attempted, outcome not yet proven.
- `PRIMARY_VERIFIED`: a concrete primary-channel receipt exists and the target was verified as strongly as practical.
- `WITNESS_REQUIRED_PENDING`: primary persistence exists but required independent witness does not.
- `WITNESSED`: an authorized independent witness receipt covers the exact checkpoint/archive bytes.
- `POLICY_DURABLE`: all channels required by the run policy are verified.
- `PRE_QA_FROZEN`: current draft-complete hashes and their required receipts were mapped before QA; the freeze artifact itself still requires ordinary external persistence.
- `RECOVERY_READY`: a highest verified checkpoint and continuation point are available.

A provider receipt is evidence of the provider operation, not of scientific validity or semantic correctness.

## Run directory

```text
<run>/
  RUN_START.json
  STATE.json
  STATUS.json
  EVENTS.jsonl
  current-manifest.json
  ExternalPersistence/
    remote-index.json
  checkpoints/
    CP0001/
      checkpoint.json
      delta-manifest.tsv
      current-manifest.json
      delta/
      CP0001.bundle.zip
  freezes/
    PRE_QA_FREEZE-<id>.json
```

Checkpoint directories are append-only after creation. `STATUS.json` is a regenerated materialized view.

## Checkpoint semantics

Each checkpoint compares the tracked root against the previous current manifest and records:

- `ADD` for a new logical path;
- `MODIFY` when bytes changed;
- `DELETE` as a tombstone without erasing older checkpoint bytes.

The checkpoint bundle contains the checkpoint record, delta manifest, current manifest, and changed bytes. Recovery can apply checkpoints in order or use a provider-maintained current mirror when one is available and verified.

## Draft-complete coverage

A draft-complete record binds a logical path to an exact SHA-256 and the checkpoint that introduced that hash. A later change invalidates prior coverage for the new bytes without deleting the old witness history.

## Policy modes

`primary_channel` is normally required for all checkpoints and defaults to `drive`. For Drive, destination resolution should prefer an explicit package/run parent, then an obvious project working folder under a unique `ExternalPersistence/<run-id>` child, then `/ChatGPT/<run-id>` in My Drive as the non-interrupting fallback.

`dirty_ceiling_minutes` is configurable and defaults to `10`. Semantic boundaries may produce earlier primary checkpoints.

`witness_mode`:

- `none`: default; no second channel is required;
- `optional`: record witness receipts when explicitly enabled/available but do not block durability on them;
- `required`: current draft-complete artifacts and required freeze/finalization states need both primary and witness coverage before the relevant gate.

`witness_interval_minutes` defaults to `10` when witnessing is enabled. Witness transport is checkpoint-level: prefer one manifested checkpoint archive at the cadence boundary rather than one message per file/save. Freeze/final safety points may force an immediate witness flush.

Gmail is the preferred currently-tested witness transport when the user opts in. Never infer a witness recipient. Slack messaging is coordination-only unless its connector later exposes verified durable file persistence.

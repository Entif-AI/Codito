# Chat adapter

Use when the runtime is ChatGPT/Atlas/API without a durable writable Git worktree that acts as the execution locus.

## Persistence

Local sandbox state is disposable. Establish external persistence before substantial work accumulates.

Default authorized file channel: Google Drive. Resolve an explicit run destination first; otherwise use the project's obvious working area or a unique `/ChatGPT/.../ExternalPersistence/<run-id>/` root.

Persist:

- run start identity/policy;
- Work Stack snapshot/bundle when material state changes;
- continuity journal/capsule;
- changed valuable artifacts or lossless checkpoint bundles;
- receipts returned by the provider.

Do not claim durability without a concrete remote receipt/readback.

## Cadence

Checkpoint at semantic boundaries. While materially dirty, default maximum external dirty interval is 10 minutes. Context pressure may force an earlier PREPARE/TRANSFER.

## GitHub

GitHub connector operations may create/update issues, branches, files, or PRs when authorized, but connector access is not a Codex worktree. Do not adopt the Codex `.entif/runtime/` branch-scratch policy unless the actual execution locus is a writable repo worktree.

## Transfer

Before deliberate context rollover, persist and verify the semantic frontier plus pointers to remote artifacts/receipts. A successor should hydrate only required live state, not replay the full transcript.

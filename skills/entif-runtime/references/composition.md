# Composition map

## Work Stack

Use Work Stack when correctness depends on execution order or payload handoff. A checkpoint operation can itself be one Work Stack task:

`prepare delta -> upload primary -> readback -> record receipt -> optional witness -> verify policy`

Work Stack answers whether the operation may run/replay. Run Durability answers whether the bytes are externally recoverable.

## Session Continuity

Continuity should record:

- durability run ID;
- highest verified checkpoint;
- current durability state;
- exact remote index/status locator;
- any primary/witness failure blocking continued work.

Do not copy every checkpoint manifest into the session journal.

## Research Factory

When Factory enables external persistence:

- prove durability during startup before a long research batch;
- when the package can encounter a partially exposed authorized connector, include the concrete same-invocation recovery contract from `connector-recovery.md` in the launch/execution package; do not compress it to generic `refresh binding`/`rediscover` language;
- preserve the explicit rule that an already-authorized read-only action surface is `CAPABILITY_NOT_EXPOSED`, not `PERMISSION_DENIED`;
- preserve the explicit instruction to restart/reinitialize/rebind the connector/session itself, tolerate the transient stream/tool interruption, rediscover after reconnection, and continue without another user prompt;
- checkpoint at semantic workstream transitions;
- checkpoint before risky rendering/package/review operations;
- complete PRE_QA_FREEZE before package-level QA when required by policy;
- keep post-freeze remote receipts outside frozen package bytes to avoid self-referential repacking.

## Research Publication

Durability operates inside a publication stage. It does not add human discussion gates. Stage handoffs should state the highest verified checkpoint when a long run used this Skill.

## Connected tool operation

The connected-tool owner performs the external mutation and returns the receipt. This Skill records that receipt and local hash relationship. If the tool cannot produce a durable artifact or receipt required by policy, fail honestly rather than substituting prose.

## Connector roles

### Google Drive

Default primary durability transport when available and authorized. Prefer a package-declared destination, otherwise an obvious project working folder with a unique run child, otherwise `/ChatGPT/<run-id>` in My Drive. Preserve one run per subfolder.

### Gmail

Opt-in witness transport. Ask for the recipient only when the user enables email witnessing and the current run lacks an authorized address. Send manifested checkpoint bundles on the configured witness cadence (default 10 minutes) plus forced freeze/final flushes. Do not mirror every file save or every semantic checkpoint.

### Slack

Use for lightweight multi-agent coordination when useful: run/checkpoint IDs, task ownership, blockers, handoff notes, and links to the durable Drive state. Under the currently observed messaging-only connector surface, Slack does not satisfy file durability and must not be counted as a primary or witness receipt.

# Execution Surface Capabilities

Runtime policy is selected from observed capabilities, permissions, durability guarantees, and failure modes. Product labels are shortcuts, not semantic authority.

## Capability census

Before substantial work, establish what is true now:

| Capability | Question | Consequence |
|---|---|---|
| durable writable worktree | Can the agent write a repository worktree whose commits can be pushed and later recovered? | Git may be the primary durability plane. |
| branch/lease control | Can the agent safely acquire/verify branch ownership and push checkpoints? | Enables branch-local Runtime state and lease-aware replay. |
| external durable file store | Can valuable state be written outside the disposable execution locus and read back? | Required when local state may disappear; useful as independent witness when policy requires. |
| local persistence guarantee | Does local filesystem state survive process/session/context replacement? | Determines whether local journals are evidence or only cache. |
| mutation authority | Which external systems may be changed, and under what classes of mutation? | Constrains Work Stack frontier and handoff authority. |
| readback/verification | Can the agent verify the canonical postcondition after writes? | Determines whether an acknowledgement is sufficient or stronger reconciliation is required. |
| context telemetry | Is native context/headroom/compaction telemetry exposed? | Preferred input to pressure controller. |
| stable run/session identity | Is there a durable run/thread/job identity? | Bind it into handoffs, telemetry, incident evidence, and Akasha export when applicable. |
| structured checkpoint source | Does a Runtime/Work Stack/checkpoint already exist? | Prefer it over transcript reconstruction. |
| incident/case access | Can prior incidents, root causes, patterns, or operational gotchas be queried? | Enables preflight failure-intelligence retrieval. |

Record unknowns as unknown. Do not infer durability from a filesystem path, authorization from tool visibility, or a writable GitHub API from the existence of a local Git worktree.

## Common profiles

### Disposable local + external persistence

Typical of Chat sessions with a sandbox and connected Drive/GitHub tools.

- local bytes are cache until externalized;
- checkpoint to a verified external destination;
- GitHub API mutations do not create a writable-worktree lease model;
- recovery prefers verified remote receipts.

`CHAT_ADAPTER.md` is the current convenience preset.

### Durable writable Git worktree

Typical of Codex/local engineering sessions, and potentially other future agents.

- feature branch is the primary execution durability plane;
- commit + push checkpoints preserve source and Runtime state;
- `.entif/runtime/` may be tracked during execution and must be absent from the final merge candidate;
- recovery prefers the latest verified pushed checkpoint.

`CODEX_ADAPTER.md` is the current convenience preset.

### Hybrid

A writable Git worktree plus one or more independent durable stores.

Use multiple channels only when they serve different guarantees: independent witness, large artifact storage, cross-surface transfer, policy requirement, or a future Akasha export. Do not mirror every byte by reflex.

### Unfamiliar surface

When no named adapter fits, compose from the census directly:

1. choose the strongest authorized durability plane;
2. establish a checkpoint cadence appropriate to loss risk;
3. define verification/readback;
4. define handoff location;
5. define ambiguous-side-effect reconciliation;
6. define context-pressure signals;
7. define incident/failure evidence destination;
8. record the resulting profile in the run state.

Do not force the surface into a Chat/Codex label merely to reuse a preset.

## Dynamic capability changes

Capabilities can change mid-run: connector methods disappear, credentials expire, branch leases are lost, network access fails, or a formerly disposable environment gains a durable mount.

When a material capability changes:

1. freeze new risky side effects;
2. preserve current state using still-working channels;
3. re-run the capability census;
4. reconcile ambiguous writes;
5. select the new legal persistence/recovery path;
6. record the transition in Runtime state and, if material, failure intelligence.

A stale capability assumption is not authority to continue.

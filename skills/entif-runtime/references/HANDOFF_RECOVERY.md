# Standard Handoff and Recovery

Use one handoff grammar across Chat and Codex so checkpoints, deliberate transfers, completion, and emergency evacuation remain mutually intelligible.

Canonical machine shape: `references/handoff.schema.json` with schema ID `entif.runtime.handoff/v1`.

## Handoff kinds

- `checkpoint`: same worker/session is expected to continue; preserve a recoverable semantic frontier.
- `transfer`: a successor session/agent is expected to continue.
- `completion`: requested work is complete; preserve receipts, closure state, and any follow-up without implying more execution is pending.
- `emergency`: context pressure, connector/runtime instability, lease risk, or another imminent failure makes rapid preservation more important than narrative polish.

The same fields are used in every environment. Only persistence adapters differ.

## Required semantic fields

A useful handoff records:

- mission and controlling objective;
- exact issue/spec/plan/repository/branch/PR/lease refs that matter;
- Work Stack identity/location and current/blocked/safe-held task IDs;
- latest verified checkpoint and adapter receipt;
- completed outcomes with receipts rather than narrative claims;
- negative knowledge: ruled-out approaches, falsified hypotheses, known tool/environment traps, unsafe retries, and expensive searches that should not be repeated;
- unresolved side effects with their recovery state;
- ordered next safe operations;
- hydration map: `read_first`, `read_if_needed`, and condition-triggered material;
- verification instructions for live state;
- cleanup/merge posture;
- optional source-trace and Akasha receipt references.

Do not dump raw transcript or tool payload history into the handoff merely because it exists.

## Checkpoint workflow

At each semantic or time-triggered checkpoint:

1. validate/reconcile Work Stack state first;
2. refresh `HANDOFF.json` from current canonical facts;
3. set `kind=checkpoint` unless transfer/emergency/completion applies;
4. persist through the active adapter;
5. verify its receipt;
6. continue without a conversational approval gate.

### Codex

Store the current handoff at `.entif/runtime/HANDOFF.json` and include it in the normal feature-branch checkpoint commit/push. Before final runtime-root deletion, externalize the final completion/transfer state through the PR/issue/closeout evidence path as applicable.

### Chat

Include `HANDOFF.json` in the verified external checkpoint bundle or equivalent durable run state. A Drive receipt or stronger readback proves persistence; sandbox existence does not.

## Graceful transfer

Before a deliberate context/session replacement:

1. finish the current coherent unit when safe;
2. reconcile ambiguous external effects;
3. materialize a `transfer` handoff;
4. persist and verify it;
5. emit a concise bootstrap pointing to that handoff;
6. continue in a fresh context.

Reliability must not depend on graceful transfer succeeding. The recovery ladder below handles missing handoffs.

## Completion handoff

When work is complete:

- use `kind=completion`;
- bind exact outcomes and verification receipts;
- record known follow-up separately from incomplete current work;
- record merge/cleanup posture;
- leave `next_safe_operations` empty when no continuation is needed, or list explicit downstream follow-up without misrepresenting the current task as unfinished.

## Emergency handoff

When failure appears imminent:

- prefer a small truthful `emergency` handoff over a polished summary;
- preserve mission, current Work Stack/task state, latest verified checkpoint, ambiguous side effects, negative knowledge, and the next safe operation;
- checkpoint immediately through the fastest authorized durable adapter;
- do not start another risky or non-idempotent operation.

## Recovery discovery order

Use the strongest available surviving structure. Do not assume every layer exists.

1. explicit handoff/bootstrap supplied by the user, prior worker, issue, PR, or run package;
2. `.entif/runtime/HANDOFF.json` and Runtime/Work Stack state;
3. latest verified adapter checkpoint/archive and durability index;
4. `FEATURE_LOG.md` plus Git/issue/PR/live-target receipts;
5. reduced run/recovery trace as last-resort evidence.

Codex may use:

```bash
python scripts/runtime_handoff.py discover --repo . [--handoff PATH] [--recovery-log PATH]
```

Then validate a found handoff with:

```bash
python scripts/runtime_handoff.py validate PATH
```

The helper selects a starting evidence source. It does not authorize replay or prove semantic correctness.

## Recovery narration contract

The resuming agent SHOULD print or vocalize each material route decision so a human can see what state is being trusted and what fallback is being attempted.

Good examples:

- `Recovery: explicit handoff not found; checking Work Stack.`
- `Recovery: Work Stack found at .entif/runtime/work/...; validating task and receipt state before replay.`
- `Recovery: Work Stack not found; locating latest verified checkpoint.`
- `Recovery: extracting checkpoint CP0002; verifying checkpoint receipt before hydration.`
- `Recovery: checkpoint unavailable; reconciling FEATURE_LOG with Git/issue/PR state.`
- `Recovery: no structured runtime state survived; parsing reduced run trace as last-resort evidence.`
- `Recovery: ambiguous side effect OP-7 found; reconciling live target before retry.`
- `Recovery: new handoff/checkpoint materialized; resuming task T5.`

Keep narration coarse. Do not narrate every file read or tool call.

## Resume law

After selecting a source:

1. verify source identity and freshness;
2. validate Work Stack/checkpoint structure when present;
3. reconcile ambiguous side effects against live targets;
4. hydrate only the recorded frontier plus required dependencies;
5. verify branch/lease/issue/spec/plan/live refs before mutation;
6. materialize a fresh `entif.runtime.handoff/v1` checkpoint before broad new work if recovery changed or reconstructed state.

A newer narrative does not automatically outrank an older verified receipt.

# Recovery and Transfer

## Materialized handoff state

A graceful transfer or recovery checkpoint must preserve enough semantic state to continue intelligently, not merely mechanically.

Include:

1. mission/current objective;
2. bounded causal history explaining why current state exists;
3. exact live refs: issue, branch, PR, commit, lease, artifact/digest as applicable;
4. completed work and exact outcomes;
5. negative knowledge: failed approaches, falsified hypotheses, known false positives, rejected paths, environment/tool failures, and expensive-to-repeat mistakes;
6. decisions/invariants the successor must not casually reinterpret;
7. unresolved hypotheses/questions, explicitly separated from established facts;
8. ordered next safe operations;
9. context hydration map;
10. live-state verification instructions;
11. session/journal provenance and checkpoint cursor.

## Hydration map

Prefer explicit tiers:

```text
READ FIRST
- FEATURE_LOG.md
- current continuity handoff/checkpoint

READ IF NEEDED
- journal tail after checkpoint
- exact authority or implementation files named by current focus

READ ONLY IF A CONDITION OCCURS
- older transcript segments
- superseded design discussions
- historical issue/PR archaeology
```

## Negative knowledge test

Promote a negative result into `FEATURE_LOG.md` when forgetting it would plausibly cause a successor to:

- repeat substantial analysis;
- retry a rejected or unsafe action;
- modify an artifact that must remain unchanged;
- confuse infrastructure/tool failure with domain failure;
- revisit a falsified hypothesis as if new.

Do not promote every transient thought. The journal already preserves chronology.

## Side-effect reconciliation

For `executed_ack_unknown` or `non_idempotent_or_ambiguous` records:

1. inspect the target system directly;
2. look for the durable operation identity, content digest, commit/comment/object ID, or equivalent evidence;
3. classify what actually happened;
4. only then decide whether retry, compensation, or safe hold is appropriate.

Never use the absence of an in-session acknowledgement as proof the external action did not occur.

## Recovery discrepancies

If `FEATURE_LOG.md`, journal identity, lease identity, Git HEAD, or live external state disagree, preserve the discrepancy explicitly and fail toward safe hold until the controlling state is established.

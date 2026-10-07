# PR Closeout Runtime Module

This module absorbs the execution-lifecycle behavior formerly exposed as `entif-pr-closeout` while keeping merge authority distinct from merge readiness.

## Inputs

Closeout consumes the authoritative execution surfaces already owned by Runtime and project governance:

- originating issue/work contract;
- accepted spec/plan refs when applicable;
- current code/diff and Git history;
- standard Runtime handoff/checkpoint state;
- Work Stack/receipt state;
- validation/test/CI evidence;
- review obligations and resolution evidence.

Do not dump runtime journals or handoff JSON verbatim into public PR prose.

## PR narrative and delta

Summarize the implemented purpose, material decisions, acceptance coverage, validation, known limitations, integration posture, and follow-up from verified evidence.

When work state materially changes after a PR/issue update, emit only the relevant delta. Suppress duplicate/no-change replay when the same checkpoint/digest is already represented.

## Review rejection

A reviewer rejection or requested change becomes a durable unresolved obligation with provenance. Import it into the Runtime execution epoch/Work Stack before renewed mutation.

Do not silently mark rejected obligations resolved because a new worker/session starts.

## Finalization

Before `READY_TO_MERGE`:

1. verify all requested outcomes and required gates;
2. reconcile unresolved review obligations and ambiguous side effects;
3. ensure the feature lease/epoch is in its required finalization state;
4. externalize the final completion handoff and exact evidence that must survive runtime-root deletion;
5. archive required final worklog/handoff evidence through the issue/PR path without overwriting the issue body;
6. remove branch-operational `FEATURE_LOG.md` when the governing workflow requires it;
7. remove `.entif/runtime/` from the candidate tree;
8. commit/push cleanup and run the Runtime merge-cleanliness proof;
9. verify the actual candidate tree and remote head.

`READY_TO_MERGE` is not `MERGE_AUTHORIZED`. Merge requires an explicit durable authority receipt applicable to the exact candidate and gates.

## Parent synopsis

After accepted child work, emit only the scope-matched one-hop synopsis the immediate parent needs, with drill-down refs to child issue/PR/merge/evidence. Do not recursively spray raw child history up the hierarchy.

## Resume after finalization

If work resumes after closeout/finalization, preserve the prior archive unchanged and create a fresh Runtime work epoch/lease/handoff rather than mutating the historical final record.

## Post-closeout routing

After the full root feature reaches its completion/deployment gate, Runtime may invoke `FEATURE_POSTMORTEM.md`. Institutional learning/adoption still routes to Governance.

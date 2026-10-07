# Codex adapter

Use as the common preset when execution occurs in a writable Git repository/worktree and branch-local commits/pushes are the durable execution substrate. Codex often fits this profile, but the capability profile controls.

## Canonical runtime root

Use repository-root:

`.entif/runtime/`

This path is intentionally tracked on the feature branch and MUST NOT be gitignored.

Recommended layout:

```text
.entif/runtime/
  RUN.json
  HANDOFF.json    # standard checkpoint/transfer/completion/emergency handoff
  work/          # Work Stack bucket(s)
  journal/       # continuity journal / recovery capsule
  durability/    # checkpoint manifests / receipts
  scratch/       # bounded runtime scratch worth preserving across crashes
  telemetry/     # optional local run metrics; future Akasha adapter seam
```

Do not put ordinary product/source files here.

## Checkpoint cadence

While materially dirty:

- target a coherent Git checkpoint about every 5 minutes;
- hard ceiling: 10 minutes between committed + pushed checkpoints unless an operation cannot be interrupted safely;
- semantic milestones, risky mutations, migrations, bulk transforms, or context PREPARE trigger earlier checkpoints.

A Codex checkpoint means:

1. update Work Stack / continuity state and refresh `HANDOFF.json`;
2. stage intended source changes plus `.entif/runtime/` state;
3. run the cheapest relevant structural verification;
4. commit on the feature branch;
5. push;
6. verify remote branch head/lease as applicable.

Google Drive mirroring is NOT required by default in Codex. Use an additional remote channel only when the governing run explicitly requires independent persistence/witnessing or the repository cannot serve as the durability plane.

## Lease and feature lifecycle

Use the existing feature-workflow lease semantics: acquire before mutation, verify before checkpoint pushes, stop on lease loss, and preserve stale lease evidence in history. Work Stack does not replace the branch lease.

## Merge cleanliness

Runtime state is branch operational evidence, not `main` source.

Before declaring merge-ready:

1. materialize the final `completion`/`transfer` handoff and ensure all needed durable receipts/closeout evidence exist outside the soon-to-be-deleted runtime directory;
2. delete `.entif/runtime/` from the worktree;
3. commit and push that deletion;
4. run `python scripts/runtime_controller.py merge-check --repo .`;
5. verify the candidate tree contains no `.entif/runtime/` entries.

The feature branch/PR history preserves prior runtime commits after the final tree is clean.

Future direction: Codito #84 owns an optional Akasha/GitHub Action (or equivalent adapter) that may export bounded runtime telemetry/evidence before deletion. This skill reserves `telemetry/` and the adapter seam but does not implement that transport now.

# Work Orchestration Module

This module absorbs the execution-facing role formerly exposed as `entif-work-orchestrator` while preserving Architecture, Rosetta, and Governance ownership boundaries.

## Input contract

Receive a bounded work unit whose durable issue/spec/plan/readiness state is already sufficiently settled by its owning planning/authority surfaces.

Do not use Runtime to invent missing desired state, create an Architecture decision by execution, or treat a GitHub issue alone as proof of readiness when a governing plan/readiness gate exists.

## Runtime responsibilities

For ready work:

1. verify authority/readiness and publication posture;
2. bind one run/work epoch and the relevant issue/spec/plan refs;
3. select the procedure/capability and execution surface needed for the actual job;
4. distinguish the procedure from the executor/provider/model used to perform it;
5. establish branch/lease state when repository mutation applies;
6. materialize Work Stack tasks for material dependencies and replay-sensitive side effects;
7. dispatch or execute the legal frontier without duplicating already-bound work;
8. checkpoint and narrate meaningful state transitions;
9. collect bounded execution evidence/telemetry and receipts;
10. route verification, closeout, continuation, or feature-postmortem work at the appropriate lifecycle boundary.

## Cross-surface routing

Reasoning difficulty alone is not a Codex trigger.

- Keep connector-capable planning, issue work, research, synthesis, and other feasible control-plane operations in Chat when Chat has the required capability and authority.
- Use Codex when a writable worktree, local build/test loop, executable mutation, repository-local generator, or another genuinely local capability is required.
- Preserve the same Work Stack/handoff identities across the boundary when the work transfers.

## Dispatch safety

- One bound work unit must not be dispatched to competing writers unless concurrency is explicitly modeled and safe.
- Ambiguous acknowledgements reconcile before retry.
- An execution failure may change procedure/executor choice without changing the durable objective.
- Continue safe independent work before blocking on human input; isolate unresolved questions explicitly.
- Procedure/executor selection and telemetry are evidence, not public Rosetta authority.

Public interoperable lifecycle representation should conform to Rosetta #1509 rather than creating a Codito-specific public record model.

# Source Skill Migration Inventory

| Source Skill | Disposition | Target / owner | Default surface |
|---|---|---|---|
| `entif-issue-decomposition` | `MOVE_TO_MODULE` | `work-shaping/*` | Chat |
| `entif-feature-architecture` | `MOVE_TO_MODULE` | `architecture/*` | Chat |
| `entif-product-requirements` | `MOVE_TO_MODULE` | `product/*` | Chat |
| `entif-idea-incubator` | `MERGE_WITH_MODULE` | `intake/*` | Chat |
| `github-work-shape-triage` | `MERGE_WITH_MODULE` | `work-shaping/classify` | Chat |
| `github-issue-cascade` | `MERGE_WITH_MODULE` | `work-shaping/prioritize` | Chat |
| `figure-it-out` | `MERGE_WITH_MODULE` | `intake/idea` | Chat |
| `how` | `MOVE_TO_MODULE` | `investigate/how` | Chat |
| `why` | `MOVE_TO_MODULE` | `investigate/why` | Chat |
| `breadcrumbs` | `MERGE_WITH_MODULE` | `investigate/why` | Either |
| `blast-radius` | `MOVE_TO_MODULE` | `risk/blast-radius` | Chat |
| `interrogate` | `MOVE_TO_MODULE` | `review/interrogate` | Chat |
| `rosetta-spine-alignment` | `REFERENCE_SHARED_CAPABILITY` | `architecture/rosetta-alignment` | Chat |
| `tdd` | `MOVE_TO_MODULE` | `implementation/testing` | Codex when applicable |
| `typescript-best-practices` | `MOVE_TO_MODULE` | `implementation/typescript` | Codex |
| `architecture-checkpoint` | `MERGE_WITH_MODULE` | `architecture/checkpoint` | Chat |
| `codegen-api` | `MOVE_TO_MODULE` | `implementation/typescript/api-codegen` | Chat select -> Codex execute |
| `javascript-ecosystem` | `MOVE_TO_MODULE` | `implementation/javascript/ecosystem` | Either |
| `requesting-code-review` | `MOVE_TO_MODULE` | `review/implementation/precommit` | Codex |
| `spike` | `MOVE_TO_MODULE` | `investigate/spike` | Chat frame -> Codex build if needed |
| `systemic-risk-assessor` | `MOVE_TO_MODULE` | `risk/systemic` | Chat |
| `test-driven-development` | `RETIRE_AFTER_PARITY` | superseded by pragmatic `tdd` | Codex when applicable |
| `writing-plans` | `RETIRE_AFTER_PARITY` | useful handoff residue -> SpecOps | Chat |
| `swarm` | `REFERENCE_SHARED_CAPABILITY` | runtime/model orchestration | runtime |
| `fable-mode` | `REFERENCE_SHARED_CAPABILITY` | runtime/model execution doctrine | runtime |
| `entif-pr-closeout` | `REFERENCE_SHARED_CAPABILITY` | `delivery/pr-closeout` | Either |
| `create-verification-skill` | `REFERENCE_SHARED_CAPABILITY` | `delivery/verification` | Codex |
| `maintain-verification-skill` | `REFERENCE_SHARED_CAPABILITY` | `delivery/verification` | Codex |
| `show-me-your-work` | `REFERENCE_SHARED_CAPABILITY` | audit owner | Either |
| `autopilot` | `KEEP_TOP_LEVEL_EXCEPTION` | runtime autonomous work selection | runtime |
| `entif-governed-creator` | `KEEP_TOP_LEVEL_EXCEPTION` | Skill mutation governor | Either |

The `principle-*` family becomes lazy doctrine under `references/doctrine/`: domain/boundary, structural economy, planning/migration, investigation/correction, and implementation/proof. Old installed eager Skills remain valid until parity/rollback gates permit retirement.

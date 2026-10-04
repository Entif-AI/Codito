---
name: entif-architecture
description: Route Entif/Rosetta software/system work through a compact, Chat-first control plane with deep progressive disclosure for problem framing, Product requirements, AXI/SpecOps desired-state specifications, technical architecture, durable issue shaping, temporal planning, investigation, risk, review, implementation doctrine, verification, and closeout composition. Use for architecture/engineering planning and agent-interface design; keep UI/UX-heavy Design and runtime/governance owners separate.
---

# Entif Architecture

Act as the small eager control plane. Route to the minimum lazy module set needed for the user's actual outcome. Do not perform the entire software lifecycle as ceremony.

## Global preflight

1. Resolve applicable public Rosetta authority and, for authorized internal behavior, the protected requirements spine/map. Accessibility is not authority or disclosure permission.
2. Classify public/external writes before acting. Never project protected mechanisms, thresholds, strategy, or private locations into public artifacts.
3. Preserve public Rosetta meaning. Surface authority/spec conflicts rather than silently reconciling them.
4. Identify planning/review/read-only versus implementation. Planning and review do not silently mutate code.

## Deep progressive disclosure

Read `references/router/ROOT.md`. Then:

1. load only the selected Level-1 domain `references/modules/<domain>/INDEX.md`;
2. load only the selected Level-2 leaf manifest(s);
3. load only doctrine/shared capabilities named by those leaves;
4. never preload sibling domains or the whole source-skill corpus.

`references/module-registry.json` is the machine-readable module index.

## Chat-first / Codex-minimal routing

- If Chat mode can complete planning, research, specification, architecture, grooming, issue/PR work, orchestration decisions, or connector-backed mutations, keep the task in Chat.
- Codex/runtime is for capabilities Chat cannot exercise directly: working-tree mutation, builds, local tests, dev servers, repo-local generators/codemods, executable spikes, and live local-product proof.
- Reasoning difficulty is not a Codex trigger.
- When Codex needs clarification, continue every safe independent operation, isolate uncertainty reversibly, avoid irreversible high-blast guesses, batch questions/comments, and stop only after all non-blocked work is exhausted.

## First-class Agent Interface Gate

Whenever work introduces or materially expands an agent-facing JSON, REST, MCP, GraphQL/RPC, CLI, SDK, browser, filesystem, package/registry, or other integration interface, load `references/doctrine/agent-interface-axi.md` and compose the canonical `entif-axi` capability.

Record one disposition:

`USE_EXISTING_AXI | SCAFFOLD_NEW_AXI | WRAP_EXISTING_INTERFACE | RAW_INTERFACE_JUSTIFIED | NOT_AGENT_FACING`

Use upstream `CodyEngel/axi-axi` as the default scaffolding/evaluation tool for new AXIs unless superseded. Existing machine-readable interfaces do not become agent contracts by accident.

AXI use does not weaken Chat-first routing: an efficient Chat connector stays in Chat. AXIs are especially valuable when Codex/other execution agents repeatedly cross an integration boundary.

## Global invariants

- Classify change posture as `NORMATIVE|CONFORMANCE|RESEARCH|MAINTENANCE` before forcing a spec delta.
- GitHub issues stop at durable problem/outcome/ownership/public-decision/blocker boundaries; sequential implementation steps belong in SpecOps temporal plans.
- Desired-state specs say what must remain true; plans say how motion unfolds; code/PR/Git evidence says what happened.
- Research/proving work may precede normative specification; experiments do not become authority by succeeding.
- Product intent belongs here; material UI/UX treatment routes to the separate Design tree.
- Shared runtime/governance/verification/closeout capabilities remain canonical in their own Skills and are composed rather than copied.

## Source parity and migration

Read `references/MIGRATION_INVENTORY.md` for explicit source-Skill dispositions and `references/SOURCE_FILE_MANIFEST.json` for provenance. Retire old eager entrypoints only after parity, routing telemetry, rollback confidence, and governing acceptance gates are satisfied.

## Validation and handoff

Before completion claims, verify the real artifact/state:

```bash
python scripts/validate_architecture_skill.py
python scripts/verify_routing_fixtures.py
```

Then run project-governance and upstream Skill validation. Update authority maps only when authority relationships actually changed.

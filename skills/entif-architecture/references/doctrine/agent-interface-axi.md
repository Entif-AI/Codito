# Doctrine: Agent Interface Gate / AXI-first design

**Agent-native interfaces are architecture.** Machine-readable JSON/REST/MCP/GraphQL-RPC/CLI/SDK/browser interfaces are not automatically agent-ergonomic.

For every material agent-facing integration record:
`USE_EXISTING_AXI | SCAFFOLD_NEW_AXI | WRAP_EXISTING_INTERFACE | RAW_INTERFACE_JUSTIFIED | NOT_AGENT_FACING`.

Evaluate repeated/sizable JSON, REST, MCP (including Entif-owned MCPs), GraphQL/RPC, package/registry, browser-automation, internal-service, SDK, filesystem, and other machine-facing interfaces.

Prefer an existing fit-for-purpose AXI. If none exists and repeated use is material, compose `entif-axi`, which uses upstream `CodyEngel/axi-axi` for scaffold/checklist/principle slices/validation/SKILL generation. Do not fork the whole upstream AXI specification.

Issue/spec/architecture contracts should identify agent consumers, source interface, existing-AXI search, disposition/rationale, token/context/round-trip/error costs, bounded output/pagination/truncation/empty-state/idempotency/discoverability behavior, owner module, and verification posture.

AXI use never overrides Chat-first routing.

## Known high-frequency Entif paths

Before raw interaction, evaluate the current authoritative AXI/catalog entry for:

- GitHub: `gh-axi` for repeated issue/PR/workflow/release traffic;
- npm: `npm-axi` for repeated registry/package/version/dependency traffic;
- AXI/SpecOps: canonical SpecOps AXI for specification/plan/readiness/closeout operations;
- Playwright/browser automation: `playwright-axi` for repeated browser-driving workloads.

These names are discovery hints, not frozen version authority. Verify the current AXI catalog and upstream tool documentation before relying on an exact package/version.

Decision order: **existing fit-for-purpose AXI first -> scaffold/wrap only if needed -> raw interface only with explicit justification**.

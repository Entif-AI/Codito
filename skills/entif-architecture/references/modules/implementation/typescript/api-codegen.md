# Module manifest: implementation/typescript/api-codegen

- **Purpose:** Choose and wire current typesafe API codegen patterns.
- **Triggers:** OpenAPI codegen, GraphQL codegen, gql.tada, generated hooks
- **Preferred surface:** `codex`
- **Agent interface kind:** `rest`
- **AXI candidate:** `conditional`
- **AXI disposition default:** `NOT_AGENT_FACING`
- **Preferred AXI:** `none until the integration is materially agent-facing; then run the Agent Interface Gate`
- **AXI scaffolder:** `axi-axi` when a new AXI is justified
- **Raw interface fallback:** allowed only when the Agent Interface Gate records why it is preferable or usage is immaterial
- **Authority sensitivity:** inherit parent preflight; resolve stronger module-specific authority where applicable
- **Requires capabilities:** only those needed to produce the declared output; prefer Chat connectors before Codex handoff
- **Forbidden side effects:** no implementation mutation from planning/read-only work; no disclosure beyond classified posture
- **Doctrine:** `implementation-proof`, `agent-interface-axi`
- **Shared capabilities:** none by default

Generate framework-agnostic options/documents, not stale generated hooks. Chat may select/verify approach; Codex wires/builds/tests.

## Handoff

If a real platform capability limit prevents completion, hand off the smallest unresolved operation plus settled inputs, proof criteria, open assumptions, and preferred AXI/tool path. Codex/runtime continues safe independent work, isolates uncertainty reversibly, batches unresolved questions, and stops only after non-blocked work is exhausted.

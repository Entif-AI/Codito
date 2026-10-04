# Module manifest: implementation/migration

- **Purpose:** Execute planned migrations toward the target architecture.
- **Triggers:** implementation migration, migrate callers, delete legacy
- **Preferred surface:** `codex`
- **Agent interface kind:** `none`
- **AXI candidate:** `false`
- **AXI disposition default:** `NOT_AGENT_FACING`
- **Preferred AXI:** `none`
- **AXI scaffolder:** `axi-axi` when a new AXI is justified
- **Raw interface fallback:** allowed only when the Agent Interface Gate records why it is preferable or usage is immaterial
- **Authority sensitivity:** inherit parent preflight; resolve stronger module-specific authority where applicable
- **Requires capabilities:** only those needed to produce the declared output; prefer Chat connectors before Codex handoff
- **Forbidden side effects:** no implementation mutation from planning/read-only work; no disclosure beyond classified posture
- **Doctrine:** `implementation-proof`
- **Shared capabilities:** none by default

Migrate callers then delete legacy APIs; optimize for target outcome, not compatibility sludge.

## Handoff

If a real platform capability limit prevents completion, hand off the smallest unresolved operation plus settled inputs, proof criteria, open assumptions, and preferred AXI/tool path. Codex/runtime continues safe independent work, isolates uncertainty reversibly, batches unresolved questions, and stops only after non-blocked work is exhausted.

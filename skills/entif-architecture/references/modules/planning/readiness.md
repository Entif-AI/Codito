# Module manifest: planning/readiness

- **Purpose:** Determine next legal work from authority and plan state.
- **Triggers:** ready, next work, execution readiness
- **Preferred surface:** `chat`
- **Agent interface kind:** `cli`
- **AXI candidate:** `true`
- **AXI disposition default:** `USE_EXISTING_AXI`
- **Preferred AXI:** `SpecOps`
- **AXI scaffolder:** `axi-axi` when a new AXI is justified
- **Raw interface fallback:** allowed only when the Agent Interface Gate records why it is preferable or usage is immaterial
- **Authority sensitivity:** inherit parent preflight; resolve stronger module-specific authority where applicable
- **Requires capabilities:** only those needed to produce the declared output; prefer Chat connectors before Codex handoff
- **Forbidden side effects:** no implementation mutation from planning/read-only work; no disclosure beyond classified posture
- **Doctrine:** `planning-migration`
- **Shared capabilities:** none by default

Keep procedure choice distinct from executor/provider choice.

## Handoff

If a real platform capability limit prevents completion, hand off the smallest unresolved operation plus settled inputs, proof criteria, open assumptions, and preferred AXI/tool path. Codex/runtime continues safe independent work, isolates uncertainty reversibly, batches unresolved questions, and stops only after non-blocked work is exhausted.

# Module manifest: risk/dependency

- **Purpose:** Assess dependency/provider/version/license/provenance risk.
- **Triggers:** dependency risk, provider, license, provenance, version
- **Preferred surface:** `chat`
- **Agent interface kind:** `rest`
- **AXI candidate:** `conditional`
- **AXI disposition default:** `SCAFFOLD_NEW_AXI`
- **Preferred AXI:** `conditional existing AXI`
- **AXI scaffolder:** `axi-axi` when a new AXI is justified
- **Raw interface fallback:** allowed only when the Agent Interface Gate records why it is preferable or usage is immaterial
- **Authority sensitivity:** inherit parent preflight; resolve stronger module-specific authority where applicable
- **Requires capabilities:** only those needed to produce the declared output; prefer Chat connectors before Codex handoff
- **Forbidden side effects:** no implementation mutation from planning/read-only work; no disclosure beyond classified posture
- **Doctrine:** none by default
- **Shared capabilities:** none by default

Treat external dependencies as moving targets; verify current primary sources.

## Handoff

If a real platform capability limit prevents completion, hand off the smallest unresolved operation plus settled inputs, proof criteria, open assumptions, and preferred AXI/tool path. Codex/runtime continues safe independent work, isolates uncertainty reversibly, batches unresolved questions, and stops only after non-blocked work is exhausted.

# Module manifest: implementation/javascript/ecosystem

- **Purpose:** Apply current JavaScript/TypeScript ecosystem paradigms for the installed major.
- **Triggers:** JavaScript framework, npm package, framework version
- **Preferred surface:** `either`
- **Agent interface kind:** `npm`
- **AXI candidate:** `true`
- **AXI disposition default:** `SCAFFOLD_NEW_AXI`
- **Preferred AXI:** `npm-axi`
- **AXI scaffolder:** `axi-axi` when a new AXI is justified
- **Raw interface fallback:** allowed only when the Agent Interface Gate records why it is preferable or usage is immaterial
- **Authority sensitivity:** inherit parent preflight; resolve stronger module-specific authority where applicable
- **Requires capabilities:** only those needed to produce the declared output; prefer Chat connectors before Codex handoff
- **Forbidden side effects:** no implementation mutation from planning/read-only work; no disclosure beyond classified posture
- **Doctrine:** `implementation-proof`
- **Shared capabilities:** none by default

Check installed version first; verify freshness against official sources; load only relevant tool note.

## Handoff

If a real platform capability limit prevents completion, hand off the smallest unresolved operation plus settled inputs, proof criteria, open assumptions, and preferred AXI/tool path. Codex/runtime continues safe independent work, isolates uncertainty reversibly, batches unresolved questions, and stops only after non-blocked work is exhausted.

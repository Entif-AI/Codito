# Module manifest: work-shaping/durable-issue-boundary

- **Purpose:** Decide whether another GitHub issue is a durable unit.
- **Triggers:** child issue, ownership seam, blocker, deliverable
- **Preferred surface:** `chat`
- **Agent interface kind:** `rest`
- **AXI candidate:** `conditional`
- **AXI disposition default:** `USE_EXISTING_AXI`
- **Preferred AXI:** `gh-axi`
- **AXI scaffolder:** `axi-axi` when a new AXI is justified
- **Raw interface fallback:** allowed only when the Agent Interface Gate records why it is preferable or usage is immaterial
- **Authority sensitivity:** inherit parent preflight; resolve stronger module-specific authority where applicable
- **Requires capabilities:** only those needed to produce the declared output; prefer Chat connectors before Codex handoff
- **Forbidden side effects:** no implementation mutation from planning/read-only work; no disclosure beyond classified posture
- **Doctrine:** none by default
- **Shared capabilities:** none by default

Create children only for durable outcomes/ownership/public decisions/external blockers/spec authority gaps.

## Handoff

If a real platform capability limit prevents completion, hand off the smallest unresolved operation plus settled inputs, proof criteria, open assumptions, and preferred AXI/tool path. Codex/runtime continues safe independent work, isolates uncertainty reversibly, batches unresolved questions, and stops only after non-blocked work is exhausted.

# Module manifest: architecture/concurrency-reliability

- **Purpose:** Define concurrency, consistency, retries, idempotency, replay, recovery, and backpressure.
- **Triggers:** concurrency, retry, idempotency, replay, partition, recovery
- **Preferred surface:** `chat`
- **Agent interface kind:** `none`
- **AXI candidate:** `conditional`
- **AXI disposition default:** `NOT_AGENT_FACING`
- **Preferred AXI:** `none`
- **AXI scaffolder:** `axi-axi` when a new AXI is justified
- **Raw interface fallback:** allowed only when the Agent Interface Gate records why it is preferable or usage is immaterial
- **Authority sensitivity:** inherit parent preflight; resolve stronger module-specific authority where applicable
- **Requires capabilities:** only those needed to produce the declared output; prefer Chat connectors before Codex handoff
- **Forbidden side effects:** no implementation mutation from planning/read-only work; no disclosure beyond classified posture
- **Doctrine:** `domain-boundary`, `structural-economy`
- **Shared capabilities:** none by default

Separate shared state before serializing it; make retry semantics explicit.

## Handoff

If a real platform capability limit prevents completion, hand off the smallest unresolved operation plus settled inputs, proof criteria, open assumptions, and preferred AXI/tool path. Codex/runtime continues safe independent work, isolates uncertainty reversibly, batches unresolved questions, and stops only after non-blocked work is exhausted.

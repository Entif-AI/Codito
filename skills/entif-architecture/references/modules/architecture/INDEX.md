# Module index: architecture

Load only the leaf or leaves required for the actual outcome.

| Leaf | Purpose | Preferred surface | AXI candidate |
|---|---|---|---|
| `architecture/system` | Define grounded technical system shape and ownership. | `chat` | `conditional` |
| `architecture/checkpoint` | Present an explicit architecture checkpoint for consequential changes. | `chat` | `false` |
| `architecture/contracts` | Design APIs, events, messages, schemas, errors, and agent-facing interfaces. | `chat` | `conditional` |
| `architecture/data-state` | Define authoritative state, lifecycle, persistence, and migrations. | `chat` | `conditional` |
| `architecture/security-trust` | Define trust, identity, tenancy, secrets, privacy, and threat boundaries. | `chat` | `conditional` |
| `architecture/concurrency-reliability` | Define concurrency, consistency, retries, idempotency, replay, recovery, and backpressure. | `chat` | `conditional` |
| `architecture/performance-resources` | Set performance/resource budgets and scaling constraints. | `chat` | `false` |
| `architecture/observability` | Define evidence, telemetry, health, and failure observability. | `chat` | `conditional` |
| `architecture/rosetta-alignment` | Gate materially Rosetta-semantic/interoperability changes. | `chat` | `false` |

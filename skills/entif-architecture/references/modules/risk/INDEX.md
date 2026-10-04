# Module index: risk

Load only the leaf or leaves required for the actual outcome.

| Leaf | Purpose | Preferred surface | AXI candidate |
|---|---|---|---|
| `risk/blast-radius` | Find non-obvious downstream breakage from a proposed change. | `chat` | `false` |
| `risk/dependency` | Assess dependency/provider/version/license/provenance risk. | `chat` | `conditional` |
| `risk/migration` | Assess migration/cutover/rollback risk. | `chat` | `false` |
| `risk/systemic` | Run second-order systemic pre-mortem across composing components and organizations. | `chat` | `false` |

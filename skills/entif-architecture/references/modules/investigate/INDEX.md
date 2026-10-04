# Module index: investigate

Load only the leaf or leaves required for the actual outcome.

| Leaf | Purpose | Preferred surface | AXI candidate |
|---|---|---|---|
| `investigate/how` | Explain runtime/codebase behavior and ownership. | `chat` | `false` |
| `investigate/why` | Recover rationale and forcing functions before change. | `chat` | `false` |
| `investigate/root-cause` | Trace symptoms to the causal source before fixing. | `either` | `false` |
| `investigate/premise` | Challenge a shared premise after repeated fixes fail. | `chat` | `false` |
| `investigate/spike` | Run disposable empirical feasibility work only when research cannot answer the question. | `chat` | `conditional` |

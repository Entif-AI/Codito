# Module index: specification

Load only the leaf or leaves required for the actual outcome.

| Leaf | Purpose | Preferred surface | AXI candidate |
|---|---|---|---|
| `specification/impact` | Classify whether accepted desired state is covered, amended, created, or blocked. | `chat` | `false` |
| `specification/desired-state` | Author or amend declarative AXI/SpecOps desired-state specifications. | `chat` | `conditional` |
| `specification/principles` | Promote durable governing principles without duplicating them across specs. | `chat` | `false` |
| `specification/drift` | Audit implementation/spec divergence. | `chat` | `false` |
| `specification/closeout` | Close/freeze desired-state motion after verified implementation. | `chat` | `conditional` |

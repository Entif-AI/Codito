# Module index: planning

Load only the leaf or leaves required for the actual outcome.

| Leaf | Purpose | Preferred surface | AXI candidate |
|---|---|---|---|
| `planning/specops` | Translate settled desired state into temporal SpecOps motion. | `chat` | `true` |
| `planning/dag` | Model temporal dependencies, awaits, specs, issues, PR, and validation. | `chat` | `true` |
| `planning/readiness` | Determine next legal work from authority and plan state. | `chat` | `true` |
| `planning/blockers` | Represent external and authority blockers explicitly. | `chat` | `conditional` |
| `planning/validation` | Bind temporal work to explicit verification criteria. | `chat` | `false` |

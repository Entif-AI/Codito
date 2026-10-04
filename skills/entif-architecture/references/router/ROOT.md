# Entif Architecture root router

Route to the smallest useful Level-1 domain index, then the minimum Level-2 leaf set, then only applicable doctrine/shared capabilities. Do not load the full tree.

## Platform decision comes before executor selection

1. Identify the actual job and authority posture.
2. Select the minimum domain/leaf set.
3. If Chat can complete it with current connectors/tools, keep it in Chat.
4. If a real capability is unavailable in Chat, hand only that bounded remainder to Codex/runtime.
5. For repeated/material agent-facing interfaces, run the Agent Interface Gate before choosing raw JSON/REST/MCP/CLI/SDK/browser access.

| Signal | Level-1 index | Typical Level-2 leaves |
|---|---|---|
| idea / unclear opportunity | `modules/intake/INDEX.md` | `intake/idea`, `intake/problem-frame` |
| PRD / scope / acceptance | `modules/product/INDEX.md` | `product/requirements`, `product/scope` |
| desired state / spec impact | `modules/specification/INDEX.md` | `specification/impact`, `specification/desired-state` |
| system/API/state/security/reliability architecture | `modules/architecture/INDEX.md` | select only relevant architecture leaves |
| GitHub work shaping | `modules/work-shaping/INDEX.md` | `work-shaping/classify`, `work-shaping/decompose` |
| temporal plan / readiness | `modules/planning/INDEX.md` | `planning/specops`, `planning/dag`, `planning/readiness` |
| how/why/root-cause/spike | `modules/investigate/INDEX.md` | narrow investigation leaves |
| change risk / systemic pre-mortem | `modules/risk/INDEX.md` | `risk/blast-radius` or `risk/systemic` |
| review | `modules/review/INDEX.md` | relevant review leaf |
| code/testing/migration | `modules/implementation/INDEX.md` | only after Chat pre-work |
| verification/closeout | `modules/delivery/INDEX.md` | route to canonical owner |
| UI/UX-heavy design | external Design tree | do not absorb |

- Classify change posture before forcing spec deltas.
- Issues stop at durable boundaries; temporal steps belong in SpecOps plans.
- Research/spikes are evidence, not authority.
- Planning/review do not silently mutate implementation.
- Shared runtime/governance/design/verification/closeout capabilities remain canonical.

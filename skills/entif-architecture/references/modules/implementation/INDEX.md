# Module index: implementation

Load only the leaf or leaves required for the actual outcome.

| Leaf | Purpose | Preferred surface | AXI candidate |
|---|---|---|---|
| `implementation/testing` | Apply pragmatic TDD/regression-test doctrine when a cheap local target exists. | `codex` | `false` |
| `implementation/typescript` | Apply TypeScript type-system discipline. | `codex` | `false` |
| `implementation/migration` | Execute planned migrations toward the target architecture. | `codex` | `false` |
| `implementation/proof` | Verify the real artifact/state before claiming done. | `codex` | `false` |
| `implementation/javascript/ecosystem` | Apply current JavaScript/TypeScript ecosystem paradigms for the installed major. | `either` | `true` |
| `implementation/typescript/api-codegen` | Choose and wire current typesafe API codegen patterns. | `codex` | `conditional` |

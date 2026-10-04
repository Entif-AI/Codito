---
name: entif-axi
description: Govern AXI-first agent-interface design for Entif/Rosetta. Use when evaluating, creating, wrapping, or validating agent-facing JSON/REST/MCP/GraphQL-RPC/CLI/SDK/browser/package interfaces, especially repeated or high-volume ones. Prefer an existing fit-for-purpose AXI; otherwise compose upstream CodyEngel/axi-axi to scaffold and validate a new AXI.
---

# Entif AXI

Treat agent-native interfaces as architecture. Machine-readable is not automatically agent-ergonomic.

## Preflight

Resolve applicable project authority before changing governed interfaces. Accessibility is not authority or disclosure permission. Classify public/external writes before acting, preserve public Rosetta meaning, and surface authority conflicts.

## Agent Interface Gate

Record one:
`USE_EXISTING_AXI | SCAFFOLD_NEW_AXI | WRAP_EXISTING_INTERFACE | RAW_INTERFACE_JUSTIFIED | NOT_AGENT_FACING`.

Evaluate agent consumers, source interface, frequency/scale, token/context/round-trip/error costs, bounded output, empty states, pagination/truncation, idempotency, discoverability, security/authority, and verification.

If a suitable AXI exists, prefer it. If not and repeated use is material, use upstream `CodyEngel/axi-axi` as the default scaffolder unless superseded.

## axi-axi golden path

```bash
npx -y axi-axi
npx -y axi-axi new <name> --dir <path>
npx -y axi-axi checklist --phase implement
npx -y axi-axi principles show <id>
npx -y axi-axi validate "<command>" --dir <path>
npx -y axi-axi skill gen --check
```

Verify freshness from `https://github.com/CodyEngel/axi-axi` and `https://axi.md/`.

## Chat / Codex boundary

Do not route work into Codex merely because an AXI exists there. If Chat has an efficient first-party connector, use Chat. Codex/runtime should use AXIs when it genuinely must repeatedly cross the external interface.

## Postflight

Validate the actual interface. For new AXIs run upstream `axi-axi validate` and verify/generate its Skill surface. Update project authority maps only when interface authority relationships changed.

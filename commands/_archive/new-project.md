---
description: Create a new Claude Code project (default mode = interactive discovery for any project type)
---

# New Project Command

Shim invoking `scaffold-project` (default mode). Full procedure lives in
[`skills/scaffold-project/assets/mode-default.md`](../skills/scaffold-project/assets/mode-default.md).

For known-type fast paths use the dedicated mode shims:
- `/cab:init-plugin` → `--mode plugin` (CAB plugin scaffold)
- `/cab:integrate-existing` → `--mode integrate` (overlay onto existing codebase)
- `/cab:new-global` → `--mode global` (`~/.claude/` setup)

## Lifecycle Advisory (preserved F009 unique content)

For full app projects, reference `knowledge/reference/INDEX.md` to access
the **product-design-cycle** (7-phase universal lifecycle). Use it as a
**conceptual framework** to help the user identify which phases apply to
their project and suggest appropriate phase-gate criteria. Not all
projects need all 7 phases — adapt to actual complexity.

## Arguments

- `$1` (optional): Project name (kebab-case)
- `$2` (optional): Domain description

If arguments provided, use them. Otherwise, prompt interactively.

## Examples

```
/new-project                                                # Interactive
/new-project my-assistant                                   # Name pre-filled
/new-project flood-analyzer "Water resources flood analysis" # Name + domain
```

## See Also

- `skills/scaffold-project/` — Unified scaffolding router (owns logic)
- `skills/scaffold-project/assets/mode-default.md` — Default mode procedure
- `knowledge/reference/INDEX.md` — Product design cycle (lifecycle advisory)
- `/cab:validate` — Verify created project structure

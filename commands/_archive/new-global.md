---
description: Set up global user configuration in ~/.claude/
---

# New Global Configuration Command

Shim invoking `scaffold-project --mode global`. Full procedure lives in
[`skills/scaffold-project/assets/mode-global.md`](../skills/scaffold-project/assets/mode-global.md).

## Arguments

- (none): Create or update interactively
- `--update`: Open existing for modification (preserves customizations)
- `--reset`: Back up existing → recreate from template

## Examples

```
/new-global              # Create or update interactively
/new-global --update     # Modify existing
/new-global --reset      # Back up + start fresh from template
```

## See Also

- `skills/scaffold-project/` — Unified scaffolding router (owns logic)
- `skills/scaffold-project/assets/mode-global.md` — Global mode procedure
- `knowledge/schemas/global-user-config.md` — Canonical global structure
- `/cab:check-sync` — Verify no plugin↔global shadow conflicts after install

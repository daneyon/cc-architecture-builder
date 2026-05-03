---
description: Initialize a new CAB plugin project with full structure, git setup, and optional GitHub remote
allowed-tools: Read, Write, Bash
---

# Init Plugin Command

Shim invoking `scaffold-project --mode plugin`. Full procedure +
template references live in
[`skills/scaffold-project/assets/mode-plugin.md`](../skills/scaffold-project/assets/mode-plugin.md).

## Arguments

- `$1` (required): Project name (kebab-case)
- `$2` (optional): Brief description
- `--github` / `--no-github`: Whether to create GitHub remote (default: ask)

## Examples

```
/init-plugin my-assistant
→ Interactive: asks for description, author, GitHub preference

/init-plugin flood-analyzer "Water resources flood analysis assistant"
→ Creates with name and description, asks remaining questions

/init-plugin my-tool "Dev tooling" --github
→ Full automated setup including GitHub remote
```

## See Also

- `skills/scaffold-project/` — Unified scaffolding router (owns logic)
- `skills/scaffold-project/assets/mode-plugin.md` — Plugin mode procedure
- `/cab:new-project` — Default-mode (interactive discovery) shim
- `/cab:validate` — Verify project structure compliance
- `/cab:init-worktree` — Set up parallel-execution worktrees

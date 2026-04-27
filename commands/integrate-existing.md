---
description: Integrate CC architecture into an existing project. Analyzes the current codebase, proposes tailored extensions, and scaffolds only the CC overlay without modifying existing files.
allowed-tools: Read, Write, Bash, Grep, Glob
---

# Integrate Existing Project

Shim invoking `scaffold-project --mode integrate`. Full procedure
(5-phase: discovery → questionnaire → plan → scaffold → verify) lives in
[`skills/scaffold-project/assets/mode-integrate.md`](../skills/scaffold-project/assets/mode-integrate.md).

**Key principle**: this mode is an **overlay** — it adds CC architecture
alongside the existing codebase without touching existing source.

## Arguments

- `$ARGUMENTS` (optional): Target project directory path. Default: current.

## Examples

```
/integrate-existing
→ Scans current directory, runs full 5-phase overlay workflow

/integrate-existing C:\Users\daniel.kang\Desktop\Automoto\hecras-2d-suite
→ Scans specified directory
```

## See Also

- `skills/scaffold-project/` — Unified scaffolding router (owns logic)
- `skills/scaffold-project/assets/mode-integrate.md` — Integrate mode procedure
- `/cab:new-project` — Greenfield project from scratch
- `/cab:init-plugin` — Quick plugin scaffold without interactive discovery
- `agents/project-integrator.md` — Companion agent for deep architecture consultation

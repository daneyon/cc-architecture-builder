---
description: Integrate CC architecture into an existing project. Analyzes the current codebase, proposes tailored extensions, and scaffolds only the CC overlay without modifying existing files.
allowed-tools: Read, Write, Bash, Grep, Glob
---

# Integrate Existing Project

Overlay the CAB standardized CC architecture onto an existing project workspace.
Unlike `/new-project` (starts from scratch), this command preserves the existing
codebase and adds only CC architecture files alongside it.

## Behavior

### Phase 1: Automated Discovery (no user input needed)

1. **Detect project basics**:
   ```bash
   # Language/framework detection
   ls package.json pyproject.toml requirements.txt Cargo.toml go.mod pom.xml *.sln 2>/dev/null
   
   # Git status
   git status 2>/dev/null && git remote -v 2>/dev/null
   
   # Directory structure (top 2 levels)
   find . -maxdepth 2 -type d | head -40
   
   # File count and types
   find . -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -15
   
   # Existing CC files
   ls CLAUDE.md .claude/ agents/ commands/ .mcp.json .claude-plugin/ 2>/dev/null
   ```

2. **Analyze codebase characteristics**:
   - Primary language(s) and frameworks
   - Project structure pattern (monorepo, microservices, monolith, scripts)
   - Existing test infrastructure (test dirs, test config)
   - Existing CI/CD (GitHub Actions, GitLab CI, etc.)
   - Existing documentation (README, docs/, wiki)
   - Data and configuration patterns

3. **Present discovery summary** to user before proceeding.

### Phase 2: Interactive Questionnaire (concise — only what automation can't detect)

Ask only what the automated scan couldn't determine:

1. **Project purpose**: "In one sentence, what does this project do?"
2. **Primary domain**: "What domain does this serve?" (engineering, web app, data pipeline, research, etc.)
3. **Team size**: "Solo or team? If team, how many?"
4. **Key workflows**: "What are the 2-3 most common tasks you do in this codebase?"
5. **Pain points**: "What's most tedious or error-prone right now?"
6. **Verification**: "What commands verify the project is working?" (test, lint, build, typecheck)

### Phase 3: Generate CC Overlay Plan

Based on discovery + answers, propose:

1. **CLAUDE.md** — Project identity, role, domain guidelines, verification commands, learned corrections
2. **Recommended rules** — Based on language/framework (e.g., Python → PEP 8 rules)
3. **Recommended agents** — Based on domain, pain points, and team formation reference
4. **Recommended skills** — Based on workflows identified
5. **Recommended commands** — Based on repetitive tasks
6. **Knowledge base structure** — Based on domain and existing docs
7. **MCP opportunities** — External tools that could be wrapped
8. **settings.json** — Permissions for project-specific safe commands

**Team Formation Advisory**: Read `knowledge/reference/INDEX.md` to access the
a-team-database (22 roles with CC extension mapping and scaling tiers). Use it as
a conceptual menu — NOT a checklist. Filter by the project's team size (solo/small/
medium/enterprise) and active phases to suggest only the roles that add value for
this specific project. Map each suggested role to its recommended CC extension type
(agent vs. skill vs. command) per the database's `cc_mapping` field.

Present as a structured plan with rationale. **Do not create files until user approves.**

### Phase 4: Scaffold (after user approval)

Create only the CC architecture files:

```bash
# CC architecture overlay — NEVER modifies existing project files
# Plugin project (default): components at root
mkdir -p .claude-plugin .claude/rules knowledge hooks notes agents skills commands

# Generate files from templates + discovery context
# CLAUDE.md — populated from questionnaire answers
# .claude-plugin/plugin.json — project metadata
# .claude/settings.json — project permissions + hooks
# knowledge/INDEX.md — initial structure based on domain
# agents/ — domain-specific agents based on recommendations
# commands/ — workflow shortcuts based on pain points
# skills/ — domain skills based on discovery
```

Run `/validate` to confirm structure compliance.

### Phase 5: First Verification

```bash
# Verify the overlay doesn't break anything
git status                    # Only new CC files should show
[user's verification commands] # Run existing test suite
/memory                       # Verify CC loads correctly
```

## Arguments

- `$ARGUMENTS` (optional): Project directory path. Default: current directory.

## Examples

```
/integrate-existing
→ Scans current directory, interactive questionnaire, proposes overlay

/integrate-existing C:\Users\daniel.kang\Desktop\Automoto\hecras-2d-suite
→ Scans specified directory
```

## What It Creates vs. What It Doesn't Touch

**Creates (CC overlay)**:
- `CLAUDE.md`, `CLAUDE.local.md`
- `.claude-plugin/plugin.json`
- `.claude/settings.json`, `.claude/rules/`
- `agents/`, `commands/`, `knowledge/INDEX.md`
- `hooks/hooks.json`, `notes/.gitkeep`
- `.mcp.json` (if MCP opportunities identified)

**Never touches**:
- `src/`, `lib/`, `app/` or any existing source code
- `tests/`, `data/`, `configs/` or any existing project directories
- `package.json`, `requirements.txt`, `Dockerfile` etc.
- `.git/`, `.github/`, `.gitignore` (except appending CLAUDE.local.md)
- Any existing file whatsoever

## Key Principle

The CC architecture is an **overlay** — it adds intelligence and automation without
restructuring the existing project. The codebase remains exactly as it was, with
CC extensions sitting alongside it.

## See Also

- `/new-project` — Guided interactive project creation from scratch
- `/init-plugin` — Quick scaffold without interactive discovery
- `/validate` — Verify project structure compliance
- `agents/architecture-advisor.md` — Detailed architecture consultation

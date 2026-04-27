# Mode: Integrate (Overlay CC Architecture onto Existing Codebase)

> Loaded just-in-time by `scaffold-project` router when `--mode integrate`.
> Adds CC architecture *alongside* an existing codebase without modifying
> existing source. Distinct from `--mode plugin` (which creates a fresh
> project from scratch).

## When This Mode Fires

- User invokes `/cab:integrate-existing` (mode shim)
- User says "add CC to this project" / "integrate Claude Code into existing"
- User has an existing repo and wants the CAB overlay

## Key Principle

**The CC architecture is an overlay** — it adds intelligence and automation
without restructuring the existing project. The codebase remains exactly
as-is, with CC extensions sitting alongside.

## Procedure

### Phase 1: Automated Discovery (no user input needed)

```bash
# Language/framework detection
ls package.json pyproject.toml requirements.txt Cargo.toml go.mod pom.xml *.sln 2>/dev/null

# Git status + remote
git status 2>/dev/null && git remote -v 2>/dev/null

# Directory structure (top 2 levels)
find . -maxdepth 2 -type d | head -40

# File count and types
find . -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -15

# Existing CC files
ls CLAUDE.md .claude/ agents/ commands/ .mcp.json .claude-plugin/ 2>/dev/null
```

Analyze:
- Primary language(s) and frameworks
- Project structure pattern (monorepo, microservices, monolith, scripts)
- Existing test infrastructure
- Existing CI/CD (GitHub Actions, GitLab CI, etc.)
- Existing documentation (README, docs/, wiki)
- Data and configuration patterns

Present discovery summary to user before continuing.

### Phase 2: Interactive Questionnaire (concise — only what automation can't detect)

1. **Project purpose**: "In one sentence, what does this project do?"
2. **Primary domain**: "What domain does this serve?"
3. **Team size**: "Solo or team? If team, how many?"
4. **Key workflows**: "What are the 2-3 most common tasks you do here?"
5. **Pain points**: "What's most tedious or error-prone right now?"
6. **Verification**: "What commands verify the project is working?"
   (test, lint, build, typecheck)

### Phase 3: Generate CC Overlay Plan

Based on discovery + answers, propose:

1. **CLAUDE.md** — Project identity, role, domain guidelines, verification commands
2. **Recommended rules** — Based on language/framework
3. **Recommended agents** — Based on domain, pain points, team formation
4. **Recommended skills** — Based on workflows identified
5. **Recommended commands** — Based on repetitive tasks
6. **Knowledge base structure** — Based on domain and existing docs
7. **MCP opportunities** — External tools that could be wrapped
8. **settings.json** — Permissions for project-specific safe commands

**Team Formation Advisory**: Consult `knowledge/reference/INDEX.md` for the
a-team-database (22 roles with CC extension mapping and scaling tiers).
Use as a conceptual menu — NOT a checklist. Filter by team size and
active phases; suggest only roles that add value for THIS project.

Present as structured plan with rationale. **Do not create files until
user approves.**

### Phase 4: Scaffold (after user approval)

Create only the CC architecture files — never touch existing project files:

```bash
# CC overlay (plugin-shape default)
mkdir -p .claude-plugin .claude/rules knowledge hooks notes agents skills commands
```

Generate from `assets/templates/` populated with discovery context.

### Phase 5: First Verification

```bash
git status                    # Only new CC files should show
[user's verification commands] # Run existing test suite
/memory                       # Verify CC loads correctly
```

## What This Mode Creates vs Doesn't Touch

**Creates (CC overlay)**:
- `CLAUDE.md`, `CLAUDE.local.md`
- `.claude-plugin/plugin.json`
- `.claude/settings.json`, `.claude/rules/`
- `agents/`, `commands/`, `knowledge/INDEX.md`
- `hooks/hooks.json`, `notes/.gitkeep`
- `.mcp.json` (if MCP opportunities identified)

**Never touches**:
- `src/`, `lib/`, `app/` or any existing source
- `tests/`, `data/`, `configs/`
- `package.json`, `requirements.txt`, `Dockerfile`
- `.git/`, `.github/`, `.gitignore` (except appending `CLAUDE.local.md`)

## Knowledge Anchors

- `knowledge/components/` — per-component deep dives (10 components)
- `knowledge/operational-patterns/` — orchestration, multi-agent, state-mgmt patterns
- `knowledge/reference/` — a-team-database for role recommendations
- `knowledge/schemas/distributable-plugin.md` — overlay aligns with plugin shape
- `agents/project-integrator.md` — companion agent for deep architecture consultation

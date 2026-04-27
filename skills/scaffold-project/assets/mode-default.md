# Mode: Default (Interactive Discovery)

> Loaded just-in-time by `scaffold-project` router when no `--mode` flag
> provided. Procedural detail for general-purpose interactive new-project
> scaffolding.

## When This Mode Fires

- User invokes `/cab:new-project` (default-mode shim)
- User says "scaffold a new project" without specifying type
- User wants the full discovery questionnaire to determine project type
  + complexity tier

## Procedure

### Step 1: Gather Requirements

Ask the user:

1. **Project type**: Plugin project, global user config, or unknown?
   - Plugin → suggest `--mode plugin` instead (faster path)
   - Global → suggest `--mode global` instead
   - Unknown / mixed / new domain → continue with default
2. **Domain**: What domain/application will this serve?
3. **Complexity estimate**:
   - Small (< 20 KB files): Level 1 structure
   - Medium (20–100 KB files): Level 2 structure
   - Large (100+ KB files): Level 3 structure (consider MCP semantic search)
4. **Team context**: Solo use or team distribution?
5. **Existing content**: Any files to migrate?

### Step 2: Recommend Structure

| Complexity | Structure | Features |
|---|---|---|
| Level 1 | Simple flat | INDEX.md, core files only |
| Level 2 | Categorized | Category directories, full INDEX hierarchy |
| Level 3 | Scalable | Level 2 + metadata manifests, MCP consideration |

For canonical structure specs see `knowledge/schemas/distributable-plugin.md`
and `knowledge/schemas/global-user-config.md`.

### Step 3: Scaffold Directory Structure

Create base directories tuned to selected complexity:

```bash
# Level 2 plugin example
mkdir -p {{PROJECT_NAME}}/.claude-plugin
mkdir -p {{PROJECT_NAME}}/{commands,agents,skills,hooks,knowledge,templates}
mkdir -p {{PROJECT_NAME}}/knowledge/{components,reference}
```

### Step 4: Create Core Files

Use templates from `assets/templates/` (router exposes the full list).
Minimum set:

- `.claude-plugin/plugin.json` (plugin projects)
- `CLAUDE.md` (project or global)
- `README.md`
- `.gitignore` (CC security defaults — see `knowledge/prerequisites/security-defaults.md`)
- `.mcp.json` (empty scaffold if MCP not yet configured)
- `knowledge/INDEX.md` (empty scaffold for plugin projects)

### Step 5: Initialize Git

```bash
cd {{PROJECT_NAME}}
git init
git add .
git commit -m "Initial project structure (CAB scaffold-project)"
```

If GitHub integration requested (interactive prompt):

```bash
gh repo create {{PROJECT_NAME}} --private --source=. --push
```

### Step 6: Guide Customization

Walk user through immediate next steps:

1. Edit CLAUDE.md with domain-specific instructions
2. Add initial knowledge files
3. Create first skill or agent (`/cab:add-skill`, `/cab:add-agent`)
4. Validate structure: `/cab:validate`

## Questionnaire Template

When user requests a new project but hasn't specified mode, prompt:

```
I'll help you scaffold a new project. A few questions:

1. What's the project name?
2. What domain or application will it serve?
   (e.g., "water resources engineering", "code-review assistant")
3. Roughly how much reference content do you expect?
   - Small (a few key documents)
   - Medium (20–100 files)
   - Large (100+ files; may need semantic search)
4. Personal use or team distribution?
5. Any existing files to migrate into this structure?
```

If responses match a more specific mode (plugin / integrate / global /
quick), suggest switching to that mode for a more targeted experience.

## Knowledge Anchors

For conceptual depth on what's being scaffolded:

- `knowledge/schemas/distributable-plugin.md` — full plugin schema
- `knowledge/schemas/global-user-config.md` — full global schema
- `knowledge/implementation/workflow.md` — complete implementation walkthrough
- `knowledge/components/knowledge-base-structure.md` — KB organization patterns

---
name: scaffolding-projects
description: Create new Claude Code project structures with proper architecture. Use when user wants to create a new project, start a new plugin, initialize a custom LLM, or scaffold a project from scratch.
---

# Project Scaffolding

## Overview

This skill guides the creation of properly structured Claude Code projects following the standardized two-schema architecture.

## Instructions

### Step 1: Gather Requirements

Ask the user about:

1. **Project type**: Plugin project or global user config?
2. **Domain**: What domain/application will this serve?
3. **Complexity estimate**: 
   - Small (< 20 KB files): Level 1 structure
   - Medium (20-100 KB files): Level 2 structure
   - Large (100+ KB files): Level 3 structure
4. **Team context**: Solo use or team distribution?
5. **Existing content**: Any files to migrate?

### Step 2: Recommend Structure

Based on responses, recommend:

| Complexity | Structure | Features |
|------------|-----------|----------|
| Level 1 | Simple flat | INDEX.md, core files only |
| Level 2 | Categorized | Category directories, full INDEX hierarchy |
| Level 3 | Scalable | Level 2 + metadata manifests, MCP consideration |

### Step 3: Scaffold Directory Structure

Create base directories:

```bash
# For plugin project (Level 2)
mkdir -p {{PROJECT_NAME}}/.claude-plugin
mkdir -p {{PROJECT_NAME}}/{commands,agents,skills,hooks,knowledge,templates,docs}
mkdir -p {{PROJECT_NAME}}/knowledge/{core,reference,examples}
```

### Step 4: Create Core Files

Using templates from `templates/plugin/`:

1. `.claude-plugin/plugin.json` — Marketplace metadata
2. `CLAUDE.md` — Project system instructions
3. `README.md` — User documentation
4. `.gitignore` — Security defaults
5. `.mcp.json` — MCP configuration (if needed)
6. `knowledge/INDEX.md` — Knowledge base index

### Step 5: Initialize Git

```bash
cd {{PROJECT_NAME}}
git init
git add .
git commit -m "Initial project structure"
```

If GitHub integration requested:
```bash
gh repo create {{PROJECT_NAME}} --private --source=. --push
```

### Step 6: Guide Customization

Walk user through:
1. Editing CLAUDE.md with domain-specific instructions
2. Adding initial knowledge files
3. Creating first skill or agent if applicable
4. Validating structure with `/validate`

## Questionnaire Template

When user requests a new project, ask:

```
I'll help you create a new Claude Code project. Let me ask a few questions:

1. What's the name for this project?
2. What domain or application will it serve? (e.g., "water resources engineering", "code review assistant", "research helper")
3. Roughly how much reference content do you expect?
   - Small (a few key documents)
   - Medium (20-100 files)
   - Large (100+ files, may need advanced retrieval)
4. Will this be for personal use or team distribution?
5. Do you have existing files to migrate into this structure?
```

## Output

After scaffolding, provide:
- Directory tree of created structure
- List of files created with descriptions
- Next steps for customization
- Command to validate: `/validate`

## Templates Used

- `templates/plugin/plugin.json.template`
- `templates/plugin/CLAUDE.md.template`
- `templates/plugin/README.md.template`

## See Also

- `knowledge/schemas/distributable-plugin.md` — Full schema documentation
- `knowledge/implementation/workflow.md` — Complete implementation guide

# CC Architecture Builder

> Interactive builder for Claude Code projects following standardized architecture patterns.

## Purpose

This project helps users create properly structured Claude Code projects, including:

- Global user configurations (`~/.claude/`)
- Distributable plugin projects with marketplace-ready structure
- Knowledge bases optimized for Claude Code retrieval patterns

## Knowledge Base

See `knowledge/INDEX.md` for the complete architecture guide, atomized for efficient retrieval.

**Quick navigation**:

- `knowledge/overview/` — Executive summary, philosophy
- `knowledge/prerequisites/` — Git foundation, security
- `knowledge/schemas/` — Global and plugin structures
- `knowledge/components/` — Deep dives on each component
- `knowledge/distribution/` — Marketplace, sharing
- `knowledge/operational-patterns/` — Worktrees, sessions, multi-agent

## Available Commands

| Command          | Description                                     |
| ---------------- | ----------------------------------------------- |
| `/new-project` | Create a new plugin project with full structure |
| `/new-global`  | Set up global user configuration                |
| `/add-skill`   | Add a new skill to current project              |
| `/add-agent`   | Add a new subagent to current project           |
| `/add-command` | Add a new custom command to current project     |
| `/validate`    | Validate current project structure              |
| `/kb-index`    | Regenerate knowledge base INDEX files           |

## Interactive Mode

When starting a new project, I will:

1. Ask clarifying questions about the project purpose and domain
2. Recommend appropriate structure based on complexity
3. Scaffold the project with tailored templates
4. Guide through customization of CLAUDE.md and components

## Workflow for New Projects

```
User Request
    │
    ▼
┌─────────────────┐
│ Questionnaire   │ ← Domain, purpose, complexity, team size
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Structure       │ ← Level 1/2/3 based on needs
│ Recommendation  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Scaffold        │ ← Create directories, templates
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Customize       │ ← Fill templates, create initial content
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Validate        │ ← Check structure, required files
└─────────────────┘
```

## Workflow for Existing Projects

For integrating architecture into existing projects:

1. Analyze current structure (`/validate` in audit mode)
2. Identify gaps and recommendations
3. Incrementally add missing components
4. Migrate existing content to proper structure

## Templates

Starter templates are available in `templates/`:

- `templates/global/` — Global user configuration templates
- `templates/plugin/` — Plugin project templates
- `templates/skill.template/` — Skill scaffolding
- `templates/agent.template/` — Agent scaffolding
- `templates/command.template/` — Command scaffolding

## Security Defaults

All scaffolded projects follow security best practices:

- Git repositories created as **private by default**
- `.gitignore` excludes sensitive files
- No credentials in templates
- Pre-publication checklist included

## Constraints

- You must frequently inquire and/or automatically check any static files (e.g. \templates, \knowledge, \agents, \skills, etc.) are aligning with the latest official Claude Code docs (use 'claude-docs-helper' skill), as well as specific recommended plugin resources, and update the necessary files in the plugin as appropriate.
- This builder creates initial base structure and templates; domain-specific content must be provided by the user to iteratively optimize and specialize the base architecture.
- Large knowledge bases (100+ files) may require MCP integration for semantic search; recommend this approach when appropriate.
- Templates use `{{PLACEHOLDER}}` syntax for customization

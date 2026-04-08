# CAB (cc-architecture-builder)

> Your taxi to stay in line to properly integrate CC with best practices — and you as the driver to apply project context engineering.

## Purpose

CAB is a standardized framework for building custom LLM solutions using Claude Code. It provides:

- Global user configurations (`~/.claude/`)
- Distributable plugin projects with marketplace-ready structure
- Knowledge bases optimized for Claude Code retrieval patterns
- **Orchestration framework** with 5 canonical agentic workflow patterns
- **Verification-first development** with structured task execution protocol

## Knowledge Base

See `knowledge/INDEX.md` for the complete architecture guide, atomized for efficient retrieval.

**Quick navigation**:

- `knowledge/overview/` — Executive summary, philosophy
- `knowledge/prerequisites/` — Git foundation, security
- `knowledge/schemas/` — Global and plugin structures
- `knowledge/components/` — Deep dives on each component
- `knowledge/distribution/` — Marketplace, sharing
- `knowledge/operational-patterns/` — **Orchestration framework**, worktrees, sessions, multi-agent, **team collaboration**

## Available Commands

| Command                 | Description                                                                  |
| ----------------------- | ---------------------------------------------------------------------------- |
| `/integrate-existing`   | Overlay CC architecture onto an existing project (auto-discover + guided)    |
| `/init-plugin`          | Initialize new CAB plugin with git setup (streamlined)                       |
| `/init-worktree`        | Set up git worktrees for parallel agent execution                            |
| `/execute-task`         | Start structured task via PLAN → VERIFY → COMMIT protocol                    |
| `/commit-push-pr`       | Stage, commit, push, and create PR in one workflow                           |
| `/techdebt`             | Scan codebase for tech debt, duplication, stale markers                      |
| `/context-sync`         | Pull recent activity into session context summary                            |
| `/validate --cab-audit` | Audit workspace against CAB v1.1.0 standards (7-dimension scored assessment) |
| `/new-project`          | Create a new plugin project (interactive discovery)                          |
| `/new-global`           | Set up global user configuration                                             |
| `/add-skill`            | Add a new skill to current project                                           |
| `/add-agent`            | Add a new subagent to current project                                        |
| `/add-command`          | Add a new custom command to current project                                  |
| `/validate`             | Validate current project structure                                           |
| `/kb-index`             | Regenerate knowledge base INDEX files                                        |
| `/sync-check`           | Detect drift between CAB plugin and global extensions                        |

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

## Core Principles

1. **Verification as Architectural Requirement** — Every agent, task, and phase gate requires a verification method
2. **Simplicity-First Complexity Ladder** — Start simple, escalate only when measured improvement justifies complexity
3. **Plan Before Execute** — PLAN → REVIEW → EXECUTE → VERIFY → COMMIT
4. **Compounding Knowledge via CLAUDE.md** — Every correctable error becomes a permanent learning
5. **Token Efficiency as Public Good** — Context window space is shared; load only what each task requires

See `knowledge/operational-patterns/orchestration/framework.md` for full detail.

## State Management

- Read `notes/TODO.md` for current task state and progress tracking
- Read `notes/progress.md` for live session state and bootstrap protocol
- Read `notes/lessons-learned.md` for operational constraints and insights
- Internal design docs are in `docs/_internal/` (not tracked in git)

## Constraints

- You must frequently inquire and/or automatically check any static files (e.g. \templates, \knowledge, \.claude\agents, \.claude\skills, etc.) are aligning with the latest official Claude Code docs (use 'claude-docs-helper' skill), as well as specific recommended plugin resources, and update the necessary files in the plugin as appropriate.
- This builder creates initial base structure and templates; domain-specific content must be provided by the user to iteratively optimize and specialize the base architecture.
- Large knowledge bases (100+ files) may require MCP integration for semantic search; recommend this approach when appropriate.
- Templates use `{{PLACEHOLDER}}` syntax for customization

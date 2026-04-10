# CAB (cc-architecture-builder)

> Your taxi to stay in line to properly integrate CC with best practices — and you as the driver to apply project context engineering.

## Purpose

CAB is a standardized framework for building custom LLM solutions using Claude Code. It provides:

- Global user configurations (`~/.claude/`)
- Distributable plugin projects with marketplace-ready structure
- Knowledge bases optimized for Claude Code retrieval patterns
- **Orchestration framework** with 5 canonical agentic workflow patterns
- **Verification-first development** with structured task execution protocol

## Domain Guidelines

- **Language**: Markdown (knowledge base, agents, skills, commands, templates)
- **Schema**: YAML frontmatter for all extension files; JSON for settings and plugin manifest
- **Architecture**: Two-schema model — Schema 1 (global `~/.claude/`), Schema 2 (plugin root)
- **Plugin convention**: Distributable components at project root (`agents/`, `skills/`, `commands/`); `.claude/` for project config only (LL-21)
- **Frontmatter fields**: Only CC-documented fields; no `context:`, `disallowedTools:`, or plugin-restricted `permissionMode:` (LL-15)
- **KB files**: ≤300 lines each, `source:` metadata required, wrapper philosophy over comprehensive mirroring (LL-11)
- **Freshness**: Always re-fetch official CC docs before modifying KB or frontmatter fields (LL-10)

## Extension Registry

### Agents (4)

| Agent | Description | Model |
|-------|-------------|-------|
| `orchestrator` | Central coordination — task routing, state management, PLAN→VERIFY→COMMIT | opus |
| `architecture-advisor` | Expert guidance on CC architecture + active project analysis | opus |
| `project-integrator` | Analyzes existing projects, proposes CC integration aligned with CAB | opus |
| `verifier` | End-to-end verification specialist — read-only, adversarial challenge | inherit |

### Skills (9)

| Skill | Description |
|-------|-------------|
| `auditing-workspace` | R2 standards audit — 7-dimension scored assessment |
| `validating-structure` | Quick structural validation of CC project conventions |
| `executing-tasks` | Structured task execution via PLAN→VERIFY→COMMIT protocol |
| `planning-implementation` | Phased implementation planning with acceptance criteria |
| `architecture-analyzer` | Codebase architecture analysis and recommendations |
| `creating-components` | Scaffold new CC components (agents, skills, commands) |
| `scaffolding-projects` | Full plugin project scaffolding from templates |
| `quick-scaffold` | Rapid minimal project setup |
| `session-close` | Standardized session state persistence + context handoff |

### Commands (15)

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

**`notes/` is TRACKED BY DEFAULT (LL-25)** — state artifacts are first-class deliverables, not scratch work. See [filesystem-patterns.md](knowledge/operational-patterns/state-management/filesystem-patterns.md#git-tracking-policy) for the full policy.

### Bootstrap Protocol (always-load)

- Read `notes/current-task.md` for active task context (<100 line anchor)
- Read `notes/progress.md` for live session state and cumulative position
- Read `notes/TODO.md` for tactical task queue and priorities
- Read `notes/lessons-learned.md` for operational constraints (**architecturally enforced**, not optional reference — LL-25)

### Track / Exclude Policy

- **Tracked**: `progress.md`, `TODO.md`, `lessons-learned.md`, `current-task.md`, `impl-plan-*.md`, audit artifacts
- **Excluded**: `notes/scratch-*.md`, `notes/draft-*.md`, `notes/personal-*.md`, `notes/_drafts/`, `notes/_archive/`
- **Curation over compression** — CAB state files optimize for lossless semantic preservation; CC's internal memory layers optimize for token efficiency. These are complementary.
- **Pre-push review** — two-layer protocol (hook + skill) catches draft markers before publication. See `hooks/pre-push-state-review.sh` + `skills/pre-push-state-review/`.
- **Internal design docs** are in `docs/_internal/` (not tracked in git)

### File Size Guidance

- `current-task.md`: **<100 lines hard target** (cold-start anchor, concise by design)
- `progress.md`, `TODO.md`, `lessons-learned.md`: **agentically flexible** — no hard limits. Archive to `notes/_archive/` before sync if bloat becomes a concern.

## Verification

Validate CAB project state with:

- `/validate` — Quick structural validation (component locations, plugin.json, naming)
- `/validate --cab-audit` — Full R2 standards audit (7 dimensions, scored, produces YAML + markdown report)
- `/sync-check` — Detect drift between CAB plugin and global `~/.claude/` extensions

Post-implementation verification: invoke the `verifier` agent with acceptance criteria before committing.

## Learned Corrections

Operational constraints from cross-session experience. Full log: `notes/lessons-learned.md`.

- **LL-02/12**: Background agents cannot write files — all artifact-writing must be foreground
- **LL-10**: Always re-fetch official CC docs in-session before modifying KB or frontmatter
- **LL-11**: Wrapper files (defer to official docs) age better than comprehensive mirrors
- **LL-13**: Self-modification deny rules take effect immediately — plan edits atomically
- **LL-15**: Agent `context:` frontmatter does NOT exist in CC — use `skills:` for preloading
- **LL-16**: `effort`, `allowed-tools`, `agent` are valid top-level skill fields (not under `metadata:`)
- **LL-21**: Plugin components at root (`agents/`, `skills/`, `commands/`); `.claude/` for config only
- **LL-25**: `notes/` tracked by default — multi-archetype policy. Curation > compression. Pre-push review protocol (hook + skill). Lessons-referenced protocols: LLs must be structurally woven into skills/agents, not passively documented

## Constraints

- You must frequently inquire and/or automatically check any static files (e.g. \templates, \knowledge, \agents, \skills, etc.) are aligning with the latest official Claude Code docs (use 'claude-docs-helper' skill), as well as specific recommended plugin resources, and update the necessary files in the plugin as appropriate.
- This builder creates initial base structure and templates; domain-specific content must be provided by the user to iteratively optimize and specialize the base architecture.
- Large knowledge bases (100+ files) may require MCP integration for semantic search; recommend this approach when appropriate.
- Templates use `{{PLACEHOLDER}}` syntax for customization

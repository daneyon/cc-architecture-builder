# CAB (cc-architecture-builder)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> Your taxi to stay in line to properly integrate CC with best practices — and you as the driver to apply project context engineering.

A standardized framework and interactive Claude Code plugin for building custom LLM solutions.

## Overview

CAB provides:

- **Global user configurations** (`~/.claude/`) with personal preferences
- **Distributable plugin projects** with marketplace-ready structure
- **Knowledge bases** optimized for Claude Code's retrieval patterns
- **Orchestration framework** with 5 canonical agentic workflow patterns (prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer)
- **Verification-first development** with structured task execution protocol (PLAN → REVIEW → EXECUTE → VERIFY → COMMIT)

For the full architecture guide, see [`docs/claude_code_architecture_guide_human-facing.md`](docs/claude_code_architecture_guide_human-facing.md).

## Installation

### Via GitHub

```bash
# Add marketplace
/plugin marketplace add https://github.com/daneyon/cc-architecture-builder

# Install
/plugin install cab@daneyon
```

### Via Local Clone

```bash
git clone https://github.com/daneyon/cc-architecture-builder.git
cd cc-architecture-builder
# Use directly as your working directory, or reference as a local marketplace
```

## Quick Start

### Create a New Project

```
/new-project
```

Follow the interactive questionnaire to scaffold a new plugin project.

### Set Up Global Configuration

```
/new-global
```

Creates your personal `~/.claude/` configuration.

### Add Components

```
/add-skill my-skill-name
/add-agent my-agent-name
/add-command my-command-name
```

### Validate Structure

```
/validate
```

Checks current project against architecture standards.

## What's Included

| Category | Count | Description |
| --- | --- | --- |
| Skills | 5 | Structure validation, task execution, scaffolding, component creation, quick scaffold |
| Agents | 4 | Orchestrator, architecture advisor, project integrator, verifier |
| Commands | 14 | Project scaffolding, validation, git workflows, tech debt scanning |
| Knowledge files | 32 | Atomized architecture docs across 8 categories |
| Templates | 9 | Global config, plugin project, skill/agent/command scaffolding |

## Commands

| Command | Description |
| --- | --- |
| `/new-project` | Create a new plugin project (interactive discovery) |
| `/new-global` | Set up global user configuration |
| `/integrate-existing` | Overlay CC architecture onto an existing project |
| `/init-plugin` | Initialize new CAB plugin with git setup |
| `/init-worktree` | Set up git worktrees for parallel agent execution |
| `/execute-task` | Start structured task via PLAN → VERIFY → COMMIT protocol |
| `/commit-push-pr` | Stage, commit, push, and create PR in one workflow |
| `/techdebt` | Scan codebase for tech debt, duplication, stale markers |
| `/context-sync` | Pull recent activity into session context summary |
| `/add-skill` | Add a new skill to current project |
| `/add-agent` | Add a new subagent to current project |
| `/add-command` | Add a new custom command to current project |
| `/validate` | Validate current project structure |
| `/kb-index` | Regenerate knowledge base INDEX files |

## Architecture

CAB implements a two-schema architecture:

```
┌─────────────────────────────────────────────┐
│  Schema 1: Global User Configuration        │
│  Location: ~/.claude/                       │
│  Purpose: Personal baseline, all projects   │
└─────────────────────────────────────────────┘
                     │
                     │ inherits / supplements
                     ▼
┌─────────────────────────────────────────────┐
│  Schema 2: Distributable Plugin Project     │
│  Location: ./your-project/                  │
│  Purpose: Team/community distribution       │
└─────────────────────────────────────────────┘
```

## Media & Presentations

Supplementary media for the v1.0.0 release (hosted as [release assets](https://github.com/daneyon/cc-architecture-builder/releases/tag/v1.0.0)):

| Resource | Format | Description |
|----------|--------|-------------|
| [Architecture Walkthrough](https://github.com/daneyon/cc-architecture-builder/releases/download/v1.0.0/Claude_Code_Architecture_2026-03-05.mp4) | MP4 | Video walkthrough of the CAB architecture |
| [Architecture Blueprint](https://github.com/daneyon/cc-architecture-builder/releases/download/v1.0.0/Claude_Code_Architecture_Blueprint_2026-03-05.pdf) | PDF | Visual blueprint of the two-schema architecture |
| [Interactive Introduction](https://github.com/daneyon/cc-architecture-builder/releases/download/v1.0.0/ai-intro-2026_ascent_2026-03-03.html) | HTML | Browser-based interactive introduction |

## Documentation

Full architecture documentation lives in two places:

- **[Architecture Guide](docs/claude_code_architecture_guide_human-facing.md)** — Comprehensive human-facing guide covering philosophy, schemas, extensions, orchestration patterns, and distribution
- **`knowledge/`** — Atomized knowledge base optimized for Claude Code retrieval:
  - `knowledge/INDEX.md` — Master index
  - `knowledge/overview/` — Philosophy and principles
  - `knowledge/components/` — Component deep dives (memory, skills, agents, commands, hooks, MCP, KB)
  - `knowledge/operational-patterns/` — Orchestration framework, worktrees, sessions, multi-agent

## Security

All scaffolded projects follow security best practices:

- Git repositories are **private by default**
- `.gitignore` excludes sensitive files (credentials, API keys, local settings)
- Pre-publication checklist included
- No credentials in templates

## License

[MIT](LICENSE)

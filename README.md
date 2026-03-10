# CAB (cc-architecture-builder)

> Your taxi to stay in line to properly integrate CC with best practices — and you as the driver to apply project context engineering.

A standardized framework and interactive Claude Code plugin for building custom LLM solutions.

## Overview

CAB provides:

- **Global user configurations** (`~/.claude/`) with personal preferences
- **Distributable plugin projects** with marketplace-ready structure
- **Knowledge bases** optimized for Claude Code's retrieval patterns
- **Orchestration framework** with 5 canonical agentic workflow patterns (prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer)
- **Verification-first development** with structured task execution protocol

## Installation

### Via Local Marketplace (Development)

```bash
# Create a local marketplace
mkdir -p dev-marketplace/.claude-plugin
echo '{"name":"dev","owner":{"name":"Dev"},"plugins":[{"name":"cc-architecture-builder","source":"./cc-architecture-builder"}]}' > dev-marketplace/.claude-plugin/marketplace.json

# Add marketplace in Claude Code
/plugin marketplace add ./dev-marketplace

# Install plugin
/plugin install cc-architecture-builder@dev
```

### Via GitHub (Distribution)

```bash
# Add marketplace with this plugin
/plugin marketplace add your-org/claude-plugins

# Install
/plugin install cc-architecture-builder@your-org
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

### Add Components to Existing Project

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

## Architecture Overview

This builder implements a two-schema architecture:

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

## Documentation

Full architecture documentation is available in `knowledge/`:

- `knowledge/INDEX.md` — Master index
- `knowledge/overview/` — Philosophy and principles
- `knowledge/components/` — Component deep dives
- `knowledge/operational-patterns/` — **Orchestration framework**, worktrees, sessions, multi-agent

Key v0.6.0 additions:

- `knowledge/operational-patterns/orchestration-framework.md` — Canonical patterns, cost model, failure modes
- `agents/verifier.md` — Verification specialist agent
- `templates/plugin/settings.json.template` — Starter settings with hooks

## Security

All scaffolded projects follow security best practices:

- Git repositories are **private by default**
- `.gitignore` excludes sensitive files
- Pre-publication checklist included
- No credentials in templates

## License

see @LICENSE

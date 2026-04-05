---
id: git-foundation
title: Git Foundation
category: prerequisites
tags: [git, github, version-control, setup, mcp]
summary: Git as an architectural requirement for Claude Code projects. Covers setup checklist, repository initialization, .gitignore patterns, and GitHub MCP integration.
depends_on: []
related: [security-defaults, marketplace]
complexity: foundational
last_updated: 2025-12-12
estimated_tokens: 650
---

# Git Foundation

## Why Git is Foundational

Git is not merely recommended—it is **architecturally required** for this framework. Claude Code's design assumes git-based workflows:

| Capability | Git Dependency |
|------------|----------------|
| Plugin distribution | Marketplaces pull from git repositories |
| Team collaboration | Project CLAUDE.md and configs shared via git |
| Version control | System instructions, skills, agents all versioned |
| Parallel execution | Git worktrees enable multiple Claude Code sessions |
| GitHub MCP | Requires repository context |

**Note**: Claude Code *functions* without git, but this architecture *requires* it.

## Initial Setup Checklist

```bash
# 1. Verify git installation
git --version

# 2. Configure identity (if not already done)
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# 3. Create project directory
mkdir my-custom-llm && cd my-custom-llm

# 4. Initialize repository FIRST (before any Claude Code work)
git init

# 5. Create initial structure and commit
mkdir -p .claude-plugin commands agents skills knowledge docs
touch CLAUDE.md README.md .gitignore
git add .
git commit -m "Initial project structure"
```

## Recommended .gitignore

```gitignore
# Claude Code local files
.claude/settings.local.json
CLAUDE.local.md

# Environment and secrets
.env
.env.local
*.key
*.pem
credentials.json

# OS files
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/

# Dependencies (if applicable)
node_modules/
__pycache__/
*.pyc

# Build outputs
dist/
build/

# Vector database (if using local semantic search)
.vectors/
```

## GitHub Repository Setup

**Critical**: Always create repositories as **private by default**.

```bash
# Using GitHub CLI (recommended for security)
gh repo create my-custom-llm --private --source=. --push

# Only make public after explicit security review
gh repo edit my-custom-llm --visibility public
```

## GitHub MCP Integration

Connect Claude Code to GitHub for enhanced repository operations:

```bash
# Add GitHub MCP server
claude mcp add --transport http github https://api.github.com/mcp

# Verify connection
claude mcp list
```

Once connected, Claude can:
- Create and manage issues
- Open pull requests
- Search code across repositories
- Review commit history

## Git Workflow for Plugin Development

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   develop   │ ──▶ │   test      │ ──▶ │   review    │ ──▶ │   release   │
│             │     │             │     │             │     │             │
│ Feature     │     │ Local       │     │ PR + team   │     │ Tag version │
│ branches    │     │ marketplace │     │ review      │     │ Publish     │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

**Branch Strategy**:
- `main` — Stable, released versions
- `develop` — Integration branch for features
- `feature/*` — Individual feature development
- `release/*` — Release preparation

## Commit Message Convention

```
<type>: <short description>

[optional body]

Types:
- feat: New feature (skill, agent, command)
- fix: Bug fix
- docs: Documentation changes
- refactor: Code restructuring
- chore: Maintenance tasks
```

## See Also

- [Security Defaults](security-defaults.md) — Pre-publication checklist
- [Marketplace](../distribution/marketplace.md) — Distribution via git
- [Worktree Workflows](../operational-patterns/multi-agent/worktree-workflows.md) — Parallel execution

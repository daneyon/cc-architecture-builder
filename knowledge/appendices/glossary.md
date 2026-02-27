---
id: glossary
title: Glossary
category: appendices
tags: [glossary, terms, definitions, reference]
summary: Definitions of key terms used throughout the Claude Code architecture documentation.
depends_on: []
related: [references]
complexity: foundational
last_updated: 2025-12-12
estimated_tokens: 400
---

# Glossary

## Core Concepts

| Term | Definition |
|------|------------|
| **CLAUDE.md** | Memory file containing system instructions that persist across sessions. Loaded automatically at session start. |
| **Skill** | Model-invoked capability packaged as SKILL.md with instructions and optional resources. Claude decides when to use. |
| **Subagent** | Specialized AI assistant operating in its own context window for delegated tasks. |
| **Command** | User-invoked shortcut triggered by `/command-name`. |
| **Hook** | Event-driven script that executes in response to system events. |
| **MCP** | Model Context Protocol—standard for connecting Claude to external tools and services. |
| **Plugin** | Distributable package containing commands, agents, skills, hooks, and MCP configs. |
| **Marketplace** | Catalog of plugins available for discovery and installation. |

## Architecture Terms

| Term | Definition |
|------|------------|
| **Memory Hierarchy** | Tiered system of CLAUDE.md files with defined precedence (Enterprise → User → Project → Subtree). |
| **Progressive Disclosure** | Pattern of loading only needed content to conserve tokens. |
| **Atomic Content** | Self-contained, single-purpose files optimized for retrieval. |
| **Two-Schema Architecture** | Separation of global user config from distributable project config. |
| **CAB** | cc-architecture-builder — standardized framework and plugin for building custom LLM solutions using Claude Code. |

## Invocation Patterns

| Term | Definition |
|------|------------|
| **Model-Invoked** | Claude autonomously decides to use based on task context (skills, some subagents). |
| **User-Invoked** | Requires explicit user trigger (commands, some subagents). |
| **Event-Driven** | Triggered by system events (hooks). |
| **Automatic** | Always loaded at session start (CLAUDE.md). |

## Technical Terms

| Term | Definition |
|------|------------|
| **Context Window** | Available token space for conversation history and instructions. |
| **Token** | Unit of text processing; roughly 4 characters or 0.75 words. |
| **Frontmatter** | YAML metadata at the top of markdown files (between `---` delimiters). |
| **@Import** | Syntax for including external files in CLAUDE.md (`@path/to/file`). |
| **INDEX.md** | Catalog file listing available resources in a directory. |

## File Types

| Term | Definition |
|------|------------|
| **plugin.json** | Required manifest file in `.claude-plugin/` directory defining plugin metadata. |
| **SKILL.md** | Required file in skill directories containing instructions and frontmatter. |
| **hooks.json** | Configuration file defining event handlers and their triggers. |
| **.mcp.json** | Configuration file defining MCP server connections. |
| **settings.local.json** | Local settings overrides (not committed to git). |

## Distribution Terms

| Term | Definition |
|------|------------|
| **Marketplace Manifest** | JSON file (marketplace.json) listing available plugins in a marketplace. |
| **Installation Scope** | Where a plugin is installed: local, project, or user level. |
| **Source** | Where to fetch a plugin from: relative path, GitHub, or git URL. |

## Git Terms

| Term | Definition |
|------|------------|
| **Worktree** | Separate working directory linked to same repository, enabling parallel branch work. |
| **Session** | Claude Code conversation instance, scoped to working directory. |

---
id: references
title: References
category: appendices
tags: [references, documentation, links, official, skill-creator, mcp-builder]
summary: Links to official Claude Code documentation, Anthropic example skills, and related resources.
depends_on: []
related: [glossary]
complexity: foundational
last_updated: 2025-12-18
estimated_tokens: 400
---

# References

## Official Claude Code Documentation

### Getting Started
| Document | URL |
|----------|-----|
| Overview | https://docs.anthropic.com/en/docs/claude-code/overview |
| Quickstart | https://docs.anthropic.com/en/docs/claude-code/quickstart |
| Common Workflows | https://docs.anthropic.com/en/docs/claude-code/common-workflows |

### Core Features
| Document | URL |
|----------|-----|
| Memory (CLAUDE.md) | https://docs.anthropic.com/en/docs/claude-code/memory |
| Skills | https://docs.anthropic.com/en/docs/claude-code/skills |
| Subagents | https://docs.anthropic.com/en/docs/claude-code/sub-agents |
| Slash Commands | https://docs.anthropic.com/en/docs/claude-code/slash-commands |
| Hooks | https://docs.anthropic.com/en/docs/claude-code/hooks |
| MCP | https://docs.anthropic.com/en/docs/claude-code/mcp |

### Plugins
| Document | URL |
|----------|-----|
| Plugins Guide | https://docs.anthropic.com/en/docs/claude-code/plugins |
| Plugins Reference | https://docs.anthropic.com/en/docs/claude-code/plugins-reference |
| Plugin Marketplaces | https://docs.anthropic.com/en/docs/claude-code/plugin-marketplaces |

### Configuration
| Document | URL |
|----------|-----|
| Settings | https://docs.anthropic.com/en/docs/claude-code/settings |
| CLI Reference | https://docs.anthropic.com/en/docs/claude-code/cli-reference |
| Model Configuration | https://docs.anthropic.com/en/docs/claude-code/model-config |

### Security & Administration
| Document | URL |
|----------|-----|
| Security | https://docs.anthropic.com/en/docs/claude-code/security |
| IAM | https://docs.anthropic.com/en/docs/claude-code/iam |
| Data Usage | https://docs.anthropic.com/en/docs/claude-code/data-usage |

## Agent Skills Documentation

| Document | URL |
|----------|-----|
| Skills Overview | https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview |
| Best Practices | https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/best-practices |

## Anthropic Example Skills

Anthropic provides example skills via the `anthropic-agent-skills` GitHub repository. This project includes adapted versions of two key skills:

| Skill | Purpose | Location in This Project |
|-------|---------|--------------------------|
| **skill-creator** | Comprehensive guide for creating effective skills | `skills/skill-creator/` |
| **mcp-builder** | Guide for building MCP servers | `skills/mcp-builder/` |

**Key resources in bundled skills**:
- `skill-creator/references/workflows.md` — Sequential and conditional workflow patterns
- `skill-creator/references/output-patterns.md` — Template and example patterns
- `skill-creator/scripts/init_skill.py` — Skill initialization script
- `skill-creator/scripts/package_skill.py` — Skill packaging script
- `mcp-builder/reference/mcp_best_practices.md` — MCP server design guidelines
- `mcp-builder/reference/python_mcp_server.md` — Python/FastMCP patterns
- `mcp-builder/reference/node_mcp_server.md` — TypeScript/SDK patterns

## Model Context Protocol

| Resource | URL |
|----------|-----|
| MCP Introduction | https://modelcontextprotocol.io/introduction |
| MCP Specification | https://modelcontextprotocol.io/specification/draft |
| MCP Quickstart | https://modelcontextprotocol.io/quickstart/server |
| TypeScript SDK | https://github.com/modelcontextprotocol/typescript-sdk |
| Python SDK | https://github.com/modelcontextprotocol/python-sdk |
| Community Servers | https://github.com/modelcontextprotocol/servers |

## Related Resources

| Resource | Description |
|----------|-------------|
| Anthropic Engineering Blog | https://www.anthropic.com/engineering |
| Claude Models Overview | https://docs.anthropic.com/en/docs/about-claude/models/overview |
| Prompt Engineering | https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview |

## This Project

| Resource | Description |
|----------|-------------|
| Architecture Guide | Main guide document (`docs/claude_code_architecture_guide.md`) |
| Modular Knowledge Base | Atomized knowledge in `knowledge/` directory |
| Bundled Skills | `skills/` directory (skill-creator, mcp-builder, etc.) |
| Templates | Starter templates in `templates/` directory |

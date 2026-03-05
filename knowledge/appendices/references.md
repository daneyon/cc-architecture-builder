---
id: references
title: References
category: appendices
tags: [references, links, documentation, resources]
summary: Comprehensive reference links to official Claude Code documentation, Agent Skills resources, MCP protocol, and supplemental materials.
depends_on: []
related: [glossary]
complexity: foundational
last_updated: 2026-02-25
estimated_tokens: 600
revision_note: "v0.6.0 — Added Anthropic engineering articles (agentic workflows, harnesses, multi-agent) and Boris Cherny CC creator tips."
---

# References

## URL Change Notice

As of late 2025, Claude Code documentation moved to a new domain:
- **OLD**: `docs.anthropic.com/en/docs/claude-code/*`
- **NEW**: `code.claude.com/docs/en/*`

---

## Official Claude Code Documentation

| Document | URL |
|----------|-----|
| Overview | https://code.claude.com/docs/en/overview |
| Quickstart | https://code.claude.com/docs/en/quickstart |
| Memory | https://code.claude.com/docs/en/memory |
| Skills | https://code.claude.com/docs/en/skills |
| Subagents | https://code.claude.com/docs/en/sub-agents |
| Plugins | https://code.claude.com/docs/en/plugins |
| Discover Plugins | https://code.claude.com/docs/en/discover-plugins |
| Hooks | https://code.claude.com/docs/en/hooks-guide |
| MCP | https://code.claude.com/docs/en/mcp |
| Settings | https://code.claude.com/docs/en/settings |
| CLI Reference | https://code.claude.com/docs/en/cli-reference |
| Programmatic Usage | https://code.claude.com/docs/en/headless |
| Troubleshooting | https://code.claude.com/docs/en/troubleshooting |

---

## Agent Skills Documentation

| Document | URL |
|----------|-----|
| Skills Overview | https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview |
| Best Practices | https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/best-practices |
| Quickstart | https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/quickstart |

---

## Model Context Protocol (MCP)

| Resource | URL |
|----------|-----|
| Introduction | https://modelcontextprotocol.io/introduction |
| Specification | https://modelcontextprotocol.io/specification/draft |
| TypeScript SDK | https://github.com/modelcontextprotocol/typescript-sdk |
| Python SDK | https://github.com/modelcontextprotocol/python-sdk |
| Community Servers | https://github.com/modelcontextprotocol/servers |

---

## Anthropic Example Skills

Available via marketplace: `https://github.com/anthropics/anthropic-agent-skills`

| Skill | Purpose |
|-------|---------|
| skill-creator | Comprehensive skill authoring guide |
| mcp-builder | MCP server development guide |

**Installation**:
```bash
claude /plugin marketplace add https://github.com/anthropics/anthropic-agent-skills
claude /plugin install skill-creator@anthropic-agent-skills
```

---

## Agent SDK

| Resource | URL |
|----------|-----|
| Overview | https://docs.anthropic.com/en/docs/agent-sdk/overview |
| TypeScript SDK | https://docs.anthropic.com/en/docs/agent-sdk/typescript |
| Python SDK | https://docs.anthropic.com/en/docs/agent-sdk/python |

---

## IDE Integrations

| IDE | URL |
|-----|-----|
| VS Code | https://code.claude.com/docs/en/vs-code |
| JetBrains | https://code.claude.com/docs/en/jetbrains |

---

## CI/CD Integration

| Platform | URL |
|----------|-----|
| GitHub Actions | https://code.claude.com/docs/en/github-actions |
| GitLab CI/CD | https://code.claude.com/docs/en/gitlab-ci-cd |

---

## Deployment

| Topic | URL |
|-------|-----|
| Third-Party Integrations | https://code.claude.com/docs/en/third-party-integrations |
| Security | https://code.claude.com/docs/en/security |
| Data Usage | https://code.claude.com/docs/en/data-usage |

---

## Other Resources

| Resource | URL |
|----------|-----|
| Anthropic Engineering Blog | https://www.anthropic.com/engineering |
| Trust Center | https://trust.anthropic.com |
| Support | https://support.claude.com |

---

## Anthropic Engineering Articles (v0.6.0 Sources)

These articles are the primary sources for the orchestration framework, agentic workflow patterns, and multi-agent collaboration content added in v0.6.0.

| Article | Date | URL | Key Topics |
|---------|------|-----|------------|
| Building Effective Agents | Dec 2024 | https://www.anthropic.com/engineering/building-effective-agents | 5 canonical workflow patterns, simplicity-first principle |
| Effective Context Engineering for AI Agents | Sep 2025 | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | Context window as shared resource, token efficiency |
| Effective Harnesses for Long-Running Agents | Nov 2025 | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | Initializer/iterator harness, feature lists, progress files, failure modes |
| Building a Multi-Agent Research System | Jun 2025 | https://www.anthropic.com/engineering/building-a-multi-agent-research-system | Multi-agent cost model, delegation templates, effort scaling |

---

## CC Creator Tips (Boris Cherny)

Practical tips from Boris Cherny, creator of Claude Code, validated against Opus 4.6 (Feb 2026).

| Source | URL | Key Topics |
|--------|-----|------------|
| CC Tips Gist (consolidated) | https://gist.github.com/AriSafTech/a63ddca53e24e450d5bea1a56a0e2df3 | Verification methods, CLAUDE.md as feedback loop, plan mode, worktrees, hooks, effort levels |
| Boris Cherny Twitter/Threads | https://x.com/basaborern | Real-time CC development tips |

---

## Context Engineering References (v0.8.0 Sources)

These sources inform the context health, filesystem-as-context, and session management patterns.

| Source | URL | Key Topics |
|--------|-----|------------|
| Koylan — Agent Skills for Context Engineering | https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering | Context fundamentals, degradation patterns, compression, filesystem-context, memory systems, multi-agent patterns, evaluation |
| Jarrod Watts — Practical Context Engineering | https://x.com/jarrodwatts/status/2008495347115630701 | Value-dense context, continue/compact/fresh decisions, context monitoring (Claude HUD plugin) |
| Fowler/Böckeler — Context Engineering for Coding Agents | https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html | Instructions vs guidance taxonomy, "who decides to load" framework, illusion of control, CC feature overview |
| High Agency (George Mack) | https://www.highagency.com/ | Clear thinking + bias to action + disagreeability as foundational human operator philosophy |

---

## Keeping Links Updated

Claude Code documentation URLs may change over time. To verify current links:

1. Check the main docs landing page: https://code.claude.com/docs
2. Use the search function on the docs site
3. Review Anthropic's changelog/release notes

This knowledge base includes `source:` metadata in each file header to track the authoritative documentation URL for that topic.

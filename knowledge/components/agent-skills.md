---
id: agent-skills
title: Agent Skills
category: components
tags: [skills, model-invoked, capabilities, SKILL.md, progressive-disclosure, commands-migration]
summary: Complete reference for Agent Skills — model-invoked capabilities defined in SKILL.md files. Covers all frontmatter fields, string substitutions, dynamic context, execution models, bundled skills, and CAB-specific patterns.
depends_on: [memory-claudemd]
related: [subagents, custom-commands, knowledge-base-structure, extension-discovery]
complexity: intermediate
last_updated: 2026-04-05
estimated_tokens: 1200
confidence: A
review_by: 2026-07-05
source: https://code.claude.com/docs/en/skills
---

# Agent Skills

> **Wrapper philosophy**: This file documents CAB-specific patterns and extensions. For native skill mechanics, see the [official docs](https://code.claude.com/docs/en/skills).

## Overview

Skills are **model-invoked** capabilities — Claude autonomously decides when to use them based on task context and description matching. Skills are lazy-loaded: only metadata occupies context at startup; full content loads on invocation.

**Commands → Skills migration**: Skills are now the preferred extension type. Commands still work but skills subsume their functionality. New projects should default to skills; migrate existing commands when practical.

---

## Skill Locations & Discovery

| Type | Location | Scope |
| ---- | -------- | ----- |
| **Personal** | `~/.claude/skills/` | All your projects |
| **Project** | `.claude/skills/` | Current project (shared via git) |
| **Plugin** | Bundled with plugins | When plugin installed |
| **Monorepo** | `packages/*/.claude/skills/` | Auto-discovered per package (B10) |

Monorepo nested discovery: CC walks the directory tree and auto-discovers `.claude/skills/` inside any package directory. No explicit registration required.

---

## SKILL.md Structure

```
skill-name/
├── SKILL.md              # Required — frontmatter + instructions
└── Bundled Resources     # Optional
    ├── scripts/          # Executable code (outputs only in context)
    ├── references/       # Documentation (loaded on demand)
    └── assets/           # Templates, images, fonts
```

---

## Frontmatter Reference

All fields are optional unless noted. See [official docs](https://code.claude.com/docs/en/skills) for canonical definitions.

| Field | Type | Default | Description |
| ----- | ---- | ------- | ----------- |
| `name` | string | Directory name | Lowercase, hyphens, max 64 chars. No reserved words ("anthropic", "claude"). |
| `description` | string | First paragraph of body | What + when. Budget: ~1% of context window (`SLASH_COMMAND_TOOL_CHAR_BUDGET`). |
| `argument-hint` | string | — | Placeholder shown in autocomplete (e.g., `<file-path>`). |
| `allowed-tools` | string (CSV) | All tools | Restrict which tools the skill can use. |
| `disable-model-invocation` | boolean | `false` | If `true`, only user `/slash` invocation works — model cannot auto-select. |
| `user-invocable` | boolean | `true` | If `false`, only the model can invoke (hidden from `/` menu). |
| `model` | string | Session default | Override model for this skill (e.g., `claude-sonnet-4-20250514`). |
| `effort` | string | Session default | Thinking effort: `"low"`, `"medium"`, `"high"`, or `"ultrathink"` (extended thinking trigger). |
| `context` | string | `"inline"` | Execution model: `"fork"` runs in isolated context; `"inline"` shares session context. |
| `agent` | boolean | `false` | Run as a subagent with its own tool-use loop. |
| `hooks` | object | — | Skill-scoped hooks (same schema as global hooks). |
| `paths` | string[] | — | File paths to auto-load into context when skill activates. |
| `shell` | string | System default | Shell override for Bash tool within this skill. |

### Invocation Control Matrix (B7)

The interaction of `disable-model-invocation` and `user-invocable` creates four modes:

| `disable-model-invocation` | `user-invocable` | Who can invoke | Use case |
| :---: | :---: | --- | --- |
| `false` | `true` | Model + User | Default — full availability |
| `true` | `true` | User only | Dangerous/costly operations |
| `false` | `false` | Model only | Internal plumbing, pipelines |
| `true` | `false` | Nobody | Effectively disabled |

### Execution Models: fork vs inline (B4)

| Mode | Context | State sharing | Use when |
| ---- | ------- | ------------- | -------- |
| `inline` | Shared session | Full access to conversation | Default — most skills |
| `fork` | Isolated copy | No bleed-back to parent | Heavy/exploratory work, subagent-like isolation |

---

## String Substitutions (B2)

Available in SKILL.md body and referenced files:

| Variable | Expands to |
| -------- | ---------- |
| `$ARGUMENTS` | Full argument string from invocation |
| `$ARGUMENTS[N]` | Nth argument (0-indexed) |
| `$N` / `$1`, `$2`, ... | Positional arguments (1-indexed) |
| `${CLAUDE_SESSION_ID}` | Current session identifier |
| `${CLAUDE_SKILL_DIR}` | Absolute path to the skill's directory |

---

## Dynamic Context Injection (B3)

Preprocessor syntax embeds live command output into the skill body at load time:

```markdown
Current branch: `!git branch --show-current`
Recent changes: `!git log --oneline -5`
```

The `` `!command` `` syntax executes shell commands and injects stdout inline before the model sees the content. Use for lightweight, fast commands only.

---

## Bundled Skills (B5)

CC ships 5 built-in skills available in every session:

| Skill | Purpose |
| ----- | ------- |
| `/batch` | Process multiple items with a repeated prompt |
| `/claude-api` | Build apps using Anthropic SDK |
| `/debug` | Systematic debugging workflow |
| `/loop` | Run a prompt on a recurring interval |
| `/simplify` | Review changed code for reuse and quality |

---

## Permission Rules Syntax (B11)

In `settings.json`, skill permissions use the `Skill()` syntax:

```json
{
  "permissions": {
    "allow": ["Skill(deploy-staging)"],
    "deny": ["Skill(dangerous-op *)"]
  }
}
```

- `Skill(name)` — match exact skill
- `Skill(name *)` — match skill and all sub-operations

---

## Enterprise Skill Tier (B9)

Organizations can distribute managed skills via enterprise settings. These are injected at the organization level and cannot be overridden by individual users. See your admin for managed settings configuration.

---

## Progressive Disclosure

| Level | Loaded when | Token cost | Content |
| ----- | ----------- | ---------- | ------- |
| **L1: Metadata** | Session start | ~100 tokens/skill | `name`, `description` |
| **L2: Instructions** | Skill triggered | < 5k tokens | SKILL.md body |
| **L3: Resources** | As needed | Unlimited | Bundled files, scripts |

**Description budget (B12)**: Descriptions consume ~1% of the context window. The `SLASH_COMMAND_TOOL_CHAR_BUDGET` env var controls the ceiling. Keep descriptions concise — keyword-rich, 1-2 sentences.

---

## CAB-Specific Patterns

### Naming Convention

CAB uses abbreviated gerund form for skill directories:

```
# Standard CC convention
processing-pdfs/

# CAB abbreviation convention (when unambiguous)
proc-pdfs/
```

This reduces filesystem clutter in projects with many skills. Full descriptive names remain in the `name` frontmatter field.

### Wrapper Philosophy in Practice

Skills in CAB projects should:

1. **Link to official docs** — Don't duplicate CC-native behavior in skill instructions
2. **Document only the delta** — What CAB adds on top (templates, conventions, verification steps)
3. **Use `${CLAUDE_SKILL_DIR}`** — Reference bundled resources via the substitution variable, not hardcoded paths

### Imperative Trigger Format

Standard descriptions degrade mid-session due to lost-in-middle attention decay. For projects with 3+ skills, use the imperative format:

```yaml
description: >
  INVOKE THIS SKILL when comparing predictions across sources.
  Pipeline position: THIRD — runs after inference, before reporting.
  DO NOT compute comparison metrics manually — use this skill's modules.
```

See [Extension Discovery](../operational-patterns/extension-discovery.md) for the full pattern and rationale.

### CAB Skill Scaffolding

Use `/add-skill` to scaffold new skills with correct structure:

```bash
# Creates .claude/skills/my-skill/ with SKILL.md template
/add-skill my-skill
```

The template includes all frontmatter fields as commented YAML for reference.

---

## Debugging

| Symptom | Check |
| ------- | ----- |
| Skill not invoked | Description too vague — add specific trigger keywords |
| Skill not discovered | Verify path: `~/.claude/skills/name/SKILL.md` or `.claude/skills/name/SKILL.md` |
| YAML parse error | Opening `---` on line 1, closing `---` before body, no tabs |
| Model ignores skill | Check `disable-model-invocation` is not `true` |
| User can't invoke | Check `user-invocable` is not `false` |

---

## See Also

- [Custom Commands](custom-commands.md) — User-invoked shortcuts (skills preferred for new work)
- [Subagents](subagents.md) — Specialized assistants with separate context
- [Extension Discovery](../operational-patterns/extension-discovery.md) — Mitigating mid-session skill awareness decay
- [Official Skills Docs](https://code.claude.com/docs/en/skills) — Canonical reference

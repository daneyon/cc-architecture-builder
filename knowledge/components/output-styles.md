---
id: output-styles
title: Output Styles
category: components
tags: [output-styles, system-prompt, persona, custom-agent, configuration]
summary: Output styles modify CC's system prompt to reshape agent behavior. Built-in styles (default, explanatory, learning) plus custom Markdown-based definitions for plugins and personal use.
depends_on: [memory-claudemd]
related: [agent-skills, subagents, distributable-plugin, global-user-config]
complexity: intermediate
last_updated: 2026-04-05
estimated_tokens: 700
source: https://code.claude.com/docs/en/output-styles
confidence: A
review_by: 2026-07-05
revision_note: "v1.0 — NEW KB card for T5-05."
---

# Output Styles

> **Official docs**: [code.claude.com/docs/en/output-styles](https://code.claude.com/docs/en/output-styles) — authoritative reference for built-in styles, custom style authoring, and configuration.

## Overview

Output styles modify CC's **system prompt** directly. Unlike CLAUDE.md (loaded as user message) or skills (on-demand), output styles reshape the foundational instructions Claude receives — enabling CC to function as any type of agent, not just a software engineering assistant.

**Key mechanism**: Custom output styles **remove** the default coding-specific instructions from the system prompt (unless explicitly retained), then inject your custom instructions.

---

## Built-in Styles

| Style | Behavior |
|-------|---------|
| **Default** | Standard software engineering system prompt |
| **Explanatory** | Adds educational "Insights" between coding tasks; teaches codebase patterns |
| **Learning** | Collaborative mode; shares insights AND asks user to implement small code via `TODO(human)` markers |

---

## Custom Style Format

Custom output styles are **Markdown files with YAML frontmatter**, placed in:

| Location | Scope |
|----------|-------|
| `~/.claude/output-styles/` | Personal (all projects) |
| `.claude/output-styles/` | Project-level (shared via git) |
| Plugin `output-styles/` directory | Bundled with plugin |

### File Structure

```markdown
---
name: My Custom Style
description: Brief description shown in /config picker
keep-coding-instructions: false
---

# Custom Instructions

Your system prompt content here...
```

### Frontmatter Fields

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `name` | string | Filename | Display name in `/config` picker |
| `description` | string | None | Description shown during selection |
| `keep-coding-instructions` | boolean | `false` | Retain CC's default coding system prompt sections |

**Critical**: When `keep-coding-instructions` is `false` (default), CC's entire coding-focused system prompt is stripped. Set to `true` if your style augments rather than replaces the default engineering behavior.

---

## Configuration

**Set active style**:
- Interactive: `/config` → select "Output style"
- Manual: Edit `outputStyle` field in settings

```json
{
  "outputStyle": "Explanatory"
}
```

Saved to `.claude/settings.local.json` (local project level).

**Session timing**: Output style is set at **session start**. Changes take effect only in a new session — this is by design to enable prompt caching within a conversation.

---

## System Prompt Interaction Model

| Feature | System Prompt Impact | Loaded When |
|---------|---------------------|-------------|
| **Output Styles** | Replaces/modifies system prompt; removes coding instructions by default | Session start (locked) |
| **CLAUDE.md** | Added as user message after system prompt; does not edit it | Session start (re-read on compact) |
| **`--append-system-prompt`** | Appended to system prompt; does not remove anything | CLI flag per session |
| **Skills** | Task-specific prompts injected on demand | On invocation |
| **Agents** | Separate context windows with own instructions | On dispatch |

**Reminders**: Claude receives periodic system reminders during conversation to adhere to the active output style.

---

## Token Cost Implications

- Custom instructions increase input tokens, but **prompt caching** mitigates cost after the first turn
- Explanatory and Learning styles produce longer responses (more output tokens) by design
- Keeping system prompt stable within a session maximizes cache hit rate

---

## CAB Patterns

### Plugin Output Styles

Plugins can bundle output styles in an `output-styles/` directory. The `outputStyles` field in `plugin.json` overrides the default discovery location:

```json
{
  "outputStyles": "./custom-styles/"
}
```

Plugin-bundled styles appear in the `/config` picker alongside built-in and personal styles.

### When to Use Output Styles vs. Alternatives

| Need | Use |
|------|-----|
| Reshape CC's core behavior for non-engineering use | **Output style** (removes coding prompt) |
| Add project-specific instructions | **CLAUDE.md** (user message, always loaded) |
| Scoped policies for file types | **Rules** (`.claude/rules/` with `paths:` frontmatter) |
| Repeatable workflows | **Skills** (on-demand, lazy-loaded) |
| Different behavior per task type | **Agents** (separate context) |

## See Also

- [Memory System](memory-claudemd.md) — CLAUDE.md hierarchy and @imports
- [Agent Skills](agent-skills.md) — On-demand capabilities
- [Global User Config](../schemas/global-user-config.md) — Settings hierarchy
- [Official Output Styles Docs](https://code.claude.com/docs/en/output-styles) — Authoritative reference

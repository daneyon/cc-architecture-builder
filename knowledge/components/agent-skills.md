---
id: agent-skills
title: Agent Skills
category: components
tags: [skills, model-invoked, capabilities, SKILL.md, progressive-disclosure]
summary: Complete guide to Agent Skills - model-invoked capabilities that extend Claude's functionality through SKILL.md files with optional bundled resources.
depends_on: [memory-claudemd]
related: [subagents, custom-commands, knowledge-base-structure]
complexity: intermediate
last_updated: 2025-12-23
estimated_tokens: 1000
source: https://code.claude.com/docs/en/skills
---
# Agent Skills

## Overview

Skills are **model-invoked** capabilities—Claude autonomously decides when to use them based on task context and skill description. This differs from commands, which require explicit user invocation. 

Skills are lazy-loaded. Only metadata is present in context; full skill content loads on invocation.

  How I Select Skills

1. Pattern match on user request — I scan the short descriptions for keyword/intent matches
2. Explicit invocation — User types /skill-name directly
3. Contextual relevance — If a task clearly matches a skill's trigger description

  Implication for you: Your skill descriptions (the when to use metadata) are critical. Keep them:

- Keyword-rich — Include trigger terms users might say
- Concise — ~1-2 sentences max
- Distinct — Avoid overlap that causes ambiguity between skills

**Source**: [Agent Skills](https://code.claude.com/docs/en/skills)

> **Core Philosophy**: The context window is a public good. Only add context Claude doesn't already have.

---

## Skill Locations

| Type                      | Location              | Scope                          |
| ------------------------- | --------------------- | ------------------------------ |
| **Personal Skills** | `~/.claude/skills/` | All your projects              |
| **Project Skills**  | `.claude/skills/`   | Current project (team via git) |
| **Plugin Skills**   | Bundled with plugins  | When plugin installed          |

---

## Skill Structure

```
skill-name/
├── SKILL.md              # Required
└── Bundled Resources     # Optional
    ├── scripts/          # Executable code
    ├── references/       # Documentation (loaded on demand)
    └── assets/           # Templates, images, fonts
```

**Bundled Resource Types**:

| Type            | Purpose                                       | Loaded Into Context? |
| --------------- | --------------------------------------------- | -------------------- |
| `scripts/`    | Executable code for deterministic operations  | No (outputs only)    |
| `references/` | Documentation Claude references while working | Yes (on demand)      |
| `assets/`     | Templates, images, fonts for output           | No (used in output)  |

---

## SKILL.md Format

```yaml
---
name: skill-name
description: What this skill does AND when to use it. Include specific triggers. Third-person voice.
---

# Skill Name

## Instructions
1. Step-by-step guidance
2. Clear procedures

## Examples
Show concrete examples of using this Skill.

## References
For details, see [reference.md](reference.md)
```

**Critical**: The `description` field determines when Claude uses the skill. Include both what it does AND when to use it.

---

## Frontmatter Fields

| Field             | Required | Description                                        |
| ----------------- | -------- | -------------------------------------------------- |
| `name`          | Yes      | Lowercase letters, numbers, hyphens (max 64 chars) |
| `description`   | Yes      | What skill does + when to use (max 1024 chars)     |
| `allowed-tools` | No       | Restrict which tools the skill can use             |

### Naming Requirements

- Max 64 characters
- Lowercase letters, numbers, hyphens only
- Cannot start/end with hyphen
- No `--` sequences
- No reserved words ("anthropic", "claude")

**Convention**: Use gerund form: `processing-pdfs`, `analyzing-data`, `managing-databases`

---

## Tool Restrictions (allowed-tools)

Limit which tools Claude can use when a skill is active:

```yaml
---
name: safe-file-reader
description: Read files without making changes. Use for read-only file access.
allowed-tools: Read, Grep, Glob
---
```

When specified, Claude can only use listed tools without asking permission. Useful for:

- Read-only skills
- Security-sensitive workflows
- Limited-scope operations

If omitted, Claude asks for permission as normal.

---

## Progressive Disclosure

Skills use a three-level loading model:

| Level                           | When Loaded      | Token Cost        | Content                      |
| ------------------------------- | ---------------- | ----------------- | ---------------------------- |
| **Level 1: Metadata**     | Always (startup) | ~100 tokens/skill | `name` and `description` |
| **Level 2: Instructions** | When triggered   | < 5k tokens       | SKILL.md body                |
| **Level 3: Resources**    | As needed        | Unlimited         | Bundled files, scripts       |

**Key Principle**: Keep SKILL.md body focused. Split into reference files as needed.

---

## View Available Skills

Ask Claude directly:

```
What Skills are available?
```

Or check filesystem:

```bash
# Personal skills
ls ~/.claude/skills/

# Project skills
ls .claude/skills/
```

---

## Debugging Skills

### Claude doesn't use my skill

**Check description specificity**:

```yaml
# Too vague
description: Helps with documents

# Specific
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

### Verify file path

```bash
# Personal: ~/.claude/skills/skill-name/SKILL.md
# Project: .claude/skills/skill-name/SKILL.md
ls ~/.claude/skills/my-skill/SKILL.md
```

### Check YAML syntax

```bash
cat SKILL.md | head -n 10
```

Ensure:

- Opening `---` on line 1
- Closing `---` before Markdown content
- Valid YAML (no tabs, correct indentation)

---

## Sharing Skills

**Recommended**: Distribute through [plugins](https://code.claude.com/docs/en/plugins).

**Alternative**: Commit to project repository:

```bash
mkdir -p .claude/skills/team-skill
# Create SKILL.md
git add .claude/skills/
git commit -m "Add team skill"
git push
```

Team members get skills automatically on `git pull`.

---

## Example: Code Reviewer Skill

```yaml
---
name: code-reviewer
description: Review code for best practices and potential issues. Use when reviewing code, checking PRs, or analyzing code quality.
allowed-tools: Read, Grep, Glob
---

# Code Reviewer

## Review checklist

1. Code organization and structure
2. Error handling
3. Performance considerations
4. Security concerns
5. Test coverage

## Instructions

1. Read target files using Read tool
2. Search for patterns using Grep
3. Find related files using Glob
4. Provide detailed feedback on code quality
```

---

## Best Practices

| Practice                     | Description                   |
| ---------------------------- | ----------------------------- |
| **Keep focused**       | One skill = one capability    |
| **Clear descriptions** | Include what AND when         |
| **Test with team**     | Verify activation and clarity |
| **Document versions**  | Track changes in SKILL.md     |

---

## See Also

- [Subagents](subagents.md) — Specialized assistants with separate context
- [Custom Commands](custom-commands.md) — User-invoked shortcuts
- [Agent Skills Best Practices](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/best-practices)

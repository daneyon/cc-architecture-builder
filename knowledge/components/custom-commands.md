---
id: custom-commands
title: Custom Commands (Legacy → Skills Migration)
category: components
tags: [commands, slash-commands, skills, migration, legacy]
summary: Custom commands are now merged into skills. Commands still work but skills are preferred. This doc covers the migration path and when commands still apply.
depends_on: [agent-skills]
related: [agent-skills, subagents]
complexity: foundational
last_updated: 2026-04-05
estimated_tokens: 400
source: https://code.claude.com/docs/en/skills
confidence: A
review_by: 2026-07-05
---

# Custom Commands → Skills Migration

## Status: Commands Merged Into Skills

As of 2026, CC has **merged commands into skills**. Skills are the preferred path for all new development. Commands still work for backward compatibility, but when both exist for the same name, the skill wins.

> **Official docs**: [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills) — covers both skills and the commands subsystem.

---

## Key Differences

| Aspect | Commands (legacy) | Skills (preferred) |
|--------|-------------------|-------------------|
| **Location** | `commands/name.md` | `skills/name/SKILL.md` |
| **Invocation** | User-only (`/name`) | User or model-invoked |
| **Frontmatter** | description, allowed-tools | 11+ fields including model, effort, context, hooks |
| **Resources** | Single file only | Directory with scripts/, assets/, references/ |
| **Substitutions** | $ARGUMENTS, $1-$N | Same + ${CLAUDE_SESSION_ID}, ${CLAUDE_SKILL_DIR} |
| **Dynamic context** | `` !`command` `` | Same |
| **Conflict resolution** | — | Skill wins if both exist for same name |

---

## Migration Path

To migrate a command to a skill:

```
# Before (command)
commands/deploy.md

# After (skill)
skills/deploy/
├── SKILL.md          # Same content, enhanced frontmatter
├── scripts/          # Optional: extracted bash logic
└── references/       # Optional: supporting docs
```

**Frontmatter upgrade**:

```yaml
# Command frontmatter (minimal)
---
description: Deploy to staging
allowed-tools: Bash
---

# Skill frontmatter (enhanced)
---
description: Deploy to staging
allowed-tools: Bash
user-invocable: true           # Preserves /deploy trigger
disable-model-invocation: true # Optional: keep user-only behavior
effort: medium
---
```

Set `user-invocable: true` to preserve the `/name` trigger. Add `disable-model-invocation: true` if you want to prevent Claude from auto-invoking it.

---

## When Commands Still Apply

Commands remain appropriate when:

- **Backward compatibility** — existing workflows depend on command paths
- **Simplicity** — single-file command with no resources needed
- **Plugin commands** — CAB maintains `commands/` for CLI-style triggers with concise abbreviated names

CAB convention: Plugin commands use concise abbreviations (e.g., `/cab:execute-task` not `/cc-architecture-builder:execute-task`). This naming convention applies regardless of whether the implementation is a command or skill.

---

## CAB Command Inventory

CAB currently maintains 14 commands in `commands/`. These function as quick-trigger wrappers that often load a corresponding skill:

| Pattern | Example |
|---------|---------|
| Command triggers skill | `/execute-task` loads `executing-tasks` skill |
| Command triggers workflow | `/commit-push-pr` runs multi-step git workflow |
| Command is self-contained | `/validate` runs structural checks directly |

Future CAB versions may migrate high-value commands to skills for enhanced frontmatter support while maintaining the abbreviated command names as aliases.

## See Also

- [Agent Skills](agent-skills.md) — Full skill documentation (11+ frontmatter fields)
- [Architecture Philosophy](../overview/architecture-philosophy.md) — Invocation patterns

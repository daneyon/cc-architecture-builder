---
description: Check for drift between CAB plugin extensions and deployed global (~/.claude/) extensions. Reports hash mismatches and content differences.
allowed-tools: Read, Bash, Grep, Glob
---

# Sync Check

Detects drift between the CAB plugin (source of truth) and deployed global
extensions. Use after making changes in CAB to identify what needs redeployment,
or periodically to ensure global config stays aligned.

## Behavior

1. **Discover paired files**: Map CAB plugin extensions to their global equivalents:

   | CAB Location | Global Location |
   |-------------|----------------|
   | `.claude/agents/*.md` | `~/.claude/agents/*.md` |
   | `.claude/skills/*/SKILL.md` | `~/.claude/skills/*/SKILL.md` |
   | `.claude/commands/*.md` | `~/.claude/commands/*.md` |

2. **Compare each pair**:
   ```bash
   # For each paired file:
   diff <(cat "cab-path") <(cat "global-path")
   ```

3. **Report results**:

   ```
   ── SYNC CHECK ─────────────────────────────────
   
   ✅ In sync (N files)
     .claude/agents/orchestrator.md
     .claude/agents/verifier.md
     ...
   
   ⚠️  Drift detected (N files)
     .claude/skills/architecture-analyzer/SKILL.md
       CAB newer: 2026-04-05 | Global: 2026-04-03
       Lines changed: +12 -3
     .claude/commands/techdebt.md
       CAB newer: 2026-04-05 | Global: 2026-04-01
       Lines changed: +5 -2
   
   ❌ Missing from global (N files)
     .claude/skills/session-close/SKILL.md
     .claude/commands/sync-check.md
   
   ❌ Extra in global (not in CAB) (N files)
     .claude/skills/strategy-framework/SKILL.md
   
   ───────────────────────────────────────────────
   ```

4. **Recommend actions** based on drift:
   - Files where CAB is newer → "Deploy to global: `cp <cab-path> <global-path>`"
   - Files where global is newer → "Review: global has changes not in CAB. Merge or overwrite?"
   - Missing from global → "Deploy new extension"
   - Extra in global → "Not CAB-managed. Ignore or integrate into CAB?"

## Arguments

- No arguments: Full sync check (all extension types)
- `agents`: Check only agents
- `skills`: Check only skills
- `commands`: Check only commands

## Examples

```
/sync-check
→ Full drift report across all extension types

/sync-check skills
→ Check only skills for drift

/sync-check agents
→ Check only agents for drift
```

## Notes

- Excludes `settings.local.json` and `CLAUDE.local.md` (personal, not synced)
- Compares content, not timestamps (content hash is the source of truth)
- See `knowledge/operational-patterns/sync-protocol.md` for the full sync protocol
- Related command: `/context-sync` (pulls git activity; this checks extension alignment)

## See Also

- `knowledge/operational-patterns/sync-protocol.md` — Full sync protocol documentation
- `/commit-push-pr` — Deploy changes after fixing drift
- `/context-sync` — Pull recent activity into session context

---
description: Check for drift between CAB plugin extensions and deployed global (~/.claude/) extensions. Detects hash mismatches, content differences, and plugin↔global name-collision shadowing (LL-27).
allowed-tools: Read, Bash, Grep, Glob
---

# Sync Check

Detects drift between the CAB plugin (source of truth) and deployed global
extensions. Use after making changes in CAB to identify what needs redeployment,
or periodically to ensure global config stays aligned.

**Also detects plugin↔global name-collision shadowing** — the LL-27 failure
mode where a global `~/.claude/agents/<name>.md` silently overrides a
plugin-provided agent of the same name due to CC's resolution precedence
(`local → user → plugin`). Shadow detection fires regardless of content
delta — even byte-identical files create future-drift risk because the
global copy is frozen at a snapshot and won't receive plugin updates.

## Behavior

1. **Discover paired files**: Map CAB plugin extensions to their global equivalents:

   | CAB Location | Global Location |
   |-------------|----------------|
   | `agents/*.md` | `~/.claude/agents/*.md` |
   | `skills/*/SKILL.md` | `~/.claude/skills/*/SKILL.md` |
   | `commands/*.md` | `~/.claude/commands/*.md` |

2. **Compare each pair**:
   ```bash
   # For each paired file:
   diff <(cat "cab-path") <(cat "global-path")
   ```

3. **Plugin shadow scan (LL-27 enforcement)**: For each agent/skill/command
   defined by the CAB plugin (or any other enabled plugin when scope
   expanded), check whether a same-named file exists under
   `~/.claude/agents/`, `~/.claude/skills/<name>/SKILL.md`, or
   `~/.claude/commands/`. Any match is a SHADOW regardless of content:

   ```bash
   # Enumerate CAB plugin agent names
   for cab_agent in agents/*.md; do
     name=$(basename "$cab_agent")
     global="$HOME/.claude/agents/$name"
     if [ -f "$global" ]; then
       if cmp -s "$cab_agent" "$global"; then
         echo "SHADOW (byte-identical, future-drift risk): $name"
       else
         echo "SHADOW (content diverged, LL-27 active): $name"
       fi
     fi
   done
   # Repeat for skills/ and commands/
   ```

   Extension scope for other enabled plugins: read `~/.claude/settings.json`
   for `enabledPlugins`, walk each plugin's `agents/|skills/|commands/`
   directory, and repeat the same-name check. Narrow to CAB-only if
   enabledPlugins enumeration is unavailable in the current shell.

4. **Report results**:

   ```
   ── SYNC CHECK ─────────────────────────────────

   ✅ In sync (N files)
     agents/orchestrator.md
     agents/verifier.md
     ...

   ⚠️  Drift detected (N files)
     skills/analyze-architecture/SKILL.md
       CAB newer: 2026-04-05 | Global: 2026-04-03
       Lines changed: +12 -3
     commands/techdebt.md
       CAB newer: 2026-04-05 | Global: 2026-04-01
       Lines changed: +5 -2

   ⚠️  SHADOW DETECTED — LL-27 failure mode (N files)
     agents/orchestrator.md
       Plugin copy: <cab-root>/agents/orchestrator.md
       Shadow copy: ~/.claude/agents/orchestrator.md (byte-identical)
       Risk: global copy freezes at current snapshot; plugin updates silently blocked
     agents/verifier.md
       Plugin copy: <cab-root>/agents/verifier.md
       Shadow copy: ~/.claude/agents/verifier.md (content diverged)
       Risk: LL-27 already active — global override intentional? If not, remove shadow

   ❌ Missing from global (N files)
     skills/close-session/SKILL.md
     commands/sync-check.md

   ❌ Extra in global (not in CAB) (N files)
     skills/strategy-framework/SKILL.md

   ───────────────────────────────────────────────
   ```

5. **Recommend actions** based on drift + shadow findings:
   - Files where CAB is newer (no shadow) → "Deploy to global: `cp <cab-path> <global-path>`"
   - Files where global is newer (no shadow) → "Review: global has changes not in CAB. Merge or overwrite?"
   - **SHADOW — byte-identical** → "Remove global shadow: `rm <global-path>` — plugin version will take over and receive future updates"
   - **SHADOW — content diverged** → "Confirm intent: is the global override intentional and documented? If not, remove shadow + backport any wanted deltas into plugin. If yes, add documented rationale in CAB CLAUDE.md's Extension Registry (or the pending Plugin Hygiene Policy per UXL-025)"
   - Missing from global → "Deploy new extension"
   - Extra in global → "Not CAB-managed. Ignore or integrate into CAB?"

## Arguments

- No arguments: Full sync check (all extension types, drift + shadow)
- `agents`: Check only agents (drift + shadow)
- `skills`: Check only skills (drift + shadow)
- `commands`: Check only commands (drift + shadow)
- `--shadow-only`: Skip drift report, only scan for plugin↔global name collisions
- `--drift-only`: Skip shadow scan, legacy behavior

## Examples

```
/sync-check
→ Full report: drift + shadow across all extension types

/sync-check agents
→ Agents only: drift + shadow

/sync-check --shadow-only
→ LL-27 shadow scan only (fast; useful for periodic audit)

/sync-check agents --shadow-only
→ Check only agent name-collision shadows
```

## Notes

- Excludes `settings.local.json` and `CLAUDE.local.md` (personal, not synced)
- Compares content, not timestamps (content hash is the source of truth)
- **Shadow scan fires regardless of content delta** — byte-identical shadows still block future plugin updates (frozen-snapshot risk)
- See `knowledge/operational-patterns/sync-protocol.md` for the full sync protocol
- See `notes/lessons-learned.md` LL-27 for the failure mode this shadow scan enforces against
- Related command: `/context-sync` (pulls git activity; this checks extension alignment)

## See Also

- `knowledge/operational-patterns/sync-protocol.md` — Full sync protocol documentation
- LL-27 — plugin↔global name-collision shadowing (the failure mode this detects)
- `/commit-push-pr` — Deploy changes after fixing drift
- `/context-sync` — Pull recent activity into session context
- UXL-012 (tracker row, pending) — new KB card `knowledge/operational-patterns/multi-agent/agent-resolution.md` will document the full local → user → plugin precedence + shadowing patterns; this command's shadow scan will reference that card when it lands
- UXL-013 (tracker row, pending) — fold shadow scan into `/validate --cab-audit` methodology; audit agent dimension scoring will flag shadows even if this command hasn't been run

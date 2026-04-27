---
name: check-sync
description: >-
  Detect drift between CAB plugin extensions (source of truth) and deployed
  global ~/.claude/ extensions. Detects content mismatches, file-presence
  differences, AND plugin↔global name-collision shadowing (LL-27).
  Triggers: sync check, plugin drift, shadow scan, deploy alignment, before
  pushing CAB changes, after global config edits.
argument-hint: "Scope: agents/skills/commands; flags: --shadow-only, --drift-only"
allowed-tools: Read, Bash, Grep, Glob
---

# Plugin ↔ Global Sync Check

## Purpose

CAB's distributable plugin extensions can become out of sync with what's
actually deployed under `~/.claude/`. Two failure modes:

1. **Drift** — file content differs between plugin and global copy
   (one was updated, the other wasn't)
2. **Shadowing (LL-27)** — a same-named file exists at the higher-precedence
   global layer (`~/.claude/agents/<name>.md`), silently overriding the
   plugin's version due to CC's resolution order
   (`local → user → plugin`)

This skill detects both — even a byte-identical shadow is a future-drift
risk because the global copy is frozen at a snapshot and won't receive
plugin updates.

## When to Invoke

- After making changes to CAB plugin extensions, before pushing
- Periodically (weekly) as a hygiene check
- After editing `~/.claude/` directly, to catch accidental shadowing
- Before publishing a new CAB plugin version

## Protocol

### Step 1: Discover Paired Files

| CAB plugin location | Global equivalent |
|---|---|
| `agents/*.md` | `~/.claude/agents/*.md` |
| `skills/*/SKILL.md` | `~/.claude/skills/*/SKILL.md` |
| `commands/*.md` | `~/.claude/commands/*.md` |

If `$ARGUMENTS` is `agents`, `skills`, or `commands`, scope to that type.

### Step 2: Drift Comparison

```bash
for cab_path in <plugin>; do
  global_path="$HOME/.claude/<corresponding-path>"
  [ -f "$global_path" ] || continue
  diff -q "$cab_path" "$global_path" >/dev/null || echo "DRIFT: $cab_path"
done
```

Skip in `--shadow-only` mode.

### Step 3: Shadow Scan (LL-27 enforcement)

For each agent/skill/command in CAB plugin (or any other enabled plugin
when scope expanded), check whether a same-named file exists under
`~/.claude/`. **Any** match is a SHADOW regardless of content:

```bash
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

For other enabled plugins: read `~/.claude/settings.json` for
`enabledPlugins`, walk each plugin's extension directories, repeat the
same-name check. Narrow to CAB-only if enumeration is unavailable.

Skip in `--drift-only` mode (legacy behavior).

### Step 4: Report

```
── SYNC CHECK ─────────────────────────────────

✅ In sync (N files)
  agents/orchestrator.md
  ...

⚠️  Drift detected (N files)
  skills/analyze-architecture/SKILL.md
    CAB newer: 2026-04-25 | Global: 2026-04-22
    Lines changed: +12 -3

⚠️  SHADOW DETECTED — LL-27 (N files)
  agents/orchestrator.md
    Plugin copy: <cab-root>/agents/orchestrator.md
    Shadow copy: ~/.claude/agents/orchestrator.md (byte-identical)
    Risk: global copy frozen at snapshot; plugin updates silently blocked

❌ Missing from global (N files)
  skills/close-session/SKILL.md

❌ Extra in global (not in CAB) (N files)
  skills/strategy-framework/SKILL.md

───────────────────────────────────────────────
```

### Step 5: Recommend Actions

Per finding:

| Finding | Recommended action |
|---|---|
| CAB newer (no shadow) | `cp <cab-path> <global-path>` to deploy |
| Global newer (no shadow) | Review — global has changes not in CAB; merge or overwrite |
| **SHADOW byte-identical** | `rm <global-path>` — plugin version takes over, receives future updates |
| **SHADOW content diverged** | Confirm intent: documented override? If not, remove shadow + backport wanted deltas. If yes, document rationale in CAB CLAUDE.md Extension Registry |
| Missing from global | Deploy new extension if intended |
| Extra in global | Not CAB-managed; ignore or integrate into CAB |

## Arguments

- (none): full sync check (all extension types, drift + shadow)
- `agents` / `skills` / `commands`: scope to that type
- `--shadow-only`: skip drift report; LL-27 collision scan only
- `--drift-only`: skip shadow scan (legacy behavior)

## Verification

This skill is working correctly when:

- Both content drift AND name-collision shadowing are detected
  independently (one type of finding doesn't mask the other)
- Byte-identical shadows are still flagged (frozen-snapshot risk)
- Recommendations are file-specific and command-ready
  (`rm <exact-path>`, not "remove shadows")
- Excludes `settings.local.json` and `CLAUDE.local.md` (personal, not synced)

## Integration Points

- `commands/sync-check.md` — shim trigger preserving `/cab:sync-check`
- `audit-workspace` skill — folds shadow-scan into `/validate --cab-audit`
  (UXL-013 coupling)
- `knowledge/operational-patterns/multi-agent/agent-resolution.md` —
  full precedence + shadowing reference
- `notes/lessons-learned.md` LL-27 — failure mode this skill enforces against
- `commit-push-pr` skill — natural follow-on after fixing drift

## See Also

- `knowledge/operational-patterns/sync-protocol.md` — full sync protocol
- LL-27 — plugin↔global name-collision shadowing (root failure mode)

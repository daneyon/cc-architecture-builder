---
id: agent-resolution
title: Agent Resolution & Shadowing — Precedence, Detection, Remediation
category: operational-patterns/multi-agent
tags: [agent, resolution, precedence, shadowing, ll-27, scope, plugin, global]
summary: Canonical reference for CC agent/skill/command resolution precedence (local → user → plugin), the LL-27 shadowing failure mode, detection patterns (via /sync-check + /validate --cab-audit), and remediation patterns (remove shadow vs document intentional override). Authoritative anchor for UXL-011 (sync-check shadow scan) and UXL-013 (audit fold-in).
depends_on: [collaboration-patterns]
related: [agent-teams, worktree-workflows]
complexity: intermediate
last_updated: 2026-04-22
estimated_tokens: 1600
source: https://code.claude.com/docs/en/sub-agents#choose-the-subagent-scope (fetched 2026-04-22 for precedence order); LL-27 (CAB notes/lessons-learned.md) for historical failure case; UXL-012 deliverable in impl-plan-ux-log-tracker-2026-04-22.md
confidence: A
review_by: 2026-07-22
---

# Agent Resolution & Shadowing

> Canonical reference for the precedence rules that determine which
> definition of an agent/skill/command a CC session actually uses, the
> failure mode this enables (LL-27 shadowing), and how CAB tooling detects
> and remediates it.

## Resolution Precedence (agents + skills + commands)

Per current CC docs, when multiple definitions share the same name, the
higher-priority location wins:

| Priority | Location | Scope | Notes |
|---|---|---|---|
| 1 (highest) | Managed settings | Organization-wide | Deployed via managed settings directory (`/Library/.../ClaudeCode/agents/*.md` etc.) |
| 2 | `--agents` / `--skills` CLI flag | Current session | JSON-passed; ephemeral; not on disk |
| 3 | `.claude/agents/` + `.claude/skills/` + `.claude/commands/` | Current project | Walked up from working directory |
| 4 | `~/.claude/agents/` + `~/.claude/skills/` + `~/.claude/commands/` | User global | Personal across all projects |
| 5 (lowest) | Plugin `agents/` + `skills/` + `commands/` | Where plugin is enabled | Shipped via installed plugins |

**Key implication**: plugins are LOWEST priority. A same-named file at any
higher priority silently overrides the plugin definition.

## The LL-27 Shadowing Failure Mode

**Symptom**: a plugin-provided agent stops reflecting plugin updates. The
session uses a frozen snapshot at a higher-priority scope instead.

**Mechanism**: a user (or past Claude session) copies a plugin agent to
`~/.claude/agents/<name>.md` — either for inspection, local editing, or
as an artifact of setup tooling. CC's precedence now picks the global
copy. Plugin updates to the authoritative version never take effect in
runtime. The session behaves per the frozen snapshot until someone
notices.

**Why it's insidious**:
- Silent — no error, warning, or log entry at load time.
- Byte-identical shadows are equally damaging — they freeze at the current
  snapshot the same way diverged ones do. Content parity at copy-time
  doesn't prevent future drift.
- Detection requires comparing names across scopes, not just paths or
  content — existing "in sync" diff-based checks miss the whole class.

**Historical incident**: LL-27 was logged after CAB's own `orchestrator`
agent accidentally existed in both `~/.claude/agents/orchestrator.md` and
the CAB plugin's `agents/orchestrator.md`. Session used global copy;
plugin updates silently blocked.

## Detection Patterns

### Per-invocation: `/cab:sync-check` (shadow scan)

Extended in UXL-011 (commit 2185da9). For each agent/skill/command in the
CAB plugin, checks whether a same-named file exists at
`~/.claude/agents/`, `~/.claude/skills/<name>/SKILL.md`, or
`~/.claude/commands/`. Emits SHADOW warning regardless of content parity.

Bash pattern:

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
```

See [commands/sync-check.md](../../../commands/sync-check.md) for the full
command spec including `--shadow-only` flag for fast periodic audit.

### Periodic audit: `/validate --cab-audit` (UXL-013 fold-in)

The Agent Frontmatter dimension in `skills/auditing-workspace/SKILL.md`
absorbs the shadow scan as part of agent-dimension scoring (UXL-013).
Findings fold into the audit's overall score: a plugin project with
unresolved shadows cannot reach EXEMPLARY on Agent Frontmatter dimension
regardless of per-file frontmatter quality.

### Build-time: pre-push hook (not yet shipped)

Candidate follow-on: add to `hooks/scripts/pre-push-state-review.sh` a
quick shadow check before push that would block merges introducing new
shadows. Tracked as potential UXL-011-adjacent row if pattern matures.

## Remediation Patterns

### Pattern 1 — Byte-identical shadow

**Cause**: copy-pasted for local inspection, no intent to override.

**Fix**:
```bash
rm ~/.claude/agents/<name>.md
# plugin version takes over immediately; future plugin updates flow
```

**Verification**: re-run `/cab:sync-check --shadow-only` — shadow warning
should clear.

### Pattern 2 — Content-diverged shadow (unintentional)

**Cause**: past edit to global copy as a "quick fix" that never propagated
back to CAB.

**Fix**:
1. Diff the two files to identify deltas:
   ```bash
   diff ~/.claude/agents/<name>.md agents/<name>.md
   ```
2. Backport wanted deltas into the CAB plugin version.
3. Commit the backport via `/commit-push-pr` (or manual).
4. Remove the global shadow.

### Pattern 3 — Content-diverged shadow (intentional override)

**Cause**: genuine need for a local/personal override — e.g., user wants
a different model for a specific agent.

**Fix**: document the override explicitly.

Per UXL-025 Global CLAUDE.md v2 (when it lands): add the override
rationale to the pending Plugin Hygiene Policy block. Until then: comment
block at the top of the override file citing:
- Source plugin + upstream version
- Reason for override
- Sunset condition (when to remove and re-sync)

```markdown
---
name: verifier
...
---
<!-- OVERRIDE: plugin version adds verbose tracing that breaks CI logs.
     Reverted to pre-tracing behavior pending plugin fix (upstream: CAB/
     plugin 1.2.0 → downgrade to 1.1.3 semantics). Sunset when CAB issue
     #NN resolves. -->
```

Without this provenance, future audits can't distinguish intentional
override from forgotten shadow.

## Anti-Patterns

- **Copying plugin agents for "safe keeping"** — creates byte-identical
  shadow; blocks future plugin updates silently.
- **Global-deploy CAB-owned commands** — e.g., running `cp commands/sync-check.md ~/.claude/commands/`
  creates exactly the shadow this command detects. CAB commands should be
  invoked via namespaced `/cab:sync-check`, not deployed globally.
- **Running `/sync-check` without `--shadow-only` during periodic audit** —
  full drift scan is slow when you only need to check shadows. Use the
  flag for fast periodic checks.
- **Trusting "in sync" reports without shadow scan** — the old sync-check
  categorized byte-identical shadows as "in sync" (content parity) while
  missing the LL-27 failure mode entirely.

## Related

- LL-27 (`notes/lessons-learned.md`) — origin incident
- [commands/sync-check.md](../../../commands/sync-check.md) — user-triggered shadow detection (UXL-011)
- [skills/auditing-workspace/SKILL.md](../../../skills/auditing-workspace/SKILL.md) — automated shadow scan during `/validate --cab-audit` (UXL-013)
- [collaboration-patterns.md](collaboration-patterns.md) — multi-agent coordination context
- UXL-025 (tracker row) — Global CLAUDE.md v2; pending Plugin Hygiene Policy will formalize override documentation convention

---
name: pre-push-state-review
description: >-
  Review notes/ state artifacts before git push to catch in-dev drafts, private
  content, or unintended publication of state files. Triggers: before pushing,
  pre-push check, about to sync, publishing state, ready to push.
argument-hint: "Optional: specific files or directories to focus review on"
allowed-tools: Read, Grep, Glob, Bash
effort: low
---

# Pre-Push State Review Protocol

## Overview

This skill is the semantic review layer of CAB's two-layer pre-push protection
(LL-25). The hook layer (`hooks/pre-push-state-review.json`) catches obvious
draft markers deterministically; this skill handles the judgment calls —
scanning `notes/` for in-dev artifacts, private content, and publication-sensitive
material before `git push`.

## When to Invoke

- User mentions pushing, syncing, or publishing (any project with tracked `notes/`)
- After the pre-push hook flags draft markers (hook fires skill with flagged file list)
- User explicitly requests a pre-push review
- Before any `git push` on a branch that has `notes/` changes

## Relationship to Hook Layer

CAB's pre-push protection is two-layer by design (LL-25):

| Layer | Type | Speed | Coverage | Failure mode |
|-------|------|-------|----------|--------------|
| Hook | Deterministic regex gate | Fast (ms) | Draft markers (`WIP`, `DRAFT`, `PRIVATE`, `TODO:redact`, `NOCOMMIT`) | Misses semantic drafts without markers |
| Skill (this) | Semantic review | Slower (model call) | Intent, context, sensitivity | Requires invocation |

The hook catches accidents. This skill catches judgment calls.

## Protocol

### Step 1: Identify Changed `notes/` Files

```bash
# Files changed on current branch vs default branch
git diff --name-only origin/main...HEAD | grep '^notes/'

# Or, files staged for the next commit
git diff --cached --name-only | grep '^notes/'
```

If no `notes/` files changed, report "no state files to review" and exit.

### Step 2: Scan for Draft Markers (Belt-and-Suspenders)

Even though the hook runs first, repeat the scan here — the hook may have been
bypassed, or this skill may be invoked without a push in flight.

Draft markers to flag:

| Marker | Signal |
|--------|--------|
| `WIP` | Work in progress, not ready |
| `DRAFT` | Explicit draft status |
| `PRIVATE` | Content not for sharing |
| `TODO:redact` | Scheduled for scrubbing |
| `NOCOMMIT` | Explicit commit block |
| `FIXME:private` | Private fix notes |
| `<!--private-->` | HTML-commented private content |

```bash
grep -rEn '\b(WIP|DRAFT|PRIVATE|NOCOMMIT|TODO:redact|FIXME:private)\b' notes/ 2>/dev/null
```

### Step 3: Semantic Review

For each changed file, ask:

1. **Intent alignment** — Does the content match what the filename suggests? (e.g., `progress.md` should be session state, not private strategy notes)
2. **Sensitivity scan** — Are there credentials, API keys, paths with usernames, or URLs that shouldn't be public?
3. **Maturity check** — Is this content ready for collaborators/public review, or does it need refinement first?
4. **Context integrity** — Does the content make sense without the full conversation that produced it? Would a stranger understand it?
5. **Archive candidate** — Should this file be moved to `notes/_archive/` instead of pushed? (Retroactive scrub escape hatch)

### Step 4: Present Findings

Structured report for the user:

```markdown
## Pre-Push State Review Report

**Files scanned**: [N files in notes/]
**Draft markers found**: [list with line refs or "none"]
**Sensitivity concerns**: [credentials/paths/urls or "none"]
**Maturity concerns**: [files that feel unfinished or "none"]
**Archive candidates**: [files that should be moved to _archive/ or "none"]

### Recommendation
- [ ] Proceed with push (all checks passed)
- [ ] Archive [file] to notes/_archive/ first
- [ ] Resolve [marker] in [file:line] first
- [ ] Review [file] for [concern] before pushing
```

### Step 5: Escape Hatch — Archive Move

If files should NOT be published:

```bash
mkdir -p notes/_archive/
git mv notes/<file> notes/_archive/
git commit -m "chore: archive <file> (pre-push review, LL-25)"
```

`notes/_archive/` is gitignored, so moving files into it makes them disappear
from git tracking going forward. Historical commits still contain the old path
content — for true scrub, use `git filter-repo` (requires explicit user intent).

## Integration Points

- **filesystem-patterns.md** — Git Tracking Policy section documents the full protocol
- **LL-25** — The lesson that motivated this skill
- **hooks/pre-push-state-review.json** — The deterministic gate layer
- **session-close skill** — Runs after each session; state is curated before push

## Verification

This skill is working correctly when:

1. Pre-push runs on every push-related user intent
2. Draft markers are caught before publication
3. Users receive structured recommendations, not vague warnings
4. `_archive/` escape hatch is suggested when appropriate
5. No false positives on legitimate state file updates (progress.md, TODO.md routine updates)

## See Also

- [filesystem-patterns.md](../../knowledge/operational-patterns/state-management/filesystem-patterns.md) — Full state management policy
- [session-close](../session-close/SKILL.md) — Session state persistence (runs before pre-push review)
- `lessons-learned.md` LL-25 — Rationale and multi-archetype justification

---
id: team-collaboration
title: Team Collaboration Patterns
category: operational-patterns
tags: [collaboration, worktree, handoff, conflict, merge, review, delegation, teams]
summary: Protocols for multi-human and multi-agent team collaboration — conflict management, handoff procedures, worktree lifecycle, PR review workflows, and cross-worktree synchronization.
depends_on: [git-worktree, multi-agent-collaboration, orchestration-framework]
related: [session-management, extension-discovery]
complexity: advanced
last_updated: 2026-03-28
estimated_tokens: 2200
revision_note: "v1.0 — Fills critical gaps: conflict zone management, human-agent handoff, worktree close-out, cross-worktree sync. Derived from real-world HydroCast parallel worktree session."
---

# Team Collaboration Patterns

## Overview

This document covers the **collaboration layer** — what happens when multiple humans and/or CC agents work on the same project simultaneously. It extends the foundational patterns in `git-worktree.md` and `multi-agent-collaboration.md` with protocols for conflict management, handoff, review, and lifecycle cleanup.

**Prerequisite reading**: `orchestration-framework.md` (task execution protocol), `git-worktree.md` (worktree basics), `multi-agent-collaboration.md` (coordination patterns).

## Core Principle: One Worktree Per Task, Then Delete

```
CREATE worktree → WORK on branch → PR → MERGE → REMOVE worktree
```

Worktrees are **ephemeral task containers**, not persistent workspaces. Each task gets a fresh worktree branched from the latest main. When the task is complete and merged, the worktree is destroyed.

| Approach | When to Use |
|----------|-------------|
| New worktree per task | **Default** — clean isolation, no stale state |
| Reuse worktree | Never recommended — stale files, cross-task contamination |
| Long-lived analysis worktree | Read-only investigation only (never merges back) |

---

## Conflict Zone Management

### Prevention: File Ownership Declarations

When parallel work is active, each worktree's `notes/current-task.md` MUST declare owned files:

```markdown
### Conflict Zones
| File | Owner | Status |
|------|-------|--------|
| src/ingestion/mrms_downloader.py | This worktree | Active — do not touch |
| src/pipeline.py | Main workspace | Frozen for this worktree |
| .claude/skills/data-ingest/ | Deferred | No changes until task merges |
```

**Rules**:
- A file can have exactly ONE active owner across all worktrees
- Frozen files may be read but not modified
- Deferred files are acknowledged future work — not blocked, just sequenced
- The orchestrator (main workspace) is the authority for ownership disputes

### Detection: Early Conflict Signals

Before starting work in a new worktree, check for overlap:

```bash
# From main workspace: see what files each branch touches
git diff --name-only main...feat/branch-a
git diff --name-only main...feat/branch-b
# Any files appearing in both lists = conflict zone
comm -12 <(git diff --name-only main...feat/branch-a | sort) \
         <(git diff --name-only main...feat/branch-b | sort)
```

### Resolution: When Conflicts Occur

| Severity | Scenario | Resolution |
|----------|----------|------------|
| Low | Formatting-only overlap (ruff, linting) | Accept either — no semantic conflict |
| Medium | Both modified same file, different sections | Git auto-merge usually handles this |
| High | Both modified same function/logic | **Human decision required** — escalate |
| Critical | Architectural disagreement (incompatible designs) | Pause both, design review, pick one approach |

**Escalation path**: Worker detects conflict → documents in PR → tags orchestrator → orchestrator decides resolution → losing branch rebases or cherry-picks.

---

## Human-Agent Handoff Protocol

### Agent → Human (Work Complete)

When an agent (CC session) completes a task:

1. **Commit all work** — nothing uncommitted
2. **Push to remote** — `git push -u origin feat/{branch}`
3. **Create PR** — with summary, validation evidence, test results
4. **Update `notes/current-task.md`** — mark phase complete, document next steps
5. **Write phase summary** — what was done, what was decided, what's deferred

The PR is the handoff artifact. The human reviews asynchronously.

### Human → Agent (Feedback Loop)

When a human reviews and wants changes:

| Feedback Channel | How Agent Picks It Up |
|------------------|-----------------------|
| PR comments on GitHub | Agent reads via `gh pr view {N} --comments` |
| Updated `notes/current-task.md` | Agent reads on session start (cold-start anchor) |
| Direct prompt in new session | Human pastes feedback or says "read PR #N comments" |
| CLAUDE.md learned corrections | Agent reads automatically on every session |

**Recommended flow**: Human adds PR review comments → starts new CC session in same worktree → tells agent "address PR feedback on #{N}" → agent reads comments, makes changes, pushes.

### Human → Agent (New Task Delegation)

When delegating a new task to a human or CC agent:

1. **Create the worktree**: `git worktree add ../ProjectName-{task} -b feat/{task}`
2. **Write `notes/current-task.md`** in the worktree with:
   - Task description and acceptance criteria
   - Key files and references
   - Conflict zones (what's frozen, what's theirs)
   - Relevant decision context (why this approach, not alternatives)
3. **Communicate the assignment**: share worktree path + branch name
4. **Worker opens worktree**, reads `notes/current-task.md`, begins work

---

## Worktree Lifecycle: Complete Close-Out Procedure

### Pre-Close Checklist

Before removing a worktree, verify:

- [ ] All work committed (`git status` — clean working tree)
- [ ] Pushed to remote (`git push`)
- [ ] PR created and merged (or decision to abandon documented)
- [ ] Local-only files preserved (untracked data, references, downloaded artifacts)
- [ ] `notes/current-task.md` updated with completion summary
- [ ] Learned corrections added to project CLAUDE.md (if applicable)
- [ ] Main workspace pulled merged changes (`git pull origin main`)

### Close-Out Commands

```bash
# 1. From MAIN workspace (not the worktree being removed):
cd /path/to/main/repo

# 2. Pull the merged work
git pull origin main

# 3. Close all editors/terminals pointing at the worktree

# 4. Remove the worktree
git worktree remove --force /path/to/worktree
# If permission denied: close VS Code/editors first, then retry
# Fallback: rm -rf /path/to/worktree && git worktree prune

# 5. Delete the local branch (remote branch deleted by PR merge)
git branch -d feat/{task-name}

# 6. Verify clean state
git worktree list   # should show only main
git branch          # feature branch should be gone
```

### Preserving Local-Only Artifacts

Worktrees may contain untracked files that shouldn't be lost:

| Artifact Type | Action Before Removal |
|---------------|----------------------|
| Downloaded data (`data/`) | Copy to main workspace if needed for future tasks |
| Reference files (`refs/`) | Copy to main workspace `references/` directory |
| Temp analysis outputs | Discard — reproducible from code |
| Session notes | Already in git via `notes/` — preserved by merge |

---

## Cross-Worktree Synchronization

### When to Sync

| Signal | Action |
|--------|--------|
| Main has new commits from another merged PR | Pull into worktree: `git merge main` or `git rebase main` |
| Worktree depends on another worktree's output | Wait for that PR to merge first, then pull |
| Divergence > 1 week | Rebase onto main to avoid large merge conflicts |
| Worktree is read-only (analysis) | Pull main periodically to stay current |

### Merge Strategy

```bash
# From the active worktree:
git fetch origin main
git merge origin/main    # Preferred — preserves history
# OR
git rebase origin/main   # Cleaner history but rewrites commits
```

**Rule**: Use `merge` for worktrees with shared/reviewed commits. Use `rebase` for local-only work that hasn't been pushed.

### Preventing Drift

- **Short-lived branches**: Merge within days, not weeks
- **Small PRs**: One task per PR, not feature bundles
- **Daily sync**: `git fetch origin` at session start to detect divergence early
- **Independent files**: Design task boundaries around file ownership, not feature scope

---

## Delegation Patterns

### Orchestrator → Specialist Routing

The orchestrator (human or agent in main workspace) classifies and delegates:

```
Task received
    │
    ├─ Single-domain, clear scope    → Create worktree, assign to specialist
    ├─ Cross-domain, decomposable    → Split into subtasks, one worktree each
    ├─ Ambiguous scope               → Clarify with requester before delegating
    └─ Quick/trivial                  → Execute directly in main workspace
```

### Task Assignment Template

When creating a worktree for delegation, the `notes/current-task.md` should include:

```markdown
# {Task Name} — Current Task

**Task:** {1-sentence description}
**Phase:** PLAN (or EXECUTE if pre-planned)
**Branch:** `feat/{task-name}`
**Assigned to:** {human name or "CC agent"}
**Created by:** {orchestrator}
**Date:** {YYYY-MM-DD}

## Acceptance Criteria
- [ ] {Specific, testable criterion 1}
- [ ] {Specific, testable criterion 2}

## Scope
### In Scope
- {What this task covers}

### Out of Scope
- {What this task explicitly does NOT cover}

## Key Files
- `src/path/to/main_file.py` — primary deliverable
- `references/relevant_doc.md` — context

## Conflict Zones
| File | Owner | Status |
|------|-------|--------|
| ... | ... | ... |

## Context
{Why this task exists, relevant decisions, links to prior work}
```

### Parallel Delegation

When delegating multiple tasks simultaneously:

1. Create all worktrees from the same base commit on main
2. Ensure file ownership is non-overlapping across all worktrees
3. Document all active worktrees in `notes/progress.md` on main
4. Merge completed work sequentially (first-done merges first, others rebase)

---

## PR Review Workflow

### Standard Flow

```
Worker commits + pushes → Creates PR → Orchestrator reviews
    │                                        │
    │                                   ┌────┴────┐
    │                                   │ APPROVE  │──→ Merge + close worktree
    │                                   ├──────────┤
    │                                   │ CHANGES  │──→ Worker addresses feedback
    │                                   │ REQUESTED│    (new commits, re-push)
    │                                   ├──────────┤
    │                                   │ ABANDON  │──→ Close PR, remove worktree
    │                                   └──────────┘    document why in notes/
```

### PR Content Requirements

Every PR should include:
- **Summary**: What changed and why (not a file list — the diff shows that)
- **Validation evidence**: Test results, download counts, comparison data
- **Limitations**: Known gaps, deferred items, edge cases not covered
- **Test plan**: How to verify the changes work

### CC Agent as PR Author

When a CC agent creates a PR (via `/commit-push-pr` or `gh pr create`):
- The agent writes the PR body with validation evidence
- The human orchestrator reviews before merging
- If changes needed: human comments on PR, starts new CC session, agent reads comments

---

## State Management Across Worktrees

### What Lives Where

| State | Location | Persists Across |
|-------|----------|-----------------|
| Task scope, acceptance criteria | `notes/current-task.md` | Sessions (via git) |
| Project backlog, decision log | `notes/progress.md` | Sessions + merges |
| Extension awareness | CLAUDE.md + `rules/capabilities.md` | All sessions |
| Learned corrections | CLAUDE.md "Learned Corrections" section | All sessions |
| Downloaded data, model artifacts | `data/`, `models/` (gitignored) | Single worktree only |
| Session transcript | `~/.claude/projects/` (auto-managed) | `claude --continue` |

### Cross-Worktree State Sync

Worktrees share the git object database but NOT the working directory. State synchronization happens through:

1. **Git commits** — the primary sync mechanism (merge/rebase)
2. **GitHub PRs** — async review and feedback
3. **`/context-sync` command** — pulls recent git log + open PRs into session context
4. **`notes/` directory** — human-readable state that any session can read

### Post-Merge State Cleanup

After merging a worktree's PR into main:
1. Update `notes/progress.md` on main to mark the task complete
2. Update `notes/current-task.md` on main to reflect new active work
3. If the completed task produced learned corrections → add to CLAUDE.md
4. If the completed task changed CC extensions → verify they work in main workspace

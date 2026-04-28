---
name: recover-session
description: >-
  Reconstruct session context after mid-dialogue death (compaction crash,
  force-close, dropped connection, hung process). Bootstraps from notes/
  first, identifies the dying-session JSONL transcript, extracts last N
  turns, synthesizes coverage gap vs current state files, backfills
  discoveries into LL/state, and resumes at the exact HITL question.
  Triggers: session crashed, lost context, force-compact recovery, dying
  session, transcript recovery, recover from compaction.
argument-hint: "Optional: dying session UUID or absolute transcript path; default = latest non-current jsonl in this project"
allowed-tools: Read, Bash, Grep, Glob, Edit, Write
---

# Recover Session — Mid-Dialogue Death Recovery Protocol

## Purpose

Mid-session deaths happen — compaction crashes, force-closes, dropped
connections, hung processes, runaway loops abandoned. The standard
3-file bootstrap cascade (`current-task.md` → `progress.md` → `TODO.md`)
recovers *committed* state, but in-flight discoveries between the last
state-refresh commit and the death are unrecoverable from `notes/` alone.

This skill closes that gap by combining the bootstrap cascade with the
dying-session JSONL transcript — extracting the in-flight signal,
classifying it (decision / artifact-pending / new lesson / open
question), and merging it into durable artifacts before resuming work.

Codifies the Session 27 recovery method (LL-28). Session 27 itself is the
canonical validation dataset.

## When to Invoke

- After a session terminates abnormally (crash, force-close, network drop)
  while substantive work was in flight
- When the standard bootstrap cascade returns state that feels incomplete
  ("we definitely discussed X but it's nowhere in `progress.md`")
- After auto-compact triggered mid-decision and the compaction context-map
  doesn't preserve the decision rationale
- Periodically as a hygiene check if you suspect drift between state files
  and what actually happened in recent sessions

## Protocol

### Step 1: Standard Bootstrap First

Run the normal 3-file cascade. This is the trusted-but-incomplete baseline:

```
Read(notes/current-task.md)            # full file
Read(notes/progress.md, limit=100)     # top T1 section
Read(notes/TODO.md, limit=80)          # top section
```

Note the latest commit hash referenced in `current-task.md`. **The gap**
to recover = whatever happened *after* that commit and *before* the
session died.

### Step 2: Locate the Dying-Session JSONL Transcript

Transcripts live at `~/.claude/projects/<project-path-encoded>/<session-uuid>.jsonl`.

Path-encoding rule (Windows): drive letter lowercase + `--` + remaining
path with `\` replaced by `-`. Example:

- Project: `c:\Users\daniel.kang\Desktop\Automoto\cc-architecture-builder`
- Encoded: `c--Users-daniel-kang-Desktop-Automoto-cc-architecture-builder`
- Transcript dir: `~/.claude/projects/c--Users-daniel-kang-Desktop-Automoto-cc-architecture-builder/`

```bash
# List all transcripts for this project, newest first
PROJECT_HASH=$(pwd | sed 's|^/c|c-|; s|/|-|g; s|^c-|c--|')
TRANSCRIPT_DIR="$HOME/.claude/projects/$PROJECT_HASH"
ls -t "$TRANSCRIPT_DIR"/*.jsonl 2>/dev/null | head -10
```

If `$ARGUMENTS` provided a session UUID or absolute path, use that
directly. Otherwise: the dying-session transcript is the **most recent
.jsonl that is NOT the current session** (skip the active session's UUID,
which the runtime locks).

### Step 3: Extract Last N Turns

Default N = 30 turns (covers ~last 15 user/assistant exchanges). Adjust
based on how long the session ran before death:

```bash
DYING_TRANSCRIPT="<path-from-step-2>"
# JSONL is one event per line; filter to user/assistant turns; tail -N
grep -E '"type":"(user|assistant)"' "$DYING_TRANSCRIPT" | tail -30
```

For richer extraction (tool use, file edits, decision-bearing thinking):

```bash
# Pull last 100 events of any type for full context
tail -100 "$DYING_TRANSCRIPT"
```

### Step 4: Synthesize Coverage Gap

For each discovery / decision / artifact-pending found in Step 3, classify
against current state files (Step 1):

| Signal in transcript | Already in state? | Action |
|---|---|---|
| New architectural decision | NO | Add to `progress.md` session entry + (if cross-project) LL candidate |
| File edit / commit not in git log | NO | Re-stage + commit with reconstructed message |
| HITL question pending answer | depends | Re-pose to user as the resume point |
| New LL implication discovered | NO | Add to `lessons-learned.md` Pending section |
| Plan refinement mid-flight | maybe | Update `current-task.md` or relevant impl-plan |
| Tool-use side effect (created/modified file) | filesystem check | `git status` reveals; commit or revert based on intent |

Filesystem reality check:

```bash
git status --short          # uncommitted intent from dying session
git diff                    # actual content
git log --oneline -5        # last few commits — confirm gap boundary
```

### Step 5: Backfill Durable Artifacts

Apply classified findings:

- **State files** (`progress.md`, `current-task.md`, `TODO.md`): append
  recovered narrative to top of progress.md as a "Session N (recovery)"
  entry; refresh current-task.md if next-step pickup changed
- **LL entries** (`lessons-learned.md`): add new entries under Pending or
  appropriate Class section; cite recovered evidence
- **Filesystem mutations** (uncommitted edits): review `git diff`, decide
  per-file whether to commit (work was good) or revert (work was
  incomplete/wrong); use `git stash` if uncertain
- **Auto-memory** (`memory/`): if recovered signal is durable +
  cross-project, add to MEMORY.md index

### Step 6: Resume at HITL Question

If the dying session was paused at a user question (HITL gate), re-pose
that question now to the user with full reconstructed context:

> "We were here before the session died: [summary]. The pending question
> was: [question]. Recovered context now in notes/ + lessons-learned.md.
> How would you like to proceed?"

If no HITL gate was pending, summarize recovery findings and offer the
top 1-3 candidate next actions based on reconstructed state.

## Verification

This skill is working correctly when:

- Standard bootstrap runs FIRST (no skipping; transcript is gap-filler not
  primary source)
- Dying-session transcript is correctly identified (not the active
  session's transcript — that file is locked + shouldn't be needed)
- Coverage gap is explicit (exact list of discoveries/decisions to
  backfill, not vague "some things happened")
- Filesystem mutations are reviewed before commit/revert (no blind
  `git add .`; LL-25 + security rules apply)
- Resume point is concrete (specific HITL question OR specific next-action
  recommendation, not "let me know what you want to do")

## Integration Points

- **`notes/lessons-learned.md` LL-28** — codifies dying-session recovery as
  a durable lesson; this skill is the operational embodiment
- **`knowledge/operational-patterns/state-management/filesystem-patterns.md`**
  — Lessons-Referenced Protocols section cross-links here
- **3-file bootstrap cascade** (`bootstrap-read-pattern.md`) — Step 1 of
  this protocol
- **`execute-task` skill** — natural follow-on once recovery completes;
  resume the protocol from PLAN/EXECUTE phase as appropriate
- **UXL-016 (parked)** — event-triggered state-write protocol; once this
  skill survives one real recovery cycle, UXL-016's design can proceed
  with empirical validation data

## Limitations

- Active-session transcript is locked by the CC runtime; this skill cannot
  recover from a session that hasn't terminated yet (use `/compact` +
  state-refresh while still alive)
- JSONL transcripts may be truncated or corrupted in extreme crash
  scenarios; if `tail` returns garbage, fall back to bootstrap-only
  recovery and accept the gap
- Filesystem mutations from the dying session that were NOT visible to git
  (e.g., environment variables, external API state) can't be recovered
  from transcript alone

## See Also

- `notes/lessons-learned.md` LL-28 — dying-session recovery lesson
- `knowledge/operational-patterns/state-management/filesystem-patterns.md`
  — Git Tracking Policy + state-mgmt protocols
- `knowledge/operational-patterns/state-management/bootstrap-read-pattern.md`
  — 3-file cascade spec
- `notes/_archive/session-28-recovery-2026-04-11.md` — historical recovery
  artifact (Session 27/28); content abstracted here + into LL-28

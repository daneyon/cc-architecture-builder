# UX Log + Ideabox Tracker — Guide

> Companion to `notes/ux-log-template.csv`, `notes/ux-log-examples.csv`, and
> active pass files `notes/ux-log-NNN-YYYY-MM-DD-pass-N.csv`. The tracker
> centralizes UX/ideation/friction observations across 5 surfaces
> (gui / cli / agentic / integration / meta) with programmatic state-linkage
> to plans, commits, and lessons-learned.

## Quick Reference — What Goes Where

- **Raw observation** → append row to active pass CSV with T1 columns filled
- **Framework questions** → `knowledge/reference/prioritization-frameworks.md`
  and `knowledge/reference/ux-testing-agentic-os.md`
- **Full 25-column schema definition** → `notes/impl-plan-ux-log-tracker-2026-04-22.md` Appendix B
- **Examples** → `notes/ux-log-examples.csv` (1+ row per surface)

## Tier Hierarchy — Fill-Cost Structure

The 25 columns split into 7 tiers by fill cost and authority. Most
day-to-day capture needs only T1.

| Tier | Who fills | Cols | Cost |
|---|---|---|---|
| **T1** Braindump minimum | User (or capturer subagent from dialogue) | `surface`, `category`, `title`, `user_comment` (+ `id` auto T2) | 30 sec |
| **T2** Intake auto | Hook / shell ergonomics | `id`, `pass`, `date`, `reviewer` | 0 |
| **T3** Intake normalization | Orchestrator / capturer subagent | `component`, `lifecycle_stage`, `severity` | 2 min |
| **T4** Strongly recommended | Orchestrator at triage (or user at log) | `observed`, `expected`, `evidence`, `value`, `effort`, `orchestrator_take` | 3-5 min |
| **T5** Triage synthesis | Orchestrator at triage | `framework_anchor`, `kano`, `rice_score`, `downstream_target` | 3-5 min |
| **T6** Promotion | Orchestrator at release-batching | `moscow` | per release |
| **T7** Lifecycle auto | Hook (`ux-log-sync.sh`) | `linked_plan`, `linked_commit`, `status` | 0 |

**KG-critical subset** (needed for programmatic orchestration):
`id` / `surface` / `lifecycle_stage` / `status` / `downstream_target` /
`linked_plan` / `linked_commit`. User-fill burden for KG participation = 1
column (`surface`).

## Column Cheat Sheets

### `surface` (T1, required, KG)
`gui` / `cli` / `agentic` / `integration` / `meta` — see plan Appendix B for
surface-to-component picklists.

### `category` (T1, required)
`bug` (broken; expected behavior absent) / `gap` (missing capability) /
`idea` (potential enhancement) / `question` (ambiguity needing resolution) /
`drift` (deviation from existing spec/convention).

### `severity` (T3, required)
`BLOCKER` (can't proceed) / `MAJOR` (significant friction) / `MINOR` (minor
friction) / `QUESTION` / `IDEA`. Reflects impact-if-unaddressed only.

### `lifecycle_stage` (T3, required, KG)
`context-of-use` (observed behavior) / `requirements` (spec correctness) /
`design` (solution quality) / `evaluation` (verification). ISO 9241-210.

### `value` + `effort` (T4)
L / M / H each. Subjective log-time estimate. See prioritization-frameworks
KB card, Tier 1 section.

### `framework_anchor` (T5)
Surface-conditional vocabulary — see ux-testing-agentic-os.md:
- `gui` → `H1..H10`, `WCAG-X.X.X`, `SH1..SH8`
- `cli` → `ISO-usability`, `ISO-maintainability`, `ISO-reliability`, ...
- `agentic`/`integration`/`meta` → `DP1..DP9`, `LL-NN`, `CC-<docs-anchor>`

### `kano` (T5, UX-surfaces only)
`basic` / `performance` / `delight`. Leave blank for infra/architecture rows.

### `rice_score` (T5, conditional)
Numeric — fill only when ≥3 comparable peers exist in same surface/category.

### `moscow` (T6, per-release only)
`M` / `S` / `C` / `W`. Re-evaluate each release; never treat as row-intrinsic.

### `downstream_target` (T5, KG)
`LL` (promote to lessons-learned) / `KB` (new/update KB card) / `rule`
(update .claude/rules/) / `skill` / `hook` / `TODO` (active backlog) /
`progress` (log to progress.md) / `followup` (deferred, revisit).

### `user_comment` (T1, required)
**VERBATIM** for user-originated rows — never paraphrase, condense, or
reformat. `orchestrator_take` is the place for synthesis.

### `status` (T7, auto)
State machine — see §Status State Machine below.

## Workflows

### Log Workflow (user raw entry OR capturer subagent)

1. Open active pass file (`ux-log-NNN-YYYY-MM-DD-pass-N.csv`)
2. Append row with T1 fields: `surface`, `category`, `title`, `user_comment`
3. (Optional) fill T4 fields if readily known: `observed`, `expected`,
   `evidence`, `value`, `effort`
4. Leave T3/T5/T6/T7 empty — orchestrator / hook fills later
5. Save; commit with message like `log(ux-log): UXL-NNN — <title>`

**Verbatim rule**: if capturer subagent is parsing NL dialogue, the source
phrase goes into `user_comment` unchanged. Synthesis goes into
`orchestrator_take` at triage, never into `user_comment`.

### Triage Workflow (orchestrator, batch review)

Per row (top-to-bottom through new/open rows):

1. Fill T3 (`component`, `lifecycle_stage`, `severity`) — derive from
   `surface` + `user_comment`
2. Fill T4 if not already populated (`observed`, `expected`, `evidence`,
   `value`, `effort`, `orchestrator_take`)
3. Fill T5:
   - `framework_anchor` — consult ux-testing-agentic-os.md surface-conditional vocab
   - `kano` if UX-surface
   - `rice_score` if ≥3 peers
   - `downstream_target` — decide routing
4. Update `status`: `open` → `triaged`
5. Identify top-N candidates for next `/cab:plan-implementation`

### Promotion Workflow (per release / sprint / phase batch)

1. Select rows to promote into active release scope
2. Fill T6 `moscow`
3. For each promoted row, invoke `/cab:plan-implementation` → produces
   `notes/impl-plan-<slug>-<date>.md`
4. Row's `linked_plan` auto-populates (hook); `status` → `planning`
5. User approves plan; invoke `/cab:execute-task`; `status` → `in-progress`

### Resolution Workflow (per row, post-execution)

1. Execute commits land with `[UXL-NNN]` suffix in message (convention)
2. Post-commit hook: writes commit hash to `linked_commit`; runs validation
   subset against row's acceptance criteria
3. On pass: `status` → `resolved`
4. If `downstream_target=LL`, author LL entry citing `UXL-NNN` as evidence;
   append `→ LL-NN` to row's `orchestrator_take`

### Archival Workflow (monthly or at pass cycle)

1. Filter `status=resolved` rows older than current pass
2. Move to `notes/_archive/ux-log-resolved-YYYY-MM.csv`
3. Keep active (non-resolved) rows in current pass file
4. New pass starts as `ux-log-NNN-YYYY-MM-DD-pass-N.csv` with fresh sequence

## Status State Machine

```
        ┌─────┐
        │ open│
        └──┬──┘
           │
      ┌────▼──────┐
      │  triaged  │◄──────────┐ (rollback)
      └──┬────────┘           │
         │                    │
    ┌────▼──────┐         ┌───┴───────┐
    │ planning  │─────────▶ in-progress│
    └───────────┘         └───────────┘
         │                    │
         │                    ▼
         │                ┌────────┐
         │                │resolved│
         │                └────────┘
         │
    ┌────▼────────┬───────────────┐
    │             │               │
    ▼             ▼               ▼
┌────────┐  ┌──────────┐  ┌──────────┐
│deferred│  │superseded│  │ wontfix  │
└────────┘  └──────────┘  └──────────┘
```

Legal transitions:
- `open` → `triaged` (orchestrator triage)
- `triaged` → `planning` (plan creation started)
- `triaged` → `deferred` / `superseded` / `wontfix` (not pursued)
- `planning` → `in-progress` (plan approved, execute-task invoked)
- `in-progress` → `resolved` (verification passed)
- `in-progress` → `triaged` (rollback — plan/execution failed, re-plan needed)
- `deferred` → `triaged` (revived after deferral)

## Execution Protocol (Phase 5 spec)

### Commit Message Convention

Commits resolving a tracker row MUST include `[UXL-NNN]` suffix in the first
line of the commit title. Examples:
- `feat(guide): add triage workflow section [UXL-012]`
- `fix(hook): handle missing argument-hint gracefully [UXL-EX2]`
- Multiple rows: `refactor(kb): consolidate prioritization sections [UXL-019, UXL-024]`

The convention enables a post-commit hook to parse commit messages, extract
`UXL-NNN` references, and update the corresponding row's `linked_commit`
column deterministically. See `.claude/rules/kb-conventions.md` for the
durable rule.

### Hook Implementation Spec (`hooks/scripts/ux-log-sync.sh`)

Implementation is deferred to a separate tracker row (self-referential).
Spec:

- **PreToolUse hook on Skill invocation**: if skill arg matches
  `UXL-\d+` pattern and skill is `cab:plan-implementation` or
  `cab:execute-task`, update matching row's `status` column:
  - `cab:plan-implementation` → status becomes `planning`; writes
    `linked_plan` with emitted plan path
  - `cab:execute-task` → status becomes `in-progress`
- **PostToolUse hook on git commit**: parse latest commit message for
  `\[UXL-\d+(?:,\s*UXL-\d+)*\]` pattern; for each match, update that row's
  `linked_commit` with commit hash
- **Optional verification pass**: if `acceptance-criteria` sidecar exists
  for the row, run `/validate` subset; if pass, status → `resolved`
- **Idempotency**: hook must be safe to re-run; use `id` column as row key

### LL Cross-Reference Convention

When a row's `downstream_target=LL` and is executed (resulting in a new LL
entry in `notes/lessons-learned.md`):

1. LL entry's evidence/source section MUST cite `UXL-NNN` (origin row)
2. Tracker row's `orchestrator_take` MUST append `→ LL-NN` (destination)

Bidirectional linkage keeps the knowledge graph reachable from either node.

## Pass File Lifecycle

- Pass 1: `notes/ux-log-001-2026-04-22-pass-1.csv`
- Pass 2 (after triage cycle completes): `notes/ux-log-002-YYYY-MM-DD-pass-1.csv`
- Within-pass updates: append rows with next `UXL-NNN` id
- Merge between passes: resolved rows → archive; unresolved carry forward

## Anti-Patterns

- **Paraphrasing `user_comment`**: destroys verbatim fidelity; use
  `orchestrator_take` for synthesis
- **Log-time framework-soup**: filling T4+T5 for every row kills capture
  rate; tiered stack exists for this
- **Ignoring `lifecycle_stage`**: makes row unqueryable on KG "where-in-lifecycle" axis
- **Orphan rows**: rows with `status=planning` but no `linked_plan` after
  24h — means plan never landed; hook should flag these as drift
- **Permanent MoSCoW**: release-transient; never set-and-forget
- **Subfolders under notes/**: flat-notes policy (LL-25); all ux-log files
  at `notes/` root

# LL-25 Tracked-Notes Policy Propagation Status — 2026-04-22

**Source rows**: UXL-020 (RAS-exec), UXL-021 (HydroCast)
**Source LL**: LL-25 (tracked-by-default notes with `_archive/` gitignored +
`scratch-*.md` / `draft-*.md` / `personal-*.md` name-prefix exclusions)

## Summary

| Project | Current state | Action needed | UXL status |
|---|---|---|---|
| **HydroCast** (`Flood-Forecasting/`) | ✅ Already LL-25 aligned | None (no-op) | UXL-021 resolved |
| **RAS-exec** | ❌ Still uses pre-LL-25 `notes/scratch/` exclusion pattern | Patch below; apply in RAS-exec session | UXL-020 resolved (CAB-side deliverable = this doc); physical apply pending in RAS-exec |

## HydroCast Evidence (UXL-021 no-op close)

`.gitignore` (extract):
```
_archive/           # ← LL-25 compliant exclusion
notes/session-log.txt
outputs/_archive/
```

`CLAUDE.md` lines 68-84 comprehensively document tracked-notes model:
```
| notes/current-task.md         | Cold-start anchor (<40 lines) — tracked: Yes
| notes/progress.md             | Persistent task tracker — tracked: Yes
| notes/session.md              | Ephemeral session journal — tracked: Yes
| notes/session-XX-transfer.md  | Optional session handoff — tracked: When needed
Archive: notes/_archive/ (gitignored graveyard for superseded versions).
```

**Verdict**: HydroCast is already at the LL-25 "tracked-by-default with
name-prefix + _archive/ exclusions" model. No propagation work needed.
UXL-021 closes as no-op resolution.

## RAS-exec Patch (UXL-020 pending apply)

**Target file**: `/c/Users/daniel.kang/Desktop/Automoto/RAS-exec/.gitignore`

**Current (line 51)**:
```
notes/scratch/
```

**Proposed replacement**:
```
# LL-25: notes/ is tracked by default. Exclusions below.
notes/_archive/
# Name-prefix exclusions (scratch-*, draft-*, personal-* + legacy scratch/)
notes/scratch/
```

**Target file**: `/c/Users/daniel.kang/Desktop/Automoto/RAS-exec/CLAUDE.md`

**Current (lines 149-151)**:
```
- Active task progress: notes/progress.md
- Session scratch: notes/scratch/ (gitignored)
- Implementation plan: notes/implementation-plan.md
```

**Proposed replacement**:
```
- Active task progress: notes/progress.md (tracked per LL-25)
- Ephemeral scratch work: use `scratch-<topic>.md` / `draft-<topic>.md` /
  `personal-<topic>.md` prefixes (excluded by .gitignore); legacy
  `notes/scratch/` directory also excluded for backward compatibility
- Implementation plan: notes/implementation-plan.md (tracked per LL-25)
- Archive (gitignored): notes/_archive/ — move superseded versions here
  instead of deleting
```

## Recommended Apply Path for RAS-exec

When next opening RAS-exec in a CC session:

```bash
cd /c/Users/daniel.kang/Desktop/Automoto/RAS-exec

# 1. Apply .gitignore patch (edit manually per above)
# 2. Apply CLAUDE.md patch (edit manually per above)
# 3. Create notes/_archive/ scaffolding if it doesn't exist:
mkdir -p notes/_archive
# 4. Commit:
git add .gitignore CLAUDE.md
git commit -m "chore(state): adopt LL-25 tracked-notes policy

Aligns RAS-exec with CAB LL-25 tracked-by-default model.
See CAB notes/ll-25-propagation-status-2026-04-22.md for rationale."
```

## Sources

- CAB LL-25: `notes/lessons-learned.md` (CAB repo)
- CAB filesystem-patterns.md §Git Tracking Policy
- UXL-020, UXL-021 tracker rows: `notes/ux-log-001-2026-04-22-pass-1.csv`

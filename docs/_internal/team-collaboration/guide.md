# Team Collaboration Quick Reference

> Practical cheat sheet for multi-human + multi-agent collaboration using git worktrees and Claude Code. For the full KB, see `knowledge/operational-patterns/team-collaboration.md`.

## The One Rule

**One worktree per task. Fresh branch from main. Delete after merge.**

```
git worktree add ../Project-{task} -b feat/{task}   # Create
# ... work, commit, push, PR, merge ...
git worktree remove --force ../Project-{task}         # Destroy
git branch -d feat/{task}                             # Clean up
```

## Delegating Work

### To a Coworker (Human or CC Agent)

1. Create worktree + branch from main
2. Write `notes/current-task.md` with scope, acceptance criteria, conflict zones
3. Share the worktree path and branch name
4. Worker opens worktree, reads current-task.md, begins work
5. Worker creates PR when done — you review and merge

### Task Assignment Template (notes/current-task.md)

```markdown
**Task:** {what}
**Branch:** feat/{task}
**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2

**Conflict Zones:**
| File | Owner | Status |
|------|-------|--------|
| src/my_file.py | This worktree | Active |
| src/shared.py | Main workspace | Frozen — read only |
```

## Conflict Prevention

- Declare file ownership in every worktree's `notes/current-task.md`
- One owner per file across all active worktrees
- Check for overlap before starting: `git diff --name-only main...feat/branch-a`
- If two branches touch the same file → redesign task boundaries or sequence them

## Close-Out Checklist

When a task is done and merged:

```
□ git status clean (no uncommitted work)
□ Pushed to remote
□ PR created, reviewed, merged
□ Local-only files copied to main workspace (data, refs)
□ Main workspace: git pull origin main
□ Close all editors pointing at worktree
□ git worktree remove --force ../Project-{task}
□ git branch -d feat/{task}
□ git worktree list  →  only main should remain
```

## Common Scenarios

### "Coworker finished their task, how do I get their work?"

```bash
# From your main workspace:
git pull origin main          # Their PR was merged → you now have it
```

### "I need to give feedback on a coworker's PR"

Add comments on the GitHub PR. Coworker starts a new CC session in their worktree:
```
"Read and address the review comments on PR #N"
```

### "Two worktrees accidentally modified the same file"

1. Merge the first PR (whichever is ready)
2. In the second worktree: `git merge origin/main`
3. Resolve conflicts manually (or ask CC agent to help)
4. Commit the resolution, update PR

### "Worktree won't delete (permission denied)"

Close VS Code / terminals pointing at the worktree directory, then:
```bash
git worktree remove --force ../Project-{task}
# If still fails:
rm -rf ../Project-{task}
git worktree prune
```

### "Should I reuse this worktree for the next task?"

**No.** Delete it and create a fresh one. Stale files and session state from the previous task will contaminate the new one.

## Parallel Work Guardrails

| Do | Don't |
|----|-------|
| Branch from latest main | Branch from another feature branch |
| Declare file ownership upfront | Assume files are uncontested |
| Merge PRs sequentially (first-done first) | Merge multiple PRs simultaneously |
| Keep branches short-lived (days, not weeks) | Let branches diverge for weeks |
| Write current-task.md before starting work | Start coding without scope doc |
| Copy local-only files before worktree removal | Assume gitignored files survive deletion |

## CC Agent-Specific Notes

- CC agents read `notes/current-task.md` as their cold-start anchor
- After compaction, agents should re-read CLAUDE.md and current-task.md
- Agents create PRs via `gh pr create` — humans review before merge
- Use `/context-sync` at session start to pull recent project activity
- Learned corrections go in CLAUDE.md so all future sessions benefit

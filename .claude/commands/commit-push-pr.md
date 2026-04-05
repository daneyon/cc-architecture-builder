---
description: Stage changes, commit with concise, descriptive message, push to remote, and create a pull request in one workflow
allowed-tools: Read, Bash, Grep
---
# Commit Push PR

Automates the full commit-to-PR cycle. Pre-computes git status and diff summary
so the commit message and PR description are accurate and context-rich, while prioritizing to be token-efficient.

## Behavior

1. **Pre-compute context**:

   ```bash
   git status --short
   git diff --stat
   git diff --cached --stat
   git log --oneline -5
   ```
2. **Stage changes** (if not already staged):

   - If unstaged changes exist, present them and ask which to include
   - Never blind `git add .` — always review what's being committed
   - Default: stage all modified/added files shown in status
3. **Generate commit message**:

   - Format: `[type]: [concise summary]`
   - Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`
   - Body: list of key changes derived from diff stat
   - If arguments provided, use as commit message override
4. **Commit and push**:

   ```bash
   git commit -m "[generated message]"
   git push origin [current-branch]
   ```
5. **Create PR** (if GitHub CLI available):

   ```bash
   gh pr create --title "[commit summary]" --body "[generated description]"
   ```

   - PR body includes: summary of changes, files modified, test status
   - If `gh` not available, output the PR description for manual creation

## Arguments

- `$ARGUMENTS` (optional): Commit message override. If provided, skip message generation.

## Examples

```
/commit-push-pr
→ Reviews status, generates message, commits, pushes, creates PR

/commit-push-pr "fix: resolve race condition in WebSocket handler"
→ Uses provided message, skips generation, commits, pushes, creates PR
```

## Safety

- Always shows `git diff --stat` before committing
- Never force-pushes
- Never commits to main/master directly (warns and aborts)
- Runs project verification commands (from CLAUDE.md) before commit if available

## See Also

- `.claude/skills/executing-tasks/` — Full task execution protocol (Phase 5: COMMIT)
- `.claude/agents/verifier.md` — Pre-commit verification

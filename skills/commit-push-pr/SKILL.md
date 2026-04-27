---
name: commit-push-pr
description: >-
  Stage changes, commit with a concise descriptive message, push to the remote,
  and open a pull request in one workflow. Pre-computes git status/diff so the
  commit message and PR description are accurate and context-rich.
  Triggers: commit and push, ship changes, open PR, publish work, end-of-task
  commit, finalize and PR.
argument-hint: "Optional commit message override; otherwise generated from diff"
allowed-tools: Read, Bash, Grep
---

# Commit, Push, and Open PR

## Purpose

Automates the full commit-to-PR cycle while keeping the human in control of
*what* gets committed. Pre-computes git context (status, diff, recent log) so
the generated message reflects actual changes rather than hand-waving.

## When to Invoke

- User says "commit", "push", "ship it", "open a PR", or similar end-of-work
  signals
- After `execute-task` Phase 5a/5b commits land and the work is ready to
  publish to the remote
- User wants to bundle stage + commit + push + PR creation in one step

## Protocol

### Step 1: Pre-compute Context

```bash
git status --short
git diff --stat
git diff --cached --stat
git log --oneline -5
```

These outputs feed the commit message and PR description generation. Never
guess at what changed — read the actual diff.

### Step 2: Stage Changes

- If there are unstaged changes, present them and ask which to include.
- **Never** use `git add .` blindly — always review what's being committed
  (sensitive files, generated artifacts, local-only configs).
- Default heuristic: stage all modified/added files visible in `git status`,
  but exclude anything matching CAB security deny patterns
  (`.env*`, `.ssh/*`, `.aws/*`, credential files).

### Step 3: Generate Commit Message

Format: `[type]: [concise summary]`

- Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`
- Body: bullet list of key changes derived from `git diff --stat`
- If `$ARGUMENTS` provided, use as message override (skip generation)

For UXL tracker rows, include `[UXL-NNN]` suffix per
`.claude/rules/kb-conventions.md` so the post-commit hook can update
`linked_commit` deterministically.

### Step 4: Commit and Push

```bash
git commit -m "[generated or provided message]"
git push origin "$(git rev-parse --abbrev-ref HEAD)"
```

### Step 5: Create PR (if `gh` CLI available)

```bash
gh pr create --title "[commit summary]" --body "[generated description]"
```

PR body should include:
- Summary of changes (1-3 bullets)
- Files modified (high-level, not full diff)
- Test plan / verification status
- Link to related UXL row or issue if applicable

If `gh` is not available, output the formatted PR description for manual
creation.

## Safety Constraints

- Always show `git diff --stat` before committing.
- Never force-push.
- Never commit directly to `main` or `master` (warn and abort; offer to
  create a feature branch).
- Run project verification commands (from CLAUDE.md) before commit if
  defined and inexpensive (`<5s`).
- For commits that resolve a UXL tracker row, ensure the `[UXL-NNN]` suffix
  is present (governance rule).

## Verification

This skill is working correctly when:

- Commit messages accurately reflect the diff content (not generic).
- No file is committed without explicit visibility in pre-stage review.
- PRs include enough context that a reviewer can assess without re-reading
  the full diff.
- Force-push, main-branch commits, and credential file inclusion are
  blocked or explicitly confirmed.

## Integration Points

- `execute-task` skill Phase 5a — produces the work commit this skill ships
- `pre-push-state-review` skill — runs before push if `notes/` files changed
- `commands/commit-push-pr.md` — shim trigger preserving `/cab:commit-push-pr`
  user habit
- `.claude/rules/security.md` — non-negotiable git op restrictions

## See Also

- `.claude/rules/security.md` — never push --force, never commit credentials
- `.claude/rules/kb-conventions.md` — `[UXL-NNN]` commit message convention

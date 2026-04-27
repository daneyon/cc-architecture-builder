---
description: Stage changes, commit with concise descriptive message, push to remote, and create a pull request in one workflow
allowed-tools: Read, Bash, Grep
---
# Commit Push PR

Shim invoking the `commit-push-pr` skill, which owns the stage → commit →
push → PR-open workflow.

## Arguments

- `$ARGUMENTS` (optional): Commit message override. If provided, the skill
  skips message generation and uses it verbatim.

## Examples

```
/commit-push-pr
→ Reviews status, generates message from diff, commits, pushes, opens PR

/commit-push-pr "fix: resolve race condition in WebSocket handler"
→ Uses provided message, skips generation

/commit-push-pr "feat(skills): promote orphan to skill [UXL-002]"
→ UXL tracker commit (post-commit hook updates linked_commit)
```

## See Also

- `skills/commit-push-pr/` — The workflow skill (owns all logic)
- `.claude/rules/security.md` — never push --force, never commit credentials
- `.claude/rules/kb-conventions.md` — `[UXL-NNN]` commit message convention

# Commands Archive

These 14 command files were shims pointing at skills of the same name (e.g.
`commands/execute-task.md` → invoked the `execute-task` skill). They are
archived here pending formal LL-32 codification in `notes/lessons-learned.md`.

## Why archived

Empirical evidence (LL-32 candidate; see
`memory/project_command_skill_type_shadowing.md`): when `commands/<name>.md`
and `skills/<name>/SKILL.md` coexist at the same scope, the resolver routes
to the command shim instead of the skill body — contradicting DP2's
"Skills are preferred; commands still work but skills win when both exist"
precedence (`knowledge/overview/design-principles.md` line 69).

Sunset reasoning:
- All 14 are pure shims — no unique logic
- User has stopped using them
- 2026 CC docs treat commands as superseded by skills (the unified registry)
- Type-shadowing was actively interfering with skill invocation in operational
  reality

## What is NOT here

`commands/init-worktree.md` remains in place at the parent directory — it
has 118 lines of genuine worktree-setup logic with no skill twin. Archiving
it would remove functionality. A skill migration is required first
(tracked in `notes/TODO.md`).

## Restoration path

If type-shadowing turns out NOT to be the issue (e.g., a CC platform fix
restores DP2 precedence) and these shims are needed again:

```bash
git mv commands/_archive/*.md commands/
rm commands/_archive/README.md
rmdir commands/_archive
```

## Slash invocation surface

Skills with the same name as the archived commands are expected to remain
slash-invocable as `/cab:<name>` if their frontmatter has `user-invocable: true`
(or if CC's default is true — needs fresh-fetch verification per TODO row).

If a skill counterpart is NOT slash-triggerable post-archive, restore the
specific command(s) needed and migrate to skill `user-invocable` flag in the
same change.

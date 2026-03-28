---
description: Set up git worktrees for parallel Claude Code agent execution
allowed-tools: Read, Write, Bash
---

# Init Worktree Command

Create git worktrees for parallel Claude Code sessions, with shell aliases for fast switching between them.

**Note:** For single worktrees, `claude --worktree <name>` (built-in) is simpler.
This command adds value for batch creation (2-5 worktrees) with auto-generated aliases.

## Behavior

1. **Verify prerequisites**:
   - Current directory is a git repository
   - Working tree is clean (or warn)
   - Remote `origin/main` (or specified base branch) exists

2. **Parse worktree names** from arguments.

3. **Create worktree directory**:
   ```bash
   mkdir -p .claude/worktrees
   ```

4. **Create each worktree**:
   ```bash
   git worktree add .claude/worktrees/$NAME origin/main
   ```

5. **Generate shell aliases** (printed to terminal + optionally appended to shell rc):
   ```bash
   alias za='cd /full/path/.claude/worktrees/$NAME1 && claude'
   alias zb='cd /full/path/.claude/worktrees/$NAME2 && claude'
   alias zc='cd /full/path/.claude/worktrees/$NAME3 && claude'
   ```

6. **Add worktree directory to .gitignore** if not already present:
   ```
   .claude/worktrees/
   ```

## Arguments

- `$ARGUMENTS`: Space-separated worktree names (1-5 names)
- `--base`: Base branch (default: `origin/main`)
- `--aliases`: Auto-append aliases to shell rc file (default: print only)

## Examples

```
/init-worktree feature-auth feature-api
→ Creates 2 worktrees, generates aliases za and zb

/init-worktree bugfix-123
→ Creates 1 worktree with alias za

/init-worktree frontend backend testing --base develop
→ Creates 3 worktrees from develop branch, aliases za/zb/zc

/init-worktree feature-auth --aliases
→ Creates worktree AND appends alias to ~/.bashrc or ~/.zshrc
```

## Post-Creation Output

```
✓ Created worktrees:
  .claude/worktrees/feature-auth (from origin/main)
  .claude/worktrees/feature-api  (from origin/main)

✓ Shell aliases (add to your shell profile):
  alias za='cd /home/user/my-project/.claude/worktrees/feature-auth && claude'
  alias zb='cd /home/user/my-project/.claude/worktrees/feature-api && claude'

✓ .gitignore updated: .claude/worktrees/

Tips:
- Name/color-code your terminal tabs to match worktrees
- Enable system notifications for long-running tasks
- 3-5 worktrees is the practical sweet spot
- Clean up when done: git worktree remove .claude/worktrees/feature-auth
```

## The "Analysis Sandbox" Pattern

Maintain a dedicated, persistent worktree strictly for read-only investigation:
log reading, data queries, passive analysis, and debugging — without risk of
accidentally modifying working code.

```bash
/init-worktree analysis --base origin/main

# Or manually:
git worktree add .claude/worktrees/analysis origin/main
alias zx='cd .claude/worktrees/analysis && claude'
```

The analysis worktree stays long-lived (don't remove after each task). Use it
for BigQuery investigations, log tailing, metrics review, or any exploratory
work that shouldn't touch the implementation branches.

## Cleanup

To remove worktrees when finished:

```bash
git worktree remove .claude/worktrees/$NAME
# Or remove all:
git worktree list | grep .claude/worktrees | awk '{print $1}' | xargs -I{} git worktree remove {}
```

## See Also

- `knowledge/operational-patterns/git-worktree.md` — Worktree deep dive
- `knowledge/operational-patterns/multi-agent-collaboration.md` — Parallel patterns
- `knowledge/operational-patterns/team-collaboration.md` — Close-out checklist, conflict zones

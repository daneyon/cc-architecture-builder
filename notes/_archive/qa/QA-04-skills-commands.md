# QA-04: Skills + Commands -- Delta Report

**Date**: 2026-04-05
**CAB files**: `knowledge/components/agent-skills.md`, `knowledge/components/custom-commands.md`
**Official sources**:
- https://code.claude.com/docs/en/skills (Skills system, frontmatter, invocation, bundled skills)
- https://code.claude.com/docs/en/commands (Built-in commands reference)
- https://code.claude.com/docs/en/plugins-reference (Plugin component specs)

## Summary

**41 items checked, 12 discrepancies found** (5 ERROR, 4 MISSING, 2 STALE, 1 EXTRA-needs-update)

---

## Discrepancies

### ERROR (factually wrong in CAB)

| # | CAB Claim | Official Reality | File | Location | Fix |
|---|-----------|-----------------|------|----------|-----|
| E1 | `effort` field options listed as `"low"`, `"medium"`, `"high"`, or `"ultrathink"` | Official docs list `low`, `medium`, `high`, `max` (Opus 4.6 only). `"ultrathink"` is NOT an effort value -- it is a keyword you place in the skill *body content* to enable extended thinking. The docs say: "To enable extended thinking in a skill, include the word 'ultrathink' anywhere in your skill content." | agent-skills.md | Line 68, frontmatter table | Change `"ultrathink"` to `"max"` in effort options. Add a separate note that including the word "ultrathink" in skill body content triggers extended thinking. |
| E2 | `context` field default described as `"inline"` with two documented values `"fork"` and `"inline"` | Official docs only document `context: fork` as a settable value. There is no `"inline"` value. The field description is: "Set to `fork` to run in a forked subagent context." The default behavior (inline/shared context) is simply the absence of `context: fork`, not `context: "inline"`. | agent-skills.md | Lines 69, 86-92 | Remove `"inline"` as a documented value. Change default from `"inline"` to omitted/absent. Reframe: "Omit for shared session context (default); set to `fork` for isolated subagent." |
| E3 | `paths` field described as "File paths to auto-load into context when skill activates" | Official docs say: "Glob patterns that limit when this skill is activated. Accepts a comma-separated string or a YAML list. When set, Claude loads the skill automatically only when working with files matching the patterns." This is an *activation filter*, not a context loader. | agent-skills.md | Line 72, frontmatter table | Rewrite `paths` description to match official: activation-limiting glob patterns, not context-loading file paths. |
| E4 | `allowed-tools` field described as `string (CSV)` format | Official docs say: "Accepts a space-separated string or a YAML list." Not CSV (comma-separated). All examples use space-separated: `allowed-tools: Read Grep Glob`. | agent-skills.md | Line 63, frontmatter table | Change "string (CSV)" to "string (space-separated) or YAML list". |
| E5 | `$N` / `$1`, `$2` described as "Positional arguments (1-indexed)" | Official docs say `$N` is "Shorthand for `$ARGUMENTS[N]`", meaning `$0` = first argument, `$1` = second. This is **0-indexed**, same as `$ARGUMENTS[N]`. The docs explicitly show: "`$0` for the first argument or `$1` for the second." | agent-skills.md | Line 103 | Change "Positional arguments (1-indexed)" to "Shorthand for `$ARGUMENTS[N]` (0-indexed). `$0` = first argument, `$1` = second." Remove the `$1`, `$2`, ... notation that implies 1-indexing. |

### MISSING (in official docs, absent from CAB)

| # | Official Feature | Source URL | Recommended Action |
|---|-----------------|------------|-------------------|
| M1 | **Agent Skills open standard**: Official docs state "Claude Code skills follow the Agent Skills (agentskills.io) open standard, which works across multiple AI tools." CAB does not mention this standard. | https://code.claude.com/docs/en/skills (intro paragraph) | Add a note about the agentskills.io open standard in the Overview section. |
| M2 | **`--add-dir` skill discovery exception**: Skills in `.claude/skills/` within an `--add-dir` directory are loaded automatically and support live change detection. Other `.claude/` config (subagents, commands, output styles) is NOT loaded from added directories. This is a significant behavioral distinction not documented in CAB. | https://code.claude.com/docs/en/skills ("Skills from additional directories") | Add a section or note about `--add-dir` skill discovery behavior. |
| M3 | **`disableSkillShellExecution` setting**: Setting `"disableSkillShellExecution": true` in settings disables `!command` preprocessing for user/project/plugin skills. Each command is replaced with `[shell command execution disabled by policy]`. Bundled and managed skills are not affected. Most useful in managed settings. | https://code.claude.com/docs/en/skills ("Inject dynamic context") | Document the `disableSkillShellExecution` setting in the Dynamic Context Injection section. |
| M4 | **Skill priority/conflict resolution across scopes**: Official docs specify precedence: enterprise > personal > project. Plugin skills use `plugin-name:skill-name` namespace so cannot conflict. When a skill and command share the same name, the skill takes precedence. | https://code.claude.com/docs/en/skills ("Where skills live") | Add explicit priority order to Skill Locations table. Currently CAB mentions "skill wins" for same-name conflicts but omits the enterprise > personal > project hierarchy. |

### STALE (outdated in CAB)

| # | CAB Content | Current Official | Fix |
|---|------------|-----------------|-----|
| S1 | Bundled skills listed as 5: `/batch`, `/claude-api`, `/debug`, `/loop`, `/simplify` | Official docs list the same 5 but with significantly updated descriptions. `/batch` now explicitly describes worktree-based parallel execution (5-30 units, one agent per unit, each opens a PR). `/debug` now mentions it enables debug logging mid-session. `/claude-api` now covers Java, Go, Ruby, C#, PHP, cURL in addition to Python/TypeScript. | agent-skills.md, Lines 124-133 | Update bundled skill descriptions to match current official docs. The skill names are correct but descriptions are abbreviated and miss key details. |
| S2 | Description budget documented as "~1% of context window (`SLASH_COMMAND_TOOL_CHAR_BUDGET`)" | Official docs provide more detail: "The budget scales dynamically at 1% of the context window, with a fallback of 8,000 characters." Also: "each entry is capped at 250 characters regardless of budget." The 8,000-character fallback is not in CAB. | agent-skills.md, Line 168 | Add the 8,000-character fallback value. The 250-char per-entry cap is already correctly noted. |

### EXTRA (in CAB only -- may be valid CAB extension)

| # | CAB Content | Assessment |
|---|------------|------------|
| X1 | **Invocation Control Matrix (B7)**: CAB documents a 4-mode matrix combining `disable-model-invocation` and `user-invocable` including a "Nobody" mode (`true`/`false`). Official docs only show a 3-row table (default, disable-model-invocation: true, user-invocable: false) with a "When loaded into context" column. | The CAB 4-mode matrix is a valid logical extension but the official docs deliberately omit the "Nobody" combination. The official 3-row table adds valuable context about when descriptions are loaded into context that CAB's matrix lacks. **Recommend**: Keep the 4-mode matrix as a CAB extension but add the "When loaded into context" column from official docs. Also note that `disable-model-invocation: true` means "Description not in context" (official confirms this removes the skill from Claude's context entirely). |

---

## Verified Correct

### agent-skills.md

| Item | Status |
|------|--------|
| Skills are model-invoked capabilities with lazy-loading | Correct |
| Commands merged into skills; skills preferred for new development | Correct |
| Skill locations: Personal (`~/.claude/skills/`), Project (`.claude/skills/`), Plugin (bundled) | Correct |
| Monorepo nested discovery from `packages/*/.claude/skills/` | Correct |
| SKILL.md is required entrypoint in skill directory | Correct |
| Supporting files: scripts/, references/ (official uses broader structure: templates, examples/, scripts/) | Correct (official is more flexible but CAB's list is not wrong) |
| `name` field: lowercase, hyphens, max 64 chars, no reserved words | Correct |
| `description` field: defaults to first paragraph; 250-char truncation | Correct |
| `argument-hint` field: placeholder for autocomplete | Correct |
| `disable-model-invocation` field: boolean, default false | Correct |
| `user-invocable` field: boolean, default true | Correct |
| `model` field: override model for skill | Correct |
| `agent` field: subagent type when `context: fork` set; default `general-purpose` | Correct |
| `hooks` field: skill-scoped hooks | Correct |
| `shell` field: shell override for Bash tool | Correct (official adds detail: `bash` default, `powershell` option with `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`) |
| `$ARGUMENTS` substitution and append-if-absent behavior | Correct |
| `$ARGUMENTS[N]` for 0-based index access | Correct |
| `${CLAUDE_SESSION_ID}` substitution | Correct |
| `${CLAUDE_SKILL_DIR}` substitution including plugin behavior | Correct |
| Dynamic context injection with `!command` syntax | Correct |
| Multi-line dynamic context with fenced code blocks | Correct (official uses ` ```! ` syntax) |
| `context: fork` runs in isolated context with no conversation history access | Correct |
| `agent` field options: built-in (`Explore`, `Plan`, `general-purpose`) or custom from `.claude/agents/` | Correct |
| Permission rules: `Skill(name)` exact, `Skill(name *)` prefix | Correct |
| Enterprise skill tier via managed settings | Correct |
| Progressive disclosure: L1 metadata at start, L2 on trigger, L3 as needed | Correct (aligns with official behavior description) |
| Debugging tips: description vague, path verification, YAML parse, model-invocation check | Correct |

### custom-commands.md

| Item | Status |
|------|--------|
| Commands merged into skills; skills preferred | Correct |
| Commands still work for backward compatibility | Correct |
| Command location: `commands/name.md` vs skill `skills/name/SKILL.md` | Correct |
| Commands are user-only invocation; skills add model-invocation | Correct |
| Skill wins if both exist for same name | Correct |
| Commands support same frontmatter as skills | Correct (official confirms: "Files in `.claude/commands/` still work and support the same frontmatter") |
| Migration path: move command .md content into SKILL.md directory with enhanced frontmatter | Correct |
| Commands support `$ARGUMENTS`, `$1-$N` substitutions | Correct (but note the indexing issue from E5 applies here too -- `$N` is 0-indexed) |
| Dynamic context injection available in commands | Correct |

---

## Additional Notes

1. **Official `/en/commands` page**: This page documents *built-in* CLI commands (`/help`, `/compact`, `/clear`, etc.), NOT custom commands. Custom commands are fully documented within the `/en/skills` page under the commands-to-skills migration notes. CAB's `custom-commands.md` source link correctly points to `/en/skills`.

2. **Plugin commands**: The plugins-reference confirms `commands/` directory at plugin root is a valid location, labeled as "legacy; use `skills/` for new skills" in the file locations reference table. Plugin commands use the standard `commands/*.md` format.

3. **No `disallowed-tools` field**: Neither the skills docs nor the plugins-reference mention a `disallowed-tools` field for skills. This field exists only for subagents (per plugins-reference: agents support `disallowedTools`). CAB correctly does not include it for skills.

4. **`/en/commands` page includes new commands not relevant to CAB**: `/ultraplan`, `/schedule`, `/branch`, `/color`, `/context`, `/diff`, `/insights`, `/stickers`, `/tasks`, and many others. These are built-in commands, not custom command mechanics.

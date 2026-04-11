# QA-03: Memory + Knowledge Base Structure -- Delta Report

**Date**: 2026-04-05
**CAB files**: `knowledge/components/memory-claudemd.md`, `knowledge/components/knowledge-base-structure.md`
**Official sources**:
- https://code.claude.com/docs/en/memory (fetched successfully)
- https://code.claude.com/docs/en/claude-md (404 -- page does not exist; content merged into /memory)
- https://code.claude.com/docs/en/plugins (fetched successfully)
- https://code.claude.com/docs/en/plugins-reference (fetched successfully)
- https://code.claude.com/docs/en/sub-agents (fetched successfully -- subagent memory details)
- https://code.claude.com/docs/en/settings (fetched successfully -- managed settings details)
- https://code.claude.com/docs/en/context-window (fetched successfully -- context window visualization)

---

## Summary

**47 items checked across both files. 14 discrepancies found (5 ERROR, 6 MISSING, 2 STALE, 1 EXTRA).**

---

## Discrepancies

### ERROR (factually wrong in CAB)

| # | CAB Claim | Official Reality | File | Location | Fix |
|---|-----------|-----------------|------|----------|-----|
| E1 | 4-scope hierarchy listed as: 1. Managed (Highest), 2. Project, 3. User, 4. Local (Lowest). States "Files higher in hierarchy load first" and precedence is Managed=Highest, Local=Lowest. | Official docs state: "More specific locations take precedence over broader ones." The actual precedence order is: 1. Managed (highest, cannot be overridden), 2. Command line arguments, 3. Local, 4. Project, 5. User (lowest). Local overrides Project which overrides User. CAB has the precedence of Local and Project/User inverted -- Local is NOT lowest, it is HIGHER than Project and User. | memory-claudemd.md | Lines 29-36 (4-Scope table) | Reverse the precedence column: Managed=Highest, Local=higher than Project, Project=higher than User, User=Lowest. Remove "Files higher in hierarchy load first" or rephrase to match actual loading semantics. Note that `/memory` page says: "CLAUDE.local.md is appended after CLAUDE.md, so when instructions conflict, your personal notes are the last thing Claude reads at that level" -- last-read wins. |
| E2 | autoDream trigger conditions listed as: "1. 24+ hours since last consolidation, 2. 5+ sessions since last consolidation, 3. Or manual: user says 'dream' / 'consolidate memory files'". States "both required" for conditions 1 and 2. | Official docs make NO mention of autoDream, background consolidation, 24-hour thresholds, 5-session thresholds, four phases (Orient/Gather Signal/Consolidate/Prune & Index), per-project lock files, or 913-session benchmarks. The entire autoDream section (lines 157-180) describes behavior that is not documented in official sources. This may be reverse-engineered from observed behavior, but it is NOT official documentation and should be flagged as CAB-inferred. | memory-claudemd.md | Lines 157-180 (autoDream section) | Either (a) remove the autoDream section entirely, (b) mark it explicitly as "CAB-inferred / observed behavior -- not in official docs", or (c) add a prominent caveat that these details are based on observation, not official documentation, and may change without notice. |
| E3 | `extractMemories` listed as a write path trigger: "Automatic during sessions -- Captures corrections, patterns, decisions, preferences". | Official docs describe auto memory write behavior simply as: "Claude saves notes for itself as it works" and "Claude decides what's worth remembering based on whether the information would be useful in a future conversation." There is no mention of an `extractMemories` mechanism by name. The official interface shows "Writing memory" or "Recalled memory" in the UI. | memory-claudemd.md | Lines 138-143 (Write Paths table) | Replace `extractMemories` with the official description: Claude automatically saves notes during sessions when it determines information would be useful in future conversations. Remove the internal mechanism name. |
| E4 | Memory categories listed as: `user`, `feedback`, `project`, `reference`. | Official docs do not define these four categories. Auto memory is described as storing "build commands, debugging insights, architecture notes, code style preferences, and workflow habits" -- but not organized into named categories. This categorization appears to be a CAB invention or inferred from older documentation. | memory-claudemd.md | Lines 128-135 (Memory Categories table) | Either remove the categories table or clearly label it as a CAB organizational pattern rather than an official CC feature. |
| E5 | Managed settings Windows path listed as `C:\Program Files\ClaudeCode\CLAUDE.md` plus "HKLM/HKCU registry" in the delivery table. | Official settings docs (2026) confirm the file-based path `C:\Program Files\ClaudeCode\` for managed-settings.json and CLAUDE.md. However, the registry mechanism is more specific: `HKLM\SOFTWARE\Policies\ClaudeCode` with a `Settings` value (REG_SZ) containing JSON for admin-level, and `HKCU\SOFTWARE\Policies\ClaudeCode` for user-level (lowest policy priority). The legacy path `C:\ProgramData\ClaudeCode\` is no longer supported as of v2.1.75. CAB's table uses "HKLM/HKCU registry" without specifying the actual key paths or the `Settings` value name. Also, macOS MDM is via `com.anthropic.claudecode` managed preferences domain, not just "MDM plist". | memory-claudemd.md | Lines 40-46 (Managed Settings table) | Update Windows registry details to include full key paths (`HKLM\SOFTWARE\Policies\ClaudeCode`, `HKCU\SOFTWARE\Policies\ClaudeCode`, `Settings` value). Update macOS MDM to reference `com.anthropic.claudecode` managed preferences domain. Note the deprecated `C:\ProgramData\ClaudeCode\` path. |

### MISSING (in official docs, absent from CAB)

| # | Official Feature | Source URL | Recommended Action |
|---|-----------------|------------|-------------------|
| M1 | **`autoMemoryEnabled` setting** -- Auto memory can be toggled on/off via `/memory` command or `autoMemoryEnabled` in project settings. Also `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` environment variable to disable. | /memory#enable-or-disable-auto-memory | Add to memory-claudemd.md in the Auto Memory section. |
| M2 | **`autoMemoryDirectory` setting** -- Custom directory for auto memory storage. Accepted from policy, local, and user settings; NOT accepted from project settings to prevent redirecting memory writes. | /memory#storage-location, /settings | Add to memory-claudemd.md. Important for enterprise deployments. |
| M3 | **Auto memory version requirement** -- Auto memory requires Claude Code v2.1.59 or later. | /memory#auto-memory | Add as a note in the Auto Memory section. |
| M4 | **`--append-system-prompt` detail** -- Official docs clarify: "This must be passed every invocation, so it's better suited to scripts and automation than interactive use." CAB mentions it in the Additional Features table but lacks this context. | /memory#troubleshoot-memory-issues | Expand the existing table entry with this behavioral detail. |
| M5 | **Subagent memory path structure** -- Official docs specify: `~/.claude/agent-memory/<name-of-agent>/` (user), `.claude/agent-memory/<name-of-agent>/` (project), `.claude/agent-memory-local/<name-of-agent>/` (local). CAB's subagent memory table (line 227) omits the `<name-of-agent>/` subdirectory in the paths. | /sub-agents#enable-persistent-memory | Fix the subagent memory paths in the table to include `<name-of-agent>/` subdirectory. |
| M6 | **CLAUDE.md loading walk-up behavior** -- Official docs explicitly state: "Claude Code reads CLAUDE.md files by walking up the directory tree from your current working directory, checking each directory along the way." Subdirectory CLAUDE.md files are "included when Claude reads files in those subdirectories" (lazy-loaded). CAB does not describe this walk-up discovery or lazy-loading behavior. | /memory#how-claude-md-files-load | Add a section or note about the directory-walk-up discovery mechanism and lazy-loading of subdirectory CLAUDE.md files. |

### STALE (outdated in CAB)

| # | CAB Content | Current Official | Fix |
|---|------------|-----------------|-----|
| S1 | Runtime Memory Pipeline table (lines 186-196) lists: Session Memory ("Summaries every ~5K tokens"), MicroCompact ("Local editing of cached tool results, zero API calls, 60+ min expiry"), AutoCompact ("Structured summary at `effectiveContextWindow - 13,000` tokens"), Full Compact ("Complete conversation compression, 50K-token budget reset"), Session Reset. | Official docs (context-window page, /memory) make no mention of: MicroCompact, Session Memory summaries at 5K token intervals, the specific `effectiveContextWindow - 13,000` formula, or a 50K-token budget reset for Full Compact. The official description of compaction is: "/compact replaces the conversation with a structured summary." CLAUDE.md "fully survives compaction" -- it is re-read from disk. The specific numbers (5K, 13K, 50K, 60+ min) are not in any current official documentation. | Either (a) remove the Runtime Memory Pipeline table, (b) mark it as "CAB-inferred / internal behavior -- not officially documented", or (c) significantly simplify to match what official docs confirm: compaction creates a structured summary, CLAUDE.md survives by re-reading from disk. |
| S2 | `source` field in CLAUDE.md frontmatter references `https://code.claude.com/docs/en/memory` but the file's `last_updated` is `2026-04-05`. The official URL `https://code.claude.com/docs/en/claude-md` returns 404 -- that page has been consolidated into `/memory`. | The `/claude-md` page no longer exists. All CLAUDE.md documentation is now at `/memory`. | Remove any references to `/claude-md` as a separate page. Update the source link to just `/memory`. |

### EXTRA (in CAB only -- may be valid CAB extension)

| # | CAB Content | Assessment |
|---|------------|------------|
| X1 | The entire "CAB-Specific Patterns" section (lines 201-229) including: Auto Memory + CAB State Management table, Seed Instruction Design guidance, and the framing of CLAUDE.md as "seed instructions." | **Valid CAB extension.** This is value-added content that connects CC's native memory system to CAB's state management patterns (notes/progress.md, notes/TODO.md). The "seed instruction" framing is good architectural guidance even though it's not in official docs. Keep as-is but ensure it's clearly labeled as CAB-specific rather than official CC behavior. |

---

## Verified Correct

### memory-claudemd.md

| Item | Status |
|------|--------|
| CLAUDE.md file locations: `./CLAUDE.md`, `.claude/CLAUDE.md`, `~/.claude/CLAUDE.md`, `./CLAUDE.local.md` | Correct -- matches official docs exactly |
| Managed CLAUDE.md locations: macOS `/Library/Application Support/ClaudeCode/CLAUDE.md`, Linux `/etc/claude-code/CLAUDE.md`, Windows `C:\Program Files\ClaudeCode\CLAUDE.md` | Correct |
| CLAUDE.local.md is auto-added to `.gitignore` | Correct -- official docs confirm `/init` configures git to ignore it |
| @imports syntax: relative files, relative paths, absolute paths with `~` | Correct |
| @imports: recursive with max depth 5 hops | Correct -- "maximum depth of five hops" |
| @imports: ignored inside code blocks | Correct -- official docs confirm this |
| @imports: missing files silently skipped | Correct -- official docs say resolved and loaded, with approval dialog for external imports; missing files are not explicitly discussed but silently skipped is consistent |
| `/memory` command to see what's loaded | Correct -- "lists all CLAUDE.md, CLAUDE.local.md, and rules files loaded" |
| Size recommendation: 200 lines per CLAUDE.md | Correct -- "target under 200 lines" |
| `.claude/rules/` directory: auto-loaded `.md` files, path scoping via `paths:` frontmatter | Correct -- matches exactly |
| Path scoping frontmatter uses `paths:` field with glob patterns | Correct |
| Rules without `paths` frontmatter loaded at launch with same priority as `.claude/CLAUDE.md` | Correct |
| HTML comments (`<!-- -->`) stripped from context; preserved in code blocks | Correct |
| `claudeMdExcludes` for monorepo exclusion | Correct |
| `/init` and `CLAUDE_CODE_NEW_INIT=1` for interactive multi-phase setup | Correct |
| `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` env var for `--add-dir` | Correct |
| AGENTS.md interop via `@AGENTS.md` import in CLAUDE.md | Correct |
| Auto memory location: `~/.claude/projects/<project>/memory/` | Correct |
| MEMORY.md: first 200 lines or 25KB loaded at session start | Correct -- "first 200 lines of MEMORY.md, or the first 25KB, whichever comes first" |
| Topic files loaded on-demand, not at startup | Correct |
| Retrieval is grep-based pattern matching, no semantic search | Correct (CC has grep/glob/read, not vector search) |
| CLAUDE.md survives all compaction stages (re-read from disk) | Correct -- "CLAUDE.md fully survives compaction. After /compact, Claude re-reads your CLAUDE.md from disk" |
| Auto memory survives compaction (re-read from disk) | Correct by extension (also loaded from disk at session start) |
| `InstructionsLoaded` hook for observability | Correct -- confirmed in hooks events list |
| Subagent memory: user scope at `~/.claude/agent-memory/`, project scope at `.claude/agent-memory/`, local scope at `.claude/agent-memory-local/` | Correct (but see M5 -- missing `<name-of-agent>/` subdirectory) |
| Subagent memory controlled by `memory:` frontmatter field | Correct -- `memory` field accepts `user`, `project`, or `local` |

### knowledge-base-structure.md

| Item | Status |
|------|--------|
| CC does not have built-in RAG/semantic search | Correct -- CC uses grep/glob/read filesystem tools |
| Retrieval flow: CLAUDE.md -> INDEX.md -> specific files | Correct as a CAB pattern (not an official CC mechanism, but accurately describes how CC discovers knowledge) |
| Three-level framework (Simple < 20, Structured 20-100, Scalable 100+) | Valid CAB extension -- not in official docs but reasonable organizational guidance |
| Atomic content principles (self-contained, single-purpose, well-named, sized 200-500 lines, metadata-rich) | Valid CAB extension |
| File metadata schema with frontmatter fields | Valid CAB extension -- CC has no official knowledge file schema |
| INDEX.md format with quick reference table | Valid CAB extension |
| Access patterns (direct @import, skill reference, on-demand, MCP query) | Correct -- aligns with CC's actual file access mechanisms |
| Anti-patterns (dump without INDEX, one huge file, vague filenames, skip metadata, assume semantic search) | Valid guidance consistent with CC behavior |

**Note on knowledge-base-structure.md**: This file is almost entirely a CAB-specific framework rather than documentation of official CC features. The official plugin docs describe a `skills/`, `agents/`, `commands/` structure but do NOT prescribe a `knowledge/` directory, INDEX.md conventions, or metadata schemas. This is expected -- the file is labeled `source: synthesized` and `confidence: A`. The key accuracy requirement is that its claims about CC's retrieval capabilities (grep-based, no semantic search) are correct, which they are. The `last_updated: 2025-12-12` and `review_by: 2026-03-12` suggest this file is overdue for review.

---

## Recommended Priority Actions

1. **HIGH** -- Fix E1 (precedence order inversion): Local > Project > User, not the reverse
2. **HIGH** -- Fix E2/E3/E4 (autoDream, extractMemories, memory categories): Mark as CAB-inferred or remove
3. **HIGH** -- Fix S1 (Runtime Memory Pipeline): Remove or caveat the specific numbers (5K, 13K, 50K, 60-min)
4. **MEDIUM** -- Add M1-M3 (autoMemoryEnabled, autoMemoryDirectory, version requirement)
5. **MEDIUM** -- Fix M5 (subagent memory paths missing `<name-of-agent>/` subdirectory)
6. **MEDIUM** -- Add M6 (walk-up directory loading behavior)
7. **LOW** -- Fix E5 (managed settings registry detail)
8. **LOW** -- Fix S2 (stale /claude-md URL reference)
9. **LOW** -- Update `knowledge-base-structure.md` metadata: `last_updated` and `review_by` are stale

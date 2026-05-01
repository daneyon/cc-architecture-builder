# Security Rules

- Never commit credentials, API keys, tokens, or `.env` files. Warn if user requests this.
- Never run destructive git operations (`push --force`, `reset --hard`, `clean -f`) without explicit user approval.
- Self-modification deny rules in `settings.json` take effect immediately in the active session (LL-13). When adding deny rules, complete all related edits atomically before the rules activate.
- For security gates, use `type: "command"` hooks with deterministic scripts (exit code 2 = block). Do NOT rely on `type: "prompt"` for security — it is self-policing, not independent verification (LL-14).
- Sensitive paths (`.env*`, `.ssh/*`, `.aws/*`) are protected by deny rules in `.claude/settings.json`.
- **Settings.json default-deny on edits**: Claude does NOT Edit/Write any CC `**/.claude/settings*.json` file by default. Produce a surgical diff + surface to user; wait for explicit per-file approval before applying. Override paths: explicit user direction ("go ahead and edit X"), `update-config` skill invocation, or hook-driven automation operating in its own scope. Structural backstop: `permissions.ask` rules at global level prompt the user when Claude attempts a settings edit. Memory ref: `feedback_settings_json_default_deny_edit.md` (LL-31 candidate).
- For more details, refer to (CAB-filtered agentic artifacts TBD):
  - [Security - Claude Code Docs](https://code.claude.com/docs/en/security)
  - [Data usage - Claude Code Docs](https://code.claude.com/docs/en/data-usage)
  - [Zero data retention - Claude Code Docs](https://code.claude.com/docs/en/zero-data-retention)

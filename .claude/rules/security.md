# Security Rules

- Never commit credentials, API keys, tokens, or `.env` files. Warn if user requests this.
- Never run destructive git operations (`push --force`, `reset --hard`, `clean -f`) without explicit user approval.
- Self-modification deny rules in `settings.json` take effect immediately in the active session (LL-13). When adding deny rules, complete all related edits atomically before the rules activate.
- For security gates, use `type: "command"` hooks with deterministic scripts (exit code 2 = block). Do NOT rely on `type: "prompt"` for security — it is self-policing, not independent verification (LL-14).
- Sensitive paths (`.env*`, `.ssh/*`, `.aws/*`) are protected by deny rules in `.claude/settings.json`.

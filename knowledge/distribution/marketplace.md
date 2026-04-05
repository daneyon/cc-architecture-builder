---
id: marketplace
title: Distribution & Marketplace
category: distribution
tags: [marketplace, distribution, sharing, github, team]
summary: Plugin distribution patterns including local testing, GitHub publication, team configuration, and security review workflows.
depends_on: [distributable-plugin]
related: [security-defaults]
complexity: intermediate
last_updated: 2026-04-05
estimated_tokens: 850
source: https://code.claude.com/docs/en/plugins, https://code.claude.com/docs/en/plugin-marketplaces
confidence: A
review_by: 2026-07-05
---

# Distribution & Marketplace

## Overview

Claude Code plugins can be distributed through marketplaces—catalogs of available plugins that users can browse and install.

## Distribution Flow

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  Development     │ ──▶ │  Local Testing   │ ──▶ │  Publication     │
│                  │     │                  │     │                  │
│  Create plugin   │     │  --plugin-dir    │     │  GitHub repo     │
│  Add components  │     │  plugin validate │     │  Marketplace     │
│  Write docs      │     │  Iterate         │     │  Team sharing    │
└──────────────────┘     └──────────────────┘     └──────────────────┘
```

## Local Testing Workflow

### 1. Create Marketplace Structure

```bash
mkdir dev-marketplace && cd dev-marketplace
mkdir -p .claude-plugin
```

### 2. Create Marketplace Manifest

```json
// .claude-plugin/marketplace.json
{
  "name": "dev-marketplace",
  "owner": {
    "name": "Developer"
  },
  "plugins": [
    {
      "name": "my-plugin",
      "source": "../my-plugin",
      "description": "Plugin under development"
    }
  ]
}
```

### 3. Add and Test

```bash
claude
/plugin marketplace add ./dev-marketplace
/plugin install my-plugin@dev-marketplace
```

## GitHub Distribution

### Repository Setup

```bash
# Create PRIVATE repo by default
gh repo create my-plugin --private --source=. --push

# Only make public after security review
gh repo edit my-plugin --visibility public
```

### Marketplace Manifest

```json
// marketplace.json
{
  "name": "org-plugins",
  "owner": {
    "name": "Organization Name",
    "email": "plugins@org.com"
  },
  "plugins": [
    {
      "name": "domain-assistant",
      "source": "./plugins/domain-assistant",
      "description": "Domain-specific assistant",
      "version": "1.0.0"
    }
  ]
}
```

## Marketplace Metadata

The marketplace manifest supports a top-level `metadata` object:

| Field | Type | Description |
|-------|------|-------------|
| `metadata.description` | string | Marketplace description |
| `metadata.version` | string | Marketplace schema version |
| `metadata.pluginRoot` | string | Default root path for relative plugin sources |

## Plugin Entry Schema

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Plugin identifier (kebab-case) |
| `source` | string/object | Where to fetch plugin |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | Brief description |
| `version` | string | Semantic version |
| `author` | object | Author info |
| `homepage` | string | Documentation URL |
| `license` | string | SPDX identifier |
| `keywords` | array | Discovery tags |
| `strict` | boolean | Controls whether `plugin.json` (false) or marketplace entry (true) is authority for component definitions. Default: `true` |
| `category` | string | Plugin category for marketplace browsing |
| `tags` | array | Additional discovery tags for marketplace search |

## Source Types

CC supports 5 plugin source types. The `source` field can be a string (shorthand) or an object (explicit type).

| Type | Fields | Use Case |
|------|--------|----------|
| Relative path | `"./plugins/my-plugin"` | Plugin within marketplace repo |
| `github` | `repo`, `ref?`, `sha?` | Public/private GitHub repos |
| `url` | `url`, `ref?`, `sha?` | Any git URL (GitLab, Bitbucket, self-hosted) |
| `git-subdir` | `url`, `path`, `ref?`, `sha?` | Sparse clone of a subdirectory within a git repo (monorepo pattern) |
| `npm` | `package`, `version?`, `registry?` | npm registry packages |

> **Note**: `hostPattern` and `pathPattern` exist only in `strictKnownMarketplaces` (managed settings restriction patterns for enterprise allowlisting). They are NOT plugin source types.

### String Shorthand

```json
{ "source": "./plugins/my-plugin" }
{ "source": "owner/plugin-repo" }
```

String sources are auto-detected: paths starting with `./` resolve as relative paths; `owner/repo` format resolves as GitHub.

### Explicit Examples

```json
{
  "source": { "source": "github", "repo": "owner/plugin-repo", "ref": "v1.0.0" }
}
```

```json
{
  "source": { "source": "git-subdir", "url": "https://github.com/org/monorepo", "path": "plugins/my-plugin" }
}
```

```json
{
  "source": { "source": "npm", "package": "@anthropic/skill-pack", "version": "^1.0.0" }
}
```

## Team Configuration

### Auto-Install Plugins

Configure in `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "team-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  },
  "enabledPlugins": [
    "domain-assistant@team-tools"
  ]
}
```

### Installation Scopes

| Scope | Location | Visibility |
|-------|----------|------------|
| **local** | Project-specific | Current project |
| **project** | `.claude/plugins/` | Team via git |
| **user** | `~/.claude/plugins/` | Personal, all projects |

## Security Review Workflow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Development    │ ──▶ │  Security       │ ──▶ │  Publication    │
│  (Private Repo) │     │  Review         │     │  (Public Repo)  │
│                 │     │                 │     │                 │
│  All work in    │     │  Run checklist  │     │  Manual release │
│  private        │     │  Remove secrets │     │  after verify   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Pre-Publication Checklist

- [ ] No API keys, tokens, or credentials
- [ ] No personal/client data in knowledge base
- [ ] `.gitignore` excludes sensitive files
- [ ] CLAUDE.md has no proprietary instructions
- [ ] All files reviewed for PII
- [ ] Dependencies audited for security
- [ ] Scripts have appropriate permissions

### Files to NEVER Commit

```
.env
*.key
*.pem
settings.local.json
CLAUDE.local.md
credentials.json
```

## CLI Commands

### Interactive (inside Claude Code session)

```bash
/plugin marketplace add owner/repo
/plugin install plugin-name@marketplace
/plugin list
/plugin remove plugin-name
```

### Non-Interactive (from terminal)

```bash
claude plugin marketplace add <source>     # Register a marketplace
claude plugin marketplace list             # List registered marketplaces
claude plugin marketplace remove <name>    # Remove a marketplace
claude plugin marketplace update [name]    # Update marketplace plugin cache

claude plugin install <plugin> [-s scope]  # Install plugin
claude plugin uninstall <plugin> [-s scope] [--keep-data]
claude plugin enable <plugin> [-s scope]
claude plugin disable <plugin> [-s scope]
claude plugin update <plugin> [-s scope]
claude plugin validate                     # Validate plugin structure
```

### Local Development Testing

```bash
# Test plugin locally without installing (bypasses cache)
claude --plugin-dir ./my-plugin

# Validate plugin structure
claude plugin validate
```

## Managed Controls (Enterprise)

Organizations can enforce marketplace policies via managed settings (precedence level 1 — cannot be overridden by users):

| Setting | Scope | Description |
|---------|-------|-------------|
| `strictKnownMarketplaces` | Managed only | Allowlist with `hostPattern`/`pathPattern` entries restricting which marketplace sources users can add |
| `blockedMarketplaces` | Managed only | Blocklist checked before download; blocked sources never touch filesystem |
| `pluginTrustMessage` | Managed only | Custom message appended to plugin trust warning before installation |
| `extraKnownMarketplaces` | Any | Pre-register marketplaces; prompts team on folder trust |
| `enabledPlugins` | Any | Plugins auto-installed for all users |
| `disabledPlugins` | Any | Plugins blocked from installation |

```json
{
  "strictKnownMarketplaces": true,
  "extraKnownMarketplaces": {
    "corp-tools": {
      "source": { "source": "github", "repo": "corp/claude-plugins" }
    }
  },
  "blockedMarketplaces": ["untrusted-source"],
  "enabledPlugins": ["security-scanner@corp-tools"]
}
```

Deploy via managed settings (MDM/plist on macOS, registry on Windows, `/etc/claude/` on Linux). See [Global User Config](../schemas/global-user-config.md) for delivery mechanisms.

## Best Practices

1. **Private by default**: Always start with private repos
2. **Version properly**: Use semantic versioning
3. **Document thoroughly**: Include README, setup guide
4. **Security review**: Run checklist before public release
5. **Test locally first**: Use local marketplace during development

## See Also

- [Security Defaults](../prerequisites/security-defaults.md)
- [Distributable Plugin Schema](../schemas/distributable-plugin.md)
- [Official Documentation](https://code.claude.com/docs/en/plugins)

---
id: custom-commands
title: Custom Commands
category: components
tags: [commands, slash-commands, user-invoked, shortcuts]
summary: User-invoked shortcuts triggered by typing /command-name. Can execute instructions, reference files, run bash commands, or combine multiple actions.
depends_on: [memory-claudemd]
related: [agent-skills, subagents]
complexity: foundational
last_updated: 2025-12-12
estimated_tokens: 600
---

# Custom Commands

## Overview

Commands are **user-invoked** shortcuts triggered by typing `/command-name`. Unlike skills (model-invoked), commands require explicit user action.

## Key Distinction

| Aspect | Commands | Skills |
|--------|----------|--------|
| **Invocation** | User types `/command` | Model decides automatically |
| **Discovery** | Listed in `/help` | Metadata in system prompt |
| **Trigger** | Explicit request | Task context matching |
| **Complexity** | Simple shortcuts | Complex capabilities |

## File Structure

**Location**: `commands/` directory

```
commands/
├── analyze.md
├── summarize.md
└── deploy.md
```

## Command File Format

```markdown
---
description: Brief description shown in /help
allowed-tools: Read, Write, Bash    # Optional: restrict tools
thinking: extended                   # Optional: enable extended thinking
---

# Command Instructions

Clear instructions for what Claude should do when this command is invoked.

## Steps
1. [Step 1]
2. [Step 2]

## Arguments
This command accepts: $ARGUMENTS
```

## Command Types by Location

| Type | Location | Scope |
|------|----------|-------|
| **Project** | `.claude/commands/` | Current project only |
| **Personal** | `~/.claude/commands/` | All your projects |
| **Plugin** | `plugin/commands/` | When plugin installed |

## Features

### Arguments

Commands can accept arguments:

```markdown
# analyze.md

Analyze the following: $ARGUMENTS

Individual arguments:
- First: $1
- Second: $2
- Third: $3
```

**Usage**: `/analyze security authentication flow`

### File References

Reference files directly in command:

```markdown
Analyze the code in @src/main.py
Compare with @tests/test_main.py
```

### Bash Execution

Execute bash and include output:

```markdown
Current branch: !git branch --show-current!
Recent commits: !git log --oneline -5!
```

### Extended Thinking

Enable for complex commands:

```yaml
---
thinking: extended
---
```

## Namespacing

Commands from different sources use namespacing:

| Source | Pattern | Example |
|--------|---------|---------|
| Plugin | `/plugin-name:command` | `/deploy-tools:staging` |
| Project | `/project:command` | `/project:build` |
| Personal | `/user:command` | `/user:my-shortcut` |

## Example: Code Analysis Command

```markdown
---
description: Analyze code for quality, security, and performance issues
allowed-tools: Read, Grep, Glob
---

# Code Analysis

Perform comprehensive code analysis on: $ARGUMENTS

## Analysis Steps

1. **Read the target files**
   - If directory provided, identify key files
   - If file provided, read contents

2. **Quality Analysis**
   - Check naming conventions
   - Evaluate code structure
   - Assess documentation

3. **Security Scan**
   - Look for hardcoded credentials
   - Check input validation
   - Identify injection vulnerabilities

4. **Performance Review**
   - Identify potential bottlenecks
   - Check for N+1 queries
   - Evaluate algorithmic complexity

## Output Format

Provide analysis as:
- **Summary**: Overall assessment
- **Issues Found**: Prioritized list
- **Recommendations**: Actionable improvements
```

## Example: Quick Deploy Command

```markdown
---
description: Deploy current branch to staging environment
allowed-tools: Bash
---

# Quick Deploy

## Pre-flight Checks
Current branch: !git branch --show-current!
Uncommitted changes: !git status --porcelain!

## Deploy Steps

1. Verify we're on a feature branch (not main/master)
2. Run tests: `npm test`
3. Build: `npm run build`
4. Deploy: `npm run deploy:staging`

## Post-Deploy

- Provide deployment URL
- List any warnings from build
```

## Best Practices

1. **Clear descriptions**: Shown in `/help`, make them scannable
2. **Appropriate tool restrictions**: Limit to necessary tools
3. **Handle missing arguments**: Provide guidance if args expected but missing
4. **Document usage**: Include example invocations in description
5. **Keep focused**: One command = one action

## See Also

- [Agent Skills](agent-skills.md) — Model-invoked alternative
- [Subagents](subagents.md) — Delegated specialized tasks
- [Official Documentation](https://code.claude.com/docs/en/slash-commands)

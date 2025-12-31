#!/usr/bin/env python3
"""
Claude Code Starter Kit - Master Setup Script (Python Version)
Version 1.0
This script sets up your Claude Code environment with all configurations
"""

import os
import sys
import shutil
from pathlib import Path
import argparse

# ANSI color codes for Windows terminal
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    GRAY = '\033[90m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

def print_color(text, color):
    """Print colored text"""
    print(f"{color}{text}{Colors.RESET}")

def create_directory_safe(path):
    """Create directory if it doesn't exist"""
    path_obj = Path(path)
    if not path_obj.exists():
        path_obj.mkdir(parents=True, exist_ok=True)
        print_color(f"✓ Created: {path}", Colors.GREEN)
    else:
        print_color(f"  Exists: {path}", Colors.GRAY)

def create_file_with_content(path, content):
    """Create file with given content"""
    path_obj = Path(path)
    path_obj.parent.mkdir(parents=True, exist_ok=True)
    path_obj.write_text(content, encoding='utf-8')
    print_color(f"✓ Created: {path}", Colors.GREEN)

def main():
    parser = argparse.ArgumentParser(description='Claude Code Starter Kit Setup')
    parser.add_argument(
        '--claude-code-root',
        default=r'C:\Users\daniel.kang\Desktop\Automoto\Claude_Code',
        help='Root directory for Claude Code projects'
    )
    parser.add_argument(
        '--kb-source',
        default='',
        help='Path to your CustomLLMRepo/Prompts directory'
    )
    parser.add_argument(
        '--skip-kb-copy',
        action='store_true',
        help='Skip copying knowledge base (manual step)'
    )
    
    args = parser.parse_args()
    
    claude_code_root = args.claude_code_root
    kb_source = args.kb_source
    skip_kb_copy = args.skip_kb_copy
    
    print_color("=" * 50, Colors.CYAN)
    print_color("Claude Code Starter Kit Setup", Colors.CYAN)
    print_color("=" * 50, Colors.CYAN)
    print()
    
    # Get user home directory
    home = Path.home()
    global_claude = home / '.claude'
    
    # Step 1: Create Global Directory Structure
    print_color("Step 1: Creating Global Directory Structure", Colors.YELLOW)
    print_color("-" * 50, Colors.YELLOW)
    
    create_directory_safe(global_claude)
    create_directory_safe(global_claude / 'knowledge-base')
    create_directory_safe(global_claude / 'knowledge-base' / 'coding')
    create_directory_safe(global_claude / 'knowledge-base' / 'strategy')
    create_directory_safe(global_claude / 'knowledge-base' / 'summarization')
    create_directory_safe(global_claude / 'knowledge-base' / 'character-base')
    create_directory_safe(global_claude / 'skills')
    create_directory_safe(global_claude / 'agents')
    
    print()
    
    # Step 2: Create Skills Directory Structure
    print_color("Step 2: Creating Skills Directory Structure", Colors.YELLOW)
    print_color("-" * 50, Colors.YELLOW)
    
    skills = [
        'readme-generator',
        'architecture-analyzer',
        'token-optimizer'
    ]
    
    for skill in skills:
        create_directory_safe(global_claude / 'skills' / skill)
    
    print()
    
    # Step 3: Create Project Root Structure
    print_color("Step 3: Creating Project Root Structure", Colors.YELLOW)
    print_color("-" * 50, Colors.YELLOW)
    
    project_root = Path(claude_code_root)
    create_directory_safe(project_root)
    create_directory_safe(project_root / 'templates')
    create_directory_safe(project_root / 'templates' / 'python-automation')
    create_directory_safe(project_root / 'templates' / 'python-automation' / '.claude')
    create_directory_safe(project_root / 'templates' / 'python-automation' / '.claude' / 'skills')
    create_directory_safe(project_root / 'templates' / 'python-automation' / '.claude' / 'agents')
    create_directory_safe(project_root / 'templates' / 'python-automation' / 'src')
    create_directory_safe(project_root / 'templates' / 'python-automation' / 'tests')
    create_directory_safe(project_root / 'templates' / 'python-automation' / 'docs')
    
    print()
    
    # Step 4: Copy Knowledge Base
    print_color("Step 4: Copying Knowledge Base (Optional)", Colors.YELLOW)
    print_color("-" * 50, Colors.YELLOW)
    
    if not skip_kb_copy and kb_source:
        kb_source_path = Path(kb_source)
        if kb_source_path.exists():
            print(f"Copying knowledge base from: {kb_source}")
            kb_dest = global_claude / 'knowledge-base'
            try:
                for item in kb_source_path.iterdir():
                    dest_item = kb_dest / item.name
                    if item.is_dir():
                        shutil.copytree(item, dest_item, dirs_exist_ok=True)
                    else:
                        shutil.copy2(item, dest_item)
                print_color("✓ Knowledge base copied successfully", Colors.GREEN)
            except Exception as e:
                print_color(f"⚠ Error copying knowledge base: {e}", Colors.RED)
        else:
            print_color(f"⚠ Knowledge base source not found: {kb_source}", Colors.YELLOW)
            print_color(f"  You can copy it manually later to: {global_claude / 'knowledge-base'}", Colors.GRAY)
    else:
        print_color("  Skipped knowledge base copy (manual step required)", Colors.GRAY)
        print_color(f"  Copy your KB to: {global_claude / 'knowledge-base'}", Colors.GRAY)
    
    print()
    
    # Step 5: Create Configuration Files
    print_color("Step 5: Creating Configuration Files", Colors.YELLOW)
    print_color("-" * 50, Colors.YELLOW)
    
    # Global settings.json
    global_settings_content = """{
  "model": "claude-sonnet-4-5-20250929",
  "allowedTools": {
    "bash": "ask",
    "edit": "ask",
    "write": "ask",
    "read": "auto_approve",
    "list_dir": "auto_approve",
    "search": "auto_approve",
    "grep": "auto_approve",
    "glob": "auto_approve"
  },
  "environmentVariables": {
    "ANTHROPIC_LOG": "info",
    "CLAUDE_CODE_DISABLE_TELEMETRY": "true",
    "PYTHONPATH": "${workspaceFolder}/src"
  },
  "subagentModel": "claude-sonnet-4-5-20250929"
}"""
    
    create_file_with_content(global_claude / 'settings.json', global_settings_content)
    
    # Global CLAUDE.md placeholder
    global_claude_md_content = """# Claude Code - Software Architect & Systems Analyst

## Instructions
This is a placeholder. Please download the complete CLAUDE.md from the starter kit
and place it in this location: ~/.claude/CLAUDE.md

The complete file contains:
- Core identity and philosophical approach
- Communication standards
- Technical philosophy
- Documentation standards
- Token management patterns
- Problem-solving methodology
- Strategic frameworks
- Implementation planning references

File location in starter kit: Artifact ID: global-claude-md
"""
    
    create_file_with_content(global_claude / 'CLAUDE.md', global_claude_md_content)
    
    print()
    
    # Step 6: Create Placeholder Files for Skills
    print_color("Step 6: Creating Placeholder Files for Skills", Colors.YELLOW)
    print_color("-" * 50, Colors.YELLOW)
    
    skill_placeholder = """---
name: {skill_name_title}
description: [Description - download complete version from starter kit]
---

# {skill_name_title}

This is a placeholder. Download the complete skill from the starter kit and replace this file.

Starter kit artifact ID: {artifact_id}
"""
    
    skill_artifacts = {
        'readme-generator': 'readme-generator-skill',
        'architecture-analyzer': 'architecture-analyzer-skill',
        'token-optimizer': 'token-optimizer-skill'
    }
    
    for skill in skills:
        skill_path = global_claude / 'skills' / skill / 'SKILL.md'
        skill_name_title = skill.replace('-', ' ').title()
        artifact_id = skill_artifacts.get(skill, f'{skill}-skill')
        content = skill_placeholder.format(
            skill_name_title=skill_name_title,
            artifact_id=artifact_id
        )
        create_file_with_content(skill_path, content)
    
    print()
    
    # Step 7: Create Placeholder Files for Subagents
    print_color("Step 7: Creating Placeholder Files for Subagents", Colors.YELLOW)
    print_color("-" * 50, Colors.YELLOW)
    
    subagents = [
        'code-reviewer',
        'debugger-specialist',
        'performance-optimizer'
    ]
    
    subagent_placeholder = """---
name: {agent_name}
description: [Description - download complete version from starter kit]
---

# {agent_name_title} Subagent

This is a placeholder. Download the complete subagent from the starter kit and replace this file.

Starter kit artifact ID: {artifact_id}
"""
    
    subagent_artifacts = {
        'code-reviewer': 'code-reviewer-subagent',
        'debugger-specialist': 'debugger-specialist-subagent',
        'performance-optimizer': 'performance-optimizer-subagent'
    }
    
    for agent in subagents:
        agent_path = global_claude / 'agents' / f'{agent}.md'
        agent_name_title = agent.replace('-', ' ').title()
        artifact_id = subagent_artifacts.get(agent, f'{agent}-subagent')
        content = subagent_placeholder.format(
            agent_name=agent,
            agent_name_title=agent_name_title,
            artifact_id=artifact_id
        )
        create_file_with_content(agent_path, content)
    
    print()
    
    # Step 8: Create Project Template Files
    print_color("Step 8: Creating Project Template Files", Colors.YELLOW)
    print_color("-" * 50, Colors.YELLOW)
    
    # Project template CLAUDE.md
    project_claude_md_content = """# Project: [PROJECT_NAME]

*Replace [PROJECT_NAME] with your actual project name*
*Run `/init` in Claude Code to have Claude populate this template*

## Project Overview

### Purpose
[Brief description of what this project does]

### Key Components
[List main classes/modules]

### Technology Stack
- Python 3.x
- [Key libraries]

## Project-Specific Instructions

### Architecture Pattern
This project follows a class-based modular architecture with:
- Single-file implementation during development
- Easy separation into package structure when needed
- AI agent analysis and debugging support
- Human oversight and intervention points

### Development Workflow
1. Component-based development with independent testing
2. Incremental delivery with validation checkpoints
3. Comprehensive error handling and logging
4. Performance monitoring and optimization

### Code Conventions
[Project-specific conventions]

### Critical Files & Locations
[Let Claude discover and document these during /init]

## Current Focus

### Active Tasks
- [ ] [Task 1]
- [ ] [Task 2]

### Recent Changes
[Claude will maintain this section]

### Next Steps
[Claude will maintain this section]

## Global Knowledge Base
This project inherits global coding practices from ~/.claude/CLAUDE.md
"""
    
    create_file_with_content(
        project_root / 'templates' / 'python-automation' / 'CLAUDE.md',
        project_claude_md_content
    )
    
    # Project template settings.json
    project_settings_content = """{
  "allowedTools": {
    "bash": "ask",
    "edit": "ask",
    "write": "ask",
    "read": "auto_approve",
    "list_dir": "auto_approve",
    "search": "auto_approve",
    "grep": "auto_approve",
    "glob": "auto_approve"
  },
  "hooks": {
    "beforeEdit": [
      {
        "name": "backup_before_edit",
        "command": "Copy-Item ${FILE} ${FILE}.backup",
        "enabled": true
      }
    ],
    "afterEdit": [
      {
        "name": "format_python",
        "command": "black ${FILE}",
        "pattern": "\\\\.py$",
        "enabled": false,
        "description": "Auto-format with Black (enable when ready)"
      },
      {
        "name": "type_check_python",
        "command": "mypy ${FILE}",
        "pattern": "\\\\.py$",
        "enabled": false,
        "description": "Type check with mypy (enable when ready)"
      }
    ]
  }
}"""
    
    create_file_with_content(
        project_root / 'templates' / 'python-automation' / '.claude' / 'settings.json',
        project_settings_content
    )
    
    # Project .gitignore
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
*.egg-info/
dist/
build/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Claude Code
.claude/settings.local.json
CLAUDE.local.md
*.backup

# OS
.DS_Store
Thumbs.db

# Project specific
*.log
temp/
output/
"""
    
    create_file_with_content(
        project_root / 'templates' / 'python-automation' / '.gitignore',
        gitignore_content
    )
    
    # Template README
    template_readme_content = """# Python Automation Project Template

This template provides a structured starting point for Python automation projects using Claude Code.

## Structure

```
project-name/
├── .claude/                  # Claude Code configuration
│   ├── settings.json        # Project settings
│   ├── skills/              # Project-specific skills
│   └── agents/              # Project-specific subagents
├── CLAUDE.md                # Project memory
├── src/                     # Source code
├── tests/                   # Test files
├── docs/                    # Documentation
├── .gitignore
└── README.md
```

## Getting Started

1. Copy this template to your project location
2. Navigate to project directory
3. Run `claude`
4. Use `/init` to populate CLAUDE.md
5. Start development!

## Next Steps

- Replace this README with project-specific content
- Update CLAUDE.md with project context
- Add project-specific skills/subagents as needed
- Configure hooks in .claude/settings.json
"""
    
    create_file_with_content(
        project_root / 'templates' / 'python-automation' / 'README.md',
        template_readme_content
    )
    
    print()
    
    # Step 9: Create Helper Scripts
    print_color("Step 9: Creating Helper Scripts", Colors.YELLOW)
    print_color("-" * 50, Colors.YELLOW)
    
    # New project script (Python version)
    new_project_script_content = '''#!/usr/bin/env python3
"""Create new Claude Code project from template"""

import sys
import shutil
from pathlib import Path
import argparse

def main():
    parser = argparse.ArgumentParser(description='Create new Claude Code project')
    parser.add_argument('project_name', help='Name of the new project')
    parser.add_argument(
        '--project-root',
        default=r'C:\\Users\\daniel.kang\\Desktop\\Automoto\\Claude_Code',
        help='Root directory for projects'
    )
    
    args = parser.parse_args()
    
    project_root = Path(args.project_root)
    template_path = project_root / 'templates' / 'python-automation'
    new_project_path = project_root / args.project_name
    
    if new_project_path.exists():
        print(f"Error: Project already exists at {new_project_path}")
        sys.exit(1)
    
    print(f"Creating new project: {args.project_name}")
    
    try:
        shutil.copytree(template_path, new_project_path)
        print(f"✓ Project created successfully at {new_project_path}")
        print()
        print("Next steps:")
        print(f"  1. cd {new_project_path}")
        print("  2. claude")
        print("  3. Run: /init to populate CLAUDE.md")
        print("  4. Start coding!")
    except Exception as e:
        print(f"Error creating project: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
'''
    
    create_file_with_content(
        project_root / 'new-project.py',
        new_project_script_content
    )
    
    print()
    
    # Final Summary
    print_color("=" * 50, Colors.CYAN)
    print_color("Setup Complete!", Colors.CYAN)
    print_color("=" * 50, Colors.CYAN)
    print()
    
    print_color("✓ Directory structure created", Colors.GREEN)
    print_color("✓ Configuration files created", Colors.GREEN)
    print_color("✓ Project template ready", Colors.GREEN)
    print_color("✓ Helper scripts created", Colors.GREEN)
    print()
    
    print_color("Important Next Steps:", Colors.YELLOW)
    print()
    print_color("1. Download Complete Files from Starter Kit:", Colors.WHITE)
    print(f"   - Global CLAUDE.md → {global_claude / 'CLAUDE.md'}")
    print(f"   - All skill SKILL.md files → {global_claude / 'skills' / '[skill-name]' / 'SKILL.md'}")
    print(f"   - All subagent .md files → {global_claude / 'agents' / '[agent-name].md'}")
    print()
    
    if skip_kb_copy or not kb_source:
        print_color("2. Copy Your Knowledge Base:", Colors.WHITE)
        print("   Copy your CustomLLMRepo\\Prompts content to:")
        print(f"   {global_claude / 'knowledge-base'}")
        print()
    
    print_color("3. Install Claude Code CLI:", Colors.WHITE)
    print("   npm install -g @anthropic-ai/claude-code")
    print()
    
    print_color("4. Authenticate Claude Code:", Colors.WHITE)
    print("   claude")
    print("   (Follow OAuth flow or configure API key)")
    print()
    
    print_color("5. Install VS Code Extension:", Colors.WHITE)
    print("   Search 'Claude Code' in VS Code Extensions")
    print()
    
    print_color("6. Create Your First Project:", Colors.WHITE)
    print(f"   cd {project_root}")
    print("   python new-project.py my-first-project")
    print()
    
    print_color("Files Created:", Colors.CYAN)
    print(f"  Global Config: {global_claude}")
    print(f"  Project Root: {project_root}")
    print(f"  Templates: {project_root / 'templates'}")
    print(f"  Helper Scripts: {project_root / 'new-project.py'}")
    print()
    
    print_color("For complete documentation, see:", Colors.CYAN)
    print("  Claude_Code_Architecture_Guide.md")
    print()

if __name__ == '__main__':
    main()

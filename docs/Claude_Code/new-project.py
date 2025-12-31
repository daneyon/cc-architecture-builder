#!/usr/bin/env python3
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
        default=r'C:\Users\daniel.kang\Desktop\Automoto\Claude_Code',
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

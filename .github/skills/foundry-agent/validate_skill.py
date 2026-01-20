#!/usr/bin/env python3
"""
Validate GitHub Copilot Skill Format

This script validates that the SKILL.md file follows the correct format:
- Has valid YAML frontmatter with required fields
- Name matches directory name and format requirements
- Description meets length requirements
- All referenced files exist
"""

import os
import re
import sys
from pathlib import Path


def validate_yaml_frontmatter(content: str) -> dict:
    """Extract and validate YAML frontmatter."""
    # Check if content starts with ---
    if not content.startswith('---\n'):
        print("✗ Error: SKILL.md must start with YAML frontmatter (---)")
        return None
    
    # Extract frontmatter
    parts = content.split('---\n', 2)
    if len(parts) < 3:
        print("✗ Error: Invalid YAML frontmatter format")
        return None
    
    yaml_content = parts[1]
    
    # Parse YAML manually (simple parsing, not full YAML)
    metadata = {}
    current_key = None
    
    for line in yaml_content.split('\n'):
        line = line.rstrip()
        if not line:
            continue
            
        # Check for indented metadata
        if line.startswith('  '):
            if current_key == 'metadata':
                key_val = line.strip().split(':', 1)
                if len(key_val) == 2:
                    if 'metadata' not in metadata or not isinstance(metadata['metadata'], dict):
                        metadata['metadata'] = {}
                    metadata['metadata'][key_val[0].strip()] = key_val[1].strip()
        else:
            key_val = line.split(':', 1)
            if len(key_val) == 2:
                key = key_val[0].strip()
                value = key_val[1].strip()
                if key == 'metadata':
                    metadata[key] = {}
                    current_key = key
                else:
                    metadata[key] = value
                    current_key = key
    
    return metadata


def validate_name(name: str, dir_name: str) -> bool:
    """Validate the skill name."""
    # Check length
    if len(name) < 1 or len(name) > 64:
        print(f"✗ Error: Name must be 1-64 characters, got {len(name)}")
        return False
    
    # Check format (lowercase, hyphens)
    if not re.match(r'^[a-z0-9-]+$', name):
        print(f"✗ Error: Name must be lowercase letters, numbers, and hyphens only")
        return False
    
    # Check matches directory name
    if name != dir_name:
        print(f"✗ Error: Name '{name}' must match directory name '{dir_name}'")
        return False
    
    print(f"✓ Name is valid: {name}")
    return True


def validate_description(description: str) -> bool:
    """Validate the skill description."""
    # Check length
    if len(description) < 10 or len(description) > 1024:
        print(f"✗ Error: Description must be 10-1024 characters, got {len(description)}")
        return False
    
    # Check not empty
    if not description.strip():
        print("✗ Error: Description cannot be empty")
        return False
    
    print(f"✓ Description is valid ({len(description)} characters)")
    return True


def validate_referenced_files(skill_dir: Path, content: str) -> bool:
    """Check that referenced files exist."""
    # Look for file references in the markdown
    file_patterns = [
        r'\*\*File:\*\*\s+`([^`]+)`',  # **File:** `filename`
        r'see\s+`([^`]+)`',             # see `filename`
        r'included\s+`([^`]+)`',        # included `filename`
    ]
    
    referenced_files = set()
    for pattern in file_patterns:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            referenced_files.add(match.group(1))
    
    missing_files = []
    for file_ref in referenced_files:
        file_path = skill_dir / file_ref
        if not file_path.exists():
            missing_files.append(file_ref)
    
    if missing_files:
        print(f"✗ Error: Referenced files not found: {', '.join(missing_files)}")
        return False
    
    if referenced_files:
        print(f"✓ All {len(referenced_files)} referenced files exist")
    
    return True


def main():
    """Main validation function."""
    print("Validating GitHub Copilot Skill Format")
    print("=" * 60)
    
    # Get skill directory
    script_dir = Path(__file__).parent
    skill_md_path = script_dir / "SKILL.md"
    
    if not skill_md_path.exists():
        print(f"✗ Error: SKILL.md not found at {skill_md_path}")
        sys.exit(1)
    
    # Read SKILL.md
    with open(skill_md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Validate YAML frontmatter
    print("\nValidating YAML frontmatter...")
    metadata = validate_yaml_frontmatter(content)
    if not metadata:
        sys.exit(1)
    
    # Check required fields
    required_fields = ['name', 'description']
    for field in required_fields:
        if field not in metadata:
            print(f"✗ Error: Required field '{field}' missing from frontmatter")
            sys.exit(1)
    
    print(f"✓ YAML frontmatter is valid")
    print(f"  - name: {metadata['name']}")
    print(f"  - description: {metadata['description'][:50]}...")
    if 'license' in metadata:
        print(f"  - license: {metadata['license']}")
    
    # Validate name
    print("\nValidating name...")
    dir_name = script_dir.name
    if not validate_name(metadata['name'], dir_name):
        sys.exit(1)
    
    # Validate description
    print("\nValidating description...")
    if not validate_description(metadata['description']):
        sys.exit(1)
    
    # Check markdown body exists
    print("\nValidating markdown body...")
    parts = content.split('---\n', 2)
    markdown_body = parts[2] if len(parts) >= 3 else ''
    
    if len(markdown_body.strip()) < 100:
        print("✗ Error: Markdown body is too short (should contain usage instructions)")
        sys.exit(1)
    
    print(f"✓ Markdown body exists ({len(markdown_body)} characters)")
    
    # Validate referenced files
    print("\nValidating referenced files...")
    if not validate_referenced_files(script_dir, content):
        sys.exit(1)
    
    # Check for example files
    print("\nChecking for example files...")
    example_files = [
        'example_python.py',
        'example_typescript.ts',
        'requirements.txt',
        'package.json',
        '.env.example'
    ]
    
    for example_file in example_files:
        file_path = script_dir / example_file
        if file_path.exists():
            print(f"  ✓ {example_file}")
        else:
            print(f"  ⚠ {example_file} (optional, but recommended)")
    
    # Summary
    print("\n" + "=" * 60)
    print("✓ Skill validation passed!")
    print("=" * 60)
    print("\nYour GitHub Copilot skill is properly formatted and ready to use.")
    print(f"\nSkill name: {metadata['name']}")
    print(f"Location: .github/skills/{dir_name}/")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

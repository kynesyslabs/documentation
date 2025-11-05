#!/usr/bin/env python3
"""
Generate/Update SUMMARY.md for GitBook documentation.
Preserves existing structure and adds missing files intelligently.
"""

import os
import re
from pathlib import Path
from typing import List, Set, Dict, Tuple


def extract_title_from_file(filepath: Path) -> str:
    """Extract title from markdown file's first heading or use filename."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # Look for first # heading
            match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if match:
                return match.group(1).strip()
    except Exception as e:
        print(f"Warning: Could not read {filepath}: {e}")

    # Fallback to filename
    name = filepath.stem
    if name == 'README':
        # Use parent directory name for README files
        parent_name = filepath.parent.name
        return parent_name.replace('-', ' ').replace('_', ' ').title()
    return name.replace('-', ' ').replace('_', ' ').title()


def should_skip_file(filepath: Path) -> bool:
    """Determine if a file should be skipped."""
    skip_files = {'SUMMARY.md', '.gitbook'}
    skip_patterns = {'.git/', 'node_modules/', '.github/'}

    if filepath.name in skip_files:
        return True

    for pattern in skip_patterns:
        if pattern in str(filepath):
            return True

    return False


def find_all_markdown_files(root_dir: Path) -> Set[Path]:
    """Find all markdown files in the repository."""
    md_files = set()

    for md_file in root_dir.rglob('*.md'):
        if should_skip_file(md_file):
            continue
        # Store relative path
        rel_path = md_file.relative_to(root_dir)
        md_files.add(rel_path)

    return md_files


def extract_existing_files(summary_content: str) -> Set[Path]:
    """Extract all files currently referenced in SUMMARY.md."""
    existing_files = set()

    # Match markdown links: [title](path.md)
    pattern = r'\[.+?\]\((.+?\.md)\)'
    matches = re.findall(pattern, summary_content)

    for match in matches:
        # Skip external URLs
        if match.startswith('http://') or match.startswith('https://'):
            continue
        existing_files.add(Path(match))

    return existing_files


def group_files_by_section(files: Set[Path]) -> Dict[str, List[Path]]:
    """Group files by their top-level directory."""
    grouped = {
        'root': [],
        'introduction': [],
        'cookbook': [],
        'sdk': [],
        'backend': [],
        'frontend': [],
        'other': []
    }

    for file_path in sorted(files):
        if len(file_path.parts) == 1:
            grouped['root'].append(file_path)
        else:
            section = file_path.parts[0].lower()
            if section in grouped:
                grouped[section].append(file_path)
            else:
                grouped['other'].append(file_path)

    return grouped


def format_file_entry(file_path: Path, root_dir: Path, indent: int = 0) -> str:
    """Format a file entry for SUMMARY.md."""
    full_path = root_dir / file_path
    title = extract_title_from_file(full_path)
    indent_str = "  " * indent
    return f"{indent_str}* [{title}]({file_path})"


def find_insertion_point(lines: List[str], section: str) -> Tuple[int, int]:
    """
    Find the best insertion point for a section.
    Returns (start_index, indent_level)
    """
    section_patterns = {
        'introduction': [r'^\* \[Introduction\]', r'introduction/'],
        'cookbook': [r'^## Cookbook', r'cookbook/'],
        'sdk': [r'^## SDK', r'sdk/'],
        'backend': [r'^## Backend', r'backend/'],
        'frontend': [r'^## Frontend', r'frontend/']
    }

    patterns = section_patterns.get(section.lower(), [])

    for i, line in enumerate(lines):
        for pattern in patterns:
            if re.search(pattern, line):
                # Find the end of this section
                current_indent = len(line) - len(line.lstrip())
                j = i + 1
                while j < len(lines):
                    next_line = lines[j]
                    if next_line.strip() == '':
                        j += 1
                        continue
                    if next_line.startswith('## '):
                        # Found next major section
                        return (j - 1, current_indent)
                    if next_line.startswith('* ') and (len(next_line) - len(next_line.lstrip())) == 0:
                        # Found next top-level item
                        return (j - 1, current_indent)
                    j += 1
                return (len(lines), current_indent)

    # If section not found, add at the end
    return (len(lines), 0)


def add_missing_files_to_summary(
    summary_content: str,
    missing_files: Set[Path],
    root_dir: Path
) -> str:
    """Add missing files to SUMMARY.md while preserving structure."""
    if not missing_files:
        return summary_content

    lines = summary_content.split('\n')
    grouped = group_files_by_section(missing_files)

    # Add files by section
    for section, files in grouped.items():
        if not files:
            continue

        if section == 'root':
            # Add root files near the top (after Introduction)
            insert_idx, indent = find_insertion_point(lines, 'introduction')
            for file_path in sorted(files):
                entry = format_file_entry(file_path, root_dir, 0)
                lines.insert(insert_idx, entry)
                insert_idx += 1
        else:
            # Find or create section
            insert_idx, base_indent = find_insertion_point(lines, section)

            # Group by subdirectory
            subdir_files = {}
            for file_path in files:
                if len(file_path.parts) > 1:
                    subdir = file_path.parts[1] if len(file_path.parts) > 1 else ''
                    if subdir not in subdir_files:
                        subdir_files[subdir] = []
                    subdir_files[subdir].append(file_path)

            # Add files grouped by subdirectory
            new_lines = []
            for subdir, subdir_file_list in sorted(subdir_files.items()):
                if subdir and len(subdir_file_list) > 0:
                    # Check if we should add a section for this subdirectory
                    first_file = subdir_file_list[0]
                    if first_file.parts[-1] == 'README.md':
                        # Add README first
                        new_lines.append(format_file_entry(first_file, root_dir, 0))
                        # Add other files indented
                        for f in subdir_file_list[1:]:
                            new_lines.append(format_file_entry(f, root_dir, 1))
                    else:
                        # Add all files
                        for f in subdir_file_list:
                            new_lines.append(format_file_entry(f, root_dir, 1))

            # Insert new lines
            for i, new_line in enumerate(new_lines):
                lines.insert(insert_idx + i, new_line)

    return '\n'.join(lines)


def update_summary(root_dir: Path) -> Tuple[str, int]:
    """
    Update SUMMARY.md with missing files.
    Returns (updated_content, number_of_files_added)
    """
    summary_path = root_dir / 'SUMMARY.md'

    # Read existing SUMMARY.md
    if summary_path.exists():
        with open(summary_path, 'r', encoding='utf-8') as f:
            summary_content = f.read()
    else:
        # Create new SUMMARY.md
        summary_content = "# Table of contents\n\n* [Introduction](README.md)\n"

    # Find all markdown files
    all_files = find_all_markdown_files(root_dir)

    # Extract files already in SUMMARY.md
    existing_files = extract_existing_files(summary_content)

    # Find missing files
    missing_files = all_files - existing_files

    if not missing_files:
        return summary_content, 0

    print(f"Found {len(missing_files)} missing file(s):")
    for f in sorted(missing_files):
        print(f"  + {f}")

    # Add missing files
    updated_content = add_missing_files_to_summary(summary_content, missing_files, root_dir)

    return updated_content, len(missing_files)


def main():
    """Main entry point."""
    # Get repository root
    repo_root = Path(__file__).parent.parent.parent

    print(f"Updating SUMMARY.md for: {repo_root}")
    print()

    # Update summary
    updated_content, num_added = update_summary(repo_root)

    if num_added > 0:
        # Write SUMMARY.md
        summary_path = repo_root / "SUMMARY.md"
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        print()
        print(f"✓ SUMMARY.md updated successfully!")
        print(f"  Added {num_added} file(s)")
    else:
        print("✓ SUMMARY.md is already up to date!")
        print("  No files needed to be added")


if __name__ == "__main__":
    main()

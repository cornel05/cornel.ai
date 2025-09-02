#!/usr/bin/env python3
"""
Script to insert text after the # symbol in the first H1 heading in all Jupyter notebooks in a specified directory.
Usage: python append_text.py <path_to_notebooks> <text_to_insert>
"""

import os
import sys
import json
import argparse
from pathlib import Path

def find_and_modify_first_h1(notebook_data, text_to_insert):
    """Find the first H1 heading in markdown cells and insert text after the # symbol."""
    
    for cell in notebook_data.get('cells', []):
        if cell.get('cell_type') == 'markdown':
            source = cell.get('source', [])
            
            # Convert source to list if it's a string
            if isinstance(source, str):
                source = source.splitlines(keepends=True)
            
            # Look for H1 heading (starts with # but not ##)
            for i, line in enumerate(source):
                stripped_line = line.strip()
                if stripped_line.startswith('# ') and not stripped_line.startswith('## '):
                    # Found first H1 heading - insert text after the # symbol
                    # Extract the original title (everything after "# ")
                    original_title = stripped_line[2:]  # Remove "# "
                    
                    # Check if text is already present
                    if original_title.startswith(text_to_insert):
                        return False
                    
                    # Create new heading: # <text_to_insert> <original_title>
                    new_heading = f"# {text_to_insert} {original_title}"
                    
                    # Preserve original line ending
                    if line.endswith('\n'):
                        new_heading += '\n'
                    
                    source[i] = new_heading
                    cell['source'] = source
                    return True
    
    return False

def process_notebook(notebook_path, text_to_insert):
    """Process a single notebook file."""
    try:
        print(f"Processing: {notebook_path}")
        
        # Read the notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook_data = json.load(f)
        
        # Find and modify the first H1 heading
        if find_and_modify_first_h1(notebook_data, text_to_insert):
            # Write back the modified notebook
            with open(notebook_path, 'w', encoding='utf-8') as f:
                json.dump(notebook_data, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Modified H1 heading in: {notebook_path}")
            return True
        else:
            print(f"⚠ No H1 heading found in: {notebook_path}")
            return False
            
    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON in notebook: {notebook_path}")
        print(f"Error: {str(e)}")
        return False
    except Exception as e:
        print(f"✗ Error processing: {notebook_path}")
        print(f"Error: {str(e)}")
        return False

def find_notebooks(directory):
    """Find all .ipynb files in the given directory and subdirectories."""
    notebook_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.ipynb') and not file.startswith('.'):
                # Skip checkpoint files
                if '.ipynb_checkpoints' not in root:
                    notebook_files.append(Path(root) / file)
    return notebook_files

def main():
    parser = argparse.ArgumentParser(
        description='Insert text after the # symbol in the first H1 heading in all Jupyter notebooks in a directory',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python append_text.py /path/to/notebooks "pandas:"
  python append_text.py . "Updated -"
  python append_text.py ~/notebooks "🐍"
        """
    )
    parser.add_argument(
        'path', 
        help='Path to directory containing notebooks'
    )
    parser.add_argument(
        'text',
        help='Text to insert after the # symbol in the first H1 heading'
    )
    parser.add_argument(
        '--dry-run', '-n',
        action='store_true',
        help='Show what would be changed without actually modifying files'
    )
    
    args = parser.parse_args()
    
    # Validate path
    if not os.path.exists(args.path):
        print(f"Error: Path '{args.path}' does not exist.")
        sys.exit(1)
    
    if not os.path.isdir(args.path):
        print(f"Error: '{args.path}' is not a directory.")
        sys.exit(1)
    
    # Find all notebooks
    print(f"Searching for notebooks in: {args.path}")
    notebooks = find_notebooks(args.path)
    
    if not notebooks:
        print("No Jupyter notebooks found in the specified directory.")
        sys.exit(0)
    
    print(f"Found {len(notebooks)} notebook(s):")
    for nb in notebooks:
        print(f"  - {nb}")
    
    if args.dry_run:
        print(f"\nDRY RUN: Would insert '{args.text}' after # in first H1 heading in each notebook")
        print("Use without --dry-run to actually modify the files.")
        sys.exit(0)
    
    print(f"\nInserting '{args.text}' after # in first H1 heading in each notebook...")
    
    # Process each notebook
    successful = 0
    no_h1_found = 0
    failed = 0
    
    for notebook in notebooks:
        try:
            result = process_notebook(notebook, args.text)
            if result:
                successful += 1
            else:
                no_h1_found += 1
        except Exception:
            failed += 1
    
    # Summary
    print(f"\nProcessing complete!")
    print(f"Successfully modified: {successful}")
    print(f"No H1 heading found: {no_h1_found}")
    print(f"Failed: {failed}")
    print(f"Total notebooks: {len(notebooks)}")
    
    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
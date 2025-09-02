#!/usr/bin/env python3
"""
Script to clean the first cell of Jupyter notebooks by removing blank lines and "Extracted from" text.
Usage: python clean_notebook_headers.py <directory_path>
"""

import argparse
import json
import os
import sys
import re
from pathlib import Path

def clean_first_cell(notebook_path):
    """Clean the first cell by removing blank lines and 'Extracted from' text."""
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        # Check if notebook has cells
        if 'cells' not in notebook or len(notebook['cells']) == 0:
            print(f"Skipping {notebook_path}: No cells found")
            return False
        
        first_cell = notebook['cells'][0]
        
        # Check if first cell has source content
        if 'source' not in first_cell:
            print(f"Skipping {notebook_path}: First cell has no source")
            return False
        
        # Get the source content (can be string or list of strings)
        source = first_cell['source']
        original_source = source.copy() if isinstance(source, list) else source
        
        # Convert to string if it's a list
        if isinstance(source, list):
            source_text = ''.join(source)
        else:
            source_text = source
        
        # Remove "Extracted from ..." lines (case insensitive)
        # This pattern matches lines that start with "Extracted from" and end with .ipynb
        source_text = re.sub(r'^Extracted from .*\.ipynb.*$', '', source_text, flags=re.MULTILINE | re.IGNORECASE)
        
        # Split into lines for processing
        lines = source_text.split('\n')
        
        # Remove empty lines and lines with only whitespace
        cleaned_lines = []
        for line in lines:
            if line.strip():  # Keep non-empty lines
                cleaned_lines.append(line)
        
        # Join back and ensure proper formatting
        cleaned_text = '\n'.join(cleaned_lines)
        
        # Add final newline if the original had content
        if cleaned_lines:
            cleaned_text += '\n'
        
        # Convert back to list format if original was a list
        if isinstance(original_source, list):
            if cleaned_text.strip():
                # Split by lines and preserve the list format
                lines = cleaned_text.split('\n')
                if lines and lines[-1] == '':
                    lines.pop()  # Remove empty last line
                first_cell['source'] = [line + '\n' for line in lines] if lines else []
            else:
                first_cell['source'] = []
        else:
            first_cell['source'] = cleaned_text
        
        # Check if any changes were made
        if original_source == first_cell['source']:
            print(f"No changes needed for {notebook_path}")
            return False
        
        # Write back to file
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=2, ensure_ascii=False)
        
        print(f"Cleaned {notebook_path}")
        return True
        
    except json.JSONDecodeError as e:
        print(f"Error reading {notebook_path}: Invalid JSON - {e}")
        return False
    except Exception as e:
        print(f"Error processing {notebook_path}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Clean first cell of Jupyter notebooks by removing blank lines and 'Extracted from' text"
    )
    parser.add_argument(
        "directory", 
        help="Directory path containing Jupyter notebooks"
    )
    parser.add_argument(
        "-r", "--recursive", 
        action="store_true",
        help="Search for notebooks recursively in subdirectories"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without actually modifying files"
    )
    
    args = parser.parse_args()
    
    # Validate directory path
    directory_path = Path(args.directory)
    if not directory_path.exists():
        print(f"Error: Directory '{args.directory}' does not exist")
        sys.exit(1)
    
    if not directory_path.is_dir():
        print(f"Error: '{args.directory}' is not a directory")
        sys.exit(1)
    
    # Find all notebook files
    if args.recursive:
        notebook_files = list(directory_path.rglob("*.ipynb"))
    else:
        notebook_files = list(directory_path.glob("*.ipynb"))
    
    if not notebook_files:
        print(f"No Jupyter notebook files found in '{args.directory}'")
        sys.exit(0)
    
    print(f"Found {len(notebook_files)} notebook(s)")
    print("Will remove:")
    print("  - Blank lines from first cell")
    print("  - Lines containing 'Extracted from *.ipynb'")
    if args.dry_run:
        print("  - DRY RUN MODE: No files will be modified")
    print("-" * 50)
    
    # Process each notebook
    updated_count = 0
    for notebook_file in notebook_files:
        if args.dry_run:
            # For dry run, just analyze without modifying
            try:
                with open(notebook_file, 'r', encoding='utf-8') as f:
                    notebook = json.load(f)
                
                if 'cells' in notebook and len(notebook['cells']) > 0:
                    first_cell = notebook['cells'][0]
                    if 'source' in first_cell:
                        source = first_cell['source']
                        source_text = ''.join(source) if isinstance(source, list) else source
                        
                        # Check if it contains "Extracted from" or empty lines
                        if re.search(r'^Extracted from .*\.ipynb.*$', source_text, re.MULTILINE | re.IGNORECASE) or '\n\n' in source_text:
                            print(f"Would clean: {notebook_file}")
                            updated_count += 1
                        else:
                            print(f"No changes needed: {notebook_file}")
            except Exception as e:
                print(f"Error analyzing {notebook_file}: {e}")
        else:
            if clean_first_cell(notebook_file):
                updated_count += 1
    
    print("-" * 50)
    print(f"Processed {len(notebook_files)} notebook(s)")
    if args.dry_run:
        print(f"Would update {updated_count} notebook(s)")
    else:
        print(f"Updated {updated_count} notebook(s)")

if __name__ == "__main__":
    main()
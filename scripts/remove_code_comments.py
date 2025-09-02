#!/usr/bin/env python3
"""
Script to remove specific comment lines from the first code cell of Jupyter notebooks.
Usage: python remove_code_comments.py <directory_path>
"""

import argparse
import json
import os
import sys
from pathlib import Path

def remove_comments_from_first_code_cell(notebook_path):
    """Remove specific comment lines from the first code cell of a Jupyter notebook."""
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        # Check if notebook has cells
        if 'cells' not in notebook or len(notebook['cells']) == 0:
            print(f"Skipping {notebook_path}: No cells found")
            return False
        
        # Find the first code cell
        first_code_cell = None
        first_code_cell_index = None
        
        for i, cell in enumerate(notebook['cells']):
            if cell.get('cell_type') == 'code':
                first_code_cell = cell
                first_code_cell_index = i
                break
        
        if first_code_cell is None:
            print(f"Skipping {notebook_path}: No code cells found")
            return False
        
        # Check if code cell has source content
        if 'source' not in first_code_cell:
            print(f"Skipping {notebook_path}: First code cell has no source")
            return False
        
        # Get the source content (can be string or list of strings)
        source = first_code_cell['source']
        original_source = source.copy() if isinstance(source, list) else source
        
        # Convert to string if it's a list
        if isinstance(source, list):
            source_text = ''.join(source)
        else:
            source_text = source
        
        # Split into lines for processing
        lines = source_text.split('\n')
        
        # Remove the specific comment lines
        filtered_lines = []
        changes_made = False
        
        for line in lines:
            stripped_line = line.strip()
            
            # Check if line matches the comments to remove
            if (stripped_line.startswith('# Add code/examples relevant to this topic here.') or
                stripped_line.startswith('# Original section heading:')):
                changes_made = True
                continue  # Skip this line
            else:
                filtered_lines.append(line)
        
        if not changes_made:
            print(f"No target comments found in {notebook_path}")
            return False
        
        # Join back the lines
        updated_source = '\n'.join(filtered_lines)
        
        # Convert back to list format if original was a list
        if isinstance(original_source, list):
            # Split by lines and preserve the list format
            if updated_source:
                lines = updated_source.split('\n')
                # Handle the newline formatting to match Jupyter's format
                if lines and lines[-1] == '':
                    lines.pop()  # Remove empty last line
                first_code_cell['source'] = [line + '\n' for line in lines[:-1]] + [lines[-1]] if lines else []
            else:
                first_code_cell['source'] = []
        else:
            first_code_cell['source'] = updated_source
        
        # Write back to file
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=2, ensure_ascii=False)
        
        print(f"Removed comments from {notebook_path}")
        return True
        
    except json.JSONDecodeError as e:
        print(f"Error reading {notebook_path}: Invalid JSON - {e}")
        return False
    except Exception as e:
        print(f"Error processing {notebook_path}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Remove specific comment lines from the first code cell of Jupyter notebooks"
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
    print("Will remove these comment lines from first code cell:")
    print("  - '# Add code/examples relevant to this topic here.'")
    print("  - '# Original section heading: ...'")
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
                
                # Find first code cell
                first_code_cell = None
                for cell in notebook.get('cells', []):
                    if cell.get('cell_type') == 'code':
                        first_code_cell = cell
                        break
                
                if first_code_cell and 'source' in first_code_cell:
                    source = first_code_cell['source']
                    source_text = ''.join(source) if isinstance(source, list) else source
                    
                    # Check if it contains the target comments
                    if ('# Add code/examples relevant to this topic here.' in source_text or
                        '# Original section heading:' in source_text):
                        print(f"Would clean: {notebook_file}")
                        updated_count += 1
                    else:
                        print(f"No target comments: {notebook_file}")
                else:
                    print(f"No code cell found: {notebook_file}")
            except Exception as e:
                print(f"Error analyzing {notebook_file}: {e}")
        else:
            if remove_comments_from_first_code_cell(notebook_file):
                updated_count += 1
    
    print("-" * 50)
    print(f"Processed {len(notebook_files)} notebook(s)")
    if args.dry_run:
        print(f"Would update {updated_count} notebook(s)")
    else:
        print(f"Updated {updated_count} notebook(s)")

if __name__ == "__main__":
    main()
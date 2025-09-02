#!/usr/bin/env python3
"""
Script to prepend text to the filenames of all Jupyter notebooks in a specified directory.
Usage: python prepend_filename.py <path_to_notebooks> <text_to_prepend>
"""

import os
import sys
import argparse
from pathlib import Path

def rename_notebook(notebook_path, text_to_prepend):
    """Rename a single notebook file by prepending text to its filename."""
    try:
        # Get the directory and filename
        directory = notebook_path.parent
        original_filename = notebook_path.name
        
        # Check if the text is already prepended
        if original_filename.startswith(text_to_prepend):
            print(f"⚠ Already has prefix '{text_to_prepend}': {original_filename}")
            return False
        
        # Create new filename
        new_filename = f"{text_to_prepend}{original_filename}"
        new_path = directory / new_filename
        
        # Check if new filename already exists
        if new_path.exists():
            print(f"✗ Target filename already exists: {new_filename}")
            return False
        
        # Rename the file
        notebook_path.rename(new_path)
        print(f"✓ Renamed: {original_filename} → {new_filename}")
        return True
        
    except Exception as e:
        print(f"✗ Error renaming {notebook_path.name}: {str(e)}")
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
        description='Prepend text to the filenames of all Jupyter notebooks in a directory',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python prepend_filename.py /path/to/notebooks "01_"
  python prepend_filename.py . "pandas_"
  python prepend_filename.py ~/notebooks "updated_"
  python prepend_filename.py . "lesson1_" --dry-run
        """
    )
    parser.add_argument(
        'path', 
        help='Path to directory containing notebooks'
    )
    parser.add_argument(
        'text',
        help='Text to prepend to notebook filenames'
    )
    parser.add_argument(
        '--dry-run', '-n',
        action='store_true',
        help='Show what would be renamed without actually renaming files'
    )
    parser.add_argument(
        '--recursive', '-r',
        action='store_true',
        default=True,
        help='Search for notebooks recursively in subdirectories (default: True)'
    )
    
    args = parser.parse_args()
    
    # Validate path
    if not os.path.exists(args.path):
        print(f"Error: Path '{args.path}' does not exist.")
        sys.exit(1)
    
    if not os.path.isdir(args.path):
        print(f"Error: '{args.path}' is not a directory.")
        sys.exit(1)
    
    # Validate text input
    if not args.text:
        print("Error: Text to prepend cannot be empty.")
        sys.exit(1)
    
    # Check for invalid filename characters
    invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    if any(char in args.text for char in invalid_chars):
        print(f"Error: Text contains invalid filename characters: {invalid_chars}")
        sys.exit(1)
    
    # Find all notebooks
    print(f"Searching for notebooks in: {args.path}")
    notebooks = find_notebooks(args.path)
    
    if not notebooks:
        print("No Jupyter notebooks found in the specified directory.")
        sys.exit(0)
    
    print(f"Found {len(notebooks)} notebook(s):")
    for nb in notebooks:
        print(f"  - {nb.name}")
    
    if args.dry_run:
        print(f"\nDRY RUN: Would prepend '{args.text}' to notebook filenames:")
        for notebook in notebooks:
            original_name = notebook.name
            if original_name.startswith(args.text):
                print(f"  ⚠ {original_name} (already has prefix)")
            else:
                new_name = f"{args.text}{original_name}"
                print(f"  {original_name} → {new_name}")
        print("\nUse without --dry-run to actually rename the files.")
        sys.exit(0)
    
    print(f"\nPrepending '{args.text}' to notebook filenames...")
    
    # Rename each notebook
    successful = 0
    skipped = 0
    failed = 0
    
    for notebook in notebooks:
        result = rename_notebook(notebook, args.text)
        if result:
            successful += 1
        elif notebook.name.startswith(args.text):
            skipped += 1
        else:
            failed += 1
    
    # Summary
    print(f"\nRenaming complete!")
    print(f"Successfully renamed: {successful}")
    print(f"Skipped (already has prefix): {skipped}")
    print(f"Failed: {failed}")
    print(f"Total notebooks: {len(notebooks)}")
    
    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Script to execute all cells in all Jupyter notebooks in a specified directory.
Usage: python execute_notebooks.py <path_to_notebooks>
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

def execute_notebook(notebook_path):
    """Execute a single Jupyter notebook using nbconvert."""
    try:
        print(f"Executing: {notebook_path}")
        
        # Use jupyter nbconvert to execute the notebook
        result = subprocess.run([
            'jupyter', 'nbconvert', 
            '--to', 'notebook',
            '--execute',
            '--inplace',
            str(notebook_path)
        ], capture_output=True, text=True, check=True)
        
        print(f"✓ Successfully executed: {notebook_path}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to execute: {notebook_path}")
        print(f"Error: {e.stderr}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error with: {notebook_path}")
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
        description='Execute all Jupyter notebooks in a specified directory'
    )
    parser.add_argument(
        'path', 
        help='Path to directory containing notebooks'
    )
    parser.add_argument(
        '--recursive', '-r',
        action='store_true',
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
    
    # Find all notebooks
    print(f"Searching for notebooks in: {args.path}")
    notebooks = find_notebooks(args.path)
    
    if not notebooks:
        print("No Jupyter notebooks found in the specified directory.")
        sys.exit(0)
    
    print(f"Found {len(notebooks)} notebook(s):")
    for nb in notebooks:
        print(f"  - {nb}")
    
    print("\nStarting execution...")
    
    # Execute each notebook
    successful = 0
    failed = 0
    
    for notebook in notebooks:
        if execute_notebook(notebook):
            successful += 1
        else:
            failed += 1
    
    # Summary
    print(f"\nExecution complete!")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total: {len(notebooks)}")
    
    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
import nbformat
import os
import sys

def add_tags_to_notebook(nb_path, tags_to_add):
    nb = nbformat.read(nb_path, as_version=4)
    changed = False
    for cell in nb.cells:
        if cell.cell_type == "code":
            tags = cell.get("metadata", {}).get("tags", [])
            for tag in tags_to_add:
                if tag not in tags:
                    tags.append(tag)
                    cell.setdefault("metadata", {})["tags"] = tags
                    changed = True
    if changed:
        nbformat.write(nb, nb_path)
        print(f"Updated: {nb_path}")

def process_all_notebooks(root_dir, tags_to_add):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".ipynb"):
                nb_path = os.path.join(dirpath, filename)
                add_tags_to_notebook(nb_path, tags_to_add)

def main():
    root_dir = "/home/dcornel/code/AI Learning Labs/notebooks"
    tags_to_add = ["hide_output", "scroll-output"]

    if len(sys.argv) != 2:
        print("Usage: python add_metadata_tags.py [all|notebook_name.ipynb]")
        sys.exit(1)

    arg = sys.argv[1]
    if arg == "all":
        process_all_notebooks(root_dir, tags_to_add)
    else:
        # Search for the notebook by name in the directory tree
        found = False
        for dirpath, _, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename == arg:
                    nb_path = os.path.join(dirpath, filename)
                    add_tags_to_notebook(nb_path, tags_to_add)
                    found = True
        if not found:
            print(f"Notebook '{arg}' not found in {root_dir}")

if __name__ == "__main__":
    main()
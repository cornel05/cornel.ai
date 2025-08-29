import nbformat
import os

root_dir = "/home/dcornel/code/AI Learning Labs/notebooks"

for dirpath, _, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith(".ipynb"):
            nb_path = os.path.join(dirpath, filename)
            nb = nbformat.read(nb_path, as_version=4)
            changed = False
            for cell in nb.cells:
                if cell.cell_type == "code":
                    tags = cell.get("metadata", {}).get("tags", [])
                    if "hide_output" not in tags:
                        tags.append("hide_output")
                        cell.setdefault("metadata", {})["tags"] = tags
                        changed = True
            if changed:
                nbformat.write(nb, nb_path)
                print(f"Updated: {nb_path}")
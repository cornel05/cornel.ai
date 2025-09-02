import nbformat
from pathlib import Path
import re
import sys

STOPWORDS = {
    "a","an","the","to","for","of","and","with","from","by","w","w/","manually"
}

def slugify(heading: str, prefix="pandas_"):
    # Remove trailing punctuation like ':'.
    heading = heading.strip().rstrip(":").lower()
    # Remove parenthetical content but keep inside words appended later if needed
    # Here we keep words inside parentheses by replacing () with space.
    heading = re.sub(r"[()]", " ", heading)
    # Split into words
    words = re.split(r"[^a-z0-9]+", heading)
    cleaned = [w for w in words if w and w not in STOPWORDS]
    if not cleaned:
        cleaned = ["section"]
    slug = "_".join(cleaned)
    # Collapse multiple underscores
    slug = re.sub(r"_+", "_", slug)
    return f"{prefix}{slug}.ipynb"

def extract_level2_headings(nb):
    headings = []
    for cell in nb.cells:
        if cell.get("cell_type") == "markdown":
            lines = cell.get("source", "").splitlines()
            for line in lines:
                if line.startswith("## "):  # level-2 only
                    # Exclude lines starting with ### (already filtered) and keep text after ##
                    text = line[3:].strip()
                    if text: 
                        headings.append(text)
    return headings

def build_notebook(heading_text, source_notebook):
    nb_new = nbformat.v4.new_notebook()
    nb_new.cells.append(
        nbformat.v4.new_markdown_cell(f"# {heading_text}")
    )
    return nb_new

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/generate_section_notebooks.py <source_notebook> [<output_dir>]")
        sys.exit(1)
    source_path = Path(sys.argv[1])
    if not source_path.is_file():
        print(f"Source notebook not found: {source_path}")
        sys.exit(1)
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else source_path.parent / "sections"
    out_dir.mkdir(parents=True, exist_ok=True)

    nb = nbformat.read(source_path, as_version=4)
    headings = extract_level2_headings(nb)

    created = []
    for h in headings:
        filename = slugify(h)
        new_nb = build_notebook(h, source_path)
        target = out_dir / filename
        nbformat.write(new_nb, target)
        created.append((h, target.name))

    print("Generated notebooks:")
    for h, f in created:
        print(f"  {h} -> {f}")

if __name__ == "__main__":
    main()
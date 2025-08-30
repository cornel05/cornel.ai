# AI Learning Labs

[![Read the Book](https://img.shields.io/badge/Read%20the%20Book-live-brightgreen.svg)](https://cornel05.github.io/cornel.ai/)
[![Build](https://github.com/cornel05/cornel.ai/actions/workflows/pages.yml/badge.svg)](https://github.com/cornel05/cornel.ai/actions)

Explore the notebooks with a clean, nbviewer-like UI:

- 📘 **Classification** → [open chapter](https://cornel05.github.io/cornel.ai/notebooks/classification/index.html)
- 📈 **Regression** → [open chapter](https://cornel05.github.io/cornel.ai/notebooks/regression/index.html)
- 🧮 **Optimization** → [open chapter](https://cornel05.github.io/cornel.ai/notebooks/optimization/index.html)
- 👁️ **Computer Vision** → [open chapter](https://cornel05.github.io/cornel.ai/notebooks/computer_vision/index.html)
- 🐼 **Pandas** → [open chapter](https://cornel05.github.io/cornel.ai/notebooks/pandas/index.html)
- 🐍 **Python Snippets** → [open chapter](https://cornel05.github.io/cornel.ai/notebooks/python_snippets/index.html)

> The site rebuilds automatically on every push to `main`.

## Local Development

Install dependencies (from project root):

```bash
pip install -r requirements.txt
```

Build the site locally:

```bash
sphinx-build -b html . _build/html
```

Preview:

```bash
python -m http.server -d _build/html
```

## Repository Structure

```
notebooks/
  classification/
  regression/
  optimization/
  computer_vision/
  pandas/
  python_snippets/
_build/
  html/
    index.html
    ...
  _static/
  _images/
  ...
README.md
requirements.txt
conf.py
index.rst
```

## Adding New Notebook Sections

1. Place notebooks under `notebooks/<new_section>/`.
2. Add the section to `index.rst` under the toctree.
3. Commit & push to `main` to trigger a rebuild.
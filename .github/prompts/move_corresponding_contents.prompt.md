---
mode: edit
---
For the notebook `{notebook_path}`, identify headings that match files in `{snippets_dir}`. Extract the relevant markdown and code cells from the notebook and insert them into the corresponding files. Simply transfer the cells while preserving the original heading order and cell sequence from the notebook. Add a dataset import cell (including their accompanying markdown with dataset links) to the beginning of each notebook, positioned after the initial imports. Ensure each notebook remains valid and executable.

- `{notebook_path}`: Target notebook file path (e.g., `basic_pandas_2.ipynb`)
- `{snippets_dir}`: Source directory for snippet files (e.g., `notebooks/snippets/pandas/new`)
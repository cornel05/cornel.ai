# -- Project info -----------------------------------------------------
project = "cornel.ai"
author = "cornel"
extensions = [
    "myst_nb",            # render .ipynb and MyST markdown
    "sphinx_copybutton",  # copy code buttons
]
nb_execution_mode = "off"        # don't execute notebooks on CI; just render
nb_render_text_lexer = "python"  # fallback for text cells
nb_output_stderr = "remove"     # hide stderr outputs

# -- HTML -------------------------------------------------------------
html_theme = "pydata_sphinx_theme"
html_title = "AI Learning Labs"
html_static_path = ["_static"]

# Optional: a touch of nice defaults without bloat
html_theme_options = {
    "show_prev_next": False,
    "navigation_depth": 2,
}

# Keep paths simple: put source files at repo root
import os, sys
sys.path.insert(0, os.path.abspath("."))

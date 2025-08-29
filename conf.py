# -- Project info -----------------------------------------------------
project = "cornel.ai"
author = "cornel"
extensions = [
    "myst_nb",            # render .ipynb and MyST markdown
    "sphinx_copybutton",  # copy code buttons
    "sphinx.ext.mathjax", # math rendering
    "sphinx_design",   # design blocks
]
nb_execution_mode = "off"        # don't execute notebooks on CI; just render
# nb_render_text_lexer = "python"  # fallback for text cells
nb_output_stderr = "show"     # hide stderr outputs
nb_execution_show_tb = True  # show traceback on errors

# -- HTML -------------------------------------------------------------
html_theme = "pydata_sphinx_theme"
html_title = "AI Learning Labs"
html_logo = "_static/logo.png"
html_favicon = "_static/logo.png"
html_static_path = ["_static"]
html_css_files = [
    "css/landing_page.css",
    "css/date.css",
    "css/footer.css"
]
html_context = {
    "default_mode": "light",
    "github_user": "cornel05",
    "github_repo": "cornel.ai",
    "github_version": "main",
}
html_theme_options = {
    "show_prev_next": True,
    "navigation_depth": 2,
    "show_nav_level": 1,
    "logo": {
        "text": "cornel.ai",
        "image": "_static/logo.png",
    },
    "navbar_align": "left",  # use underscore
    "navbar_start": ["navbar-logo"],
    "navbar_center": ["navbar-nav"],
    "navbar_end": ["theme-switcher", "navbar-icon-links"],
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/cornel05/AI-Learning-Labs",
            "icon": "fa-brands fa-github"
        },
        {
            "name": "Twitter",
            "url": "https://x.com/dcornel05",
            "icon": "fa-brands fa-twitter"
        },
        {
            "name": "LinkedIn",
            "url": "https://www.linkedin.com/in/cornel-ai",
            "icon": "fa-brands fa-linkedin"
        }
    ],
    "footer_start": ["copyright"],
    "footer_center": ["sphinx-version"],
    "footer_end": ["theme-version"]
}

# MathJax settings -----------------------------------------------------------
# Use a CDN to load MathJax faster
mathjax_path = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"

# Sphinx settings -------------------------------------------------------------
sphinx ={}

# MyST extensions --------------------------------------------------------------
myst_enable_extensions = [
    "dollarmath",
    "amsmath", 
    "deflist",
    "html_admonition",
    "html_image",
    "colon_fence",
    "smartquotes",
    "replacements",
    "linkify",
    "substitution"
]

# Copyright info -----------------------------------------------------
copyright = "2025, cornel @ AI Learning Labs"

# Keep paths simple: put source files at repo root
import os, sys
sys.path.insert(0, os.path.abspath("."))

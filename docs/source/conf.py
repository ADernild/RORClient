# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Setting sys.path for sphinx to locate modules ---------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#ensuring-the-code-can-be-imported
import os
import sys

# Add the Django project to the python path
sys.path.insert(0, os.path.abspath("../"))


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "RORClient"
copyright = "2025, Alexander Dernild"
author = "Alexander Dernild"
release = "0.1.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_book_theme"
html_static_path = ["_static"]
pygments_style = "sphinx"

# -- Setting default options for autodoc -------------------------------------

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": False,
    "attribute-order": "bysource",
    "member-order": "bysource",
}

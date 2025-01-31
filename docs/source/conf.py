import os
import sys

sys.path.insert(0, os.path.abspath('../../src'))  # Adjust this path if needed


# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'gitHubAirflow'
copyright = '2025, Kristof Farago'
author = 'Kristof Farago'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["myst_parser", "sphinx.ext.autodoc"]
myst_heading_anchors = 3
templates_path = ['_templates']
exclude_patterns = []
source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
autodoc_typehints = "both"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

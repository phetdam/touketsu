# configuration file for the Sphinx documentation builder.
#
# modified by Derek Huang for touketsu project.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
#
# Changelog:
#
# 07-02-2020
#
# make change to autodoc_default_options to not include undocumented members
# plus correct missing assignment of _delim (used - instead of = oops). added
# html_logo option to point to new (kind of sh*tty) logo. also add option for
# sphinx_rtd_theme to change sidebar header color (looks more ice-like).
#
# 06-30-2020
#
# initial creation by sphinx-quickstart. added changelog, autodoc, autosummary,
# and intersphinx configuration. added read the docs theme setup.

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
from os.path import dirname, abspath
import sys
# change delimiter style based on whether system os NT or POSIX
_delim = "/"
if os.name == "nt": _delim = "\\"
# back up two directory levels with correct delimiters
sys.path.insert(0, _delim.join(dirname(abspath(__file__)).split(_delim)[:-2]))


# -- Project information -----------------------------------------------------

project = "touketsu"
copyright = "2020, Derek Huang"
author = "Derek Huang"

# The full version, including alpha/beta/rc tags
release = "0.1.0"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your own.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx"
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -- autodoc configuration ---------------------------------------------------

# set default options for autodoc directives. include __repr__ special member
# and any private members (names prepended with _), show class inheritance.
#
# note: since ignore-module-all is not set, only the members in __all__ in
# __init__.py will be looked for and their order will be maintained. since
# undoc-members was not specified, members with no docstring are skipped.
autodoc_default_options = {
    "members": True,
    "private-members": True,
    "show-inheritance": True,
    "special-members": "__repr__"
}

# -- autosummary configuration -----------------------------------------------

# set to True to generate stub files for any modules named in a file's
# autosummary directive(s). so far, only index.rst should have autosummary.
autosummary_generate = True

# -- intersphinx configuration -----------------------------------------------

# determines which external package documentations to link to. this package has
# no dependencies, so the intersphinx config is really easy.
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None)
}

# -- Options for HTML output -------------------------------------------------

# html theme (my favorite theme); register as extension
html_theme = "sphinx_rtd_theme"
extensions.append(html_theme)

# no HTML theme options
html_theme_options = {
    # color for the sidebar navigation header
    "style_nav_header_background": "#a2c4cd"
}

# file for image to be used in sidebar logo (must not exceed 200 px in width)
html_logo = "./touketsu_logo.png"

# use emacs style for pygments highlighting in code blocks or inline code
pygments_style = "emacs"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

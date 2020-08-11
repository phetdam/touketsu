# configuration file for the Sphinx documentation builder.
#
# modified by Derek Huang for touketsu project.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- read the docs setup -----------------------------------------------------

import os
# boolean for whether or not we are building on read the docs
_ON_RTD = os.environ.get("READTHEDOCS") == "True"

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

from os.path import dirname, abspath
import sys
# change delimiter style based on whether system os NT or POSIX
_delim = "/"
if os.name == "nt": _delim = "\\"
# back up two directory levels with correct delimiters
_PROJECT_ROOT = _delim.join(dirname(abspath(__file__)).split(_delim)[:-2])
# don't insert if on read the docs
sys.path.insert(0, _PROJECT_ROOT)

# -- Project information -----------------------------------------------------

project = "touketsu"
copyright = "2020, Derek Huang"
author = "Derek Huang"

# The full version, including alpha/beta/rc tags (get from ../../VERSION)
with open(_PROJECT_ROOT + _delim + "VERSION", "r") as vf:
    release = vf.read().rstrip()
# version, which we set equal to release
version = release

# -- General configuration ---------------------------------------------------

# specifiy minimum sphinx version (3)
needs_sphinx = "3.0"

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

# html theme (my favorite theme)
html_theme = "sphinx_rtd_theme"
extensions.append(html_theme)

# HTML theme options for local RTD build
html_theme_options = {
    # don't display version on documentation sidebar header
    "display_version": False,
    # color for the sidebar navigation header
    "style_nav_header_background": "#a2c4cd"
}

# file for image to be used in sidebar logo (should not exceed 200 px in width)
html_logo = "./_static/touketsu_logo.png"

# use emacs style for pygments highlighting in code blocks or inline code
pygments_style = "emacs"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

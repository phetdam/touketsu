# __init__.py for touketsu
#
# Changelog:
#
# 06-23-2020
#
# initial creation. added package docstring and import from .core

__doc__ = """A tiny package for classes without dynamic attribute creation.

Provides a simple implementation for a "frozen" class, i.e. a class that cannot
dynamically create instance attributes. This is the default class behavior in
Python and may be undesirable for some people.
"""

# make stuff from core available in top-level package namespace
from .core import *

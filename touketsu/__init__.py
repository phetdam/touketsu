__doc__ = "``__init__.py`` for ``touketsu."

# make stuff from core available in top-level package namespace
__all__ = ["class_decorator_factory", "unrestrict", "orig_init", "immutable",
           "nondynamic", "identity_immutable", "identity_nondynamic"]

from .core import *
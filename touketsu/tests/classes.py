__doc__ = "Some test classes for testing ``touketsu`` functions."

import sys

from ..core import immutable, nondynamic, orig_init
from . import srepr, vrepr


@nondynamic
@vrepr
class a_class:
    """Docstring for ``a_class``.
    
    :param a: Parameter ``a``
    """
    def __init__(self, a = "a"): self.a = a


# note: vrepr/srepr decoration order does not matter
@srepr
@immutable
class b_class:
    """Docstring for ``b_class``.
    
    :param b: Parameter ``b``
    """
    def __init__(self, b = "b"): self.b = b


@nondynamic
class c_class(a_class, b_class):
    """Docstring for ``c_class``.
    
    :param a: Parameter ``a``
    :param b: Parameter ``b``
    :param c: Parameter ``c``
    """
    def __init__(self, a = "aa", b = "bb", c = "c"):
        orig_init(a_class.__init__)(self, a = a)
        orig_init(b_class.__init__)(self, b = b)
        self.c = c


if __name__ == "__main__": 
    print(f"{__file__}: do not run module as script.", file = sys.stderr)
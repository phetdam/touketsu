__doc__ = "Utility functions for ``touketsu`` test suite."

import sys

_global_eps = 8e-16

def almost_equals(val_a, val_b, eps = _global_eps):
    """Returns ``True`` if ``val_a``, ``val_b`` are ``eps`` close.
    
    Necessary since Python floats have infinite precision.
    
    :param val_a: First value to compare
    :type val_a: float
    :param val_b: Second value to compare
    :type val_b: float
    :param eps: Value to determine the closeness of ``val_a`` and ``val_b``,
        currently ``8e-16`` by default.
    :type eps: float, optional
    :rtype: bool
    """
    if abs(val_a - val_b) <= eps: return True
    return False


def almost_one(val, eps = _global_eps):
    """Returns ``True`` if ``val`` is within ``eps`` of ``1``.
    
    Equivalent to calling :func:`almost_equals` with ``val`` as ``val_a`` and
    ``1`` as ``val_b`` for a particular value of ``eps``.
    
    :param val: Numeric value close to 1 
    :type val: float
    :param eps: Value to determine the closeness of ``val_a`` and ``val_b``,
        currently ``8e-16`` by default.
    :type eps: float, optional
    :rtype: bool
    """
    return almost_equals(val, 1, eps = eps)


if __name__ == " __main__":
    print(f"{__file__}: do not run module as script.", file = sys.stderr)
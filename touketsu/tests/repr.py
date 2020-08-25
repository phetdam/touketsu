__doc__ = """Decorators for simple, human-readable object representations.

.. note:: This file may be spun out into a separate, more functional project.
"""

import inspect
import sys
import textwrap


def _simple_repr_factory(verbose = False):
    """Factory method for overrides for :meth:`~object.__repr__`.
    
    Representations produced by the returned function wrap to 80 columns and are
    inspired by the representations produced by scikit-learn estimators.

    .. important:: All parameters in the :meth:`~object.__init__` method of
        ``self``'s class must be present as instance attributes in ``self``.
        
    .. caution:: This function allows representations of infinite length.
    
    Use through :func:`srepr` or :func:`vrepr`, i.e. for class ``a_class``,
    
    .. code:: python
    
        @vrepr
        class a_class:
        
            def __init__(self, a, b, aa = "aa", bb = "bb"):
                self.a = a
                self.b = b
                self.aa = aa
                self.bb = bb

    Calling :func:`repr` on ``a_class("a", "b")`` will yield
    
    .. code:: python
    
        a_class("a", "b", aa="aa", bb="bb")

    If :func:`srepr` was used instead of :func:`vrepr`, then values of ``aa``
    and ``bb`` would be shown only if they were passed arguments not equal to
    their given defaults.
    
    :param verbose: ``True`` to include all keyword args from ``__init__``
        signature, ``False`` to include only keyword args from ``__init__`` that
        do not equal the 
    :type verbose: bool, optional
    :returns: Unbound drop-in replacement for :meth:`~object.__repr__`.
    :rtype: function
    """
    # define simple repr function
    def _simple_repr(self):
        class_name = self.__class__.__name__
        out = class_name + "("
        params = inspect.signature(self.__init__).parameters
        for p in params.keys():
            if p == "self": continue
            # get value to look up and value of default
            val, dval = getattr(self, p), params[p].default
            # if positional argument (no default)
            if dval == inspect._empty: out = out + repr(val) + ", "
            # else treat as keyword argument only if default doesn't equal the
            # value looked up by getattr or verbose is True
            elif (dval != inspect._empty) and \
                ((dval != val) or (verbose == True)):
                out = out + p + "=" + repr(val) + ", "
            # else treat as keyword argument with default and skip
        # if last two characters are ", ", remove
        if out[-2:] == ", ": out = out[:-2]
        # return pretty-printed
        return textwrap.fill(out + ")", width = 80,
                                subsequent_indent = " " * (len(class_name) + 1))

    # usage example for _simple_repr docstring if verbose == False
    repr_example = (
        "    Output is as follows. For a class ``a_class`` defined as\n\n"
        "    .. code:: python\n\n       @srepr\n       class a_class:\n\n"
        "           def __init__(self, a, b, aa = \"aa\", bb = \"bb\"):\n"
        "               self.a = a\n               self.b = b\n"
        "               self.aa = aa\n               self.bb = bb\n\n"
        "    Calling :func:`repr` on ``a_class(\"a\", \"b\")`` yields\n\n"
        "    .. code:: python\n\n       a_class(\"a\", \"b\")"
    )
    # if verbose == True, then use different example
    if verbose == True:
        repr_example = (
            "    Output is as follows. For a class ``a_class`` defined as\n\n"
            "    .. code:: python\n\n       @srepr\n       class a_class:\n\n"
            "           def __init__(self, a, b, aa = \"aa\", bb = \"bb\"):\n"
            "               self.a = a\n               self.b = b\n"
            "               self.aa = aa\n               self.bb = bb\n\n"
            "    Calling :func:`repr` on ``a_class(\"a\", \"b\")`` yields\n\n"
            "    .. code:: python\n\n"
            "       a_class(\"a\", \"b\", aa=\"aa\", bb=\"bb\")"
        )
    # adjust docstring of _simple_repr and return
    _simple_repr.__doc__ = (
        "Human-readable override for :meth:`~object.__repr__`.\n\n"
        f"{repr_example}\n\n    :param self: self\n    :returns: \n"
        "    :rtype: str"
    )
    return _simple_repr


def srepr(cls):
    """Decorate class with ``_simple_repr_factory(verbose = False)`` for repr.
    
    Creates and sets to ``False`` class attribute ``_simple_repr_is_verbose``.
    
    :param cls: A class
    :type cls: type, :class:`abc.ABCMeta`
    :rtype: type
    """
    cls._simple_repr_is_verbose = False
    cls.__repr__ = _simple_repr_factory(verbose = cls._simple_repr_is_verbose)
    return cls


def vrepr(cls):
    """Decorate class with ``_simple_repr_factory(verbose = True)`` for repr.
    
    Creates and sets to ``True`` class attribute ``_simple_repr_is_verbose``.
    
    :param cls: A class
    :type cls: type, :class:`abc.ABCMeta`
    :rtype: type
    """
    cls._simple_repr_is_verbose = True
    cls.__repr__ = _simple_repr_factory(verbose = cls._simple_repr_is_verbose)
    return cls


def has_simple_repr(obj):
    """Determine if ``obj`` has repr returned by  :func:`_simple_repr_factory`.
    
    ``True`` if ``obj._simple_repr_is_verbose`` exists, ``False`` otherwise. If
    ``True`` is returned, then ``obj`` or its class (if a class instance) was
    decorated with :func:`srepr` or :func:`vrepr`.
    
    :param obj: Class or class instance
    :type obj: object
    :rtype: bool
    """
    return hasattr(obj, "_simple_repr_is_verbose")


def get_simple_repr_verbosity(obj):
    """Utility function for getting a decorated class's repr verbosity.
    
    Returns ``True`` if ``obj._simple_repr_is_verbose == True``, ``False`` if
    ``obj._simple_repr_is_verbose == False``. Raises :class:`AttributeError`
    if ``obj._simple_repr_is_verbose`` does not exist, i.e. ``obj`` was not
    decorated with a function returned by :func:`_simple_repr_factory`.
    
    :param obj: Class or class instance
    :type obj: object
    :raises AttributeError: Raised if ``_simple_repr_is_verbose`` is not a
        member of ``obj``.
    :rtype: bool
    """
    return obj._simple_repr_is_verbose


if __name__ == "__main__":
    print(f"{__file__}: do not run module as script.", file = sys.stderr)
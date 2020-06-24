# core code for package touketsu
#
# Changelog:
#
# 06-23-2020
#
# initial creation. added FrozenClass implementation. added multiple inheritance
# example to illustrate how to use the FrozenClass implementation.

class FrozenClass:
    """A mixin class to disallow dynamic attribute creation.

    For example, suppose we want to define a class ``c_class`` that inherits
    from ``a_class`` and ``b_class``, which are defined as

    .. code:: python

       class a_class:

           def __init__(self, a, b = "aaa"):
               self.a = a
               self.b = b

       class b_class:

           def __init__(self, c = "xxx", d = "yyy"):
               self.c = c
               self.d = d

    If we want to disable dynamic instance attribute creation for ``c_class``,
    we could define ``c_class`` as follows [#]_:

    .. code:: python

       class c_class(a_class, b_class, FrozenClass):

           def __init__(self, a, b = "bbb", c = "ccc", d = "ddd"):
               a_class.__init__(self, a, b = b)
               b_class.__init__(self, c = c, d = d)
               self._freeze()

    The :meth:``_freeze`` call will disable dynamic instance attribute creation.
    Any attempts to create an instance attribute at runtime will result in an
    :class:`AttributeError`. Note that :meth:``_freeze`` should be treated as an
    irreversible operation.

    .. [#] Note that we opt to use explicit :meth:`__init__` calls due to the
       different :meth:`__init__` signatures. Cooperative subclassing by calling
       :meth:`super` could also be used, but only if we allow each
       :meth:`__init__` signature to support variable arguments and keyword
       arguments. Please see `this StackOverflow post`__ for a nice explanation.

    .. __: https://stackoverflow.com/questions/26927571/multiple-inheritance-in
       -python3-with-different-signatures
    """
    _is_frozen = False

    def __setattr__(self, key, value):
        # if frozen and dynamic attribute creation is attempted, raise exception
        if (self._is_frozen == True) and (key not in self.__dict__):
            raise AttributeError("frozen class cannot dynamically create "
                                 "attributes")
        self.__dict__[key] = value

    def _freeze(self):
        """Freezes a ``FrozenClass`` instance.

        No new instance attributes can be created after calling :meth:`_freeze`.
        A frozen class also cannot be "unfrozen".
        """
        self._is_frozen = True

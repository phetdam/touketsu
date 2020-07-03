# core code for package touketsu
#
# Changelog:
#
# 07-03-2020
#
# added class docstring.
#
# 07-02-2020
#
# renamed FrozenClass to NDClass, as a "frozen" class should be immutable. also
# [re]defined FrozenClass as a mixin for immutable class instances. modified
# docstring for NDClass with more detail and started docstring for FrozenClass.
#
# 06-23-2020
#
# initial creation. added FrozenClass implementation. added multiple inheritance
# example to illustrate how to use the FrozenClass implementation.

__doc__ = """Core package code.

Contains mixin classes that can be used to make subclasses immutable or
nondynamic, i.e. existing instance attributes may be modified while no new
instance attributes can be created at runtime.
"""

class FrozenClass:
    """A mixin class for defining immutable class instances.

    Classes inheriting :class:`FrozenClass` can be defined to have permanently
    immutable instances, i.e. no dynamic instance attribute creation and no
    modification of existing attributes.

    .. note::

       Class instances still have the :attr:`__dict__` property, which can be
       manually modified.

    For generality and to illustrate how the :class:`FrozenClass` works well
    with multiple inheritance, consider the following example. Suppose we have
    the classes ``a_class`` and ``b_class``, which have the definitions

    .. code:: python

       class a_class:

           def __init__(self, a, b = "aaa"):
               self.a = a
               self.b = b

       class b_class:

           def __init__(self, c = "xxx", d = "yyy"):
               self.c = c
               self.d = d

    Now suppose we want to define a class ``c_class`` which inherits from
    ``a_class`` and ``b_class``. ``c_class`` introduces one new instance
    attribute ``x`` and overrides some keyword argument defaults passed to the 
    :meth:`__init__` methods of ``a_class`` and ``b_class``. If we wanted to
    also define ``c_class`` to have immutable instances, we could define
    ``c_class`` as follows: [#]_

    .. code:: python

       class c_class(a_class, b_class, FrozenClass):

           def __init__(self, a, b = "bbb", c = "ccc", d = "ddd", x = -1):
               a_class.__init__(self, a


    .. [#] Note that we opt to use explicit :meth:`__init__` calls due to the
       different :meth:`__init__` signatures. Cooperative subclassing by calling
       :meth:`super` could also be used, but only if we allow each
       :meth:`__init__` signature to support variable arguments and keyword
       arguments. Please see `this StackOverflow post`__ for a nice explanation.

    .. __: https://stackoverflow.com/questions/26927571/multiple-inheritance-in
       -python3-with-different-signatures
    """
    __frozen = False

    def __setattr__(self, key, value):
        # if frozen, raise AttributeError
        if self.__frozen == True:
            raise AttributeError("FrozenClass instances cannot dynamically "
                                 "create new instance attributes nor modify "
                                 "existing instance attributes")
        self.__dict__[key] = value

    def _freeze(self):
        """Freeze an instance of :class:`FrozenClass`.

        After freezing, no new instance attributes may be created and no
        existing instance attributes may be modified using :meth:`__setattr__`.
        However, the :attr:`__dict__` attribute may still be modified.
        """
        self.__frozen = True


class NDClass:
    """A mixin class for disallowing dynamic instance attribute creation. [#]_

    Classes inheriting :class:`NDClass` can allow modification of existing
    instance attributes while disallowing dynamic attribute creation using
    :meth:`__setattr__` for a class instance at runtime.

    .. note::

       Class instances still have the :attr:`__dict__` property, which can be
       manually modified.

    To 
    See :doc:`../examples`

    For generality and to show how the :class:`NDClass` works well with
    multiple inheritance, consider the following example. Suppose we want to
    define a new class ``c_class`` that inherits from ``a_class`` and
    ``b_class``, whose definitions can be found in the :class:`FrozenClass`
    docstring above. The ``c_class`` definition does not introduce additional
    instance attributes, but overrides some keyword argument defaults for the 
    :meth:`__init__` methods for ``a_class`` and ``b_class``. If we want to
    disable dynamic instance attribute creation for ``c_class``, we could define
    ``c_class`` as follows:

    .. code:: python

       class c_class(a_class, b_class, NDClass):

           def __init__(self, a, b = "bbb", c = "ccc", d = "ddd"):
               a_class.__init__(self, a, b = b)
               b_class.__init__(self, c = c, d = d)
               self._make_nondynamic()

    The :meth:`_make_nondynamic` call will disable dynamic instance attribute
    creation. Any attempts to create an instance attribute at runtime will
    result in an :class:`AttributeError`. Note that :meth:`_make_nondynamic` 
    should be treated as an irreversible operation.

    .. warning::

       :meth:`_make_nondynamic` **must** be called after initialization of
       parent classes and any other instance attribute definitions or an
       :class:`AttributeError` will be raised by :meth:`__setattr__`.

    .. [#] :class:`NDClass` is an abbreviation for NonDynamicClass.
    """
    __nondynamic = False

    def __setattr__(self, key, value):
        # if class instance is nondynamic and dynamic attribute creation is
        # attempted, raise AttributeError
        if (self.__nondynamic == True) and (key not in self.__dict__):
            raise AttributeError("NDClass instances cannot dynamically create "
                                 "new instance attributes")
        self.__dict__[key] = value

    def _make_nondynamic(self):
        """Make an instance of :class:`NDClass` nondynamic.

        No new instance attributes may be created using :meth:`__setattr__`
        after calling :meth:`_make_nondynamic` and a class instance made
        nondynamic cannot be made dynamic again. However, as noted, the 
        :attr:`__dict__` attribute may still be modified.
        """
        self.__nondynamic = True



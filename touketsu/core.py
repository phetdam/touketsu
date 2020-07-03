# core code for package touketsu
#
# Changelog:
#
# 07-03-2020
#
# added class docstring, changed references to examples.rst to user_guide.rst.
# remove example from FrozenClass to user_guide.rst; working on NDClass
# docstring which will later be migrated to user_guide.rst as well.
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

    Simply inheriting from :class:`FrozenClass` does not do anything by itself.
    To make all instances of the class inheriting :class:`FrozenClass` are
    immutable, after definition of all instance attributes in the subclass's
    :meth:`__init__` method, the :meth:`_freeze` method should be called.

    See :doc:`../user_guide` for details examples on using :class:`FrozenClass`.
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
    See :doc:`../user_guide`

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



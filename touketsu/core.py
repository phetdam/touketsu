# core code for package touketsu
#
# Changelog:
#
# 07-07-2020
#
# cleaned up/added docstrings for class_decorator_factory, fancy_immutable, and
# identity_immutable. little actual work done because summer internship started.
#
# 07-05-2020
#
# added decorators; working on decorator factory. moved _classdocmod and
# constants to _utils, now utils. figured out how to get the decorators to work
# with inheritance structures; we balling. shorten AttributeErrors. remove bug
# in unrestrict that ended up giving classes their superclass __doc__ attribute.
# clean up some docstrings and correct some spacing.
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

Contains the decorators and decorator factory that are the package's lifeblood.
"""

from copy import deepcopy
from inspect import signature
from functools import wraps
import warnings

from .utils import classdocmod

# set up warnings
warnings.simplefilter("always")

def class_decorator_factory(dectype = None, docmod = None, docindent = "auto",
                            use_tabs = False, fancy_caution = None,
                            fancy_note = None):
    """``touketsu`` class decorator factory.

    The returned decorator is able to automatically modify the docstrings of
    the wrapped class, provided they follow the docstring format specified in
    `PEP 257`__.

    .. note::

       It is possible to tell which classes have been wrapped a decorator
       returned by :func:`class_decorator_factory` because the decoration
       process introduces additional class attributes prepended by 
       ``_touketsu``. Using :func:`unrestrict` on any of these decorated classes
       undos the decoration and returns the class to its original definition.

    .. __: https://www.python.org/dev/peps/pep-0257/

    :param dectype: The decorator type. Pass ``"immutable"`` to return a class
        decorator that makes a class instance immutable or ``"nondynamic"`` to
        make a class instance nondynamic.
    :type dectype: str
    :param docmod: How to modify the docstring of the class the returned
        decorator is applied to. Either ``"fancy"``, ``"brief"``, or ``"identity"``.
        The default value is ``"brief"``.
    :type docmod: str, optional
    :param docstr: The replacement docstring, if ``docmod = "manual"``. If
        ``docmod != "manual"``, then ``docstr`` is ignored.
    :type docstr: str, optional
    """
    _fn = class_decorator_factory.__name__
    # if dectype is not valid, raise error
    if (dectype != "immutable") and (dectype != "nondynamic"):
        raise ValueError("{0}: dectype must be \"immutable\" or \"nondynamic\"")

    # decorator for a class
    def wrapper(cls):
        # raise TypeError if this is not a type
        if cls.__class__.__name__ != "type":
            raise TypeError("{0}: expected type, received {1}"
                            .format(_fn, type(cls)))
        # class attribute indicating restriction imposed by touketsu
        cls._touketsu_restriction = None
        # original class docstring and original class __init__ method
        cls._touketsu_orig__doc__ = cls.__doc__
        _orig__init__ = cls.__init__

        # new __setattr__
        def _touketsu_restricted_setattr(self, key, value):
            if self._touketsu_restriction == "immutable":
                raise AttributeError("Immutable class instance")
            # disable manual "unrestriction" of the restricted class
            elif (self._touketsu_restriction == "nondynamic") and \
                 (key != "_touketsu_restriction") and (not hasattr(self, key)):
                raise AttributeError("Nondynamic class instance")
            object.__setattr__(self, key, value)

        # wrapper for class __init__ method
        def init_wrapper(init):
            # for "well-behaved" decoration (don't lose signature and docstring)
            @wraps(init)
            def _init_wrapper(self, *args, **kwargs):
                init(self, *args, **kwargs)
                self._touketsu_restriction = dectype

            return _init_wrapper
        
        # perform docstring modification
        classdocmod(cls, dectype, docmod = docmod)
        # override __setattr__ and __init__ of class + preserve original
        # signature. it is known that sphinx doesn't work well with functools.wraps.
        cls.__setattr__ = _touketsu_restricted_setattr
        try: cls.__init__.__signature__ = signature(cls.__init__)
        except AttributeError:
            warnings.warn("Class without __init__ decorated. object.__init__ "
                          "signature will be displayed instead.")
        cls.__init__ = init_wrapper(cls.__init__)
        # also bind original __init__ method to new __init__ (so orig_init) works
        cls.__init__._touketsu_orig__init__ = _orig__init__
        # return class
        return cls

    # return decorator
    return wrapper


def unrestrict(cls):
    """Remove the nondynamic or immutable restriction from a class.

    For any class decorated by a decorator returned by 
    :func:`~touketsu.core.class_decorator_factory`, :func:`unrestrict` removes
    the decorator's effect, restoring the original :meth:`__init__` and 
    :meth:`~object.__setattr__` methods.

    Useful for temporarily removing a ``touketsu`` decorator restriction from
    a decorated class.

    .. note::

       If the class is undecorated, then :func:`unrestrict` will have no effect.

    .. caution::

       Calling :func:`unrestrict` on subclasses of classes decorated by a
       decorator returned from :func:`~touketsu.core.class_decorator_factory`
       will result in warnings being raised. The decorator restrictions do not
       persist through the inheritance structure if :func:`super` is used for
       inheritance or if the unbound superclass :meth:`__init__` methods are
       wrapped with :func:`orig_init`.

    :param cls: Class decorated by a decorator returned from 
        :func:`~touketsu.core.class_decorator_factory`
    :type cls: type
    :returns: The original class, without decoration
    :rtype: type
    """
    # try to delete restriction; doesn't work if superclass is also restricted
    if hasattr(cls, "_touketsu_restriction"):
        try: delattr(cls, "_touketsu_restriction")
        except AttributeError:
            warnings.warn("Unable to delete _touketsu_restriction; likely a "
                          "superclass attribute")
    # restore original docstring if necessary and delete _touketsu_orig__doc__
    # note we do delattr before doc assignment since this may be the superclass
    # __doc__, which we do not want
    if hasattr(cls, "_touketsu_orig__doc__"):
        try:
            _orig__doc__ = cls._touketsu_orig__doc__
            delattr(cls, "_touketsu_orig__doc__")
            cls.__doc__ = _orig__doc__
        except AttributeError:
            warnings.warn("Unable to delete _touketsu_orig__doc__; likely a "
                          "superclass attribute")
    # override __setattr__ with object's __setattr__ if necessary
    if cls.__setattr__ != object.__setattr__:
        cls.__setattr__ = object.__setattr__
    # use original __init__ method if necessary. no need for try statement as
    # the __init__ method does not have a direct superclass with the same attr
    if hasattr(cls.__init__, "_touketsu_orig__init__"):
        cls.__init__ = cls.__init__._touketsu_orig__init__
    # return class
    return cls


def orig_init(init):
    """Return original :meth:`__init__` from decorated :meth:`__init__`.

    If ``init`` is not the :meth:`__init__` of a decorated class, then ``init``
    itself is returned.

    :param init: The unbound :meth:`__init__` of the decorated class.
    :type init: function
    :returns: The unbound original :meth:`__init__` of the decorated class or
        ``init``, if ``init`` is not the :meth:`__init__` of a decorated class.
    :rtype: function
    """
    _fn = orig_init.__name__
    # should be a function
    if init.__class__.__name__ == "function":
        # if it contains original init, return that
        if hasattr(init, "_touketsu_orig__init__"):
            return getattr(init, "_touketsu_orig__init__")
        # else return init itself
        return init
    # raise TypeError if necessary
    raise TypeError("{0}: init must be a method or function".format(_fn))


def immutable(cls):
    """Decorator to make a class immutable. Imparts a minor docstring change.

    Equivalent to :func:`class_decorator_factory` with ``dectype = "immutable"``
    and ``decmod = "brief"``. The standard decorator to use for making a class
    immutable.

    .. note::

       Do not apply to a previously decorated class. Instead, use
       :func:`unrestrict` first to return the class to its original state before
       applying :func:`immutable`.

    :param cls: The class to decorate.
    :type cls: type
    :returns: A decorated version of the original class with immutable
        instances.
    :rtype: type
    """
    return class_decorator_factory("immutable", "brief")(cls)


def identity_immutable(cls):
    """Decorator to make a class immutable, with no docstring changes.

    .. caution::

       Since :func:`identity_immutable` does not modify the docstring of the
       class it decorates, it is easy to mistake the decorated class for the
       undecorated class. It is recommended to use the plain :func:`immutable`
       decorator instead.

    .. note::

       Do not apply to a previously decorated class. Instead, use
       :func:`unrestrict` first to return the class to its original state before
       applying :func:`identity_immutable`.

    :param cls: The class to decorate.
    :type cls: type
    :returns: A decorated version of the original class with immutable
        instances.
    :rtype: type
    """
    return class_decorator_factory("immutable", "identity")(cls)


def fancy_immutable(cls):
    """Decorator to make a class immutable, with more fancy docstring changes.

    Equivalent to :func:`class_decorator_factory` with ``dectype = "immutable"``
    and ``decmod = "fancy"``. The decorator to use for making a class immutable
    while also providing a more visible indication, through the use of a
    ``.. caution::`` block, that inheritance must be considered more carefully.

    .. note::

       Do not apply to a previously decorated class. Instead, use
       :func:`unrestrict` first to return the class to its original state before
       applying :func:`fancy_immutable`.    

    .. note::

       I really should put this warning in :doc:`../api_ref` instead.

    :param cls: The class to decorate.
    :type cls: type
    :returns: A decorated version of the original class with immutable
        instances.
    :rtype: type
    """
    return class_decorator_factory("immutable", "fancy")(cls)


def nondynamic(cls):
    return class_decorator_factory("nondynamic", "brief")(cls)


def identity_nondynamic(cls):
    return class_decorator_factory("nondynamic", "identity")(cls)


def fancy_nondynamic(cls):
    return class_decorator_factory("nondynamic", "fancy")(cls)


@fancy_nondynamic
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

    def __init__(self, a = 1, b = 2): self.a = a


@fancy_immutable
class a_class(FrozenClass):

    def __init__(self, a = "aa", b = "bb"):
        #super().__init__(a = a, b = b) # this works; decorator is ignored
        orig_init(FrozenClass.__init__)(self, a = a, b = b) # also works; returns original __init__
        self.b = a + b

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



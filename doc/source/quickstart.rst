.. quickstart guide for touketsu. sphinx-enabled formatting.

   see quickstart_plain.rst for the same content, but without sphinx-specific
   restructuredtext markup.

Quickstart
==========

The most commonly used decorators in ``touketsu`` are
:func:`~touketsu.core.immutable` and :func:`~touketsu.core.nondynamic`.
:func:`~touketsu.core.immutable` makes class instances immutable, while
:func:`~touketsu.core.nondynamic` makes class instances nondynamic, i.e.
existing attributes may be modified, but no new attributes can be created
dynamically at runtime. For example, suppose we have a class ``my_class``, where

.. code:: python

   class my_class:
       """This is my class.

       :param a: First parameter.
       :param b: Second parameter.
       """
       def __init__(self, a = 1, b = 2):
           self.a = a
           self.b = b

Typically, it is possible to do something like in the interpreter:

>>> a = my_class()
>>> a.d = 14
>>> a.d
14

If ``my_class`` was decorated with :func:`~touketsu.core.nondynamic`, then an
:class:`AttributeError` would be raised, although an assignment to an existing
attribute like ``a.a = 13`` would be allowed.

Note that :func:`~touketsu.core.immutable` and :func:`~touketsu.core.nondynamic`
modify the docstrings of the classes they modify. Respectively, they prepend 
``"[Immutable] "`` and ``"[Nondynamic] "``, sans double quotes, to the docstring
of the decorated class. If no changes to the docstring are desired, use
:func:`~touketsu.core.identity_immutable` and
:func:`~touketsu.core.identity_nondynamic` instead.

A simple example
----------------

Using the decorators is very simple. Suppose we have a class ``a_class`` defined
as [#]_

.. code:: python

   class a_class:
       """A sample class.

       :param a: The first parameter.
       """
       def __init__(self, a = "a"):
           self.a = a
   
If we wanted instances of ``a_class`` to allow modification of instance
attributes but not to allow dynamic instance attribution creation, we would use
the :func:`~touketsu.core.nondynamic` decorator as follows:

.. code:: python

   from touketsu import nondynamic

   @nondynamic
   class a_class:
       """A sample class.

       :param a: The first parameter.
       """
       def __init__(self, a = "a"):
           self.a = a

If we then make an instance of ``a_class`` named ``aa``, we would be able to
modify ``aa.a``, but attempting ``aa.aaa = 15`` or a similar operation would
result in an :class:`AttributeError`.

Note that the ``a_class`` docstring has now been modified into

.. code:: python

   """**[Nondynamic]** A sample class.

   :param a: The first parameter.
   """

Sphinx__ would be able to properly read this docstring and generate formatted
documentation.

.. [#] It is recommended that class docstrings are `PEP 257`__ compliant for
   best results.

.. __: https://www.sphinx-doc.org/en/master/

.. __: https://www.python.org/dev/peps/pep-0257/


Inheritance
-----------

When using decorators like this that disable the ability of Python class
instances to dynamically create new instance attributes, we run into trouble
with inheritance. Fortunately, using ``touketsu`` decorators requires minimal
changes to existing code in order to preserve multiple inheritance.

Let's define a second class ``b_class`` as follows:

.. code:: python

   from touketsu import immutable

   @immutable
   class b_class:

       def __init__(self, b = "b"):
           self.b = b

Suppose we also have classes ``c_class`` and ``A_class``, where

.. code:: python

   class c_class(a_class, b_class):

       def __init__(self, a = "aa", b = "bb", c = "cc"):
           a_class.__init__(self, a = a)
           b_class.__init__(self, b = b)
           self.c = c

   class A_class(a_class):

       def __init__(self, a = "A", aa = "AA"):
           super().__init__(a = a)
           self.aa = aa

Now, suppose that ``a_class`` was decorated with
:func:`~touketsu.core.nondynamic`. Which of these two classes'
:meth:`__init__` methods would raise an :class:`AttributeError` when called?

As you may have expected, both, as the bound and unbound :meth:`__init__` have
been decorated already. Fortunately, ``touketsu`` provides the
:func:`~touketsu.core.orig_init` function to wrap unbound :meth:`__init__`
methods, returning the original class :meth:`__init__`. Therefore, if we define
``c_class`` as

.. code:: python

   from touketsu import orig_init

   class c_class(a_class, b_class):

       def __init__(self, a = "aa", b = "bb", c = "cc"):
           orig_init(a_class.__init__)(self, a = a)
           orig_init(b_class.__init__)(self, b = b)
           self.c = c

Now no :class:`AttributeError` will be thrown when ``c_class()`` is executed.
Note that although ``a_class`` is decorated with
:func:`~touketsu.core.immutable` and ``b_class`` is decorated with
:func:`~touketsu.core.nondynamic`, ``c_class`` is just a normal class. We can
then in turn decorate ``c_class`` if we want to.


Class and instance methods
--------------------------

It remains to address how class and instance methods are treated in classes
decorated by ``touketsu`` class decorators like
:func:`~touketsu.core.nondynamic`. For example, we may have a class
``some_class`` that is defined as

.. code:: python

   class some_class:

       def __init__(self, a = "a", b = "b"):
           self.a = a
           self.b = b

       @classmethod
       def special_class_method(cls):
           cls.aa = 1000
           return cls(a = "A")

       def method_one(self, val):
           self.aaa = val

       def method_two(self):
           if hasattr(self, aa) and hasattr(self, aaa):
               return 2
           if hasattr(self, aa):
               return 0
           elif hasattr(self, aaa):
               return 1
           return -1

Suppose we want class instances to be immutable. We cannot just decorate
``some_class`` with :func:`~touketsu.core.immutable`, since ``method_one``
attempts to create a new instance attribute, which will cause an
:class:`AttributeError` to be raised upon call. Instead, we would define
``some_class`` as follows:

.. code:: python

   from touketsu import immutable, urt_method

   @immutable
   class some_class:

       def __init__(self, a = "a", b = "b"):
           self.a = a
           self.b = b

       @classmethod
       def special_class_method(cls):
           cls.aa = 1000
           return cls(a = "A")

       @urt_method
       def method_one(self, val):
           self.aaa = val

       def method_two(self):
           if hasattr(self, aa) and hasattr(self, aaa):
               return 2
           if hasattr(self, aa):
               return 0
           elif hasattr(self, aaa):
               return 1
           return -1

Note that we do not need to decorate the :func:`classmethod`
``special_class_method`` with :func:`~touketsu.core.urt_method`, as ``touketsu``
restrictions only affect the *instances* of a class, not the class itself.
``method_two`` also does not need to be decorated with
:func:`~touketsu.core.urt_method` since it does not create or modif instance
attributes.
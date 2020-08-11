.. quickstart guide for touketsu without sphinx-enabled formatting.

   see quickstart.rst for the same content, but *with* sphinx-specific
   restructuredtext markup.

Quickstart
==========

The most commonly used decorators in ``touketsu`` are ``immutable`` and
``nondynamic``. ``immutable`` makes class instances immutable, while
``nondynamic`` makes class instances nondynamic, i.e. existing attributes may be
modified, but no new attributes can be created dynamically at runtime. For
example, suppose we have a class ``my_class``, where

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

If ``my_class`` was decorated with ``nondynamic``, then an ``AttributeError``
would be raised, although an assignment to an existing attribute like
``a.a = 13`` would be allowed.

Note that ``immutable`` and ``nondynamic`` modify the docstrings of the classes
they modify. Respectively, they prepend ``"[Immutable] "`` and
``"[Nondynamic] "``, sans double quotes, to the docstring of the decorated
class. If no changes to the docstring are desired, use ``identity_immutable``
and ``identity_nondynamic`` instead.

A first look
------------

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
the ``nondynamic`` decorator as follows:

.. code:: python

   @nondynamic
   class a_class:
       """A sample class.

       :param a: The first parameter.
       """
       def __init__(self, a = "a"):
           self.a = a

If we then make an instance of ``a_class`` named ``aa``, we would be able to
modify ``aa.a``, but attempting ``aa.aaa = 15`` or a similar operation would
result in an ``AttributeError``.

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

Now, suppose that ``a_class`` was decorated with ``nondynamic``. Which of these
two classes' ``__init__`` methods would raise an ``AttributeError`` when called?

As you may have expected, both, as the bound and unbound ``__init__`` have
been decorated already. Fortunately, ``touketsu`` provides the ``orig_init``
function to wrap unbound ``__init__`` methods, returning the original class
``__init__``. Therefore, if we define ``c_class`` as

.. code:: python

   class c_class(a_class, b_class):

       def __init__(self, a = "aa", b = "bb", c = "cc"):
           orig_init(a_class.__init__)(self, a = a)
           orig_init(b_class.__init__)(self, b = b)
           self.c = c

Now no ``AttributeError`` will be thrown when ``c_class()`` is executed. Note
that although ``a_class`` is decorated with ``immutable`` and ``b_class`` is
decorated with ``nondynamic``, ``c_class`` is just a normal class. We can in
turn decorate ``c_class`` if we want to, but keep in mind that properties
imparted by a ``touketsu`` decorator do **not** persist through inheritance.
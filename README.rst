.. README for touketsu package

   Changelog:

   07-05-2020

   modified introduction, added notes and installation section + example.

   06-23-2020

   initial creation.

touketsu
========

| *last updated: 07-05-2020*
| *file created: 06-23-2020*
|

A tiny package of decorators for creating classes that disallow dynamic instance attribute creation or modification while preserving class inheritance. This project was inspired by all the unfortunate incidences where fat-finger errors led to the creation of a new instance attribute instead of the modification of an existing instance attribute.

  Note: [#]_

  The code is undergoing significant changes but is somewhat ready for use. Proper documentation is in the process of being written; currently ``doc/source`` contains a very old and no longer relevant set of documentation from the early stages of the project. Please take a look if you are curious.

.. [#] One may notice that I used a block quote, not the ``.. note::`` directive. This renders better in Github when there is no HTML theme in place to generate fancier output.

Installation
------------

  Note:

  Package is not on PyPI yet, but once it is, you can expect to simply use ``pip`` to install.

Install from source by simply ``cd``\ ing to a preferred directory and typing

.. code:: bash

   git clone https://github.com/phetdam/touketsu
   make install

Then check that the package is properly working by trying an example in the interpreter, for example

>>> from touketsu import immutable
>>> @immutable
... class a_class:
...     def __init__(self, a = "a"):
...         self.a = a
>>> aa = a_class()

Attempting to execute ``aa.a = 5`` will result in an ``AttributeError``, as ``a_class`` instances are immutable.

Quickstart
----------

The most commonly used decorators in ``touketsu`` are ``immutable``, ``fancy_immutable``, ``nondynamic``, and ``fancy_nondynamic``. These four decorators make minor changes to the decorated class's docstring--``immutable`` and ``nondynamic`` respectively prepend ``"[Immutable] "`` and ``"[Nondynamic] "`` sans double quotes to the docstring of the decorated class, while the ``fancy`` variants also embed a generated restructuredText ``.. caution::`` block.

  Note:

  The ``.. caution::`` block content is slightly out of date. Use the non-\ ``fancy`` decorators for now.

A first look
~~~~~~~~~~~~

Using the decorators is very simple. Suppose we have a class ``a_class`` defined as [#]_

.. code:: python

   class a_class:
       """A sample class.

       :param a: The first parameter.
       """
       def __init__(self, a = "a"):
           self.a = a
   
If we wanted instances of ``a_class`` to allow modification of instance attributes but not to allow dynamic instance attribution creation, we would use the ``nondynamic`` decorator as follows:

.. code:: python

   @nondynamic
   class a_class:
       """A sample class.

       :param a: The first parameter.
       """
       def __init__(self, a = "a"):
           self.a = a

If we then make an instance of ``a_class`` named ``aa``, we would be able to modify ``aa.a``, but attempting ``aa.aaa = 15`` or a similar operation would result in an ``AttributeError``. Also, the ``a_class`` docstring has now become

.. code:: python

   """**[Nondynamic]** A sample class.

   :param a: The first parameter.
   """

A tool like Sphinx__ would be able to properly read this docstring and generate formatted documentation.

Inheritance
~~~~~~~~~~~

When using decorators like this that disable the ability of Python class instances to dynamically create new instance attributes, we run into trouble with inheritance. Fortunately, using ``touketsu`` decorators requires minimal changes to existing code in order to preserve multiple inheritance.

Suppose we also have the classes ``b_class``, ``c_class``, and ``A_class``, where

.. code:: python

   @immutable
   class b_class:

       def __init__(self, b = "b", c = "c"):
           self.b = b
	   self.c = c

   class c_class(a_class, b_class):

       def __init__(self, a = "aa", b = "bb", c = "cc", d = "d"):
           a_class.__init__(self, a = a)
	   b_class.__init__(self, b = b, c = c)
	   self.d = d

   class A_class(a_class):

       def __init__(self, a = "A", aa = "AA"):
           super().__init__(a = a)
	   self.aa = aa

Now, suppose that ``a_class`` was decorated with ``nondynamic``. Which one of these classes would raise an ``AttributeError`` upon an attempt to create a class instance?

It turns out that ``A_class()`` works, and does not inherit the nondynamic property of ``a_class``, while ``c_class()`` will raise an ``AttributeError`. This is because super__ ignores the ``nondynamic`` decorator and will call the *original* bound ``__init__`` method of ``a_class``. However, the unbound ``__init__`` methods of ``b_class`` and ``a_class`` are from the decorated versions of these classes, which have ``__setattr__`` overriden. Therefore, after calling ``a_class.__init__``, an ``AttributeError`` is thrown upon execution of ``b_class.__init__``.

Fortunately, ``touketsu`` provides the ``orig_init`` function to wrap the unbound ``__init__`` methods to return the original class ``__init__``. Therefore, if we define ``c_class`` as

.. code:: python

   class c_class(a_class, b_class):

       def __init__(self, a = "aa", b = "bb", c = "cc", d = "d"):
           orig_init(a_class.__init__)(self, a = a)
	   orig_init(b_class.__init__)(self, b = b, c = c)
	   self.d = d

Now no ``AttributeError`` will be thrown when ``c_class()`` is executed. Note that although ``a_class`` is decorated with ``immutable`` and ``b_class`` is decorated with ``nondynamic``, ``c_class`` is just a normal class. However, we can in turn decorate ``c_class`` if so desired.

.. [#] It is recommended that class docstrings are `PEP 257`__ compliant for best results.

.. __: https://www.python.org/dev/peps/pep-0257/

.. __: https://www.sphinx-doc.org/en/master/

.. __: https://docs.python.org/3/library/functions.html#super


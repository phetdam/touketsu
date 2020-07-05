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
...     def __init__(self, a = "a", b = "b"):
...         self.a = a
...         self.b = b
>>> aa = a_class()

Attempting to execute ``aa.a = 5`` will result in an ``AttributeError``, as ``a_class`` instances are immutable.

Quickstart
----------

The most commonly used decorators in ``touketsu`` are ``immutable``, ``fancy_immutable``, ``nondynamic``, and ``fancy_nondynamic``. These four decorators make minor changes to the docstring of the class they are wrapping--``immutable`` and ``nondynamic`` respectively prepend ``"[Immutable] "`` and ``"[Nondynamic] "`` sans double quotes to the docstring of the decorated class, while the ``fancy`` variants also embed a generated restructuredText ``.. caution::`` block.

  Note:

  The ``.. caution::`` block content is slightly out of date. Use the non-\ ``fancy`` decorators for now.

Using the decorators is very simple. Suppose we have a class ``a_class`` defined as

.. code:: python

   class a_class:
       """A sample class.

       :param a: The first parameter.
       :param b: The second parameter.
       """
       def __init__(self, a = "a", b = "b"):
           self.a = a
	   self.b = b
   
If we wanted instances of ``a_class`` to allow modification of instance attributes but not to allow dynamic instance attribution creation, we would use the ``nondynamic`` decorator as follows:

.. code:: python

   @nondynamic
   class a_class:
       """A sample class.

       :param a: The first parameter.
       :param b: The second parameter.
       """
       def __init__(self, a = "a", b = "b"):
           self.a = a
	   self.b = b

If we then make an instance of ``a_class`` named ``aa``, we would be able to modify ``aa.a`` and ``aa.b``, but attempting ``aa.c = 15`` or a similar operation would result in an ``AttributeError``. Also, if we were to inspect the docstring for ``a_class``, one would see that it has now become

.. code:: python

   """**[Nondynamic]** A sample class.

   :param a: The first parameter.
   :param b: The second parameter.
   """

Choosing to instead use the ``immutable`` decorator would make instances of ``a_class`` immutable, i.e. operations like ``aa.a = 5`` would also raise an ``AttributeError``.


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

Installing from source
~~~~~~~~~~~~~~~~~~~~~~

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
>>> aa.a = 5
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "c:\Users\D\START\prog_proj\touketsu\touketsu\core.py", line 89, in _touketsu_restricted_setattr
    raise AttributeError("Immutable class instance cannot dynamically "
AttributeError: Immutable class instance cannot dynamically create new instance attributes nor modify its existing attributes.
>>>

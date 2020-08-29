.. README for touketsu package

.. image:: https://github.com/phetdam/touketsu/blob/master/doc/source/_static/
   touketsu_logo_small.png

.. image:: https://img.shields.io/travis/phetdam/touketsu?logo=travis
   :target: https://travis-ci.org/github/phetdam/touketsu
   :alt: Travis (.org)

.. image:: https://readthedocs.org/projects/touketsu/badge/?version=latest
   :target: https://touketsu.readthedocs.io/en/latest/
   :alt: Documentation Status

**touketsu** is a tiny package for creating classes that disallow dynamic
instance attribute creation or modification while preserving class inheritance.
This project was inspired by all the unfortunate incidences where fat-finger
errors led to the creation of a new instance attribute instead of the
modification of an existing instance attribute.

Installation
------------

  Note:

  Package is not on PyPI yet, but once it is, you can expect to simply use 
  ``pip`` to install.

Install from source by simply ``cd``\ ing to a preferred directory and typing

.. code:: bash

   git clone https://github.com/phetdam/touketsu
   make install

This will perform a user install by default. If you have a virtual environment
activated, you may perform a root install by replacing ``make install`` with
``make root_install``.

After installing, check that the package is properly working using the
interpreter, for example

>>> from touketsu import immutable
>>> @immutable
... class a_class:
...     def __init__(self, a = "a"):
...         self.a = a
>>> aa = a_class()

Attempting to execute ``aa.a = 5`` will result in an ``AttributeError``, as 
``a_class`` instances are immutable.

Documentation
-------------

The documentation for ``touketsu`` is hosted on Read the Docs here__.

.. __: https://touketsu.readthedocs.io/en/latest/


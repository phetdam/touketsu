.. api reference page for touketsu

API Reference
=============

This page lists the two classes that form of the core of this package. For
detailed examples and best practices for using the classes in this package,
please refer to the :doc:`./user_guide`.

Classes
-------

.. autosummary::
   :toctree: generated
   :template: class.rst

   ~touketsu.core.FrozenClass
   ~touketsu.core.NDClass

Decorators
----------

.. autosummary::
   :toctree: generated
   :template: decorator.rst

   ~touketsu.core.immutable
   ~touketsu.core.identity_immutable
   ~touketsu.core.nondynamic
   ~touketsu.core.identity_immutable

If these decorators are too limited for one's use case, ``touketsu`` also
provides a simple decorator factory function for users to write their own
modified class decorators.

.. autosummary::
   :toctree: generated

   ~touketsu.core.class_decorator_factory

The class decorator :func:`~touketsu.core.unrestrict` can be used to undo the
effect of an applied decorator and return the class back to its original
undecorated state, removing all extra class attributes introduced by decoration.

.. autosummary::
   :toctree: generated

   ~touketsu.core.unrestrict

The :func:`~touketsu.core.orig_init` can be used to gain access to a class's
original undecorated :func:`__init__` function, which is necessary when
subclassing a decorated class.

.. autosummary::
   :toctree: generated

   ~touketsu.core.orig_init
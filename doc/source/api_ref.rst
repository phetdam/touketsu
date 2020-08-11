.. api reference page for touketsu

API Reference
=============

This page lists the main ``touketsu`` components. Please refer to the
:doc:`./quickstart` for usage details.

Decorators
----------

.. autosummary::
   :toctree: generated
   :template: decorator.rst

   ~touketsu.core.immutable
   ~touketsu.core.identity_immutable
   ~touketsu.core.nondynamic
   ~touketsu.core.identity_nondynamic

The above decorators are produced by the factory method below.

.. autosummary::
   :toctree: generated

   ~touketsu.core.class_decorator_factory

The class decorator :func:`~touketsu.core.unrestrict` undos the effect of an
applied decorator, returning the class back to its original undecorated state.
If applied to a non-decorated class, it returns the class itself.

.. autosummary::
   :toctree: generated
   :template: decorator.rst

   ~touketsu.core.unrestrict

The :func:`~touketsu.core.orig_init` can be used to gain access to a class's
original undecorated :func:`__init__` function, which is necessary when
subclassing a decorated class.

.. autosummary::
   :toctree: generated
   :template: decorator.rst

   ~touketsu.core.orig_init
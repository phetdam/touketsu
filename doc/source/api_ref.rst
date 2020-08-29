.. api reference page for touketsu

API Reference
=============

This page lists the main ``touketsu`` components. Please refer to the
:doc:`./user_guide` for usage details.

Below we list the main decorators that will be accessed by users.

.. autosummary::
   :toctree: generated
   :template: decorator.rst

   ~touketsu.core.immutable
   ~touketsu.core.identity_immutable
   ~touketsu.core.nondynamic
   ~touketsu.core.identity_nondynamic

These are produced by the factory method
:func:`~touketsu.core.class_decorator_factory` listed below.

.. autosummary::
   :toctree: generated

   ~touketsu.core.class_decorator_factory

The class decorator :func:`~touketsu.core.urt_class` undos the effect of an
applied class decorator, returning the class back to its original undecorated
state. If applied to a non-decorated class, it returns the class itself.

.. autosummary::
   :toctree: generated
   :template: decorator.rst

   ~touketsu.core.urt_class

The :func:`~touketsu.core.orig_init` can be used to gain access to a class's
original undecorated :func:`__init__` function, which is necessary when
subclassing a decorated class.

.. autosummary::
   :toctree: generated
   :template: decorator.rst

   ~touketsu.core.orig_init

The decorator :func:`~touketsu.core.urt_method` temporarily removes a
``touketsu`` restriction from a class instance during the instance method's
execution.

.. autosummary::
   :toctree: generated
   :template: decorator.rst

   ~touketsu.core.urt_method
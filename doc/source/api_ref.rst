.. api reference page for touketsu

   Changelog:

   07-05-2020

   add more autosummary for decorators and some of the new decorators.

   07-03-2020

   initial creation. first attempt making documentation that actually looks
   legit, as i looked at the arch package's documentation for inspiration.
   add template to classes autosummary to use own class template. add link
   and sentence directing user to user guide.

API Reference
=============

This page lists the two classes that form of the core of this package. For detailed examples and best practices for using the classes in this package, please refer to the :doc:`./user_guide`.

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

   ~touketsu.core.immutable
   ~touketsu.core.fancy_immutable
   ~touketsu.core.nondynamic
   ~touketsu.core.fancy_nondynamic

If these decorators are too limited for one's use case, ``touketsu`` also provides a simple decorator factory function for users to write their own modified class decorators.

.. autosummary::
   :toctree: generated
   :nosignatures:

   ~touketsu.core.class_decorator_factory

The class decorator :func:`~touketsu.core.unrestrict` can be used to undo the effect of an applied decorator and return the class back to its original undecorated state, removing all extra class attributes introduced by decoration.

.. autosummary::
   :toctree: generated

   ~touketsu.core.unrestrict

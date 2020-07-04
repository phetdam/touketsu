.. user guide on how to use FrozenClass and NDClass

   Changelog:

   07-04-2020

   moved all the section content into separate documents and instead added
   toctree. add note that base_classes.rst is doc on bad practices. add caption
   to toctree and update paths to user guide docs.

   07-03-2020

   initial creation with touch. added document title and section titles. renamed
   file from examples.rst to user_guide.rst. statr using ~ to get shortened ref
   links that only use the top-level object name. added more examples, starting
   with simple mixin use of NDClass and FrozenClass (in progress).

User Guide
==========

This guide contains detailed examples of how to use both the :class:`touketsu.core.NDClass` and :class:`touketsu.core.FrozenClass` classes in different contexts and covers best practices.

.. note::

   The :doc:`./user_guide/base_classes` document describes a usage of the ``touketsu`` classes that is considered very bad practice. If possible, please follow the practice described in :doc:`./user_guide/best_practices`.

.. toctree::
   :maxdepth: 3
   :caption: Contents

   user_guide/best_practices
   user_guide/simple_mixin
   user_guide/multiple_inheritance
   user_guide/base_classes









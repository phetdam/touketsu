.. short document on best practices.

   Changelog:

   07-04-2020

   initial creation; taken from original user_guide doc. added changelog;
   corrected link refernce to base_classes.rst; moved caution to top.

Best practices
==============

.. caution::

   Mixing in :class:`~touketsu.core.NDClass` or :class:`~touketsu.core.FrozenClass` should involve either one or the other, but not both. Mixing in :class:`~touketsu.core.NDClass` and calling :meth:`~touketsu.core.NDClass._make_nondynamic` in the :meth:`__init__` method of the subclass results in the subclass acquiring a strict subset of the restrictions acquired from mixing in :class:`~touketsu.core.FrozenClass` and calling :meth:`~touketsu.core.FrozenClass._freeze` in the :meth:`__init__` method of the subclass. Therefore, mixing in both classes and enforcing the restrictions of each by calling both :meth:`~touketsu.core.NDClass._make_nondynamic` and :meth:`~touketsu.core.FrozenClass._freeze` in the subclass :meth:`__init__` method is simply unnecessary and bad practice.

It is possible to sum up best practices for mixing in the :class:`~touketsu.core.NDClass` and :class:`~touketsu.core.FrozenClass` in one sentence:

.. admonition:: Best practice

   Only mix into child classes that will not be subclassed, calling :meth:`~touketsu.core.NDClass._make_nondynamic` or :meth:`~touketsu.core.FrozenClass._freeze` methods as necessary as the final statement of each child class's :meth:`__init__` method.

Although it is possible to mix in :class:`~touketsu.core.NDClass` or :class:`~touketsu.core.FrozenClass` into a base class and then subclass that base class, calling :meth:`~touketsu.core.NDClass._make_nondynamic` or :meth:`~touketsu.core.FrozenClass._freeze` as necessary as the final statement of each child class's :meth:`__init__` method, as detailed in the :doc:`./base_classes` document, it is highly discouraged and to be considered very bad practice. Interestingly, one can sum up the wrong way to mix the :class:`~touketsu.core.NDClass` or :class:`~touketsu.core.FrozenClass` in one sentence as well:

.. admonition:: Bad practice

   Only mix into a common parent class, and for each of its child classes, call :meth:`~touketsu.core.NDClass._make_nondynamic` or :meth:`~touketsu.core.FrozenClass._freeze` as necessary as the final statement of each child class's :meth:`__init__` method.

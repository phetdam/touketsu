.. document on how to not use the mixins with base classes.

   07-04-2020

   initial creation; taken from original user_guide doc. added changelog.
   shortened title to fit on the sidebar. corrected link to best_practices.rst.

Mixing into base classes
========================

.. caution::

   It is highly recommended that you do **not** do this. The following section is provided only for completeness, in the highly unlikely case that this is the only option available.

Consider the following scenario, in which we want to mix in :class:`~touketsu.core.NDClass` or :class:`~touketsu.core.FrozenClass` into a base class that we intend to subclass later on. Since the idea is the same when using both the :class:`~touketsu.core.FrozenClass` and the :class:`~touketsu.core.NDClass`, with the only difference being in whether we call :meth:`~touketsu.core.FrozenClass._freeze` or :meth:`~touketsu.core.NDClass._make_nondynamic`, we will use the :class:`~touketsu.core.NDClass` for our example to avoid repetition.

Again, this is something to avoid if at all possible.

What doesn't work
-----------------

Suppose that we want to define a base class :class:`BaseClass` that inherits :class:`~touketsu.core.NDClass`, has instance attributes ``a`` and ``b``, and has an :meth:`__init__` method of that takes only keyword arguments. Now suppose that we have already imported :class:`~touketsu.core.NDClass` from the top-level namespace and in all our wisdom have decided to define :class:`BaseClass` as follows:

.. code:: python

   class BaseClass(NDClass):

       def __init__(self, a = "a", b = "b"):
           self.a = a
	   self.b = b
	   self._make_nondynamic()

This is exactly what we do not want to do if we intend to subclass :class:`BaseClass`. It should be apparent as to why this is a terrible idea, but for the sake of completeness, we will continue along with our example to show what happens if we try and subclass this definition of :class:`BaseClass`.

Suppose we try and define a subclass of :class:`BaseClass` called :class:`ChildClass` that overrides the defaults for ``a`` and ``b`` in the :meth:`__init__` method of :class:`BaseClass` and also has a third instance attribute ``c`` that corresponds to a keyword argument in the :meth:`__init__` method of :class:`ChildClass` that has a default value of ``"c"``. We would thus define :class:`ChildClass` as

.. code:: python

   class ChildClass(BaseClass):

       def __init__(self, a = "aa", b = "bb", c = "c"):
           super().__init__(self, a = a, b = b)
	   self.c = c

What will happen when we create an instance of :class:`ChildClass`? We will get an :class:`AttributeError`, as after the :func:`super` call, :class:`ChildClass` is already nondynamic. The last line of the :class:`ChildClass` :meth:`__init__` method will fail as the :meth:`__setattr__` method defined in :class:`~touketsu.core.NDClass` raises

::

   AttributeError: NDClass instances cannot dynamically create new instance attributes

Since this doesn't work, now let's discuss what does work, along with a reminder of what is the best practice, which is to **not** mix :class:`~touketsu.core.NDClass` or :class:`~touketsu.core.FrozenClass` into a base class intended for subclassing.

What does work
--------------

For our example to work, the only thing we need to change is the move the call to :meth:`~touketsu.core.NDClass._make_nondynamic` from the :meth:`__init__` method of :class:`BaseClass` to the :meth:`__init__` method of :class:`ChildClass`. Therefore, we would define :class:`BaseClass` and :class:`ChildClass` as follows:

.. code:: python

   class BaseClass(NDClass):

       def __init__(self, a = "a", b = "b"):
           self.a = a
	   self.b = b

   class ChildClass(BaseClass):

       def __init__(self, a = "aa", b = "bb", c = "c"):
           super().__init__(self, a = a, b = b)
	   self.c = c
	   self._make_nondynamic()

Although this does work, as we have mentioned several times already, this is bad practice. It looks like :class:`BaseClass` instances should be nondynamic, but this behavior is not enforced through a call to :meth:`~touketsu.core.NDClass._make_nondynamic` so dynamic instance attribute creation is still possible. Instances of :class:`ChildClass` are nondynamic, as :meth:`~touketsu.core.NDClass._make_nondynamic` is called in the :meth:`__init__` of :class:`ChildClass`, but if one fails to see the call to :meth:`~touketsu.core.NDClass._make_nondynamic` in its :meth:`__init__` method and is unaware that :class:`BaseClass` has :class:`~touketsu.core.NDClass` mixed in, :class:`ChildClass` appears to still support dynamic instance attribute creation when in reality attempting to do so will result in an :class:`AttributeError`.

If we were following best practices, we would define :class:`BaseClass` and :class:`ChildClass` as follows:

.. code:: python

   class BaseClass:

       def __init__(self, a = "a", b = "b"):
           self.a = a
	   self.b = b

   class ChildClass(BaseClass, NDClass):

       def __init__(self, a = "aa", b = "bb", c = "c"):
           super().__init__(self, a = a, b = b)
	   self.c = c
	   self._make_nondynamic()

We can easily see why the second set of definitions is considered the best practice. It is clear that :class:`BaseClass` supports dynamics instance attribute creation, as :class:`~touketsu.core.NDClass` is not mixed in. Also, the definition of :class:`ChildClass` makes it clear that :class:`ChildClass` should be nondynamic, as :class:`~touketsu.core.NDClass` is mixed in and :meth:`~touketsu.core.NDClass._make_nondynamic` is called in the last line of the :meth:`__init__` method of :class:`ChildClass` to force any class instances to be nondynamic.

Again, please avoid mixing in :class:`~touketsu.core.NDClass` or :class:`~touketsu.core.FrozenClass` into bases classes if possible. Follow the best practice for mixing in these classes, which can be found in :doc:`./best_practices`.

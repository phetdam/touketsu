.. user guide on how to use FrozenClass and NDClass

   Changelog:

   07-03-2020

   initial creation with touch. added document title and section titles. renamed
   file from examples.rst to user_guide.rst. statr using ~ to get shortened ref
   links that only use the top-level object name. added more examples, starting
   with simple mixin use of NDClass and FrozenClass (in progress).

User Guide
==========

This document contains detailed examples of how to use both the :class:`touketsu.core.NDClass` and :class:`touketsu.core.FrozenClass` classes in different contexts and covers best practices.

Best practices
--------------

It is possible to sum up best practices for mixing in the :class:`~touketsu.core.NDClass` and :class:`~touketsu.core.FrozenClass` in one sentence:

.. admonition:: Best practice

   Only mix into child classes that will not be subclassed, calling :meth:`~touketsu.core.NDClass._make_nondynamic` or :meth:`~touketsu.core.FrozenClass._freeze` methods as necessary as the final statement of each child class's :meth:`__init__` method.

Although it is possible to mix in :class:`~touketsu.core.NDClass` or :class:`~touketsu.core.FrozenClass` into a base class and then subclass that base class, calling :meth:`~touketsu.core.NDClass._make_nondynamic` or :meth:`~touketsu.core.FrozenClass._freeze` as necessary as the final statement of each child class's :meth:`__init__` method, as detailed in `Defining frozen or nondynamic base classes`_, it is highly discouraged and to be considered very bad practice. Interestingly, one can sum up the wrong way to mix the :class:`~touketsu.core.NDClass` or :class:`~touketsu.core.FrozenClass` in one sentence as well:

.. admonition:: Bad practice

   Only mix into a common parent class, and for each of its child classes, call :meth:`~touketsu.core.NDClass._make_nondynamic` or :meth:`~touketsu.core.FrozenClass._freeze` as necessary as the final statement of each child class's :meth:`__init__` method.

.. caution::

   Mixing in :class:`~touketsu.core.NDClass` or :class:`~touketsu.core.FrozenClass` should involve either one or the other, but not both. Mixing in :class:`~touketsu.core.NDClass` and calling :meth:`~touketsu.core.NDClass._make_nondynamic` in the :meth:`__init__` method of the subclass results in the subclass acquiring a strict subset of the restrictions acquired from mixing in :class:`~touketsu.core.FrozenClass` and calling :meth:`~touketsu.core.FrozenClass._freeze` in the :meth:`__init__` method of the subclass. Therefore, mixing in both classes and enforcing the restrictions of each by calling both :meth:`~touketsu.core.NDClass._make_nondynamic` and :meth:`~touketsu.core.FrozenClass._freeze` in the subclass :meth:`__init__` method is simply unnecessary and bad practice.

Simple mixin use
----------------

The easiest way to get started with using the :class:`~touketsu.core.NDClass` and :class:`~touketsu.core.FrozenClass` mixins is with a simple example. Suppose we have a class ``a_class`` defined as follows:

.. code:: python

   class a_class:

       def __init__(self, a = "a", b = "b", c = "c"):
           self.a = a
	   self.b = b
	   self.c = c

       def as_tuple(self): return (self.a, self.b, self.c)

If we were to define this in the Python interpreter, create an ``a_class`` instance, we could observe the somewhat surprising results shown in block below.

>>> aa = a_class()
>>> aa.a
'a'
>>> aa.as_tuple()
('a', 'b', 'c')
>>> aa.new_ting
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'a_class' object has no attribute 'new_ting'
>>> aa.new_ting = 19203
>>> aa.new_ting
19203

This is odd--our definition of ``a_class`` did not include the instance attribute ``new_ting``, which we created dynamically at runtime when we performed the assignment ``aa.new_ting = 19203``. Although this behavior is the default Python class behavior, it can be undesirable for many reasons. For example, suppose we need to assign a new value to ``c``, but accidentally type ``self.d`` instead of ``self.c``. This is perfectly legal and will silently introduce a bug into seemingly normal code.

Using the NDClass
~~~~~~~~~~~~~~~~~

However, the :class:`~touketsu.core.NDClass` mixin allows one to create classes that disallow dynamic instance attribution creation, in effect making Python class instances behave more like those typically found in languages like Java and C++. Using :class:`~touketsu.core.NDClass` preserves all the normal attributes of a Python class, for example the :attr:`~object.__dict__` and :attr:`__weakref__` attributes, with minimal influence on class inheritance structure and minimal changes made to the existing class definition compared to using :attr:`__slots__`.

.. note::

   Although it is seemingly possible to enforce this behavior using :attr:`__slots__`, it is messier to use :attr:`__slots__` with an existing system of class inheritance and there are several changes in class behavior that need to be noted if the decision to use :attr:`__slots__` is made. See the `Python data model documentation`__ for details on using :attr:`__slots__`.

   .. __: https://docs.python.org/3/reference/datamodel.html#slots

To use :class:`~touketsu.core.NDClass`, all we need to do is mix it in and call :meth:`~touketsu.core.NDClass._make_nondynamic` after defining all ``a_class`` instance attributes. We first import :class:`~touketsu.core.NDClass` from ``touketsu`` into the current namespace:

.. code:: python

   from touketsu import NDClass

Then, we just need to modify our definition of ``a_class`` into

.. code:: python

   class a_class(NDClass):

       def __init__(self, a = "a", b = "b", c = "c"):
           self.a = a
	   self.b = b
	   self.c = c
	   self._make_nondynamic()

       def as_tuple(self): return (self.a, self.b, self.c)

Instances of :class:`a_class` will now be unable to acquire new instance attributes at runtime unless the :attr:`~object.__dict__` attribute is manipulated manually. In the Python interpreter, if we were to redefine ``a_class`` in this manner and create an instance ``ab``, we could observe the following results.

>>> ab = a_class()
>>> ab.a
'a'
>>> ab.new_ting
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'a_class' object has no attribute 'new_ting'
>>> ab.new_ting = 257
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "c:\Users\D\START\python3\lib\site-packages\touketsu-0.1.0-py3.8.egg\touketsu\core.py", line 119, in __setattr__
AttributeError: NDClass instances cannot dynamically create new instance attributes

Say goodbye to silently introducing bugs through fat-finger errors.

Using the FrozenClass
~~~~~~~~~~~~~~~~~~~~~

However, in some instances, disallowing dynamic class instance attribute creation is not enough. Rather, one may want to make class instances immutable, in which case :class:`~touketsu.core.FrozenClass` should be used instead.

.. note::

   Section in progress.

Multiple inheritance
--------------------

The :class:`~touketsu.core.NDClass` and :class:`~touketsu.core.FrozenClass` mixins work well with multiple inheritance, as we will show. Suppose we have the classes ``a_class`` and ``b_class``, which have the definitions

.. code:: python

   class a_class:

       def __init__(self, a, b = "aaa"):
           self.a = a
           self.b = b

   class b_class:

       def __init__(self, c = "xxx", d = "yyy"):
           self.c = c
           self.d = d

Now suppose we want to define a class ``c_class`` which inherits from ``a_class`` and ``b_class``. ``c_class`` introduces one new instance attribute ``x`` and overrides some keyword argument defaults passed to the :meth:`__init__` methods of ``a_class`` and ``b_class``. If we wanted to also define ``c_class`` to have immutable instances, we could define ``c_class`` as follows: [#]_

.. code:: python

   class c_class(a_class, b_class, FrozenClass):

       def __init__(self, a, b = "bbb", c = "ccc", d = "ddd", x = -1):
           a_class.__init__(self, a, b = b)
	   b_class.__init__(self, c = c, d = d)
	   self.x = x
	   self._freeze()

Instances of :class:`c_class` are now immutable. Assuming we have a :class:`c_class` instance ``aci``, operations like ``aci.a = 3`` and ``aci.d = "cheese"`` would result in an :class:`AttributeError` being raised by the :meth:`__setattr__` method defined in :class:`~touketsu.core.FrozenClass`.

.. [#] Note that we opt to use explicit :meth:`__init__` calls since ``a_class`` and ``b_class`` have different :meth:`__init__` signatures. Cooperative subclassing by calling :func:`super` could also be used, but only if we allow each :meth:`__init__` signature to support variable arguments and keyword arguments. Please see `this StackOverflow post`__ for a nice explanation.

.. __: https://stackoverflow.com/questions/26927571/multiple-inheritance-in-python3-with-different-signatures

Defining frozen or nondynamic base classes
------------------------------------------

.. caution::

   It is highly recommended that you do **not** do this. The following section is provided only for completeness, in the highly unlikely case that this is the only option available.

Consider the following scenario, in which we want to mix in :class:`~touketsu.core.NDClass` or :class:`~touketsu.core.FrozenClass` into a base class that we intend to subclass later on. Since the idea is the same when using both the :class:`~touketsu.core.FrozenClass` and the :class:`~touketsu.core.NDClass`, with the only difference being in whether we call :meth:`~touketsu.core.FrozenClass._freeze` or :meth:`~touketsu.core.NDClass._make_nondynamic`, we will use the :class:`~touketsu.core.NDClass` for our example to avoid repetition.

Again, this is something to avoid if at all possible.

What doesn't work
~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~

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

Again, please avoid mixing in :class:`~touketsu.core.NDClass` or :class:`~touketsu.core.FrozenClass` into bases classes if possible. Follow the best practice for mixing in these classes, which can be found in `Best practices`_.

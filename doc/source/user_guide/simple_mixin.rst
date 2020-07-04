.. document on basic use of the mixin classes.

   Changelog:

   07-04-2020

   initial creation; taken from original user_guide doc. added changelog.

Simple mixin use
================

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
-----------------

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
---------------------

However, in some instances, disallowing dynamic class instance attribute creation is not enough. Rather, one may want to make class instances immutable, in which case :class:`~touketsu.core.FrozenClass` should be used instead.

.. note::

   Section in progress.

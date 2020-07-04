.. document on using the mixins with multiple inheritance.

   Changelog:

   07-04-2020
   
   initial creation; taken from original user_guide doc. added changelog.

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

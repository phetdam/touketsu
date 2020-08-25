__doc__ = "Some test classes for testing ``touketsu`` functions."

from abc import ABCMeta, abstractmethod
import math
from random import Random
import sys

from ..core import immutable, nondynamic, orig_init, urt_class, urt_method
from . import srepr, vrepr

_global_random_state = Random()
"""Module level :class:`random.Random` instance.

Avoids state issues if other methods outside of this module are modifying the
state of the module-level :class:`random.Random` instance created upon import of
the ``random`` module. This instance is the ``_inst`` attribute defined in
https://github.com/python/cpython/blob/3.8/Lib/random.py.
"""


@immutable
@vrepr
class a_class:
    """Test class whose methods can create and delete instance/class attributes.
    
    :param a: Parameter ``a``
    """
    def __init__(self, a = "a"):
        self.a = a
        # updated when crate_attr is called
        self.create_attr_called = False
    
    @classmethod
    def random_aa(cls, width = 1, random_state = None):
        """Adds/deletes the class attribute ``aa`` to/from  :class:`a_class`.
        
        .. admonition:: Remark.
        
           This is a terribly useless method.
        
        Not affected by ``touketsu`` class decorators. Returns value of ``aa``,
        which is either a random number in the range ``[0, width)``, or ``None``
        if ``aa`` was deleted by this method.
        
        :param width: Width of range to uniformly sample from, default ``1``.
        :type width: float, optional
        :param random_state: A shared :class:`random.Random` instance or an
            integer seed for :attr:`_global_random_state`, default ``None``
            to use :attr:`_global_random_state` without seeding.
        :type random_state: :class:`random.Random` or int, optional
        """
        val = None
        if hasattr(cls, "aa"): delattr(cls, "aa")
        else:
            # use existing _global_random_state
            if random_state is None:
                cls.aa = _global_random_state.random() * width
            # else if int, seed _global_random_state
            elif isinstance(random_state, int):
                _global_random_state.seed(a = random_state)
                cls.aa = _global_random_state.random() * width
            # else use state of the random_state
            elif isinstance(random_state, Random):
                cls.aa = random_state.random() * width
            # else TypeError
            else: raise TypeError("random_state must be int or random.Random")
            val = cls.aa
        return val
    
    @classmethod
    def has_aa(cls):
        """Returns ``True`` if ``aa`` is a class attribute, ``False`` otherwise.
        
        :rtype: bool
        """
        return hasattr(cls, "aa")

    @urt_method
    def create_attr(self, attr, shift = 0, random_state = None):
        """Creates an instance attribute ``attr`` with a random float value.
        
        .. note:: This would raise :class:`AttributeError` if it was not
           decorated with :func:`~touketsu.core.urt_method`.

        The random float value is in the range ``[shift, shift + 1)``. Also
        updates instance attribute :attr:`create_attr_called`.
        
        :param attr: Attribute name. Cannot be the name of an existing member.
        :type attr: str
        :param shift: Determines range of generated value
        :type shift: int or float, optional
        :param random_state: A shared :class:`random.Random` instance or an
            integer seed for :attr:`_global_random_state`, default ``None``
            to use :attr:`_global_random_state` without seeding.
        :type random_state: :class:`random.Random` or int, optional
        :rtype: None
        """
        if attr is self.__dict__:
            raise KeyError(f"attribute {attr} already exists")
        # if None, use current state of _global_random_state
        if random_state is None:
            self.__setattr__(attr, _global_random_state.random() + shift)
        # seed _global_random_state if int or use state of random_state
        elif isinstance(random_state, int):
            _global_random_state.seed(a = random_state)
            self.__setattr__(attr, _global_random_state.random() + shift)
        elif isinstance(random_state, Random):
            self.__setattr__(attr, random_state.random() + shift)
        # else TypeError
        else: raise TypeError("random_state must be int or random.Random")
        # update self.create_attr_called
        self.create_attr_called = True

# note: vrepr/srepr decoration order does not matter
@vrepr
@nondynamic
class b_class:
    """Test class with stochastic static method and stochastic class method.
    
    :param b: Parameter ``b``
    """
    
    b_default = 8.888
    "Default value for ``b`` if ``b`` is not numeric."
    
    def __init__(self, b = "b"):
        self.b = b
        # won't show up in repr, but is used by b_static_method
        if isinstance(self.b, (int, float)): self._b = math.sqrt(b)
        else: self._b = math.sqrt(self.b_default)

    @staticmethod
    def random_member_avg(*args, weights = None, random_state = None):
        """Return random weighted average of :class:`b_class` instance members.
        
        For each :class:`b_class` instance passed to args, there is a half-half
        chance that its ``_b`` member will be used instead of its ``b`` member
        in the final result returned by the method. If ``b`` is not numeric,
        then the value of :attr:`b_class.b_default` will be used instead.
        
        :param args: :class:`b_class` instances.
        :param weights: Iterable of float weights, default ``None``. Weights
            must add up to 1, or a :class:`ValueError` will be raised.
        :type weights: iterable, optional
        :param random_state: A shared :class:`random.Random` instance or an
            integer seed for :attr:`_global_random_state`, default ``None``
            to use :attr:`_global_random_state` without seeding.
        :type random_state: :class:`random.Random` or int, optional
        :returns: Weighted average of members of the :class:`b_class` instances
            passed to ``args``.
        :rtype: float
        """
        # get number of arguments passed to args
        nargs = len(args)
        if nargs == 0: raise ValueError("at least one positional arg required")
        # get weights if None + check they add up to 1
        if weights is None: weights = [1 / nargs for _ in range(nargs)]
        if sum(weights) != 1: raise ValueError("weights must add up to 1")
        # random.Random instance to generate random values with
        rr = _global_random_state
        # if random_state is None, use existing state of _global_random_state
        if random_state is None: pass
        # else if random_state is int, seed _global_random_state (rr)
        elif isinstance(random_state, int):
            _global_random_state.seed(a = random_state)
        # else if random_state is random.Random instance, use its state
        elif isinstance(random_state, Random): rr = random_state
        # else wrong type
        else: raise TypeError("random_state must be int or random.Random")
        # get the weighted average
        total = 0
        for arg, w in zip(args, weights):
            if rr.random() < 0.5: total = total + w * arg._b
            else:
                if isinstance(arg.b, (int, float)): total = total + w * arg.b
                else: total = total + w * arg.b_default
        return total

    @classmethod
    def touch_b_default(cls, random_state = None):
        r"""Doubles or halves :attr:`b_class.b_default` with equal probability.
        
        
        The expected value of :attr:`~b_class.b_default` after ``n`` calls of
        :meth:`touch_b_default` is :math:`8.888 * 1.25^n`. Here is a proof.
        
        *Proof.* Define :math:`I_k, k \in \{1, \ldots n\}`, where
        :math:`I_k \in \{1 / 2, 2\}`, i.i.d., and
        :math:`\mathbb{P}\{I_k = 1 / 2\} = \mathbb{P}\{I_K = 2\} = 1 / 2`.
        Define :math:`X_0 \triangleq 8.888`. Note that :math:`\forall k`,
        
        .. math::
        
           \mathbb{E}[I_k] = \frac{1}{2}(2) + \frac{1}{2}\left(\frac{1}{2}) =
           \frac{5}{4}
           
        Therefore, since each :math:`I_k` is i.i.d., we see that
        
        .. math::
        
           X_n = X_0\prod_{k = 1}^nI_k \Rightarrow \mathbb{E}[X_n] = 
           X_0\prod_{k = 1}^n\mathbb{E}[I_k] = X_0\left(\frac{5}{4})^n
           
        Since :math:`X_0 = 8.888`, we are done.
        
        :param random_state: A shared :class:`random.Random` instance or an
            integer seed for :attr:`_global_random_state`, default ``None``
            to use :attr:`_global_random_state` without seeding.
        :type random_state: :class:`random.Random` or int, optional
        """
        # random.Random to use
        rr = _global_random_state
        # if random_state is int, see _global_random_state. if random_state is
        # a random.Random instance, use its existing state.
        if random_state is None: pass
        elif isinstance(random_state, int):
            _global_random_state.seed(a = random_state)
        elif isinstance(random_state, Random): rr = random_state
        else: raise TypeError("random_state must be int or random.Random")
        # randomly double or halve b_default
        if rr.random() < 0.5: cls.b_default = cls.b_default * 2
        else: cls.b_default = cls.b_default / 2


# note that __repr__ is inherited from a_class due to the MRO.
@immutable
class c_class(a_class, b_class):
    """Test class that modifies existing instance attributes.
    
    :param a: Parameter ``a``
    :param b: Parameter ``b``
    :param c: Parameter ``c``
    """
    def __init__(self, a = "aa", b = "bb", c = "c"):
        orig_init(a_class.__init__)(self, a = a)
        orig_init(b_class.__init__)(self, b = b)
        self.c = c
        ## does not show up in __repr__ ##
        # modified internally; check if c is dirty after make_c_dirty is called.
        self.c_is_dirty = False

    @urt_method
    def make_c_dirty(self, random_state = None):
        """Randomly set ``c`` to a numeric value in ``[0, 1)``.
        
        Also sets the :attr:`c_is_dirty` attribute to ``True``.
        
        :param random_state: A shared :class:`random.Random` instance or an
            integer seed for :attr:`_global_random_state`, default ``None``
            to use :attr:`_global_random_state` without seeding.
        :type random_state: :class:`random.Random` or int, optional
        """
        # random.Random to use
        rr = _global_random_state
        # if random_state is int, see _global_random_state. if random_state is
        # a random.Random instance, use its existing state.
        if random_state is None: pass
        elif isinstance(random_state, int):
            _global_random_state.seed(a = random_state)
        elif isinstance(random_state, Random): rr = random_state
        else: raise TypeError("random_state must be int or random.Random")
        # make self.c dirty and set _c_is_dirty to True
        self.c = rr.random()
        self.c_is_dirty = True
        
    @urt_method
    def make_c_clean(self):
        "Sets :attr:`c_is_dirty` to ``False``."
        self.c_is_dirty = False

@immutable
@vrepr
class an_abc(metaclass = ABCMeta):
    """Class type :class:`abc.ABCMeta` with an abstact method.
    
    :param a: Parameter ``a``
    """
    def __init__(self, a = "_a"): self.a = a

    @abstractmethod
    def random_touch_ab(self): pass


def _random_touch_ab(self, random_state = None):
    """Randomly assigns ``a`` and ``b`` attributes values in ``[0, 1)``.
    
    Not decorated with :func:`~touketsu.core.urt_method`, so will fail.
    
    :param random_state: A shared :class:`random.Random` instance or an
        integer seed for :attr:`_global_random_state`, default ``None``
        to use :attr:`_global_random_state` without seeding.
    :type random_state: :class:`random.Random` or int, optional
    """
    # random.Random to use
    rr = _global_random_state
    # if random_state is int, see _global_random_state. if random_state is
    # a random.Random instance, use its existing state.
    if random_state is None: pass
    elif isinstance(random_state, int):
        _global_random_state.seed(a = random_state)
    elif isinstance(random_state, Random): rr = random_state
    else: raise TypeError("random_state must be int or random.Random")
    # randomly assign values
    self.a = rr.random()
    self.b = rr.random()


class abc_child_a(an_abc):
    """Subclass of :class:`an_abc`. Inherits ``touketsu`` restriction.
    
    Restriction inherited due to no :meth:`__init__` override.
    """
    def random_touch_ab(self, random_state = None):
        """Wraps :func:`_random_touch_ab`.
        
        Not wrapped with :func:`~touketsu.core.urt_method`, so will fail.
        
        See :func:`_random_touch_ab` for method details.
        """
        return _random_touch_ab(self, random_state = random_state)
    
    @urt_method
    def random_touch_ab_urt(self, random_state = None):
        """Wraps :func:`_random_touch_ab`.
        
        Succeeds since it is wrapped with :func:`~touketsu.core.urt_method`.
        
        See :func:`_random_touch_ab` for method details.
        """
        return _random_touch_ab(self, random_state = random_state)


@urt_class
class abc_child_b(an_abc):
    """Subclass of :class:`an_abc`. Inherits ``touketsu`` restriction.
    
    Inherited restriction due to no :meth:`__init__` override removed with
    :func:`~touketsu.core.urt_class`.
    """
    def random_touch_ab(self, random_state = None):
        """Wraps :func:`_random_touch_ab`.
        
        Succeeds since :class:`abc_child_b` is decorated with
        :func:~touketsu.core.urt_class`.
        
        See :func:`_random_touch_ab` for method details.
        """
        return _random_touch_ab(self, random_state = random_state)


if __name__ == "__main__": 
    print(f"{__file__}: do not run module as script.", file = sys.stderr)
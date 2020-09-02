__doc__ = "Tests some core features of ``touketsu`` using the test classes."

import pytest
from random import Random
import textwrap

from .classes import (a_class, b_class, c_class, an_abc, abc_child_a,
                      abc_child_b, almost_one)
from .fixtures import _GLOBAL_SEED, global_random_state

_module_random_state = Random()
"""Module level :class:`random.Random` instance.

Avoids state issues if other methods outside of this module are modifying the
state of the module-level :class:`random.Random` instance created upon import of
the ``random`` module. This instance is the ``_inst`` attribute defined in
https://github.com/python/cpython/blob/3.8/Lib/random.py.
"""

## -- Non-test functions -------------------------------------------------------

def random_weights(n, dist = "uniform", random_state = None):
    """Create ``n`` random weights that sum up to 1.
    
    :param n: Number of weights to randomly generate.
    :type n: int
    :param dist: Distribution the weights should be drawn from. Default is
        ``"uniform"``. Other options are ``"normal"`` for normally distributed
        weights with variance ``1``, guaranteed to be nonnegative,
        ``"exponential"`` for exponentially distributed weights with parameter
        ``1``, and ``"lognormal"`` for lognormally distributed weights with
        ``mu = 0`` and ``sigma = 1``.
    :param random_state: Optional :class:`random.Random` instance to use for
        random number generation. If not provided, :attr:`_module_random_state`
        is used.
    :type random_state: :class:`random.Random`, optional
    """
    # check n
    assert isinstance(n, int) and (n > 0)
    # default Random instance created upon module import
    rr = _module_random_state
    if random_state is None: pass
    elif isinstance(random_state, Random): rr = random_state
    else: raise TypeError("random_state must be None or random.Random instance")
    # args for distribution functions
    dargs = (0, 1) # for uniform distribution
    # function to generate deviates
    rfunc = rr.uniform
    if dist == "uniform": pass
    elif dist == "normal":
        dargs = (15, 1) # make it essentially impossible for negative weights
        rfunc = rr.gauss
    elif dist == "exponential": dargs, rfunc = (1,), rr.expovariate
    elif dist == "lognormal": rfunc = rr.lognormvariate
    else:
        raise ValueError("dist must be one or \"uniform\", \"normal\", "
                         "\"exponential\", or \"lognormal\"")
    # create weights using rfunc and dargs
    weights = list(map(lambda x: rfunc(*x), [dargs for _ in range(n)]))
    weights_sum = sum(weights)
    # normalize the weights so they add up to 1
    return tuple(map(lambda x: x / weights_sum, weights))


## -- Fixtures -----------------------------------------------------------------

@pytest.fixture(scope = "function")
def a_class_instance():
    """Return default :class:`~touketsu.tests.classes.a_class` instance.
    
    Default value for ``scope`` is ``"function"``.
    """
    return a_class()


@pytest.fixture
def b_class_instance():
    "Return default :class:`~touketsu.tests.classes.b_class` instance."
    return b_class()


@pytest.fixture(scope = "module", params = [("b1", "b2", "b3", "b4", "b5")])
def b_class_instances(request):
    """Return several :class:`~touketsu.tests.classes.b_class` instances.
    
    :rtype: tuple
    """
    return tuple(map(b_class, request.param))    


@pytest.fixture
def c_class_instance():
    "Return default :class:`~touketsu.tests.classes.c_class` instance."
    return c_class()


## -- Tests --------------------------------------------------------------------

## a_class tests ##

def test_aa_creation(a_class_instance, global_random_state):
    """Test :meth:`touketsu.tests.classes.a_class.random_aa` ``aa`` creation.
    
    Call :meth:`~touketsu.tests.classes.a_class.random_aa` once and then call
    :meth:`~touketsu.tests.classes.a_class.has_aa` to determine if the class
    attribute ``aa`` is created in :class:`~touketsu.tests.classes.a_class`.
    
    :param a_class_instance: :func:`a_class_instance` ``pytest`` fixture.
    :type a_class_instance: :class:`~touketsu.tests.classes.a_class`
    :param global_random_state: :func:`global_random_state` ``pytest`` fixture.
    :type global_random_state: :class:`random.Random`
    """
    a_class_instance.random_aa(random_state = global_random_state)
    assert a_class_instance.has_aa()


def test_aa_deletion(a_class_instance, global_random_state, n_calls = 4):
    """Test :meth:`touketsu.tests.classes.a_class.random_aa` ``aa`` deletion.
    
    Call :meth:`~touketsu.tests.classes.a_class.random_aa` an even number of
    times to determine if class attribute deletion is working fine. Also prints
    the values assigned to ``aa`` on odd-numbered invocations and
    the :class:`random.Random` seed used.
    
    :param a_class_instance: :func:`a_class_instance` ``pytest`` fixture.
    :type a_class_instance: :class:`~touketsu.tests.classes.a_class`
    :param global_random_state: :func:`global_random_state` ``pytest`` fixture.
    :type global_random_state: :class:`random.Random`
    :param n_calls: Number of :func:`~touketsu.tests.classes.a_class.random_aa`
        calls to make. Must be an even number, default 4.
    :type n_calls: int, optional
    """
    # n_calls must be even
    assert n_calls % 2 == 0, "n_calls must be even"
    # remove class attribute if it exists
    if hasattr(a_class_instance.__class__, "aa"):
        delattr(a_class_instance.__class__, "aa")
    # call random_aa n_calls times, print on odd calls
    vals = [0. for _ in range(n_calls // 2)]
    for i in range(n_calls):
        a_class_instance.random_aa(random_state = global_random_state)
        # write to vals if odd-numbered call
        if i % 2 == 0: vals[i // 2] = a_class_instance.__class__.aa
    # print results (only upon failure) and assert
    vals_str = textwrap.fill(str(vals), width = 80, initial_indent = " " * 4,
                             subsequent_indent = " " * 4)
    print(f"values of a_class_instance.__class__.aa:\n{vals_str}")
    print(f"_GLOBAL_SEED = {_GLOBAL_SEED}")
    # check that attribute is gone
    assert a_class_instance.has_aa() == False


@pytest.mark.parametrize("attr", ["new_1", "new_2", "new_3"])
def test_create_attr(a_class_instance, global_random_state, attr, shift = 0):
    """Test :meth:`touketsu.tests.classes.a_class.create_attr`.
    
    Create several attributes and check that they were successfully created.
    Also checks that the ``create_attr_called`` instance attribute is ``True``.
    
    :param a_class_instance: :func:`a_class_instance` ``pytest`` fixture.
    :type a_class_instance: :class:`~touketsu.tests.classes.a_class`
    :param global_random_state: :func:`global_random_state` ``pytest`` fixture.
    :type global_random_state: :class:`random.Random`
    :param attr: Name of attribute to create in ``a_class_instance``.
    :type attr: str
    :param shift: Shift range of range number generation, default ``0``.
    :type shift: float, optional
    """
    # create new attribute
    a_class_instance.create_attr(attr, shift = shift,
                                 random_state = global_random_state)
    # assert that the attribute was created
    assert hasattr(a_class_instance, attr)
    # check that create_attr_called is set
    assert a_class_instance.create_attr_called == True


## b_class tests ##

#def random_weights(n, dist = "uniform", random_state = None)
@pytest.mark.parametrize("wopt", ["equal", "uniform", "normal"])
def test_random_member_avg(b_class_instances, global_random_state, wopt):
    """Test :meth:`touketsu.tests.classes.b_class.random_member_avg`.
    
    .. note:: :meth:`~touketsu.tests.classes.b_class.random_member_avg` is a
       static method.
    
    :param b_class_instance: :func:`b_class_instance` ``pytest`` fixture.
    :type b_class_instance: :class:`~touketsu.tests.classes.b_class`
    :param global_random_state: :func:`global_random_state` ``pytest`` fixture.
    :type global_random_state: :class:`random.Random`
    :param wopt: Determines the kind of weights to use when calling
        :meth:`~touketsu.tests.classes.b_class.random_member_avg`. ``"equal"``
        passes ``None`` to the ``weights`` parameter for equal weights. Any of
        the other acceptable values that can be passed to the ``dist`` named
        argument of :func:`random_weights` can be used to randomly select
        weights from a particular distribution.
    :type wopt: str
    """
    # must have at least one b_class instance
    assert len(b_class_instances) > 0
    # generate weights
    weights = None
    if wopt == "equal": pass
    else:
        weights = random_weights(len(b_class_instances), dist = wopt,
                                 random_state = global_random_state)
    # get the result from random_member_avg; print value (show on failure)
    _class = b_class_instances[0].__class__
    ravg = _class.random_member_avg(*b_class_instances, weights = weights,
                                    random_state = global_random_state)
    print(f"ravg = {ravg}")
    # test to see if it worked
    assert isinstance(ravg, (int, float))


def test_touch_b_default(b_class_instance, global_random_state, n_calls = 8):
    """Test :meth:`touketsu.tests.classes.b_class.touch_b_default`.
    
    .. note:: :meth:`~touketsu.tests.classes.b_class.touch_b_default` is a
       class method.
    
    :meth:`~touketsu.tests.classes.b_class.touch_b_default` will be called
    ``n_calls`` times, each call doubling or halving the class attribute
    :attr:`touketsu.tests.classes.b_class.b_default` with equal probability.
    
    :param b_class_instance: :func:`b_class_instance` ``pytest`` fixture.
    :type b_class_instance: :class:`~touketsu.tests.classes.b_class`
    :param global_random_state: :func:`global_random_state` ``pytest`` fixture.
    :type global_random_state: :class:`random.Random`
    :param n_calls: Number of times to call
        :meth:`~touketsu.tests.classes.b_class.touch_b_default` in the test.
    :type n_calls: int, optional
    """
    assert isinstance(n_calls, int) and (n_calls > 0)
    # save original value of b_default
    b_old = b_class_instance.__class__.b_default
    # call touch_b_default n_calls times, checking if value has been changed
    for _ in range(n_calls):
        b_class_instance.touch_b_default(random_state = global_random_state)
        assert b_old != b_class_instance.__class__.b_default
        b_old = b_class_instance.__class__.b_default


## c_class tests ##

def test_make_c_dirty(c_class_instance, global_random_state):
    """Test :meth:`touketsu.tests.classes.c_class.make_c_dirty`.
    
    Set ``c_is_dirty`` attribute of the :class:`c_class` instance to ``True``.
    
    :param c_class_instance: :func:`c_class_instance` ``pytest`` fixture.
    :type c_class_instance: :class:`~touketsu.tests.classes.c_class`
    :param global_random_state: :func:`global_random_state` ``pytest`` fixture.
    :type global_random_state: :class:`random.Random`
    """
    c_class_instance.make_c_dirty(random_state = global_random_state)
    assert c_class_instance.c_is_dirty


def test_make_c_clean(c_class_instance, global_random_state):
    """Test :meth:`touketsu.tests.classes.c_class.make_c_clean`.
    
    Set ``c_is_dirty`` attribute of the :class:`c_class` instance to ``True``.
    
    :param c_class_instance: :func:`c_class_instance` ``pytest`` fixture.
    :type c_class_instance: :class:`~touketsu.tests.classes.c_class`
    :param global_random_state: :func:`global_random_state` ``pytest`` fixture.
    :type global_random_state: :class:`random.Random`
    """
    # forcibly set to dirty first
    object.__setattr__(c_class_instance, "c_is_dirty", True)
    # unset and assert
    c_class_instance.make_c_clean()
    assert c_class_instance.c_is_dirty == False
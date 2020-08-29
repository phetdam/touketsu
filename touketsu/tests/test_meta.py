__doc__ = "Tests ``touketsu`` features with metaclasses and inheritance."

import pytest

from .classes import abc_child_a, abc_child_b
from .test_core import global_random_state

## -- Fixtures -----------------------------------------------------------------

@pytest.fixture
def abc_child_a_instance():
    """Return default :class:`~touketsu.tests.classes.abc_child_a` instance.
    
    .. note:: Since :class:`~touketsu.tests.classes.abc_child_a` does not
       override the :meth:`~object.__init__` method of
       :class:`~touketsu.tests.classes.an_abc`, so it inherits the ``touketsu``
       restriction applied to :class:`~touketsu.tests.classes.an_abc`.
    """
    return abc_child_a()


@pytest.fixture
def abc_child_b_instance():
    """Return default :class:`~touketsu.tests.classes.abc_child_b` instance.
    
    See the note in the :func:`abc_child_a_instance` docstring.
    """
    return abc_child_b()


## -- Tests --------------------------------------------------------------------

## abc_child_a tests ##

@pytest.mark.xfail(raises = AttributeError,
                   reason = "Instance method not decorated with urt_method")
def test_a_random_touch_bad(abc_child_a_instance, global_random_state):
    """Test :meth:`touketsu.tests.classes.abc_child_a.random_touch_ab`.
    
    Expected to fail since
    :meth:`~touketsu.tests.classes.abc_child_a.random_touch_ab` is not wrapped
    with :func:`~touketsu.core.urt_method`.
    
    :param abc_child_a_instance: :func:`abc_child_a_instance` ``pytest``
        fixture.
    :type abc_child_a_instance: :class:`~touketsu.tests.classes.abc_child_a`
    :param global_random_state: :func:`global_random_state` ``pytest`` fixture.
    :type global_random_state: :class:`random.Random`
    """
    abc_child_a_instance.random_touch_ab(random_state = global_random_state)
    # these will never be reached
    assert isinstance(abc_child_a_instance.a, (int, float))
    assert hasattr(abc_child_a_instance, "b")


def test_a_random_touch_good(abc_child_a_instance, global_random_state):
    """Test :meth:`touketsu.tests.classes.abc_child_a.random_touch_ab_urt`.
    
    Succeeds since
    :meth:`~touketsu.tests.classes.abc_child_a.random_touch_ab_urt` is
    decorated with :func:`~touketsu.core.urt_method`.
    
    :param abc_child_a_instance: :func:`abc_child_a_instance` ``pytest``
        fixture.
    :type abc_child_a_instance: :class:`~touketsu.tests.classes.abc_child_a`
    :param global_random_state: :func:`global_random_state` ``pytest`` fixture.
    :type global_random_state: :class:`random.Random`
    """
    abc_child_a_instance.random_touch_ab_urt(random_state = global_random_state)
    # default value is string, check if numeric == check if a is dirty
    assert isinstance(abc_child_a_instance.a, (int, float))
    # attribute created after the method call
    assert hasattr(abc_child_a_instance, "b")


def test_b_random_touch(abc_child_b_instance, global_random_state):
    """Test :meth:`touketsu.tests.classes.abc_child_b.random_touch_ab`.
    
    Succeeds since
    :meth:`~touketsu.tests.classes.abc_child_b.random_touch_ab` is decorated
    with :func:`~touketsu.core.urt_method`.
    
    :param abc_child_b_instance: :func:`abc_child_b_instance` ``pytest``
        fixture.
    :type abc_child_a_instance: :class:`~touketsu.tests.classes.abc_child_b`
    :param global_random_state: :func:`global_random_state` ``pytest`` fixture.
    :type global_random_state: :class:`random.Random`
    """
    abc_child_b_instance.random_touch_ab(random_state = global_random_state)
    # default value is string, check if numeric == check if a is dirty
    assert isinstance(abc_child_b_instance.a, (int, float))
    # attribute created after the method call
    assert hasattr(abc_child_b_instance, "b")
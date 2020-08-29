__doc__ = "Fixtures required globally across ``touketsu`` test modules."

import pytest
from random import Random
import sys

_GLOBAL_SEED = 888
"""Seed used for :func:`global_random_state` :class:`random.Random` instance.

.. note:: This is not a fixture function but a module attribute.
"""

@pytest.fixture(scope = "session", params = [_GLOBAL_SEED])
def global_random_state(request):
    "Returns session global :class:`random.Random`, seed :attr:`_GLOBAL_SEED"
    return Random(request.param)


if __name__ == "__main__":
    print(f"{__file__}: do not run module as script.", file = sys.stderr)
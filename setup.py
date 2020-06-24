# setup.py for touketsu
#
# Changelog:
#
# 06-23-2020
#
# initial creation. maybe i should use setuptools instead of distutils.

from disutils.core import setup

_DESC = ("A package for creating classes that disallow dynamic attribute "
         "creation.")

def _setup():
    setup(name = "touketsu",
          version = "0.0.1",
          description = _DESC,
          packages = ["touketsu"]
    )

if __name__ == "__main__":
    _setup()

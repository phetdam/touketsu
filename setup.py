# setup.py for touketsu
#
# Changelog:
#
# 06-23-2020
#
# initial creation. changed from distutils to setuptools

from setuptools import setup

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

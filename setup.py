# setup.py for touketsu
#
# Changelog:
#
# 07-03-2020
#
# get version from VERSION ro prevent version conflicts with conf.py
#
# 06-26-2020
#
# removed _DESC, now desc_short, and read long description from README.rst.
# added author name, long description content type, and license.
#
# 06-23-2020
#
# initial creation. changed from distutils to setuptools

from setuptools import setup

def _setup():
    # short and long descriptions
    desc_short = ("A package for creating classes that disallow dynamic "
                  "attribute creation.")
    with open("README.rst", "r") as rmf:
        desc_long = rmf.read()
    # version
    with open("VERSION", "r") as vf:
        version = vf.read().rstrip()
    # setup
    setup(name = "touketsu",
          version = version,
          description = desc_short,
          long_description = desc_long,
          long_description_content_type = "text/x-rst",
          author = "Derek Huang",
          packages = ["touketsu"],
          license = "MIT"
    )

if __name__ == "__main__":
    _setup()

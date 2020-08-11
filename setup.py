# setup.py for touketsu

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

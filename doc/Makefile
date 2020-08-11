# Minimal makefile for Sphinx documentation. edited by Derek Huang.

SPHINXBUILD   = sphinx-build
# sphinx-build options
BUILDOPTS     = 
SOURCEDIR     = source
BUILDDIR      = build

.PHONY: help html html_clean

# put first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help $(SOURCEDIR) $(BUILDDIR) $(BUILDOPTS)

# make html documentation
html:
	@$(SPHINXBUILD) -M html $(SOURCEDIR) $(BUILDDIR) $(BUILDOPTS)

# make html documentation, but writing all output and ignoring old environment
html_clean:
	@$(RM) -f $(SOURCEDIR)/generated/*.rst
	@$(SPHINXBUILD) -M html $(SOURCEDIR) $(BUILDDIR) -E -a $(BUILDOPTS)

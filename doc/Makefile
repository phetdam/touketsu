# Minimal makefile for Sphinx documentation. edited by Derek Huang.
#
# Changelog:
#
# 07-03-2020
#
# correct mistaken use of SPHINXOPTS with BUILDOPTS. add clean build option.
# remove deletion of generated rST files from clean target and clean target.
#
# 06-30-2020 
#
# initial autogeneration by sphinx-quickstart. added changelog and got rid of
# catchall target. added clean and html targets + cleanup.

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
	@$(SPHINXBUILD) -M html $(SOURCEDIR) $(BUILDDIR) -E -a $(BUILDOPTS)

# Minimal makefile for Sphinx documentation. edited by Derek Huang.
#
# Changelog:
#
# 06-30-2020 
#
# initial autogeneration by sphinx-quickstart. added changelog and got rid of
# catchall target. added clean and htrml targets + cleanup.

SPHINXBUILD   = sphinx-build
# sphinx-build options
BUILDOPTS     = 
SOURCEDIR     = source
BUILDDIR      = build

.PHONY: clean help html

# put first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help $(SOURCEDIR) $(BUILDDIR) $(SPHINXOPTS)

# remove emacs autosave files and autosummary generated module files to force
# rebuild. note that this is a dummy target
clean:
	@rm $(SOURCEDIR)/modules/*.rst
	@rm -vf *~

# make html documentation
html:
	@$(SPHINXBUILD) -M html $(SOURCEDIR) $(BUILDDIR) $(SPHINXOPTS)

# for simple touketsu package setup/install.
#
# Changelog:
#
# 06-30-2020
#
# apparently i had an uncommited change, so i'm just making a note here.
#
# 06-23-2020
#
# initial creation. essentially copied from the shizuka project with extra dist
# target and more dummy targets to force target runs.

CC          = gcc
CFLAGS      =
PYTHON      = python
SETUP_FLAGS = 

.PHONY: dummy clean build dist install

dummy:
	@echo "Please specify a target to build."

# removes emacs autosave files and local build + dist directories
clean:
	@rm -vf *~
	@rm -vrf ./build
	@rm -vrf ./dist

# build touketsu package
build:
	@$(PYTHON) setup.py build $(SETUP_FLAGS)

# make source and wheel distribution for touketsu
dist:
	@$(PYTHON) setup.py sdist bdist_wheel

# install in site-packages directory for importing. builds if necessary.
install: build
	@$(PYTHON) setup.py install

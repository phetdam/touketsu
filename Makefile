# Makefile for simple touketsu package setup/install.

CC          = gcc
CFLAGS      =
PYTHON      = python3
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

# user install in site-packages directory for importing. builds if necessary.
# under ubuntu, you will need to manually remove zipped egg to uninstall.
install: build
	@$(PYTHON) setup.py install --user

# install to root; don't use unless absolutely necessary!
root_install: build
	@$(PYTHON) setup.py install
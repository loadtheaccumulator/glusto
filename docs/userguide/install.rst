Installing Glusto
-----------------

There is more than one way to install Glusto.

* Cloning from github and installing via setuptools.
* Installing the package directly from the github repo.
* Installing via rpm.

Cloning the Glusto Github Repo
==============================

On the system where Glusto is to be installed, change directory and clone the repo...
	::

		# cd workspace
		# git clone https://github.com/loadtheaccumulator/glusto.git

Installing Glusto from a Git Clone
==================================

To install the Glusto package via setuptools.

#. Change directory into the glusto directory.

	::

		# cd glusto

#. Run the setuptools script.

	::

		# python setup.py

Installing Glusto Directly from Git via Pip
===========================================

The ``pip`` command can install directly from the Glusto project repo on github.com.

	::

		# pip install --upgrade git+git://github.com/loadtheaccumulator/glusto.git

Uninstalling
============

What?! But, why?!

To uninstall glusto, use the ``pip`` command.

	::

		# pip uninstall glusto


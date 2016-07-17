Installing Glusto
-----------------

There is more than one way to install Glusto.

* Installing the package directly from the github repo via the ``pip`` command.
* Installing a docker image from Docker Hub.
* Cloning from github and installing via setuptools.


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


Using Glusto via Docker
=======================

A minimal Docker image is available to download and experiment with Glusto.

.. Note::

	The image has currently been tested on Fedora 23 and Mac OS X (El Capitan)
	running *Docker for Mac* without issues.

To use the Glusto Docker image, pull the image from Docker Hub and go.

	::

		docker pull loadtheaccumulator/glusto
		docker run -it --rm loadtheaccumulator/glusto /bin/bash

This takes you into the running container as root. Please reference the documentation
on docker.com (or available all over the web now) for more information on using Docker.

.. Note::

	You will need to pay particular attention to keys and configs when using
	the docker image. It might be useful to create a Dockerfile to build a new
	image, based on the Glusto image, that makes your own custom config, keys,
	and tests available. The Dockerfile used to create the Glusto image is available
	in the GitHub repo, so you can also just roll your own on the distro image of your choice.
	More on Docker later, but for now... experiment.


Cloning the Glusto Github Repo
==============================

On the system where Glusto is to be installed, clone the repo...

	::

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



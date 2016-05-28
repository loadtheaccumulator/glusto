.. _connectible:

Working With Remote Systems
---------------------------

Glusto provides functions for running commands on remote systems,
as well as sending and retrieving files.

Passwordless SSH with Keys
==========================

Glusto relies on existing SSH keys. Please consult the docs for your specific
platform for more information on how to setup passwordless ssh.

Configuring Glusto to Use Specific Keys
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add a specific SSH key to the /etc/glusto defaults configs...

Example::

	keyfile: "~/ssh/id_rsa"


Run a Single Command via SSH
============================

To run a command on a remote system via SSH, use the "run" command.

Example:
	>>> retcode, stdout, stderr = g.run('server01.example.com', 'uname -a')



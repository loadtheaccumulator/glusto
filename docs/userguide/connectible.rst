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

For example, add the following line to ``/etc/glusto/defaults.yml``::

	keyfile: "~/ssh/id_rsa"


Run a Single Command via SSH
============================

To run a command on a remote system via SSH, use the "run" command::

	>>> g.run('server01.example.com', 'uname -a')
	(0, 'Linux server01 2.6.32-431.29.2.el6.x86_64 #1 SMP Sun Jul 27 15:55:46 EDT 2014 x86_64 x86_64 x86_64 GNU/Linux\n', '')


It is also easy enough to assign the return code, stdout, and stderr to variables::

	>>> retcode, stdout, stderr = g.run('server01.example.com', 'uname -a')
	>>> retcode
	0
	>>> stdout
	'Linux server01 2.6.32-431.29.2.el6.x86_64 #1 SMP Sun Jul 27 15:55:46 EDT 2014 x86_64 x86_64 x86_64 GNU/Linux\n'
	>>> stderr
	''

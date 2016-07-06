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

Run a Single Command on the Localhost
=====================================

A command can be run on the localhost via SSH by simply passing 'localhost'
as the hostname. As a convenience, and to save some overhead, Glusto provides
a method to run a command locally and get the return code, stdout, and
stderr like the remote run command.

To run a command on the local system::

	>>> g.run_local('uname -a')
	(0, 'Linux localhost 4.4.9-300.fc23.x86_64 #1 SMP Wed May 4 23:56:27 UTC 2016 x86_64 x86_64 x86_64 GNU/Linux\n', '')


Transferring Files To and From Remote Systems
=============================================

Glusto provides methods to call SShMachine's upload and download commands,
as well as a method to transfer a file directly between remote systems.

Uploading a File
~~~~~~~~~~~~~~~~

To upload a file to a remote system, use the ``upload`` method.

	::

		>>> g.upload('server01.example.com', '/etc/localfile.txt', '/tmp/localfile_remotecopy.txt')

Downloading a File
~~~~~~~~~~~~~~~~~~

To download a file from a remote system, use the ``download`` method.

	::

		>>> g.download('server01.examples.com', '/etc/remotefile.txt', '/tmp/remotefile_localcopy.txt')


Transferring a File from Remote to Remote
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To transfer a file directly from a remote system to another remote system,
without having to first download to the local system and then upload to the remote,
use the ``transfer`` method.

	::

		>>> g.transfer('server01.example.com', '/etc/remote1file.txt', 'server02.example.com', '/tmp/remote1file_remote2copy.txt')



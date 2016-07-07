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


Run a Command on More than One Host
===================================

Glusto provides convenience methods to run commands against multiple hosts.

Run a Command Serially on Multiple Servers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To run a command against a list of hosts, use the ``run_serial()`` method.
The command will be run against the hosts one after another.

	::

	>>> hosts = ["breedshill.example.com", "bunkerhill.example.com"]
	>>> results = g.run_serial(hosts, 'uname -a')


Run a Command in Parallel
~~~~~~~~~~~~~~~~~~~~~~~~~

To run a command against a list of hosts in parallel, use the ``run_parallel()`` method.
The command will be run against the hosts at the same time.

	::

	    >>> command = "uname -a"
	    >>> results = g.run_parallel(hosts, 'uname -a')
		{'192.168.1.221':
			(0, 'Linux rhserver1 2.6.32-431.29.2.el6.x86_64 #1 SMP Sun Jul 27 15:55:46 EDT 2014 x86_64 x86_64 x86_64 GNU/Linux\n', ''),
		'192.168.1.222':
			(0, 'Linux rhserver2 2.6.32-431.29.2.el6.x86_64 #1 SMP Sun Jul 27 15:55:46 EDT 2014 x86_64 x86_64 x86_64 GNU/Linux\n', '')}


Run a Command Asynchronously
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``run_parallel`` method is a convenience method and runs the same command against
a list of systems using the same user. It is possible to use the underlying
``run_async`` command directly to run a variety of combinations asynchronously.

An example of how ``run_parallel`` uses ``run_async``::

    >>> command = "uname -a"
    >>> proc1 = g.run_async("bunkerhill", command)
    >>> proc2 = g.run_async("breedshill", command)

    >>> results1 = proc1.async_communicate()
    >>> results2 = proc2.async_communicate()

To asynchronously run the same command against the same server as a different user::

    >>> command = "uname -a; echo $USER"
    >>> proc1 = g.run_async("breedshill", command, user="howe")
    >>> proc2 = g.run_async("breedshill", command, user="pigot")

    >>> results1 = proc1.async_communicate()
    >>> results2 = proc2.async_communicate()

.. Note::

    run_async() runs commands asynchronously, but blocks on
    async_communicate() and reads output sequentially.
    This might not be a good fit for run-and-forget commands.


Transferring Files To and From Remote Systems
=============================================

Glusto provides methods to call SShMachine's upload and download commands,
as well as a method to transfer a file directly between remote systems.

Uploading a File
~~~~~~~~~~~~~~~~

To upload a file to a remote system, use the ``upload()`` method.

	::

	>>> g.upload('server01.example.com', '/etc/localfile.txt', '/tmp/localfile_remotecopy.txt')

Downloading a File
~~~~~~~~~~~~~~~~~~

To download a file from a remote system, use the ``download()`` method.

	::

	>>> g.download('server01.examples.com', '/etc/remotefile.txt', '/tmp/remotefile_localcopy.txt')


Transferring a File from Remote to Remote
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To transfer a file directly from a remote system to another remote system,
without having to first download to the local system and then upload to the remote,
use the ``transfer`` method.

	::

	>>> g.transfer('server01.example.com', '/etc/remote1file.txt', 'server02.example.com', '/tmp/remote1file_remote2copy.txt')


Listing SSH Connections
=======================

To see a list of the current SSH connections, use the ``ssh_list_connections()`` method.

	::

		>>> g.ssh_list_connections()
		root@192.168.1.222
		root@192.168.1.223
		root@192.168.1.221
		root@192.168.1.224

Closing Connections
===================

It is typically not necessary to close a connection. Connections are cached for
quick re-use and SSH connections should close at program exit. Should the need arise...

Closing a Connection
~~~~~~~~~~~~~~~~~~~~

To close a connection use the ``ssh_close_connection()`` method.

	::

	>>> g.ssh_close_connection('192.168.1.221')
	>>> g.ssh_close_connection('192.168.1.221', user='george')


Close All Connections
~~~~~~~~~~~~~~~~~~~~~

To close all connections use the ``ssh_close_connections()`` method.

	::

	>>> g.ssh_close_connections()




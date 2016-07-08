.. _rpycable:

Using RPyC
----------

Let's start with this...

.. Warning::

	Per the install documentation for RPyC, it is not possible to connect to
	a Python 3.x remote from a Python 2.x system and vice-versa.

	See the RPyC Install documentation [#]_ for more information. That's not
	necessarily a show-stopper for everyone, but certainly worth consideration
	depending on your environment.


Passwordless Connections
========================

Glusto's implementation of RPyC leverages the same SSH connections described in
the previous section. See `Passwordless SSH with Keys <connectible.html#passwordless-ssh-with-keys>`__
for more information on configuring Glusto for specific SSH keys.


Setting up Connections
======================

Unlike the SSH connections that are created automatically when you use ``run()``
or the other SSH methods, the RPyC connection needs to be created before it can
be used. After the connection is made, it is cached for use by subsequent RPyC calls.

Setting up a Single Connection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To setup an RPyC connection to a remote server, use the ``rpyc_get_connection()``
method.

	::

		>>> g.rpyc_get_connection('192.168.1.221')

Listing Connections
~~~~~~~~~~~~~~~~~~~

To see the list of connections, use the ``rpyc_list_connections()`` method.

	::

		>>> g.rpyc_list_connections()
		root@192.168.1.221:1

Setting up a Connection with a Specific User
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The default user is root. To setup a connection with a user other than the default,
add the ``user`` parameter.

	::

		>>> g.rpyc_get_connection('192.168.1.221', user='george')
		>>> g.rpyc_list_connections()
		george@192.168.1.221:1

Setting up Multiple Connections with Different Users
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes it is necessary to run commands as different users at the same time.
With RPyC, it is possible to setup multiple connections to the same server with
different users.

	::

		>>> g.rpyc_get_connection('192.168.1.221', user='george')
		>>> g.rpyc_get_connection('192.168.1.221', user='alexander')

		>>> g.rpyc_list_connections()
		alexander@192.168.1.221:1
		george@192.168.1.221:1

	On the remote server, multiple instances of the rpyc server are run::

		$ ps -ef | grep deployed
		george    7504  5456  0 18:13 ?        00:00:00 bash -c cd /home/george && /usr/bin/python2 /tmp/tmp.XuDwqQkXVq/deployed-rpyc.py
		george    7511  7504  1 18:13 ?        00:00:00 /usr/bin/python2 /tmp/tmp.XuDwqQkXVq/deployed-rpyc.py
		root      7579  3041  0 18:13 ?        00:00:00 bash -c cd /root && /usr/bin/python2 /tmp/tmp.xAfvVdtmjg/deployed-rpyc.py
		root      7582  7579  4 18:13 ?        00:00:00 /usr/bin/python2 /tmp/tmp.xAfvVdtmjg/deployed-rpyc.py


Setting up Multiple Connections with the Same User
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are also times when it is helpful to be able to run commands at the same 
time, but as the same user. For example, to run a long running command while
checking another command running at the same time. With RPyC, it is 
possible to setup multiple connections to the same server with the the same user.

To setup a connection to the same server as the same user, use the ``instance``
parameter to specificy an instance number.

	::

		>>> g.rpyc_get_connection('192.168.1.221')
		>>> g.rpyc_get_connection('192.168.1.221', instance=2)
		>>> g.rpyc_get_connection('192.168.1.221', user='george')
		>>> g.rpyc_get_connection('192.168.1.221', user='george', instance=2)

		>>> g.rpyc_list_connections()
		george@192.168.1.221:2
		root@192.168.1.221:2
		root@192.168.1.221:1
		george@192.168.1.221:1

.. Note::

	Glusto doesn't automatically increment the instance number. Specifying the
	same instance number will return the cached connection and not a new instance.


Making RPyC Calls
=================

.. Note::

	Rather than cover RPyC in-depth here, below are some examples of using RPyC with Glusto.
	Please refer to the RPyC documentation [#]_ for more information.

Using the Connection
~~~~~~~~~~~~~~~~~~~~

Once an RPyC connection is made, it can be referenced to make RPyC calls against the remote system.

	::

		conn1 = g.rpyc_get_connection('192.168.1.221')
		>>> conn1.modules.sys.platform
		'linux2'

Asynchronous RPyC Calls
~~~~~~~~~~~~~~~~~~~~~~~

RPyC provides an asynchronous mechanism to allow for running remote calls in the background.

Backgrounding an RPyC Call
..........................

Sometimes you just want to kick off a process and let it run without needing
to wait for it to finish or caring about the result.

To run a command in the background without waiting for a result.

	::

		>>> import rpyc
		>>> conn1 = g.rpyc_get_connection('192.168.1.221')
		>>> async_sleep1 = rpyc.async(conn1.modules.time.sleep)
		>>> async_sleep1(10)
		<AsyncResult object (pending) at 0x7f3382bc6f50>

Waiting for a Backgrounded Call
..................................

Other times you want to wait for the processes to finish before continuing.

To wait for a backgrounded process, use the rpyc ``wait()`` method.

	::

		>>> import rpyc
		>>> conn1 = g.rpyc_get_connection('192.168.1.221')
		>>> async_sleep1 = rpyc.async(conn1.modules.time.sleep)
		>>> res1 = async_sleep1(10)
		<AsyncResult object (pending) at 0x7f3382bc6530>
		>>> res1.wait()


Running a Second Call Against the Same System
.................................................

When it is necessary to run a background command against a system and run another
command against the same system, you can use ``wait()`` to wait for a return for
each call made.

		>>> res1 = async_sleep(60)
		>>> res2 = async_sleep(10)
		>>> res2.wait()
		>>> res1.wait()

.. Note::

	Because the backgrounded calls are made against the same connection, the
	first call blocks the connection until complete. In the above example, the
	``res2.wait()`` will block for 70 seconds. The ``res1.wait()`` returns instantly.

To run multiple background calls against the same system, you can create a
second connection and run the second background call against it.

	::

		>>> import rpyc

		>>> conn1 = g.rpyc_get_connection('192.168.1.221')
		>>> async_sleep1 = rpyc.async(conn1.modules.time.sleep)
		
		>>> conn2 = g.rpyc_get_connection('192.168.1.221', instance=2)
		>>> async_sleep2 = rpyc.async(conn2.modules.time.sleep)

		>>> res1 = async_sleep(60)
		>>> res = async_sleep(10)
		>>> res.wait()
		>>> res1 = async_sleep(60)
		>>> res2 = async_sleep2(10)
		>>> res2.wait()
		>>> res1.wait()

The first call will block on the first connection, while the second call runs
in parallel on the other connection.


Running Local Code on the Remote System
=======================================

Normally, a module already needs to reside on the remote system or be
transferred at runtime to be called. Glusto leverages a feature of RPyC to
define a local module on the remote system without the extra step of transferring
a file into the remote PYTHONPATH.

This feature makes it simple to create module files of commonly used function,
class, and method snippets for use on remote servers without the need to package,
distribute, and install on each remote server ahead of time.

To define a local module on the remote system, use the ``rpyc_define_module()`` method.

	Local module script named ``mymodule`` with a function called ``get_uname``::

		>>> import mymodule
		>>> connection = g.rpyc_get_connection('192.168.1.221')
		>>> r = g.rpyc_define_module(connection)
		>>> r.get_uname()
		('Linux', 'rhserver1', '2.6.32-431.29.2.el6.x86_64', '#1 SMP Sun Jul 27 15:55:46 EDT 2014', 'x86_64')


Going Ape with Monkey-Patching
==============================

Monkey-patching with RPyC can be a useful feature.

Monkey-patching Standard Out
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

While using the Python interpreter, it is sometimes helpful to be able to see
the output of a call that is normally directed to stdout on the remote.

To wire the remote stdout to the local stdout...

	::

		>>> import sys
		>>> conn = g.rpyc_get_connection('192.168.1.221')
		>>> conn.modules.sys.stdout = sys.stdout
		>>> conn.execute("print 'Hello, World!'")
		Hello, World!

Re-wiring Local and Remote
~~~~~~~~~~~~~~~~~~~~~~~~~~

Monkey-patching can be used to make lengthy or often-used remote calls appear local.

	An oversimplified example::

		# Monkey-patching the remote to a local object
		>>> conn = g.rpyc_get_connection('192.168.1.221')
		>>> r_uname = conn.modules.os.uname
		>>> r_uname()
		('Linux', 'rhserver1', '2.6.32-431.29.2.el6.x86_64', '#1 SMP Sun Jul 27 15:55:46 EDT 2014', 'x86_64')

		# Calling the local uname method
		>>> import os
		>>> os.uname()
		('Linux', 'mylaptop', '4.4.9-300.fc23.x86_64', '#1 SMP Wed May 4 23:56:27 UTC 2016', 'x86_64')

	A slightly better example::

		>>> # create a function unaware of remote vs local
		>>> def collect_os_data(os_object):
		...     print os_object.uname()
		...     print os_object.getlogin()
		...

		>>> # pass it the local object
		>>> collect_os_data(os)
		('Linux', 'mylaptop', '4.4.9-300.fc23.x86_64', '#1 SMP Wed May 4 23:56:27 UTC 2016', 'x86_64')
		loadtheaccumulator

		>>> # pass it the remote object
		>>> collect_os_data(ros)
		('Linux', 'rhserver1', '2.6.32-431.29.2.el6.x86_64', '#1 SMP Sun Jul 27 15:55:46 EDT 2014', 'x86_64')
		root


Checking Connections
====================

To check a connection is still available, use the ``rpyc_ping_connection()`` method.

	::

		>>> g.rpyc_ping_connection()
		connection is alive

.. Note::

	Pinging a connection gets the connection from cache, but if the connection
	was not established before the ping it will be opened--followed by the ping.


Closing Connections
===================

On occasion, it might be necessary to remove a connection from the cache (e.g.,
when a cached connection is no longer needed or when looping through
connections to execute the same command against all connections and an unwanted
connection is in the list).

.. Warning::

	Closing a connection directly without using the methods discussed in this
	section will leave a connection definition in the connection dictionary.
	You will want to close rpyc connections via these methods to avoid
	unnecessary cleanup. It will also guarantee any future features are handled
	correctly upon close.

Closing a Single Connection
~~~~~~~~~~~~~~~~~~~~~~~~~~~

To remove a cached connection, close it with the ``rpyc_close_connection()`` method.

	::

		>>> g.rpyc_close_connection('192.168.1.221')

		>>> g.rpyc_list_connections()
		george@192.168.1.221:2
		root@192.168.1.221:2
		george@192.168.1.221:1

		>>> g.rpyc_close_connection('192.168.1.221', user='george')

		>>> g.rpyc_list_connections()
		george@192.168.1.221:2
		root@192.168.1.221:2

		>>> g.rpyc_close_connection('192.168.1.221', user='george', instance=2)
		
		>>> g.rpyc_list_connections()
		root@192.168.1.221:2

Closing All Connections
~~~~~~~~~~~~~~~~~~~~~~~

To remove all cached connections, use the ``rpyc_close_connections()`` method.

	::

		>>> g.rpyc_close_connections()


Undeploying the RPyC Server
===========================

With the RPyC Zero-Deploy automated setup, the RPyC server process running on the
remote system does not stop when a connection is closed. To stop that process,
it is necessary to close the deployed server connection setup by Zero-Deploy.

To list the deployed servers, use the ``rpyc_list_deployed_servers()`` method.

	::

		>>> g.rpyc_list_deployed_servers()
		george@192.168.1.221
		root@192.168.1.221
		alexander@192.168.1.221

.. Note::

	When multiple connection instances to the same server with the same user
	exist, they share the same deployed server, so only one deployed server will
	appear in the list.

To close a deployed server connection, use the ``rpyc_close_deployed_server()`` method.

	::

		>>> g.rpyc_list_deployed_servers()
		george@192.168.1.221
		root@192.168.1.221

		>>> g.rpyc_close_deployed_server('192.168.1.221', user='george')

		>>> g.rpyc_list_deployed_servers()
		root@192.168.1.221

.. Note::

	Glusto will automatically close all of the connection instances related to
	the deployed server being closed. However, it does not dispose of the cached
	SSH connection.

To close all deployed servers, use the ``rpyc_close_deployed_servers()`` method.

	::

		>>> g.rpyc_close_deployed_servers()

.. Note::

	Glusto leverages the RPyC Zero-Deploy methodology which copies the RPyC
	server files to the remote and sets up the SSH tunnel automatically.
	This can add overhead when the first ``g.rpyc_get_connection()`` call to a
	remote server is made. The time lag is negligible on the LAN or short
	distances across the WAN, but when dealing with a large number of systems
	across the globe, especially on a slow link (DSL, etc), there may be lengthy
	"go get something to drink" periods of time. Try it out and adjust according to your taste.


.. rubric:: Footnotes

.. [#] https://rpyc.readthedocs.io/en/latest/install.html#cross-interpreter-compatibility
.. [#] http://rpyc.readthedocs.io/en/latest/index.html

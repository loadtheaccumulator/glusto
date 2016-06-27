Using Glusto
------------

Using Glusto in a Module
========================

To use Glusto in a module, import the Glusto class at the top of each module leveraging the glusto tools.

Example:
    To use Glusto in a module::

        from glusto.core import Glusto as g

This provides access to all of the functionality of Glusto via the ``g`` object
created by the import statement.


Using Glusto via the Python Interactive Interpreter
===================================================

One of the primary objectives of Glusto is to maintain feature support from the
Python Interactive Interpreter. Most, if not all, features should be easily
referenced via the interpreter to ease use and reduce time during development.

To use Glusto via the Python Interactive Interpreter, enter the interpreter via
the ``python`` command.

	::

		$ python
		>>> from glusto.core import Glusto as g

This provides access to all of the functionality of Glusto via the ``g.`` object
created by the import statement--in the same way as imported in a script.

	For example::

		$ python
		>>> from glusto.core import Glusto as g

		>>> g.run_local('uname -a')
		(0, 'Linux mylaptop 4.4.9-300.fc23.x86_64 #1 SMP Wed May 4 23:56:27 UTC 2016 x86_64 x86_64 x86_64 GNU/Linux\n', '')

		>>> config = g.load_config('examples/systems.yml')
		>>> config
		{'nodes': ['192.168.1.221', '192.168.1.222', '192.168.1.223', '192.168.1.224'], 'clients': ['192.168.1.225'], 'masternode': '192.168.1.221'}

		>>> g.run(config['nodes'][0], 'uname -a')
		(0, 'Linux rhserver1 2.6.32-431.29.2.el6.x86_64 #1 SMP Sun Jul 27 15:55:46 EDT 2014 x86_64 x86_64 x86_64 GNU/Linux\n', '')
		>>> g.list_ssh_connections()
		root@192.168.1.221

		>>> g.run_serial(config['nodes'], 'hostname')
		{'192.168.1.224': (0, 'rhserver4\n', ''), \
		'192.168.1.221': (0, 'rhserver1\n', ''), \
		'192.168.1.223': (0, 'rhserver3\n', ''), \
		'192.168.1.222': (0, 'rhserver2\n', '')}
		>>> g.list_ssh_connections()
		root@192.168.1.222
		root@192.168.1.223
		root@192.168.1.221
		root@192.168.1.224

Typing ``from glusto.core import Glusto as g`` each time you start the
interpreter can become tedious. To automatically run commands, the PYTHONSTARTUP
environment variable can be pointed to a python script containing common setup commands.

	::

		$ cat examples/pythonstartup_script.py
		from glusto.core import Glusto as g
		
		print "Python startup starting"
		config = g.load_config('examples/systems.yml')
		rcode, rout, rerr = g.run(config['nodes'][0], 'uname -a')
		print ('The uname info is: %s' % rout)
		print "Python startup complete"

	::

		$ export PYTHONSTARTUP=examples/pythonstartup_script.py

		$ python
		Python 2.7.11 (default, Mar 31 2016, 20:46:51) 
		[GCC 5.3.1 20151207 (Red Hat 5.3.1-2)] on linux2
		Type "help", "copyright", "credits" or "license" for more information.
		Python startup starting
		Python startup complete
		>>> g
		<class 'glusto.core.Glusto'>
		>>> config
		{'nodes': ['192.168.1.221', '192.168.1.222', '192.168.1.223', '192.168.1.224'], 'clients': ['192.168.1.225'], 'masternode': '192.168.1.221'}
		>>> uname_info
		'Linux rhserver1 2.6.32-431.29.2.el6.x86_64 #1 SMP Sun Jul 27 15:55:46 EDT 2014 x86_64 x86_64 x86_64 GNU/Linux\n'


Using the Glusto CLI Utility
============================

Glusto provides a wrapper utility for features like unittest support, etc.
Currently, the Glusto CLI allows leveraging the unittest module
features in an easily configurable and callable wrapper.

To see the options available, use the ``--help`` option.

	::

		$ /usr/bin/glusto --help
		Starting glusto via main()
		usage: glusto [-h] [-c CONFIG_LIST] [-u] [-d DISCOVER_DIR]
		
		Glusto CLI wrapper
		
		optional arguments:
		  -h, --help            show this help message and exit
		  -c CONFIG_LIST, --config CONFIG_LIST
		                        Config file(s) to read.
		  -u, --unittest        Run unittests per provided config file.
		  -d DISCOVER_DIR, --discover DISCOVER_DIR
		                        Discover unittests from directory
          -t RUN_PYTEST, --pytest RUN_PYTEST
                                Run tests using the pytest framework

By default, the ``glusto`` command will read the default config files in the ``/etc/glusto/`` directory

	For example, this run of the command reads the ``defaults.yml`` and ``defaults.ini`` files in ``/etc/glusto/``::

		$ glusto
		Starting glusto via main()
		defaults: {that: yada2, the_other: yada1 and yada2, this: yada1}
		globals: {some_default: yada yada}
		keyfile: ~/ssh/id_rsa
		log_color: true
		that: yada2
		the_other: yada1 and yada2
		this: yada1
		use_controlpersist: true
		use_ssh: true
		Ending glusto via main()


Options for Running Unit Tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To run unit tests via the Glusto CLI Utility, see the examples and link to
additional documentation below.

Running PyUnit Tests
++++++++++++++++++++

Example::

	# glusto -c 'examples/systems.yml' -u -d 'tests'
	# glusto -c 'examples/unittests/unittest.yml examples/unittests/unittest_list.yml examples/systems.yml' -u

For more information on working with unit tests, see `Unittests and Glusto <unittest.html#unittests_and_glusto>`__

Running PyTest Tests
++++++++++++++++++++

Example::

    # glusto -c 'examples/systems.yml' --pytest='-v -x tests -m response'


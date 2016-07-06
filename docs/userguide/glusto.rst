Using Glusto
------------

Using Glusto in a Module
========================

To use Glusto in a module, import the Glusto class at the top of each module leveraging the glusto tools.

	::

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

Glusto provides a wrapper utility for features like unit test support, etc.
Currently, the Glusto CLI allows leveraging the PyUnit, PyTest, and Nose module
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
		  -n RUN_NOSETESTS, --nosetests RUN_NOSETESTS
		                        Run tests using the nose framework

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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To run unit tests via the Glusto CLI Utility, see the examples and links to
additional documentation below.

Running PyUnit Tests
++++++++++++++++++++

	Example::

		$ glusto -c 'examples/systems.yml' -u -d 'tests'
		$ glusto -c 'examples/unittests/unittest.yml examples/unittests/unittest_list.yml examples/systems.yml' -u

For more information on working with unit tests, see `Unittests and Glusto <unittest.html>`__

Running PyTest Tests
++++++++++++++++++++

	Example::

	    $ glusto -c 'examples/systems.yml' --pytest='-v -x tests -m response'

For more information on working with unit tests, see `PyTest and Glusto <pytest.html>`__

Running Nose Tests
++++++++++++++++++

	Example::

		$ glusto -c 'examples/systems.yml' --nosetests='-v -w tests'

For more information on working with unit tests, see `Nose and Glusto <nosetests.rst>`__

Running Different Frameworks in a Single Run
++++++++++++++++++++++++++++++++++++++++++++

Not that the need would arise, but the capability to run all three in a single command is there.

	Example running tests with ``--pytest=`` and ``nosetests=`` options::

		$ glusto -c 'examples/systems.yml examples/unittests/unittest.yml' -u --nosetests='-w tests' --pytest='-x tests -m response'
		Starting glusto via main()
		clients: [192.168.1.225]
		masternode: 192.168.1.221
		nodes: [192.168.1.221, 192.168.1.222, 192.168.1.223, 192.168.1.224]
		unittest:
		  load_tests_from_module: {module_name: tests.test_glusto, use_load_tests: true}
		  output_junit: false

		clients: [192.168.1.225]
		masternode: 192.168.1.221
		nodes: [192.168.1.221, 192.168.1.222, 192.168.1.223, 192.168.1.224]
		unittest:
		  load_tests_from_module: {module_name: tests.test_glusto, use_load_tests: true}
		  output_junit: false

		PREFIX: tests.test_glusto.TestGlustoBasics
		Setting Up Class: TestGlustoBasics
		test_return_code (tests.test_glusto.TestGlustoBasics)
		Testing the return code ... Setting Up: tests.test_glusto.TestGlustoBasics.test_return_code
		Running: tests.test_glusto.TestGlustoBasics.test_return_code - Testing the return code
		Tearing Down: tests.test_glusto.TestGlustoBasics.test_return_code
		ok
		test_stdout (tests.test_glusto.TestGlustoBasics)
		Testing output to stdout ... Setting Up: tests.test_glusto.TestGlustoBasics.test_stdout
		Running: tests.test_glusto.TestGlustoBasics.test_stdout - Testing output to stdout
		Tearing Down: tests.test_glusto.TestGlustoBasics.test_stdout
		Cleaning up after setup on fail or after teardown
		ok
		test_stderr (tests.test_glusto.TestGlustoBasics)
		Testing output to stderr ... Setting Up: tests.test_glusto.TestGlustoBasics.test_stderr
		Running: tests.test_glusto.TestGlustoBasics.test_stderr - Testing output to stderr
		Tearing Down: tests.test_glusto.TestGlustoBasics.test_stderr
		ok
		test_expected_fail (tests.test_glusto.TestGlustoBasics)
		Testing an expected failure. This test should fail ... Setting Up: tests.test_glusto.TestGlustoBasics.test_expected_fail
		Running: tests.test_glusto.TestGlustoBasics.test_expected_fail - Testing an expected failure. This test should fail
		expected failure
		Tearing Down: tests.test_glusto.TestGlustoBasics.test_expected_fail
		test_negative_test (tests.test_glusto.TestGlustoBasics)
		Testing an expected failure as negative test ... Setting Up: tests.test_glusto.TestGlustoBasics.test_negative_test
		Running: tests.test_glusto.TestGlustoBasics.test_negative_test - Testing an expected failure as negative test
		Tearing Down: tests.test_glusto.TestGlustoBasics.test_negative_test
		ok
		test_skip_me (tests.test_glusto.TestGlustoBasics)
		Testing the unittest skip feature ... skipped 'Example test skip'
		Tearing Down Class: TestGlustoBasics

		----------------------------------------------------------------------
		Ran 6 tests in 0.585s

		OK (skipped=1, expected failures=1)
		pytest: -x tests -m response
		==================================================================================== test session starts =====================================================================================
		platform linux2 -- Python 2.7.11, pytest-2.9.2, py-1.4.31, pluggy-0.3.1
		rootdir: glusto, inifile: 
		collected 21 items 

		tests/test_glusto_pytest.py ...

		=========================================================================== 18 tests deselected by "-m 'response'" ===========================================================================
		========================================================================== 3 passed, 18 deselected in 0.32 seconds ===========================================================================
		nosetests: -w tests
		/usr/lib64/python2.7/unittest/case.py:378: RuntimeWarning: TestResult has no addExpectedFailure method, reporting as passes
		  RuntimeWarning)
		...S..E...F.....E......
		======================================================================
		ERROR: Load tests in a specific order.
		----------------------------------------------------------------------
		Traceback (most recent call last):
		  File "/usr/lib/python2.7/site-packages/nose/case.py", line 197, in runTest
		    self.test(*self.arg)
		TypeError: load_tests() takes exactly 3 arguments (0 given)

		======================================================================
		ERROR: Load tests in a specific order.
		----------------------------------------------------------------------
		Traceback (most recent call last):
		  File "/usr/lib/python2.7/site-packages/nose/case.py", line 197, in runTest
		    self.test(*self.arg)
		TypeError: load_tests() takes exactly 3 arguments (0 given)

		======================================================================
		FAIL: Testing an expected failure. This test should fail
		----------------------------------------------------------------------
		Traceback (most recent call last):
		  File "glusto/tests/test_glusto_pytest.py", line 98, in test_expected_fail
		    self.assertEqual(rcode, 0)
		AssertionError: 1 != 0
		-------------------- >> begin captured stdout << ---------------------
		Setting Up: tests.test_glusto_pytest.TestGlustoBasicsPyTest.test_expected_fail
		Running: tests.test_glusto_pytest.TestGlustoBasicsPyTest.test_expected_fail - Testing an expected failure. This test should fail

		--------------------- >> end captured stdout << ----------------------
		-------------------- >> begin captured logging << --------------------
		plumbum.local: DEBUG: Running ['/usr/bin/ssh', '-T', '-oPasswordAuthentication=no', '-oStrictHostKeyChecking=no', '-oPort=22', '-oConnectTimeout=10', '-oControlMaster=auto', '-oControlPersist=4h', '-oControlPath=~/.ssh/glusto-ssh-%r@%h:%p', 'root@192.168.1.221', 'cd', '/root', '&&', 'false']
		--------------------- >> end captured logging << ---------------------

		----------------------------------------------------------------------
		Ran 23 tests in 1.964s

		FAILED (SKIP=1, errors=2, failures=1)
		Ending glusto via main()

.. Note::

	I'll be able to demonstrate this better when I have PyTest example test scripts written.
	The above command runs the same PyUnit-based test scripts against the PyUnit, PyTest and Nose frameworks.

Nose and Glusto
---------------


Running Nosetests from the CLI
==============================

Use the ``-n=`` or ``--nostests=`` parameter followed by the options normally passed to ``nosetests``

	::

		$ glusto -c 'examples/systems.yml' --nosetests='-v -w tests'
		Starting glusto via main()
		...
		nosetests: -v -w tests
		Testing an expected failure. This test should fail ... /usr/lib64/python2.7/unittest/case.py:378: RuntimeWarning: TestResult has no addExpectedFailure method, reporting as passes
		  RuntimeWarning)
		ok
		Testing an expected failure as negative test ... ok
		Testing the return code ... ok
		Testing the unittest skip feature ... SKIP: Example test skip
		Testing output to stderr ... ok
		Testing output to stdout ... ok
		Load tests in a specific order. ... ERROR
		Testing ini config file(s) ... ok
		Testing ordered ini config file(s) ... ok
		Testing yaml config file ... ok
		Testing an expected failure. This test should fail ... FAIL
		Testing an expected failure as negative test ... ok
		Testing the return code ... ok
		Testing the unittest skip feature ... ok
		Testing output to stderr ... ok
		Testing output to stdout ... ok
		Load tests in a specific order. ... ERROR
		Testing rpyc connection ... ok
		Testing local module definition on remote system ... ok
		test_remote_call (tests.test_glusto_rpyc.TestGlustoRpyc) ... ok
		Testing template for loop ... ok
		Testing template include ... ok
		Testing template scalar ... ok

		...

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
		Ran 23 tests in 2.791s
		
		FAILED (SKIP=1, errors=2, failures=1)
		Ending glusto via main()

For a list of available options, pass ``--help`` to the ``pytest`` parameter or use the ``pytest`` command itself.

	::

		$ glusto --noseests='--help'
		$ nosetests --help


Running Nosetests from Python Interpreter
=========================================

	::

		>>> import nose
		>>> nose.run(argv=['-v', '-w', 'tests'])


To Do
=====

* Expand text and examples

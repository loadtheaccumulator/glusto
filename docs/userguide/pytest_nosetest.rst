Working with PyTest and Nose
----------------------------

It is easy to integrate Glusto capability into a PyTest or Nose formatted test script.
Simply add the import to the script and all of the Glusto methods are available.

	::

		import pytest
		from glusto.core import Glusto as g


The Glusto command-line utility currently wraps the PyUnit mechanism for discovering
and running tests. PyUnit tests using Glusto can also run under PyTest and, with
some exceptions, Nose.

.. Note::

	Except where noted, the examples provided here are currently only written
	with the Python ``unittest`` module in mind. This section discusses running
	those scripts under PyTest and Nose. At some point, I will write a set of
	specific examples for each. For now, this discussion is intended to demonstrate
	the flexibility Glusto as a library of utilities can provide across the
	three popular test frameworks. 

The following examples use the tests included in the ``tests`` directory.


PyTest
======

With the provided examples, PyTest runs the tests without issue and even
handles skipped tests and expected failures. There are some notable exceptions
they make (e.g., ignoring test order with load_tests).

	A simple py.test run::

		$ py.test
		==================== test session starts =============================
		platform linux2 -- Python 2.7.11, pytest-2.9.2, py-1.4.31, pluggy-0.3.1
		rootdir: /home/loadtheaccumulator/glusto, inifile: 
		collected 21 items 

		test_glusto.py x..s..
		test_glusto_configs.py ...
		test_glusto_pytest.py x..s..
		test_glusto_rpyc.py ...
		test_glusto_templates.py ...

		============= 17 passed, 2 skipped, 2 xfailed in 2.63 seconds ========


	The same run with verbose output::

		$ py.test -v
		================== test session starts ===============================
		platform linux2 -- Python 2.7.11, pytest-2.9.2, py-1.4.31, pluggy-0.3.1 -- /usr/bin/python
		cachedir: ../.cache
		rootdir: /home/loadtheaccumulator/Dropbox/glusto, inifile: 
		collected 21 items 

		test_glusto.py::TestGlustoBasics::test_expected_fail <- ../../../../usr/lib64/python2.7/unittest/case.py xfail
		test_glusto.py::TestGlustoBasics::test_negative_test PASSED
		test_glusto.py::TestGlustoBasics::test_return_code PASSED
		test_glusto.py::TestGlustoBasics::test_skip_me <- ../../../../usr/lib64/python2.7/unittest/case.py SKIPPED
		test_glusto.py::TestGlustoBasics::test_stderr PASSED
		test_glusto.py::TestGlustoBasics::test_stdout PASSED
		test_glusto_configs.py::TestGlustoConfigs::test_ini PASSED
		test_glusto_configs.py::TestGlustoConfigs::test_ini_ordered PASSED
		test_glusto_configs.py::TestGlustoConfigs::test_yaml PASSED
		test_glusto_pytest.py::TestGlustoBasicsPyTest::test_expected_fail <- ../../../../usr/lib64/python2.7/unittest/case.py xfail
		test_glusto_pytest.py::TestGlustoBasicsPyTest::test_negative_test PASSED
		test_glusto_pytest.py::TestGlustoBasicsPyTest::test_return_code PASSED
		test_glusto_pytest.py::TestGlustoBasicsPyTest::test_skip_me SKIPPED
		test_glusto_pytest.py::TestGlustoBasicsPyTest::test_stderr PASSED
		test_glusto_pytest.py::TestGlustoBasicsPyTest::test_stdout PASSED
		test_glusto_rpyc.py::TestGlustoRpyc::test_connection PASSED
		test_glusto_rpyc.py::TestGlustoRpyc::test_local_module_on_remote PASSED
		test_glusto_rpyc.py::TestGlustoRpyc::test_remote_call PASSED
		test_glusto_templates.py::TestGlustoTemplates::test_template_forloop PASSED
		test_glusto_templates.py::TestGlustoTemplates::test_template_include PASSED
		test_glusto_templates.py::TestGlustoTemplates::test_template_scalar PASSED

		============== 17 passed, 2 skipped, 2 xfailed in 2.85 seconds ========

PyTest supports running PyUnit and Nose tests, so it's simple to leverage PyTest
features, such as markers, in a PyUnit script. See the ``test_glusto_pytest.py``
script for an example of combining PyTest marker features in a unittest.

	A test run of only tests with a py.test formatted marker *response*::

		$ py.test -v -m "response"
		===================== test session starts ============================
		platform linux2 -- Python 2.7.11, pytest-2.9.2, py-1.4.31, pluggy-0.3.1 -- /usr/bin/python
		cachedir: ../.cache
		rootdir: /home/loadtheaccumulator/Dropbox/glusto, inifile: 
		collected 21 items 
		
		test_glusto_pytest.py::TestGlustoBasicsPyTest::test_return_code PASSED
		test_glusto_pytest.py::TestGlustoBasicsPyTest::test_stderr PASSED
		test_glusto_pytest.py::TestGlustoBasicsPyTest::test_stdout PASSED
		
		============== 18 tests deselected by "-m 'response'" =================
		============== 3 passed, 18 deselected in 0.69 seconds ================


Nose
====

Nose successfully runs the test methods, but does not handle the load_tests function
as easily as PyTest.

	::

		$ nosetests
		/usr/lib64/python2.7/unittest/case.py:378: RuntimeWarning: TestResult has no addExpectedFailure method, reporting as passes
		  RuntimeWarning)
		...S..E.........E......
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
		
		----------------------------------------------------------------------
		Ran 23 tests in 2.253s
		
		FAILED (SKIP=1, errors=2)

Twenty-three tests run successfully, two with errors (expected though), and 1 skipped.
Apparently Nose ignores the py.test markers and did not skip a test in the py.test example.


	A Nose test run with results written to an xunit xml file::

		$ nosetests --with-xunit --xunit-file=/tmp/nosetests.xml


Glusto for Good Measure
=======================

	::

		$ glusto -d 'tests'
		Starting glusto via main()

		...

		----------------------------------------------------------------------
		Ran 21 tests in 2.522s
		
		OK (skipped=1, expected failures=2)


Not surprisingly, the ``unittest`` module does not recognize the PyTest skip marker,
so it is currently necessary to run PyTest-savvy scripts with the ``py.test`` command.


To Do
=====

* split this out and merge into individual test framework pages

* Add examples of PyTest and Nose specific test scripts using Glusto calls.

*more on this subject later...*

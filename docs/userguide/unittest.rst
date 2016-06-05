Unittests and Glusto
--------------------

Glusto plugs into the Python unittest module methodology and can run
test modules with the Glusto features imported or existing scripts without
Glusto imported in the test module. This makes it possible to combine
tests that do not require any of the Glusto functionality with Glusto-savvy
test cases.

Glusto also supports running test cases in a number of ways.

* Using the Python interpreter interactive mode to execute commands manually.
* Running an individual script at the command-line via ``if __name__ == '__main__':`` logic.
* Running an individual script via an IDE (e.g., Eclipse PyDev plug-in [#]_ test runner).
* Running testcases directly at the command-line via the ``python -m unittest`` module.
* Using the glusto cli command with CLI options or config files.

Each of the above options is documented below.

.. Note::

	All of the examples are based on the samples provided in the ``examples`` directory installed with the glusto package.

Running Unittests via the Python Interpreter Interactive Mode
=============================================================

Running the tests via the Python interpreter can come in handy while developing
and debugging tests scripts.

To run tests via the Python interpreter...

#. Enter the Python Interpreter.

	::

		# python

#. Type commands...

	For example::

		>>> import unittest
		>>> loader = unittest.TestLoader()
		>>> suite = loader.loadTestsFromName('tests.test_glusto.TestGlustoBasics.test_stdout')
		>>> runner = unittest.TextTestRunner()
		>>> runner.run(suite)
		Setting Up Class: TestGlustoBasics
		Setting Up: tests.test_glusto.TestGlustoBasics.test_stdout
		Running: tests.test_glusto.TestGlustoBasics.test_stdout - Testing output to stdout
		Tearing Down: tests.test_glusto.TestGlustoBasics.test_stdout
		Cleaning up after setup on fail or after teardown
		.Tearing Down Class: TestGlustoBasics

		----------------------------------------------------------------------
		Ran 1 test in 0.242s

		OK
		<unittest.runner.TextTestResult run=1 errors=0 failures=0>


Running Unittests with the CLI Option
=====================================

The simplest and most direct way to run unittests with Glusto is via the
glusto cli discover option.

The discover (-d,--discover) option accepts a directory name and the unittest
module discover feature [#]_ searches the directory and subdirectories for modules
with a name matching ```test*.py```.

.. Note::

	It is possible to fine-tune the discover options with a specific pattern
	and top_level_directory via the configuration option described below.

Example::

	# glusto -d 'tests' -c 'examples/systems.yml'

Running Tests in a Specific Order
=================================

One of the most argued elements of unit testing is creating a relationship
between test cases by specifying an order where one has to be run before the
other to satisfy a dependency, etc. Some will say test cases should
never be related and always standalone. Some say there is a need in
integration testing where it makes sense to leverage one test case to setup
another without jumping through programmatic hoops to prevent a dependency.
Regardless of which camp you might side with, the Python unittest module can
be leveraged for a variety of use cases, so Glusto provides a convenient
interface to the capability added in Python 2.7.

Add the following example to the test module containing a standard
unittest.TestCase class.

.. code-block:: python
    :linenos:

    def load_tests(loader, standard_tests, pattern):
		'''Load tests in specified order'''
        testcases_ordered = ['test_return_code',
                             'test_stdout',
                             'test_stderr']

        suite = g.load_tests(TestGlustoBasics, loader, testcases_ordered)

        return suite

See ``tests/test_glusto.py`` for a full example of a unittest.TestCase using
Glusto and running tests in order.


Running Unittests with the Configuration Options
================================================

If more control over discovery options, or the ability to select tests at the
module or test case level is required, you can use config files to specify
those requirements.

To run tests with information from config files, use the -u option::

	# glusto -u -c 'examples/systems.yml examples/unittests/unittest.yml examples/unittests/unittest_list.yml'

Configuring Glusto for Unittests
================================


Base Unittest Options
~~~~~~~~~~~~~~~~~~~~~

Config::

	unittest:
	  output_junit: false

Discover Tests from a Directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Config::

	# DISCOVER TESTS FROM DIRECTORY
	  discover_tests:
	    start_dir: 'tests'
	    # optional
	    pattern: 'test*.py'
	    top_level_dir: 'tests'

Load Tests from a List
~~~~~~~~~~~~~~~~~~~~~~

Config (unittest.yml)::

	# LOAD TESTS FROM LIST (SEE unittest_list.yml)
	  load_tests_from_list: true


Config (unittest_list.yml)::

	unittest_list:
	  module_name: 'tests.test_glusto'
	  list: [
	    'TestGlustoBasics.test_stdout',
	    'TestGlustoBasics.test_return_code',
	    'TestGlustoBasics.test_stderr',
	    'TestGlustoBasics.test_expected_fail',
	    ]


Load Tests from a Module
~~~~~~~~~~~~~~~~~~~~~~~~

Config::

	# LOAD TESTS FROM MODULE w/ TEST_LOAD ORDERED TESTS
	  load_tests_from_module:
	    module_name: 'tests.test_glusto'
	    use_load_test: true

Load Tests from a Module with Ordered Test List
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Config::

	# LOAD TESTS FROM MODULE w/o TEST_LOAD ORDERED TESTS
	  load_tests_from_module:
	    module_name: 'tests.test_glusto'
	    use_load_test: false

Load Tests Using a Name
~~~~~~~~~~~~~~~~~~~~~~~

Config::

	# LOAD TESTS FROM NAME
	  load_tests_from_name: 'tests.test_glusto'
	  load_tests_from_name: 'tests.test_glusto.TestGlustoBasics'
	  load_tests_from_name: 'tests.test_glusto.TestGlustoBasics.test_stdout'

Load Tests from a List of Names
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Config::

	# LOAD TESTS FROM LIST OF NAMES
	  load_tests_from_names: ['tests.test_glusto',
	                          'tests.test_glusto_configs',
	                          'tests.test_glusto.TestGlustoBasics.test_stdout']

Writing Unittests
=================

Example Using setUp and tearDown
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``test_glusto_configs.py``

Eample Using setUpClass and tearDownClass
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``test_glusto_templates.py``

.. rubric:: Footnotes

.. [#] http://www.pydev.org/
.. [#] https://docs.python.org/2.7/library/unittest.html#unittest.TestLoader.discover

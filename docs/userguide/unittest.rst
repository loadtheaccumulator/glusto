PyUnit (unittest) and Glusto
----------------------------

Glusto plugs into the Python unittest module methodology and can run
test modules with the Glusto features imported or existing scripts without
Glusto imported in the test module. This makes it possible to combine
tests that do not require any of the Glusto functionality with Glusto-savvy
test cases.

Running Unittests with Glusto
=============================

Glusto supports running test cases in a number of ways.

* Using the Python interpreter interactive mode to execute commands manually.
* Running an individual script at the command-line via ``if __name__ == '__main__':`` logic.
* Running an individual script via an IDE (e.g., Eclipse PyDev plug-in [#]_ test runner).
* Running testcases directly at the command-line via the ``python -m unittest`` module.
* Using the glusto cli command with CLI options or config files.

Each of the above options is documented below.

.. Note::

	All of the examples are based on the samples provided in the ``examples`` directory installed with the glusto package.

Running Unittests via the Python Interpreter Interactive Mode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The simplest and most direct way to run unittests with Glusto is via the
glusto cli discover option.

The discover (*-d,--discover*) option accepts a directory name and the unittest
module discover feature [#]_ searches the directory and subdirectories for modules
with a name matching ```test*.py```.

.. Note::

	It is possible to fine-tune the discover options with a specific pattern
	and top_level_directory via the configuration option described below.

Example::

	# glusto -d 'tests' -c 'examples/systems.yml'


Running Tests in a Specific Order
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If more control over discovery options, or the ability to select tests at the
module or test case level is required, you can use config files to specify
those requirements.

To run tests with information from config files, use the -u option::

	# glusto -u -c 'examples/systems.yml examples/unittests/unittest.yml examples/unittests/unittest_list.yml'

Configuring Glusto for Unittests
================================

Along with the simple discovery method at the CLI, Glusto supports more granular
control over Unittests via configuration files.

Base Unittest Options
~~~~~~~~~~~~~~~~~~~~~

Configuration items that control options Glusto-wide can be configured.

	**output_junit**
	The ``output_junit`` option writes the test results in junit xml format.

		::

			unittest:
			    output_junit: false

	**test_method_prefix**
	The ``test_method_prefix`` option changes the name prefix used by unittest to discover tests.

		::

			unittest:
			    test_method_prefix: 'rhgs'



Discover Tests from a Directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Discovery via config is similar to the CLI, but offers additional options.

Config::

	# DISCOVER TESTS FROM DIRECTORY
	  discover_tests:
	    start_dir: 'tests'
	    # optional
	    pattern: 'test*.py'
	    top_level_dir: 'tests'

Load Tests from a List
~~~~~~~~~~~~~~~~~~~~~~

To run a specific set of tests, Glusto supports configuring a list.

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

To limit test list to only those in a specific module, use the ``load_tests_from_module`` option.
Tests are discovered automatically and run in alphabetical order.


Config::

	# LOAD TESTS FROM MODULE w/ TEST_LOAD ORDERED TESTS
	  load_tests_from_module:
	    module_name: 'tests.test_glusto'
	    use_load_tests: false

Load Tests from a Module with Ordered Test List
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To limit the test list to a specific module and specify an order, set the ``use_load_test`` option to ``true``.

Config::

	# LOAD TESTS FROM MODULE w/o TEST_LOAD ORDERED TESTS
	  load_tests_from_module:
	    module_name: 'tests.test_glusto'
	    use_load_tests: true

.. Note::

	When setting ``use_load_tests: true`` it is necessary to add a ``load_tests()`` method to your test script.
	For more information on the load_tests() method, please see the "*Running Tests in a Specific Order*" section earlier in this doc.

Load a Test Using a Name
~~~~~~~~~~~~~~~~~~~~~~~~

To limit the test to a specific test module, class, or method, use the ``load_tests_from_name`` option.

Config::

	# LOAD TESTS FROM NAME
	  load_tests_from_name: 'tests.test_glusto.TestGlustoBasics.test_stdout'

When providing a module, the list is created from all tests in the module.

	::

		load_tests_from_name: 'tests.test_glusto'

When providing a class, the list is created from all tests in the class.

	::

		load_tests_from_name: 'tests.test_glusto_configs'

When providing a method, only that method is run.

	::

		load_tests_from_name: 'tests.test_glusto.TestGlustoBasics.test_stdout'


Load Tests from a List of Names
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To limit the test to a list of names described above, use the ``load_tests_from_names`` option.

Config::

	# LOAD TESTS FROM LIST OF NAMES
	  load_tests_from_names: ['tests.test_glusto',
	                          'tests.test_glusto_configs',
	                          'tests.test_glusto.TestGlustoBasics.test_stdout']

The list will be composed of all tests combined.

Writing Unittests
=================

Glusto's unit test features are based on the Python unittest module.
The unittest module provides a simple class structure that makes testcase
development rather robust without modification.

To use the ``unittest`` module for creating a testcase, import the ``unittest`` module
and create a subclass of ``unittest.TestCase``.

.. code-block:: python
    :linenos:

	import unittest

	class MyTestClass(unittest.TestCase)

The base class for ``unittest`` is ``unittest.TestCase``. It consists of several
automatically called methods that are designed to be overridden to provide your own functionality.

.. Note::

	In the future, I will look at integrating some PyTest or other frameworks,
	but don't have an immediate need.


Example Using setUp and tearDown
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``test_glusto_configs.py``

Example Using setUpClass and tearDownClass
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``test_glusto_templates.py``

To Do
=====

* Expand the Writing Test Cases section with more examples.

.. rubric:: Footnotes

.. [#] http://www.pydev.org/
.. [#] https://docs.python.org/2.7/library/unittest.html#unittest.TestLoader.discover

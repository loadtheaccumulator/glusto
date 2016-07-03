Dynamic Cartesian Product Test Case Creation
--------------------------------------------

Glusto provides a decorator class that, given some variables by overriding the
__init__ method and passing data in a decorator, will create test cases on the
fly based on cartesian product combinations.

Currently, the only decorator available in Carteplex is the CarteTestClass.
It was written with ``unittest.TestCase`` in mind and includes some wiring
specific to unittest (leveraging load_tests, test class-based, etc.).
The Cartetestclass is available with the same Glusto import that provides the
other functionality.

.. Note::

	Carteplex is a new feature to meet a very specific use case. Currently,
	the unittest and PyTest loaders/runners work without issue. The Nose runner
	currently chokes on the load_test function. The goal, of course, is to keep
	it generic and make it work across the test frameworks. Working on it.


Using Carteplex
===============

To make the CarteTestClass decorator available to your test class, import Glusto.

	::

   from glusto.core import Glusto as g


An Example Config File
~~~~~~~~~~~~~~~~~~~~~~

Test case scripts accept dynamic configuration variables from config files.
In this case, a configuration state is added to a config file for the
base class to use when creating the test case classes on the fly.


.. code-block:: plain
   :linenos:
   :caption: gluster_config.yml

   run_on_volumes : 'ALL'
   run_on_mounts : 'ALL'


Subclassing the CarteTestClass Decorator Class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Providing information specific to the tests being run is necessary for the
decorator to work correctly. This is accomplished by subclassing the
decorator class and overriding the ``__init__()`` method to provide the
specific data.

There are three attributes in particular that the CarteTestClass uses to 
create the resulting array of test cases.

axis_names
	This is a list of names used to automatically create class attributes in
	the resulting test classes. For example, adding the name *volume* results
	in the class attribute named ``volume`` being added to the test class
	with the value resulting from the cartesian product process. In this way,
	the test methods have access to the values of that specific combination.

selections
	This is a list of lists containing the options passed in via config file.
	For example, in the case of the gluster examples below, the desired values
	for the configurations to be run are passed in via a config file. The
	decorator in this case would be used to *limit* the configurations each
	test class can be run on. The CarteTestClass intersects the *selections*
	lists with the *limits* list to create the resulting list of
	used to create a test class for each combination.

limits
	Limits are automatically passed in via the decorator and are used to limit
	the *selections* the test case can/will run on.

available_options
	This is the full list of all values allowed for a specific attribute and
	is used to populate the *selections* value when 'ALL' is specified for the
	*selections* attribute.


.. code-block:: python
   :emphasize-lines: 6
   :linenos:
   :caption: gluster_base_class.py
   :name: example-decoratorsubclass

   import unittest

   from glusto.core import Glusto as g


   class runs_on(g.CarteTestClass):
       """Decorator providing runs_on capability for standard unittest script"""

       def __init__(self, value):
           self.axis_names = ['volume', 'mount']

           self.available_options = [['distributed', 'replicated',
                                      'distributed-replicated',
                                      'disperse', 'distributed-disperse'],
                                     ['glusterfs', 'nfs', 'cifs']]

           config = g.load_config('gluster_config.yml')
           if config:
               g.update_config(config)
           run_on_volumes = g.config.get('run_on_volumes',
                                         self.available_options[0])
           run_on_mounts = g.config.get('run_on_mounts',
                                        self.available_options[1])
           self.selections = [run_on_volumes, run_on_mounts]
           self.limits = value


Creating a Custom unittest.TestCase Subclass
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: python
   :linenos:
   :caption: gluster_base_class.py
   :name: example-testcaseclass

   class GlusterBaseClass(unittest.TestCase):

       @classmethod
       def setUpClass(cls):
           print "setUpClass: %s" % cls.__name__
           print "SETUP GLUSTER VOLUME: %s on %s" % (cls.volume, cls.mount)

       def setUp(self):
           """Setting this up"""
           print "\tsetUp: %s - %s" % (self.id(), self.shortDescription())

       def tearDown(self):
           print "\ttearDown: %s - %s" % (self.id(), self.shortDescription())

       @classmethod
       def tearDownClass(cls):
           print "tearDownClass: %s" % cls.__name__
           print "TEARDOWN GLUSTER VOLUME: %s on %s" % (cls.volume, cls.mount)


Using the Decorator
~~~~~~~~~~~~~~~~~~~

.. code-block:: python
   :linenos:
   :caption: test_gluster_runsauto.py
   :name: example-testcase-script
   :emphasize-lines: 3-4,10-11,14-15,21,27

   from glusto.core import Glusto as g

   from gluster_base_class import GlusterBaseClass
   from gluster_base_class import runs_on

   import pytest
   import unittest


   volumes = ['distributed', 'replicated', 'disperse']
   mounts = ['glusterfs', 'nfs']


   @runs_on([volumes, mounts])
   class MyGlusterTest(GlusterBaseClass):
       def test_gluster1(self):
           """Test 1"""
           print "\t\tRunning: %s - %s" % (self.id(), self.shortDescription())
           print "\t\t%s on mount %s" % (self.volume, self.mount)

       @pytest.mark.test2
       def test_gluster2(self):
           """Test 2"""
           print "\t\tRunning: %s - %s" % (self.id(), self.shortDescription())
           print "\t\t%s on mount %s" % (self.volume, self.mount)

       @pytest.mark.skip
       def test_gluster3(self):
           """Test 3"""
           print "\t\tRunning: %s - %s" % (self.id(), self.shortDescription())
           print "\t\t%s on mount %s" % (self.volume, self.mount)


Run the Tests
~~~~~~~~~~~~~

.. code-block:: none
   :linenos:
   :emphasize-lines: 11,14,17,20,23,26

   $ glusto -c 'examples/systems.yml tests_gluster/gluster_conf.yml' --pytest='-vv -q tests_gluster/test_gluster_runsauto.py'
   Starting glusto via main()
   ...
   pytest: -vvv -q tests_gluster/test_gluster_runsauto.py
   ==================================================================================== test session starts =====================================================================================
   platform linux2 -- Python 2.7.11, pytest-2.9.2, py-1.4.31, pluggy-0.3.1 -- /usr/bin/python
   cachedir: .cache
   rootdir: glusto, inifile: 
   collected 18 items 

   tests_gluster/test_gluster_runsauto.py::MyGlusterTest_distributed_nfs::test_gluster1 PASSED
   tests_gluster/test_gluster_runsauto.py::MyGlusterTest_distributed_nfs::test_gluster2 PASSED
   tests_gluster/test_gluster_runsauto.py::MyGlusterTest_distributed_nfs::test_gluster3 SKIPPED
   tests_gluster/test_gluster_runsauto.py::MyGlusterTest_replicated_glusterfs::test_gluster1 PASSED
   tests_gluster/test_gluster_runsauto.py::MyGlusterTest_replicated_glusterfs::test_gluster2 PASSED
   tests_gluster/test_gluster_runsauto.py::MyGlusterTest_replicated_glusterfs::test_gluster3 SKIPPED
   tests_gluster/test_gluster_runsauto.py::MyGlusterTest_disperse_glusterfs::test_gluster1 PASSED
   tests_gluster/test_gluster_runsauto.py::MyGlusterTest_disperse_glusterfs::test_gluster2 PASSED
   tests_gluster/test_gluster_runsauto.py::MyGlusterTest_disperse_glusterfs::test_gluster3 SKIPPED
   tests_gluster/test_gluster_runsauto.py::MyGlusterTest_disperse_nfs::test_gluster1 PASSED
   tests_gluster/test_gluster_runsauto.py::MyGlusterTest_disperse_nfs::test_gluster2 PASSED
   tests_gluster/test_gluster_runsauto.py::MyGlusterTest_disperse_nfs::test_gluster3 SKIPPED
   tests_gluster/test_gluster_runsauto.py::MyGlusterTest_distributed_glusterfs::test_gluster1 PASSED
   tests_gluster/test_gluster_runsauto.py::MyGlusterTest_distributed_glusterfs::test_gluster2 PASSED
   tests_gluster/test_gluster_runsauto.py::MyGlusterTest_distributed_glusterfs::test_gluster3 SKIPPED
   tests_gluster/test_gluster_runsauto.py::MyGlusterTest_replicated_nfs::test_gluster1 PASSED
   tests_gluster/test_gluster_runsauto.py::MyGlusterTest_replicated_nfs::test_gluster2 PASSED
   tests_gluster/test_gluster_runsauto.py::MyGlusterTest_replicated_nfs::test_gluster3 SKIPPED

   ============================================================================ 12 passed, 6 skipped in 0.04 seconds ============================================================================
   Ending glusto via main()


ToDo
~~~~

* Add decorator for function and method.
* Finish this document.



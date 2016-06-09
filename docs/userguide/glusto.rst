Using Glusto
------------

Using Glusto in a Module
========================

To use Glusto in a module, import the Glusto class at the top of each module leveraging the glusto tools.

Example:
    To use Glusto in a module::

        from glusto.core import Glusto as g


Using Glusto via the Python Interactive Interpreter
===================================================


Using the Glusto CLI Utility
============================



Options for Running Unittests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example::

	# glusto -c 'examples/systems.yml' -u -d 'tests'
	# glusto -c 'examples/unittests/unittest.yml examples/unittests/unittest_list.yml examples/systems.yml' -u

For more information on working with unit tests, see `Unittests and Glusto <unittest.html#unittests_and_glusto>`__
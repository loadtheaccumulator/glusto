Using the Glusto CLI Utility
----------------------------



Options for Running Unittests
=============================

Example::

	# glusto -c 'examples/systems.yml' -u -d 'tests'
	# glusto -c 'examples/unittests/unittest.yml examples/unittests/unittest_list.yml examples/systems.yml' -u


unittest.yml::

	unittest:
	  output_junit: false
	  discover:
	    start_dir: 'tests'

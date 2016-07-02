PyTest and Glusto
-----------------


Running PyTests from the CLI
============================

Use the ``-t=`` or ``--pytest=`` parameter followed by the options normally passed to ``pytest``

	::

		$ glusto -c 'examples/systems.yml' --pytest='-v -x tests -m response'
		Starting glusto via main()
		...
		pytest: -v -x tests -m response
		========================= test session starts ============================================
		platform linux2 -- Python 2.7.11, pytest-2.9.2, py-1.4.31, pluggy-0.3.1 -- /usr/bin/python
		cachedir: .cache
		rootdir: glusto, inifile: 
		collected 21 items 

		tests/test_glusto_pytest.py::TestGlustoBasicsPyTest::test_return_code PASSED
		tests/test_glusto_pytest.py::TestGlustoBasicsPyTest::test_stderr PASSED
		tests/test_glusto_pytest.py::TestGlustoBasicsPyTest::test_stdout PASSED

		========================= 18 tests deselected by "-m 'response'" =========================
		======================== 3 passed, 18 deselected in 0.62 seconds =========================
		Ending glusto via main()

For a list of available options, pass ``--help`` to the ``pytest`` parameter or use the ``pytest`` command itself.

	::

		$ glusto --pytest='--help'
		$ pytest --help


Running PyTest from Python Interactive Interpreter
==================================================

	::

		>>> import pytest
		>>> pytest.main('-v -x tests -m response')
		========================== test session starts ===========================================
		platform linux2 -- Python 2.7.11, pytest-2.9.2, py-1.4.31, pluggy-0.3.1 -- /usr/bin/python
		cachedir: .cache
		rootdir: glusto, inifile: 
		collected 21 items 
		
		tests/test_glusto_pytest.py::TestGlustoBasicsPyTest::test_return_code PASSED
		tests/test_glusto_pytest.py::TestGlustoBasicsPyTest::test_stderr PASSED
		tests/test_glusto_pytest.py::TestGlustoBasicsPyTest::test_stdout PASSED
		
		========================= 18 tests deselected by "-m 'response'" =========================
		======================== 3 passed, 18 deselected in 0.55 seconds =========================
		0

To make config files available to test cases when running interactively,
use the ``load_config`` and ``update_config`` methods.

	::

		>>> from glusto.core import Glusto as g
		>>> config = g.load_config('examples/systems.yml')
		>>> g.update_config(config)
		>>> import pytest
		>>> pytest.main('-v -x tests -m response')


To Do
=====

* Expand text and examples

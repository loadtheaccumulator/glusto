Handling Templates with Glusto
------------------------------


Create a File from a Template
=============================

	::

		>>> g.render_template("templates/template_testcase.jinja",
		... template_vars, "/tmp/testcase.py", searchpath='examples/')

The Template File
=================


Template Variables
==================


Providing Vars Programmatically
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Providing Vars in a Config File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



A Bit About Search Path
=======================

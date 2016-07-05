Configuring Glusto
------------------

Glusto currently reads configuration files in yaml, json, or ini format.
It looks in ``/etc/glusto`` for ``defaults.yml``, ``defaults.yaml``, ``defaults.json`` and ``defaults.ini``.
You can provide any or all at the same time.

.. Note::

	It is currently necessary to create the ``/etc/glusto`` directory manually
	and populate it with ``defaults.`` files. Automatic creation of the defaults
	directory, a default ``defaults.yml``, and sample configs is upcoming.

defaults.yml or defaults.yaml::

	keyfile: "~/ssh/id_rsa"
	use_ssh: True
	use_controlpersist: True
	log_color: True

defaults.ini::

	[defaults]
	this = yada1
	that = yada2
	the_other = %(this)s and %(that)s
	
	[globals]
	some_default = yada yada

defaults.json::

	{"things": {
	  "thing_one": "yada",
	  "thing_two": "yada yada",
	  "thing_three": {
	    "combo_thing": [
	      {"combo_thing_one": "yada", "combo_thing_two": "yada yada"}
	    ]
	  }
	}}


The ini format provides some simple variable capability.

For example, this line from the above defaults.ini config::

	the_other = %(this)s and %(that)s

...will populate the_other variable in your Python script as "yada1 and yada2"::

	defaults: {that: yada2, this: yada1, this_and_that: yada1 and yada2}

.. Note::

	It is also possible to pass additional configuration files at the command-line, in IDLE, or from within script.
	via the ``-c`` option. See `Using Config Files with Glusto <configurable.html#using-config-files-with-glusto>`_ and
	`Using the Glusto CLI Utility <glusto.html#using-the-glusto-cli-utility>`_ for more information.

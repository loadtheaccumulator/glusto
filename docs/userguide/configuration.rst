Configuring Glusto
------------------

Glusto currently reads configuration files in yaml or ini format.
It looks in /etc/glusto for defaults.yml and defaults.ini.
You can provide one or the other or both at the same time.

defaults.yml::

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

The ini format provides some simple variable capability.

For example, this line from the above defaults.ini config::

	the_other = %(this)s and %(that)s

...will populate the_other variable in your Python script as "yada1 and yada2"::

	defaults: {that: yada2, this: yada1, this_and_that: yada1 and yada2}

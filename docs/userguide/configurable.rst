Using Config Files with Glusto
------------------------------

Glusto currently supports loading and storing configs in YAML, INI, and JSON format.
File format can be specified explicitly or Glusto can determine the format based on file extension.


Loading Config Files
====================

To load configuration from a file, use the ``load_config()`` method.

	Example config file ``examples/systems.yml``::

		$ cat examples/systems.yml
		clients: [192.168.1.225]
		masternode: 192.168.1.221
		nodes: [192.168.1.221, 192.168.1.222, 192.168.1.223, 192.168.1.224]

	Example ``load_config()``::

		>>> config = g.load_config('examples/systems.yml')
		>>> config
		{'nodes': ['192.168.1.221', '192.168.1.222', '192.168.1.223', '192.168.1.224'], 'clients': ['192.168.1.225'], 'masternode': '192.168.1.221'}

The ``config`` dictionary object now contains Python object representations of the config in the file.


Setting the Glusto Config Dictionary with a Config File
=======================================================

Glusto stores configs in a dictionary object named ``config`` at the root of the Glusto class.
Using the ``set_config()`` method will assign a loaded configuration to the Glusto ``config`` class attribute.

The config will be available in any module where the Glusto class is imported.

	Adding some data to demonstrate the effects of using ``set_config()``::

		>>> g.config['this'] = 'yada'
		>>> g.config
		{'this': 'yada'}

	Example of using the ``set_config()`` method::

		>>> config = g.load_config('examples/systems.yml')

		>>> g.set_config(config)
		>>> g.config
		{'nodes': ['192.168.1.221', '192.168.1.222', '192.168.1.223', '192.168.1.224'], 'clients': ['192.168.1.225'], 'masternode': '192.168.1.221'}

The Glusto class attribute ``g.config`` is now populated with the configuration loaded from file,
and the ``this`` dictionary item is no longer there.

.. Warning::

	This is destructive. Any existing data in the ``g.config`` attribute will be overwritten by the data passed to ``set_config()``.


Updating the Glusto Config Dictionary with a Config File
========================================================

Updating with the ``update_config`` method is similar to using ``set_config``,
but will add to the config and not overwrite everything in the ``config`` class attribute automatically.

	Adding some data to demonstrate the effects of using ``update_config()``::

		>>> g.config['this'] = 'yada'
		>>> g.config
		{'this': 'yada'}

	Example of using the ``update_config()`` method::

		>>> config = g.load_config('examples/systems.yml')

		>>> g.update_config(config)
		>>> g.config
		{'this': 'yada','nodes': ['192.168.1.221', '192.168.1.222', '192.168.1.223', '192.168.1.224'], 'clients': ['192.168.1.225'], 'masternode': '192.168.1.221'}

With ``update_config()``, the ``this`` dictionary item is still there.

To organize different configs in the ``g.config`` dictionary, you can leverage
Python's ability to have nested dictionaries.

	Example::

		g.config['systems'] = {}
		g.config['myapp'] = {}

.. Warning::

	When using nested dictionaries to separate different configs under the same
	``g.config`` dictionary, as mentioned above, you will need to use update_config()
	instead of set_config() as described in the *Setting the Glusto Config Dictionary with a Config File* section.


Displaying Objects in Config File Format
========================================

To output objects to stdout in config file format, use the ``show_config()`` method.

	::

		>>> g.show_config(g.config)
		clients: [192.168.1.225]
		masternode: 192.168.1.221
		nodes: [192.168.1.221, 192.168.1.222, 192.168.1.223, 192.168.1.224]


Storing Objects in Config File Format
=====================================

Glusto provides a simple interface for formatting objects and storing them in a config file.

To format and store an object in a file, use the ``store_config()`` method.

	::

		>>> g.config
		{'this': 'yada', 'nodes': ['192.168.1.221', '192.168.1.222', '192.168.1.223', '192.168.1.224'], 'clients': ['192.168.1.225'], 'masternode': '192.168.1.221'}

		>>> g.store_config(g.config, filename='/tmp/glusto_config.yml')

	::

		$ cat /tmp/glusto_config.yml
		clients: [192.168.1.225]
		masternode: 192.168.1.221
		nodes: [192.168.1.221, 192.168.1.222, 192.168.1.223, 192.168.1.224]
		this: yada

The ``store_config()`` method will determine the config format based on the filename extension passed to it.
If a format needs to be specified (maybe the extension does not represent the format),
the format can be specified with the ``config_type`` parameter.

	::

		>>> g.store_config(g.config, filename='/tmp/glusto_config.conf, config_type='ini')


.. Note::

	Glusto currently defaults to yaml format.


Creating an INI Config Format Compatible Object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The INI format is simple in layout with a section header followed by key=value pairs.
For that reason, an object being stored in INI format needs to be a dictionary (or dictionaries)
of key:value dictionaries.

	::

		>>> config = {'section1': {'this': 'yada', 'that': 'yada yada'}, 'section2': {'the_other': 'yada yada yada'}}
		>>> config
		{'section2': {'the_other': 'yada yada yada'}, 'section1': {'this': 'yada', 'that': 'yada yada'}}

Storing the INI Formatted Config
................................

To store the INI formatted object, pass it to the ``store_config()`` method.

	::

		>>> g.store_config(config, filename='/tmp/config.ini')

	::

		$ cat /tmp/config.ini
		[section2]
		the_other = yada yada yada
		
		[section1]
		this = yada
		that = yada yada

.. Note::

	Due to the nature of Python not maintaining order in certain objects,
	the order of the sections may not be the order in the dictionary being passed.
	To maintain section order, you will need to use an OrderedDict.


Storing the INI Formatted Config in a Specific Order
....................................................

To store the INI formatted object with the sections in a specific order,
pass it to the ``store_config()`` method as an OrderedDict object.

The argument to the ``order`` parameter should be a list of the names of the top-level
dictionary keys in the object.

	::
		>>> from collections import OrderedDict
		>>> config = OrderedDict()
		>>> config.update('section1': {'this': 'yada'})
		>>> config.update('section2': {'that': 'yada yada'})
		>>> config.update('section3': {'the_other': 'yada yada yada'})
        >>> g.store_config(config, '/tmp/ordered.ini')

	::

		$ cat /tmp/ordered.ini
		[section1]
		this = yada

		[section2]
		that = yada yada

		[section3]
		the_other = yada yada yada


Loading Config from a String
============================

YAML formatted text can be converted into a dictionary object using the ``load_yaml_string()`` method.

	::

		>>> g.load_yaml_string(yaml_string)
		{'clusters': ['e2effa75a5a50560c3250b67cf71b465']}

JSON formatted text can be converted into a dictionary object using the ``load_json_string()`` method.

	::

		>>> config = g.load_json_string(json_string)
		>>> config
		{u'clusters': [u'e2effa75a5a50560c3250b67cf71b465']}


.. Note::

	There is not a current method for loading an INI formatted string.


Adding Simple Configuration Capability to Your Own Class
========================================================

Glusto provides an inheritable class (``Intraconfig``) that can add basic introspection and config functionality to classes in your scripts.

Making a Class Configurable
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Making a class configurable is as simple as making it inherit from the Intraconfig class.

To inherit from the Intraconfig, add ``Intraconfig`` to the class definition.

	Example making the class MyClass configurable::

    	>>> from glusto.configurable import Intraconfig
        >>> class MyClass(Intraconfig):
        >>>    def __init__(self):
        >>>        self.this = 'yada1'
        >>>        self.that = 'yada2'

Displaying the Class Config
~~~~~~~~~~~~~~~~~~~~~~~~~~~

To output attributes of the ``myinst`` instance of ``MyClass``, use the inherited ``show_config()`` method. 

	Example with myinst as an instance of class MyClass::

		>>> myinst = MyClass()
		>>> myinst.show_config()
		{that: yada2, this: yada1}

Loading Config from a File into Class Attributes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To load a config file into a dictionary attribute of a class instance, use the inherited ``load_config()`` method.

	Example loading a config from ``examples/systems.yml`` into class instance ``myinst``::

		>>> myinst.load_config('examples/systems.yml')
		>>> myinst.show_config()
		clients: [192.168.1.225]
		masternode: 192.168.1.221
		nodes: [192.168.1.221, 192.168.1.222, 192.168.1.223, 192.168.1.224]
		that: yada2
		this: yada1

Storing Attributes of an Instance to File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To store the attributes of a class instance, use the inherited ``store_config()`` method.

	Example storing the attributes from the ``myinst`` instance of ``MyClass`` to file ``/tmp/myinst.yml``::

		>>> myinst.store_config('/tmp/myinst.yml')

	Looking at the contents of the resulting config file::

		$ cat /tmp/myinst.yml 
		clients: [192.168.1.225]
		masternode: 192.168.1.221
		nodes: [192.168.1.221, 192.168.1.222, 192.168.1.223, 192.168.1.224]
		that: yada
		this: yada

.. Warning::

	Glusto will currently throw errors when using Instaconfig to store INI formatted config to file.
	Currently, the best way to store in INI format would be to form your config data, and then use ``g.store_config()``.

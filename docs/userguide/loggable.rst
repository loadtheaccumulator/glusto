Handling Logging with Glusto
----------------------------


Default Logging
===============

By default, a logging object (``glustolog``) is setup by Glusto.
Both are initially pointed at the same logfile (``/tmp/glusto.log``)

The ``glustolog`` object is designed for use by Glusto itself.
If you need a log that is independent of the events logged by Glusto, you can
create a new log object for use in your scripts.

Setting up Logging
==================

To create a new logging object, use the ``create_log`` command:

	::

	    >>> mylog = g.create_log(name='mylog', filename='/tmp/my.log')

The default severity level is ``INFO``.

To create a logging object with a severity level other than the default:

	::

	    >>> mylog = g.create_log(name='mylog', filename='/tmp/my.log', level='WARNING')

The options are ``INFO``, ``WARNING``, ``ERROR``, ``CRITICAL``, and ``DEBUG``

Sending Log Events to Multiple Logfiles
=======================================

If you need to log to multiple files at the same time, you can add
additional log handlers to an existing log object.

To add an additional logfile to an existing log object:

	::

		>>> g.add_log(g.mylog, filename='/tmp/my_other.log', level='CRITICAL')

.. Warning::

	The level parameter sets the level at the logger, not the logfile, so all
	handlers will log at the newly specified level. Leaving the parameter off
	will change all handlers to the default logging level (currently ``INFO``).


If 'STDOUT' is passed as the filename, a log will be added that prints to stdout.

	::

		>>> g.add_log(g.mylog, filename='STDOUT')


You can confirm there are multiple logfiles attached to the log object, by
running the following command...

	::

		>>> g.show_logs(g.mylog)
		mylog0: /tmp/my.log
		mylog1: sys.stdout


Logging with Color Text
=======================

With the simple ANSI color capability built into Glusto, it is possible to add color text in logs or other output.

Changing the Color of a String
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To wrap a string in color, use the colorfy command.

	::

		>>> print g.colorfy(g.RED, 'This string is RED')

The printed string will be output in the color red and any following text will return to default color.

Changing the Background Color of a String
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is possible to change the background color of a string.

	::

		>>> print g.colorfy(g.BG_YELLOW, 'This string has a YELLOW background')


Changing an ANSI Attribute of a String
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is also possible to make a string bold.

	::

		>>> print g.colorfy(g.BOLD, 'This string is BOLD')

The attribute options include:

* NORMAL
* BOLD
* DIM
* UNDERLINE
* BLINK
* REVERSE
* HIDDEN

.. Warning::

	Mileage may vary depending on the output device.


Combining Colors and Attributes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Glusto allows multiple combinations of color and attributes to be used at the same time.

To combine colors and attributes, pass a Bitwise Or'd list to ``colorfy()``.

	::

		>>> print g.colorfy(g.BOLD | g. RED | g.BG_YELLOW, 'This string is BOLD and RED on a YELLOW BACKGROUND.')


.. Tip::

	Create your own combinations ahead of time for re-use throughout your script.

	::

		>>> COLOR_ALERT =  g.BOLD | g.RED | g.REVERSE
		>>> COLOR_WARNING =  g.BOLD | g.RED
		>>> print '%s %s' %(g.colorfy(COLOR_ALERT, 'WARNING:'), g.colorfy(COLOR_WARNING, 'This is a warning!'))

Send Color Text to the Log
~~~~~~~~~~~~~~~~~~~~~~~~~~

Any of the previously discussed print commands can be replaced with logging
commands to send the color text to logfiles.

	Example::
		>>> g.log.debug(g.colorfy(g.BOLD | g. RED | g.BG_YELLOW, 'This string is BOLD and RED on a YELLOW BACKGROUND.'))

.. Enabling Color Logging for Built-In Commands
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  Some of the Glusto internal commands (e.g., ``g.run()``) already use color output for logging.

  To enable the built-in color logging, add a line to the Glusto ``/etc/glusto/defaults.log`` file.

	::

		log_color: True

  To disable the built-in color logging...

	::

		log_color: False

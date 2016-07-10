Handling Logging with Glusto
----------------------------


Default Logging
===============

By default, a logging object (``glustolog``) is setup by Glusto.
It writes to ``/tmp/glusto.log``

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
		>>> g.mylog.info('This is a test log entry to stdout.')
		2016-06-05 10:27:24,175 INFO (<module>) This is a test log entry to stdout.


Show the Logfiles Attached to a Specific Logger
===============================================

To show a list of the logfiles attached to a logger, use the ``show_logs()`` command.

	::

		>>> g.show_logs(g.mylog)
		Log:  mylog
		... mylog1: /tmp/my.log (WARNING)
		... mylog2: /tmp/my_other.log (CRITICAL)



Removing a Log
==============

If a logfile is no longer needed, remove the logfile from the logger with the ``remove_log()`` command.

	::

		>>> g.show_logs(g.mylog)
		Log: mylog
		... mylog1: /tmp/my.log
		... mylog2: sys.stdout
		>>> g.remove_log(g.mylog, 'mylog1')

		>>> g.show_logs(g.mylog)
		Log: mylog
		... mylog1: /tmp/my.log

To remove all logfiles from a logger, use the ``remove_log`` command without passing a name.

	::

		>>> g.remove_log(g.mylog)


Changing the Level of an Existing Log Handler
=============================================

To change the level of an existing log, use the ``set_log_level()`` method.

	::

		>>> g.show_logs(g.log)
		Log:  glustolog
		... glustolog1: /tmp/glusto.log (DEBUG)
		... glustolog2: /tmp/testtrunc.log (INFO)

		>>> g.set_log_level('glustolog', 'glustolog2', 'WARNING')

		>>> g.show_logs(g.log)
		Log:  glustolog
		... glustolog1: /tmp/glusto.log (DEBUG)
		... glustolog2: /tmp/testtrunc.log (WARNING)


Changing the Filename of an Existing Log Handler
================================================

To change the level of an existing log, use the ``set_log_filename()`` method.

	::

		>>> g.show_logs(g.log)
		Log:  glustolog
		... glustolog1: /tmp/glusto.log (DEBUG)
		... glustolog2: /tmp/testtrunc.log (INFO)

		>>> g.set_log_filename('glustolog', 'glustolog2', '/tmp/my.log')

		>>> g.show_logs(g.log)
		Log:  glustolog
		... glustolog1: /tmp/glusto.log (DEBUG)
		... glustolog2: /tmp/my.log (WARNING)


Clearing a Log
==============

To empty a logfile, use the ``clear_log()`` method.

	::

		>>> g.show_logs(g.log)
		Log:  glustolog
		... glustolog1: /tmp/glusto.log (DEBUG)
		... glustolog2: /tmp/testtrunc.log (INFO)
		>>> g.clear_log('glustolog', 'glustolog2')


Temporarily Disable Logging
===========================

There might be times when suspending logging at a certain level is necessary.
For example, if a particular function tends to spam the log.

To suspend logging at a specific level, use the ``disable_log_levels()`` method.

	::

		>>> g.disable_log_levels('WARNING')

.. Note::

	This will suspend logging for the specific level and all levels below it
	across all logs.

To resume logging at the previously defined levels, use the ``reset_log_levels()`` method.

	::

		>>> g.reset_log_levels()


Logging with Color Text
=======================

With the simple ANSI color capability built into Glusto, it is possible to add color text in logs or other output.

Changing the Color of a String
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To wrap a string in color, use the colorfy command.

::

	>>> print g.colorfy(g.RED, 'This string is RED')

The printed string will be output in the color red and any following text will return to default color.

See the "Available Color Values" below for the full list of Foreground Colors.


Changing the Background Color of a String
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is possible to change the background color of a string.

	::

		>>> print g.colorfy(g.BG_YELLOW, 'This string has a YELLOW background')

See the "Available Color Values" below for the full list of Background Colors.


Changing an ANSI Attribute of a String
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is also possible to make a string bold.

	::

		>>> print g.colorfy(g.BOLD, 'This string is BOLD')

.. Warning::

	Mileage may vary depending on the output device.

See the "Available Color Values" below for the full list of Attributes.


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

	::

		>>> g.log.debug(g.colorfy(g.BOLD | g.RED | g.BG_YELLOW, 'This string is BOLD and RED on a YELLOW BACKGROUND.'))

.. Enabling Color Logging for Built-In Commands
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  Some of the Glusto internal commands (e.g., ``g.run()``) already use color output for logging.

  To enable the built-in color logging, add a line to the Glusto ``/etc/glusto/defaults.log`` file.

	::

		log_color: True

  To disable the built-in color logging...

	::

		log_color: False


Available Color Values
~~~~~~~~~~~~~~~~~~~~~~

When using the color values listed in the table below, remember to add the Glusto ``g.`` reference in front of each color value.

	For example, ``g.BG_LTMAGENTA``


============  ==========  ==========
BACKGROUND    FOREGROUND  ATTRIBUTES
============  ==========  ==========
BG_DEFAULT    DEFAULT     NORMAL
BG_BLACK      BLACK       BOLD
BG_RED        RED         DIM
BG_GREEN      GREEN       UNDERLINE
BG_YELLOW     YELLOW      BLINK
BG_BLUE       BLUE        REVERSE
BG_MAGENTA    MAGENTA     HIDDEN
BG_CYAN       CYAN
BG_LTGRAY     LTGRAY
BG_DKGRAY     DKGRAY
BG_LTRED      LTRED
BG_LTGREEN    LTGREEN
BG_LTYELLOW   LTYELLOW
BG_LTBLUE     LTBLUE
BG_LTMAGENTA  LTMAGENTA
BG_LTCYAN     LTCYAN
BG_WHITE      WHITE
============  ==========  ==========



Glusto (Python3 Beta)
=====================

Glusto is a suite of modules designed to provide features commonly used in a
remote/distributed environment via a single and easy-to-access object.

It started out as a port of some shell ssh functions I had written
and was adopted for use in PyUnit* tests for Gluster.

Some of the key concepts and features of Glusto:

* Glusto inherits from multiple classes providing configuration (yaml, json, ini), remote connection (SSH, SCP, RPyC), ANSI color output, logging, and unit test functionality (PyUnit, PyTest, Nose)--presenting them in a single global Class object.

* Glusto also acts as a global class for maintaining state and configuration data across multiple modules and classes.

* Glusto provides a wrapper utility (``/usr/bin/glusto``) to help make configuration files available to test cases from the command-line.

This is the Python3 port and will, for the near future, be maintained as a separate branch.
Eventually, the Python3 branch will become master and Python2 will be moved to a branch for availability.

Note:
    The Python3 requests library has become even more straight-forward to use, so Glusto restable may be deprecated in a future version.


#### How to Use Glusto

Import at the top of each module leveraging the glusto tools.

Example:
    To use Glusto in a module::

        >>> from glusto.core import Glusto as g


Glusto inherits from multiple classes providing configuration,
remote connection, ANSI color output, and logging functionality,
presenting them in a single global Class object.
Glusto also acts a global class for maintaining state across
multiple modules and classes.

Note:
    It is no longer necessary to say "Glusto Importo!" out loud
    before executing scripts using the Glusto module. The import statement is 
    more than sufficient.

#### User Guide

The User Guide is hosted on Read the Docs @ http://glusto.readthedocs.io/en/latest/

#### TODO
* add more config handling
* better docs and more examples


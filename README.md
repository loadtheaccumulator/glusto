Glusto
======

Glusto is a framework designed to provide features commonly used in a
remote/distributed test environment.

It started out as a port of some shell ssh functions I had written
and was meant for use in PyUnit* tests for Gluster.

I don't see much reason it could not be used with other Python test frameworks.
Feel free to give it a go, and please let me know how it works out.

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


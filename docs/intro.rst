.. _introduction:

Glusto is a framework designed to provide features commonly used in a
remote/distributed environment.

It started out as a port of some shell ssh functions I had written
and was meant for use in PyUnit* tests and config scripts for Gluster.

I've removed the Gluster specifics from this package, and I don't see reason
why it could not be used with other Python test frameworks or scripts.
Feel free to give it a go, and please let me know how it works out.

Glusto inherits from multiple classes providing configuration,
remote connection, ANSI color output, logging, and unittest functionality,
presenting them in a single global Class object.
Glusto also acts a global class for maintaining state and configuration data
across multiple modules and classes.

Adding Glusto utilities to a Python module is as simple as an import.

Example:
    To use Glusto in a module::

        from glusto.core import Glusto as g

.. note:: It is no longer necessary to say "Glusto Importo!" out loud
   before executing scripts using the Glusto module. The import statement is
   more than sufficient.

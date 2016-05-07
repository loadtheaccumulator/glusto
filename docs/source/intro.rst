.. _introduction:

Glusto is a framework designed to provide features common to a remote
distributed Gluster environment.

How to Use Glusto
=================

Import at the top of each module leveraging the glusto tools.

Example:
    To use Glusto in a module::

        from glusto.core import Glusto as g


Glusto inherits from multiple classes providing configuration,
remote connection, ANSI color output, and logging functionality,
presenting them in a single global Class object.
Glusto also acts a global class for maintaining state across
multiple modules and classes.

.. note:: It is no longer necessary to say "Glusto Importo!" out loud
   before executing scripts using the Glusto module.

   The import statement is more than sufficient.

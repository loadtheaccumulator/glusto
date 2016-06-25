# Copyright 2014 Jonathan Holloway <loadtheaccumulator@gmail.com>
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software. If not, see <http://www.gnu.org/licenses/>.
#

"""The brains of the Glusto toolset.

Glusto inherits from multiple classes providing configuration,
remote connection, and logging functionality and presents them in a single
global Class object. Glusto also acts a global class for maintaining state
across multiple modules and classes.

Example:
    To use Glusto in a module,
    import at the top of each module leveraging the glusto tools.::

        from glusto.core import Glusto as g
"""

from glusto.configurable import Configurable
from glusto.connectible import Connectible
from glusto.colorfiable import Colorfiable
from glusto.loggable import Loggable
from glusto.templatable import Templatable
from glusto.unittestable import Unittestable
from glusto.restable import Restable
from glusto.rpycable import Rpycable


class Glusto(Configurable, Connectible, Colorfiable, Loggable,
             Templatable, Unittestable, Restable, Rpycable):
    """The locker for all things Glusto."""

    # TODO: figure out how we want to do this with cli options
    # TODO: call this after configs are read to be more effective
    # TODO: do this by default or force to be from main() or other importer
    # create default log
    log = Loggable.create_log()
    #log = Loggable.create_log('userlog', filename='/tmp/glusto.log')

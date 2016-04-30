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

Import at the top of each module leveraging the glusto tools.

Example:
    To use Glusto in a module::

        from glusto.core import Glusto as g


Glusto inherits from multiple classes providing configuration,
remote connection, and logging functionality and presents them in a single
global Class object. Glusto also acts a global class for maintaining state
across multiple modules and classes.

"""
import logging
import os

from glusto.configurable import Configurable
from glusto.connectible import Connectible
from glusto.colorfiable import Colorfiable
from glusto.loggable import Loggable


class Glusto(Configurable, Connectible, Colorfiable, Loggable):
    """Glusto class
    The locker for all things Glusto
    """
    #config["ssh_keyfile"] = "~/.ssh/id_rsa"
    # TODO: figure which of these are class and config parameters
#    config["nodes"] = ['192.168.1.221', '192.168.1.222',
#                       '192.168.1.223', '192.168.1.224']
#    config['clients'] = ['192.168.1.225']
    # TODO: keep glusto dumb and leave nodes in config. ???
    config = {}
    nodes = []
    clients = []

    # TODO: figure out how we want to do this with cli options
    # TODO: call this after configs are read to be more effective
    # TODO: do this by default or force to be from main() or other importer
    # create default log
    log = Loggable.create_log()


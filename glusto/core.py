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


class Glusto(Configurable, Connectible, Colorfiable):
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

    # TODO: load default config(s)
    # TODO: add ability to log to STDOUT instead of logfile
    # setup logging
    log = logging.getLogger('glustolog')
    log.propagate = False

    # Create file handler for logger
    # TODO: set logfile from config (with default)
    _logfile = config.get('logfile', '/tmp/glusto.log')
    if not os.path.exists(_logfile):
        _logdir = os.path.dirname(_logfile)
        if not os.path.exists(_logdir):
            os.makedirs(_logfile)
    _logfh = logging.FileHandler(_logfile)

    # Set log string format for logger
    # TODO: set log string format from config (with default)
    _formatter = logging.Formatter('%(asctime)s %(levelname)s '
                                   '(%(funcName)s) %(message)s')
    _logfh.setFormatter(_formatter)

    # Add handler to logger
    log.addHandler(_logfh)

    # Set log level
    # TODO: set level from config (with default)
    log.setLevel(logging.DEBUG)

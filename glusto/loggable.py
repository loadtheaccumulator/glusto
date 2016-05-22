# Copyright 2016 Jonathan Holloway <loadtheaccumulator@gmail.com>
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
"""All things logging.

NOTE:
    Loggable is inherited by the Glusto class
    and not designed to be instantiated.
"""

import logging
import os


class Loggable(object):
    """The class providing logging functionality."""
    # TODO: load default config(s)
    # TODO: add ability to log to STDOUT instead of logfile
    # setup logging

    # Create file handler for logger
    # TODO: set logfile from config (with default)
    # setup default logging

    @classmethod
    def create_log(cls, name='glustolog', filename='/tmp/glusto.log',
                   level='INFO'):
        """Creates a log object using the Python "logging" module.

        Args:
            name (optional[str]): The reference name for the logging object.
                Defaults to "glustolog".
            filename (optional[str]): Fully-qualified path and filename.
                Defaults to "/tmp/glusto.log".
            level (optional[str]): The minimum log level. Defaults to "INFO".

        Returns:
            A logging object.
        """

        log = logging.getLogger(name)
        log.propagate = False
        _logfile = filename
        # _logfile = config.get('logfile', '/tmp/glusto.log')
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
        # TODO: verify all of the available options
        # TODO: catch illegal options???
        _level = {'DEBUG': logging.DEBUG,
                  'INFO': logging.INFO,
                  'WARNING': logging.WARNING,
                  'CRITICAL': logging.CRITICAL}[level]
        log.setLevel(_level)

        return log

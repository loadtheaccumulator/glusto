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
import sys


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
                   level='DEBUG', allow_multiple=False):
        """Creates a log object using the Python "logging" module.

        Args:
            name (optional[str]): The reference name for the logging object.
                Defaults to "glustolog".
            filename (optional[str]): Fully-qualified path and filename.
                Defaults to "/tmp/glusto.log".
            level (optional[str]): The minimum log level. Defaults to "INFO".
            allow_multiple (bool): Can multiple logfiles exist?
                Tells method whether to create a new handler or wipe existing
                before creating a new handler.
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

        # TODO: check for existing handler with same filename
        # cleanup existing handlers
        if not allow_multiple:
            for handler in log.handlers[:]:
                log.removeHandler(handler)

        if filename == 'STDOUT':
            _logfh = logging.StreamHandler(sys.stdout)
        else:
            _logfh = logging.FileHandler(_logfile)
        num_handlers = len(log.handlers)
        # TODO: handle name conflict when a log has been removed
        # TODO: catch "OSError: [Errno 13] Permission denied: '/var/log/t.log'"
        # TODO: catch "IOError: [Errno 21] Is a directory: '/tmp/log/test.log'"
        handler_name = "%s%i" % (name, num_handlers)
        _logfh.set_name(handler_name)

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
                  'ERROR': logging.ERROR,
                  'CRITICAL': logging.CRITICAL}[level]
        log.setLevel(_level)

        return log

    @classmethod
    def add_log(cls, logobj, filename='/tmp/glusto.log',
                level='INFO'):
        """Add a logfile to the logobj

        Args:
            logobj (object): A logging object.
            filename (optional[str]): Fully-qualified path and filename.
                Defaults to "/tmp/glusto.log".
            level (optional[str]): The minimum log level. Defaults to "INFO".
        """
        name = logobj.name
        log = cls.create_log(name=name, filename=filename, level=level,
                             allow_multiple=True)

        return log

    @classmethod
    def remove_log(cls, logobj, name=None):
        """Remove a log handler from a logger object.

        Args:
            logobj (object): A logging object.
            name (optional[str]): The name of the log handler to remove.
                If None, will remove all log handlers from the logger.
        """
        # remove all if no name is supplied else delete the one specified
        if not name:
            for handler in logobj.handlers[:]:
                logobj.removeHandler(handler)
        else:
            for handler in logobj.handlers[:]:
                if handler.get_name() == name:
                    logobj.removeHandler(handler)

    @classmethod
    def show_logs(cls, logobj):
        """Show a list of log handlers attached to a logging object

        Args:
            logobj (object): A logging object.
        """
        for handler in logobj.handlers:
            name = handler.get_name()
            if handler.stream == sys.stdout:
                filename = 'sys.stdout'
            else:
                filename = handler.baseFilename

            print "%s: %s" % (name, filename)

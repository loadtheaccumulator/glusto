# Copyright 2016-2018 Jonathan Holloway <loadtheaccumulator@gmail.com>
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


class Loggable():
    """The class providing logging functionality."""

    handler_counter = 0

    # pylint: disable=too-many-arguments
    @classmethod
    def create_log(cls, name='glustolog', filename='/tmp/glusto.log',
                   level='DEBUG', log_format=None, allow_multiple=False):
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
        # TODO: one call -> multiple levels
        if not log_format:
            log_format = ('%(asctime)s %(levelname)s '
                          '(%(funcName)s) %(message)s')
        log = logging.getLogger(name)
        log.propagate = False
        _logfile = filename
        # _logfile = config.get('logfile', '/tmp/glusto.log')
        if not os.path.exists(_logfile):
            _logdir = os.path.dirname(_logfile)
            if not os.path.exists(_logdir):
                os.makedirs(_logfile)

        # TODO: check for existing handler with same filename ???
        # cleanup existing handlers
        if not allow_multiple:
            for handler in log.handlers[:]:
                log.removeHandler(handler)

        if filename == 'STDOUT':
            _logfh = logging.StreamHandler(sys.stdout)
        else:
            _logfh = logging.FileHandler(_logfile)

        # TODO: make this re-use deleted numbers and track per log
        # num_handlers = len(log.handlers)
        cls.handler_counter += 1

        # TODO: catch "OSError: [Errno 13] Permission denied: '/var/log/t.log'"
        # TODO: catch "IOError: [Errno 21] Is a directory: '/tmp/log/test.log'"
        handler_name = "%s%i" % (name, cls.handler_counter)
        _logfh.set_name(handler_name)

        # Set log string format for logger
        _formatter = logging.Formatter(log_format)
        _logfh.setFormatter(_formatter)
        # Set log level
        # TODO: catch illegal options???
        _level = logging.getLevelName(level)
        _logfh.level = _level
        # Add handler to logger
        log.addHandler(_logfh)

        if not allow_multiple:
            log.setLevel(_level)

        return log

    @classmethod
    def add_log(cls, logobj, filename='/tmp/glusto.log',
                level='INFO', log_format=None):
        """Add a logfile to the logobj

        Args:
            logobj (object): A logging object.
            filename (optional[str]): Fully-qualified path and filename.
                Defaults to "/tmp/glusto.log".
            level (optional[str]): The minimum log level. Defaults to "INFO".
        """
        name = logobj.name
        log = cls.create_log(name=name, filename=filename,
                             level=level, log_format=log_format,
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
        log_name = logobj.name
        print("Log: ", log_name)
        for handler in logobj.handlers:
            name = handler.get_name()
            if handler.stream == sys.stdout:
                filename = 'sys.stdout'
            else:
                filename = handler.baseFilename

            level = logging.getLevelName(handler.level)
            print("- %s: %s (%s)" % (name, filename, level))

    @classmethod
    def disable_log_levels(cls, level):
        """Disable level (and lower) across all logs and handlers.
        Handy if a method continually spams the logs.
        Use reset_log_level() to return to normal logging.

        .. Note::

            See Python logging module docs for more information.

        Args:
            level (str): String name for the top log level to disable.

        Returns:
            Nothing
        """
        logging.disable(logging.getLevelName(level))

    @classmethod
    def reset_log_levels(cls):
        """Reset logs to current handler levels.
        Convenience method to undo disable_log_level()

        Args:
            None

        Returns:
            Nothing
        """
        logging.disable(logging.NOTSET)

    @classmethod
    def set_log_level(cls, log_name, handler_name, level):
        """Set the log level for a specific handler.
        Use show_logs() to get the list of log and handler names.

        Args:
            log_name (str): The name of the log.
            handler_name (str): The name of the specific log handler.
            level (str): The string representation of the log level.

        Returns:
            Nothing
        """
        log = logging.getLogger(log_name)

        for handler in log.handlers:
            if handler.name == handler_name:
                level_name = logging.getLevelName(level)
                handler.setLevel(level_name)
                break

    @classmethod
    def set_log_filename(cls, log_name, handler_name, filename):
        """Change the logfile name for a specific handler.
        Use show_logs() to get the list of log and handler names.

        Args:
            log_name (str): The name of the log.
            handler_name (str): The name of the specific log handler.
            filename (str): The path/filename to log to.

        Returns:
            Nothing

        .. Note::

            Nothing in logging docs mentions this method (close and set
            baseFilename) over removing the handler and creating a new handler
            with the new filename. Research and correct if needed.
            Caveat emptor.
        """
        filename = os.path.abspath(filename)
        log = logging.getLogger(log_name)
        for handler in log.handlers:
            if handler.name == handler_name:
                handler.close()
                handler.baseFilename = filename
                break

    @classmethod
    def clear_log(cls, log_name, handler_name):
        """Empties an existing log file

        Args:
            log_name (str): The name of the log.
            handler_name (str): The name of the specific log handler.

        Returns:
            Nothing
        """
        log = logging.getLogger(log_name)
        for handler in log.handlers:
            if handler.name == handler_name:
                handler.close()
                file_descriptor = open(handler.baseFilename, 'r+')
                file_descriptor.truncate()
                file_descriptor.close()

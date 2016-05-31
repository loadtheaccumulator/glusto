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
"""Glusto CLI wrapper"""
import argparse
from unittest import TestLoader, TestSuite, TextTestRunner
import xmlrunner
import importlib

from glusto.core import Glusto as g


def handle_configs(config_list):
    """Load default and user-specified configuration files"""

    # load default config
    g.glustolog.info("Loading default configuration files.")
    g.load_config_defaults()

    # load user specified configs
    if (config_list):
        g.glustolog.info("Loading user specified configuration files.")
        config_files = config_list.split()
        config = g.load_configs(config_files)
        g.update_config(config)

    # XXX: remove me
    g.show_config(g.config)


def main():
    """Entry point console script for setuptools.

    Provides a command-line interface to Glusto.

    Currently does nothing useful, but plan to wrap Glusto functionality in a
    CLI interface that can be injected into shell scripts, etc.

    Example:
        # glusto run hostname.example.com "uname -a"
    """
    g.glustolog.info("Starting glusto via main()")
    print "Starting glusto via main()"

    parser = argparse.ArgumentParser(description="Glusto CLI wrapper")
    parser.add_argument("-c", "--config",
                        help="Config file(s) to read.",
                        action="store", dest="config_list")
    parser.add_argument("-u", "--unittest",
                        help="Run unittests per provided config file.",
                        action="store_true", dest="run_unittest")
    args = parser.parse_args()

    # read config files and update g.config attributes
    handle_configs(args.config_list)

    g.show_config(g.config)

    # TODO: break everything into separate methods

    # handle actionable config items
    # logging
    log_name = g.config.get('log_name', 'glustomain')
    log_filename = g.config.get('log_filename', '/tmp/glustomain.log')
    log_level = g.config.get('log_level', 'INFO')

    if log_filename:
        g.log = g.create_log(name=log_name, filename=log_filename,
                             level=log_level)
        g.log.info("Logfile %s created as %s "
                   "with log level %s", log_name, log_filename, log_level)

    # unittest
    if args.run_unittest:
        tsuite = TestSuite()
        unittest_config = g.config.get('unittest', False)
        if not unittest_config:
            print ("ERROR: Unittest option requires a unittest configuration.")
            return False

        output_junit = unittest_config.get('output_junit', False)
        if output_junit:
            trunner = xmlrunner.XMLTestRunner(output='/tmp/glustoreports')
        else:
            trunner = TextTestRunner(verbosity=2)

        discover = unittest_config.get('discover')
        # TODO: Add ability to run multiple discoveries in a single config
        if discover:
            print "START - RUNNING DISCOVERED TESTS..."
            start_dir = discover.get('start_dir', '.')
            pattern = discover.get('pattern', 'test_*')
            top_level_dir = discover.get('top_level_dir', None)
            discovered_tests = TestLoader().discover(start_dir, pattern,
                                                     top_level_dir)
            tsuite.addTests(discovered_tests)
            print "END - RUNNING DISCOVERED TESTS..."

        run_list = unittest_config.get('run_list')
        # TODO: ability to load multiple lists
        # TODO: list format more conducive to automation ???
        if run_list:
            print "START - RUNNING LIST OF TESTS..."
            unittest_config = g.config['unittest']
            unittest_list = g.config['unittest_list']
            module_name = unittest_list['module_name']
            test_list = unittest_list['list']

            test_module_obj = importlib.import_module(module_name)

            loader = TestLoader()
            tests_to_run = loader.loadTestsFromNames(test_list,
                                                     test_module_obj)

            tsuite.addTests(tests_to_run)
            #result = unittest.TestResult()
            #suite.run(result)
            print "END - RUNNING LIST OF TESTS..."

        run_module = unittest_config.get('run_module')
        if run_module:
            print "START - RUNNING MODULE (%s)..." % run_module
            loader = TestLoader()
            #test_module_obj = importlib.import_module(run_module)
            test_module_obj = __import__(run_module, fromlist='TestGlustoBasics')
            print test_module_obj
            # FIXME: issue with load_tests in test_glusto needs to be resolved
            #            using False for now
            tests_from_module = loader.loadTestsFromModule(test_module_obj,
                                                           True)
            tsuite.addTests(tests_from_module)
            print "END - RUNNING MODULE"

        # TODO: Add a skip test option
        trunner.run(tsuite)

    g.glustolog.info("Ending glusto via main()")
    print "Ending glusto via main()"


# TODO: remove print statements (or swap for log debug/info)
if __name__ == '__main__':
    main()

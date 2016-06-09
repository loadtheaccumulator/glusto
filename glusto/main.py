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
import inspect
import sys

from glusto.core import Glusto as g


def handle_configs(config_list):
    """Load default and user-specified configuration files"""

    # load default config
    g.log.info("Loading default configuration files.")
    g.load_config_defaults()

    # load user specified configs
    if (config_list):
        g.log.info("Loading user specified configuration files.")
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
    g.log.info("Starting glusto via main()")
    print "Starting glusto via main()"

    parser = argparse.ArgumentParser(description="Glusto CLI wrapper")
    parser.add_argument("-c", "--config",
                        help="Config file(s) to read.",
                        action="store", dest="config_list")
    parser.add_argument("-u", "--unittest",
                        help="Run unittests per provided config file.",
                        action="store_true", dest="run_unittest")
    parser.add_argument("-d", "--discover",
                        help="Discover unittests from directory",
                        action="store", dest="discover_dir")
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
    # TODO: functionalize this so it can be used for standalone test scripts
    if args.run_unittest or args.discover_dir:
        tsuite = TestSuite()
        if args.discover_dir:
            unittest_config = {'cli_discover': 'true'}
        else:
            unittest_config = g.config.get('unittest', False)

        if not unittest_config:
            print ("ERROR: Unittest option requires a unittest configuration.")
            return False

        output_junit = unittest_config.get('output_junit', False)
        if output_junit:
            trunner = xmlrunner.XMLTestRunner(output='/tmp/glustoreports')
        else:
            trunner = TextTestRunner(verbosity=2)

        loader = TestLoader()
        loader.testMethodPrefix = unittest_config.get('test_method_prefix',
                                                      'test')

        discover = unittest_config.get('discover_tests')
        if args.discover_dir:
            discover = {'start_dir': args.discover_dir}
        # TODO: ??? Add ability to run multiple discoveries in a single config
        if discover:
            g.log.debug('unittest - discover')
            start_dir = discover.get('start_dir', '.')
            pattern = discover.get('pattern', 'test_*')
            top_level_dir = discover.get('top_level_dir', None)
            discovered_tests = loader.discover(start_dir, pattern,
                                               top_level_dir)
            tsuite.addTests(discovered_tests)

        run_list = unittest_config.get('load_tests_from_list')
        # TODO: ability to load multiple lists
        # TODO: ??? list format more conducive to automation
        if run_list:
            g.log.debug('unittest - load_tests_from_list')
            unittest_config = g.config['unittest']
            unittest_list = g.config['unittest_list']
            module_name = unittest_list['module_name']
            test_list = unittest_list['list']

            test_module_obj = importlib.import_module(module_name)

            tests_to_run = loader.loadTestsFromNames(test_list,
                                                     test_module_obj)

            tsuite.addTests(tests_to_run)
            #result = unittest.TestResult()
            #suite.run(result)

        run_module = unittest_config.get('load_tests_from_module')
        if run_module:
            g.log.debug('unittest - load_tests_from_module')
            module_name = run_module.get('module_name')
            use_load_tests = run_module.get('use_load_tests', True)

            # TODO: is there a better way to do this without the dual import?
            __import__(module_name)
            class_list = inspect.getmembers(sys.modules[module_name],
                                            inspect.isclass)
            # TODO: is __import__ Python3.x friendly???
            test_module_obj = __import__(module_name,
                                         fromlist=class_list)
            tests_from_module = loader.loadTestsFromModule(test_module_obj,
                                                           use_load_tests)
            tsuite.addTests(tests_from_module)

        # Load tests from a name (string)
        # NOTE: does not use load_test()
        test_name = unittest_config.get('load_tests_from_name')
        if test_name:
            g.log.debug('unittest - load_tests_from_name')
            # TODO: can we collapse these loader instances into one at top???
            tests_from_name = loader.loadTestsFromName(test_name)
            tsuite.addTests(tests_from_name)

        # Load tests from a name (string)
        # NOTE: only uses load_test() when name is module level
        #        e.g., tests.test_glusto
        test_name_list = unittest_config.get('load_tests_from_names')
        if test_name_list:
            g.log.debug('unittest - load_tests_from_names')
            # TODO: can we collapse these loader instances into one at top???
            tests_from_names = loader.loadTestsFromNames(test_name_list)
            tsuite.addTests(tests_from_names)

        # TODO: Add a skip test option
        trunner.run(tsuite)

    g.log.info("Ending glusto via main()")
    print "Ending glusto via main()"


if __name__ == '__main__':
    main()

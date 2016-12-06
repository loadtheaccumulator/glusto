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
#from unittest import TestLoader, TestSuite, TextTestRunner
import unittest
import pytest
import nose
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

    # load user specified configs (can also override defaults)
    if (config_list):
        g.log.info("Loading user specified configuration files.")
        config_files = config_list.split()
        config = g.load_configs(config_files)
        g.update_config(config)


def main():
    """Entry point console script for setuptools.

    Provides a command-line interface to Glusto.

    Currently does nothing useful, but plan to wrap Glusto functionality in a
    CLI interface that can be injected into shell scripts, etc.

    Example:
        # glusto run hostname.example.com "uname -a"
    """
    epilog = ('NOTE: If encountering an "unknown option" issue '
              'with the -t and -n options, use param=\'args\' syntax.'
              '(e.g., -t="-v -x tests")')
    parser = argparse.ArgumentParser(description="Glusto CLI wrapper",
                                     epilog=epilog)
    parser.add_argument("-c", "--config",
                        help="Config file(s) to read.",
                        action="store", dest="config_list",
                        default=None)
    parser.add_argument("--ssh-keyfile",
                        help="SSH keyfile for connections.",
                        action="store", dest="ssh_keyfile")
    parser.add_argument("-l", "--log",
                        help="Default logfile location.",
                        action="store", dest="log_filename",
                        default=None)
    parser.add_argument("--log-level",
                        help="Default log level.",
                        action="store", dest="log_level",
                        default=None)
    parser.add_argument("--pytest",
                        help="Run tests using the pytest framework.",
                        action="store", dest="run_pytest")
    parser.add_argument("--nosetests",
                        help="Run tests using the nose framework.",
                        action="store", dest="run_nosetests")
    parser.add_argument("--unittest",
                        help="Run tests using the unittest framework.",
                        action="store", dest="run_unittest")
    parser.add_argument("-u",
                        help="Run unittests per provided config file.",
                        action="store_true", dest="run_unittest_config")
    parser.add_argument("-d", "--discover",
                        help="Discover unittests from directory.",
                        action="store", dest="discover_dir")
    args = parser.parse_args()

    # read config files and update g.config attributes
    handle_configs(args.config_list)

    # TODO: break everything into separate methods

    # handle actionable config items
    # logging
    # set defaults
    log_name = "glustomain"
    log_filename = "/tmp/glustomain.log"
    log_level = "INFO"
    # override with config
    log_filename = g.config.get('log_filename', log_filename)
    log_level = g.config.get('log_level', log_level)
    # override with CLI options
    if args.log_filename:
        log_filename = args.log_filename
    if args.log_level:
        log_level = args.log_level

    g.log = g.create_log(name=log_name, filename=log_filename,
                         level=log_level)
    print("Log %s created as %s with log level %s" % (log_name, log_filename,
                                                      log_level))

    g.log.info("Starting glusto via main()")
    print "Starting glusto via main()"

    # override ssh_keyfile @ CLI
    if args.ssh_keyfile:
        g.ssh_set_keyfile(args.ssh_keyfile)

    g.show_config(g.config)

    # unittest
    # TODO: functionalize this so it can be used for standalone test scripts
    if args.run_unittest_config or args.discover_dir:
        tsuite = unittest.TestSuite()
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
            trunner = unittest.TextTestRunner(verbosity=2)

        loader = unittest.TestLoader()
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

        # Load tests from names (list)
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

    PYTEST_FAIL = 1
    NOSETESTS_FAIL = 2
    UNITTEST_FAIL = 4

    retcode = 0
    if args.run_pytest:
        print "pytest: %s" % args.run_pytest
        result = pytest.main(args.run_pytest)
        if result > 0:
            retcode = retcode | PYTEST_FAIL

    if args.run_nosetests:
        print "nosetests: %s" % args.run_nosetests
        argv = args.run_nosetests.split(' ')
        argv.insert(0, 'glusto')
        result = nose.run(argv=argv)
        if not result:
            retcode = retcode | NOSETESTS_FAIL

    if args.run_unittest:
        print "unittest: %s" % args.run_unittest
        argv = args.run_unittest.split(' ')
        argv.insert(0, 'glusto')
        test_object = unittest.main(exit=False, argv=argv)

        num_errors = len(test_object.result.errors)
        num_failures = len(test_object.result.failures)
        if num_errors > 0 or num_failures > 0:
            retcode = retcode | UNITTEST_FAIL

    g.log.info("Ending glusto via main()")
    print "Ending glusto via main()"

    return retcode

if __name__ == '__main__':
    exitcode = main()

    sys.exit(exitcode)

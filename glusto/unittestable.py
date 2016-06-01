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
"""All things Jinja templates.

NOTE:
    Templatable is inherited by the Glusto class
    and not designed to be instantiated.
"""
import unittest
import sys


class Unittestable(object):
    """The class providing Jinja template functionality."""

    @staticmethod
    def load_tests(test_class, loader, ordered_testcases):
        '''Load tests in a specific order.
        unittest standard feature requires Python2.7
        '''
        module_name = test_class.__module__
        class_name = test_class.__name__
        prefix = "%s.%s" % (module_name, class_name)
        print "PREFIX: %s" % prefix

        suite = unittest.TestSuite()
        # Add tests that need to be run in a specific order
        for testcase_name in ordered_testcases:
            testcase_fullname = "%s.%s" % (prefix, testcase_name)
            loaded_test = loader.loadTestsFromName(testcase_fullname)
            suite.addTest(loaded_test)
        # Add the remaining tests
        test_list_all = loader.getTestCaseNames(test_class)
        testcases_remaining = []
        for test_name in test_list_all:
            if test_name not in ordered_testcases:
                full_test_name = "%s.%s" % (prefix, test_name)
                testcases_remaining.append(full_test_name)
        remaining_tests = loader.loadTestsFromNames(testcases_remaining)
        suite.addTest(remaining_tests)

        return suite

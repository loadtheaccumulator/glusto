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


class Unittestable(object):
    """The class providing Jinja template functionality."""

    @staticmethod
    def load_tests(loader, module_name, class_name, test_list_all,
                   testcases_ordered):
        suite = unittest.TestSuite()
        # Add tests that need to be run in a specific order
        tests = loader.loadTestsFromNames(testcases_ordered)
        suite.addTests(tests)

        # Add the remaining tests
        #test_list_all = loader.getTestCaseNames(class_name)
        testcases_remaining = []
        for test_name in test_list_all:
            full_test_name = "%s.%s.%s" % (module_name, class_name, test_name)
            if full_test_name not in testcases_ordered:
                testcases_remaining.append(full_test_name)
        remaining_tests = loader.loadTestsFromNames(testcases_remaining)
        suite.addTest(remaining_tests)

        return suite

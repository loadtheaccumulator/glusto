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
"""Test glusto basic functionality"""
import unittest

from glusto.core import Glusto as g


class TestGlustoColorfy(unittest.TestCase):
    """Glusto basics test class"""
    @classmethod
    def setUpClass(cls):
        """unittest standard setUpClass method
        Runs before all test_ methods in the class
        """
        print "Setting Up Class: %s" % cls.__name__

        cls.non_color_message = 'this is a test'
        cls.color_message = '\x1b[43;31;1mthis is a test\x1b[0m'

    def setUp(self):
        """unittest standard setUp method
        Runs before each test_ method
        """
        print "Setting Up: %s" % self.id()

    def test_log_color_true(self):
        g.config['log_color'] = True

        message = g.colorfy(g.RED | g.BG_YELLOW | g.BOLD,
                            self.non_color_message)

        self.assertEqual(message, self.color_message,
                         "color message does not match expectation")

    def test_log_color_false(self):
        g.config['log_color'] = False

        message = g.colorfy(g.RED, self.non_color_message)

        self.assertEqual(message, self.non_color_message,
                         "non color message does not match expectation")

    def tearDown(self):
        """Unittest tearDown override"""
        print "Tearing Down: %s" % self.id()

    @classmethod
    def tearDownClass(cls):
        """unittest tearDownClass override"""
        print "Tearing Down Class: %s" % cls.__name__

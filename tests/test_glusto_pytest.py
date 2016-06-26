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
import pytest

from glusto.core import Glusto as g


class TestGlustoBasicsPyTest(unittest.TestCase):
    """Glusto basics test class"""
    @classmethod
    def setUpClass(cls):
        """unittest standard setUpClass method
        Runs before all test_ methods in the class
        """
        print "Setting Up Class: %s" % cls.__name__

    def setUp(self):
        """unittest standard setUp method
        Runs before each test_ method
        """
        print "Setting Up: %s" % self.id()
        config = g.load_configs(["../examples/systems.yml",
                                 "../examples/glusto.yml"])
        g.update_config(config)

        self.masternode = g.config["nodes"][0]
        self.client = g.config["clients"][0]

    @pytest.mark.response
    def test_stderr(self):
        """Testing output to stderr"""
        print "Running: %s - %s" % (self.id(), self.shortDescription())
        rcode, rout, rerr = g.run(self.masternode, "uname -a >&2")
        self.assertEqual(rcode, 0)
        self.assertFalse(rout)
        self.assertTrue(rerr)

    @pytest.mark.response
    def test_stdout(self):
        """Testing output to stdout"""
        print "Running: %s - %s" % (self.id(), self.shortDescription())
        # add a cleanup method to run after tearDown()
        self.addCleanup(self.cleanup_remote_commands)
        for node in g.config["nodes"]:
            rcode, rout, rerr = g.run(node, "ls -ld /etc")
        self.assertEqual(rcode, 0)
        self.assertTrue(rout)
        self.assertFalse(rerr)

    def cleanup_remote_commands(self):
        """Cleanup remote commands method
        Called after teardown for additional cleanup specific to this test
        """
        print "Cleaning up after setup on fail or after teardown"

    @pytest.mark.response
    def test_return_code(self):
        """Testing the return code"""
        print "Running: %s - %s" % (self.id(), self.shortDescription())
        rcode, rout, rerr = g.run(self.masternode, "cat /etc/fstab")
        self.assertEqual(rcode, 0)
        self.assertTrue(rout)
        self.assertFalse(rerr)

    @pytest.mark.skip(reason="Example test skip")
    def test_skip_me(self):
        """Testing the unittest skip feature"""
        print "Running: %s - %s" % (self.id(), self.shortDescription())
        rcode, _, _ = g.run(self.masternode, "cat /etc/hosts")
        self.assertEqual(rcode, 0)

    def test_negative_test(self):
        """Testing an expected failure as negative test"""
        print "Running: %s - %s" % (self.id(), self.shortDescription())
        rcode, _, _ = g.run(self.masternode, "false")
        self.assertEqual(rcode, 1)

    @unittest.expectedFailure
    def test_expected_fail(self):
        """Testing an expected failure. This test should fail"""
        print "Running: %s - %s" % (self.id(), self.shortDescription())
        rcode, _, _ = g.run(self.masternode, "false")
        self.assertEqual(rcode, 0)

    def tearDown(self):
        """Unittest tearDown override"""
        print "Tearing Down: %s" % self.id()

        return True

    @classmethod
    def tearDownClass(cls):
        """unittest tearDownClass override"""
        print "Tearing Down Class: %s" % cls.__name__


def load_tests(loader, standard_tests, pattern):
    '''Load tests in a specific order.
    unittest standard feature requires Python2.7
    '''
    # TODO: make this configurable!!!
    testcases_ordered = ['test_return_code',
                         'test_stdout',
                         'test_stderr']

    suite = g.load_tests(TestGlustoBasicsPyTest, loader, testcases_ordered)

    return suite

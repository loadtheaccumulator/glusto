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
"""Test glusto rpyc functionality"""
import os
import unittest

from glusto.core import Glusto as g


class TestGlustoRpyc(unittest.TestCase):
    """Glusto rpyc test class"""
    @classmethod
    def setUpClass(cls):
        """unittest standard setUpClass method
        Runs before all test_ methods in the class
        """
        print("Setting Up Class: %s" % cls.__name__)
        cls.script_dir = os.path.dirname(os.path.realpath(__file__))
        config = g.load_config('%s/supporting_files/remote_tests/systems.yml'
                               % cls.script_dir)
        g.update_config(config)

    def setUp(self):
        """unittest standard setUp method
        Runs before each test_ method
        """
        print("Setting Up: %s" % self.id())

        self.masternode = g.config["nodes"][0]
        self.client = g.config["clients"][0]
        g.log.info('masternode: %s ' % self.masternode)
        g.log.info('ssh keyfile: %s' % g.config['ssh_keyfile'])

    def test_connection(self):
        """Testing rpyc connection"""
        print("Running: %s - %s" % (self.id(), self.shortDescription()))

        g.rpyc_get_connection(self.masternode)
        pingable = g.rpyc_ping_connection(self.masternode)

        self.assertTrue(pingable, "Connection did not ping.")

    def test_local_module_on_remote(self):
        """Testing local module definition on remote system"""
        connection = g.rpyc_get_connection(self.masternode)
        import tests_functional.supporting_files.rpyc.local_module
        r = g.rpyc_define_module(connection,
                                 tests_functional.supporting_files.rpyc.local_module)

        # test global variable
        self.assertEqual(r.myvariable, 'yada yada yada')

        # test class attribute
        self.assertEqual(r.myclass.myclassattribute, 'yada yada yada')

        # test static method
        output = r.myclass.static_method()
        self.assertIn('static:', output)

        # test class method
        output = r.myclass.class_method()
        self.assertIn('class:', output)

        # test instance method
        x = r.myclass()
        output = x.instance_method()
        self.assertIn('instance:', output)

    def test_remote_call(self):

        rpyc_conn = g.rpyc_get_connection(self.masternode)
        platform = rpyc_conn.modules.sys.platform

        self.assertEqual(platform, 'linux')

    def tearDown(self):
        """Unittest tearDown override"""
        print("Tearing Down: %s" % self.id())

        return True

    @classmethod
    def tearDownClass(cls):
        """unittest tearDownClass override"""
        print("Tearing Down Class: %s" % cls.__name__)

        # rpyc should do this on script exit, but for cleanliness sake...
        g.rpyc_close_deployed_servers()

# Copyright 2019 Jonathan Holloway <loadtheaccumulator@gmail.com>
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
"""Test glusto logging functionality"""
import unittest
import pytest

from glusto.core import Glusto as g


class TestGlustoLogging(unittest.TestCase):
    """Glusto basics test class"""
    @classmethod
    def setUpClass(cls):
        """unittest standard setUpClass method
        Runs before all test_ methods in the class
        """
        print "Setting Up Class: %s" % cls.__name__

        # TODO: replace this with parms in tox.ini
        config = g.load_configs(["examples/systems.yml",
                                 "examples/glusto.yml"])
        g.update_config(config)

        cls.unicode_string = u'abcdefghi\xe2ihgfedcba'

        cls.masternode = g.config["nodes"][0]
        cls.tmp_unicode_file = '/tmp/glusto_unicode.txt'
        cls.tmp_local_unicode_file = ('tests/supporting_files/'
                                      'unicode/unicode.txt')

        g.run(cls.masternode, 'rm %s' % cls.tmp_unicode_file)
        g.upload(cls.masternode, cls.tmp_local_unicode_file,
                 cls.tmp_unicode_file)
        #g.run(cls.masternode, u'printf "123456789\xe2987654321" > %s' %
        #      cls.tmp_unicode_file)

    def setUp(self):
        """unittest standard setUp method
        Runs before each test_ method
        """
        print "Setting Up: %s" % self.id()

    # @pytest.mark.skip
    def test_connectible_forced_coloroff(self):
        """Testing logging run_local()"""
        print "Running: %s - %s" % (self.id(), self.shortDescription())
        g.config['log_color'] = False
        g._log_results("FORCED COLOR OFF", 0,
                       self.unicode_string, self.unicode_string)

    # @pytest.mark.skip
    def test_connectible_forced_coloron(self):
        """Testing logging run_local()"""
        print "Running: %s - %s" % (self.id(), self.shortDescription())
        g.config['log_color'] = True
        g._log_results("FORCED COLOR ON", 0,
                       self.unicode_string, self.unicode_string)

    # @pytest.mark.skip
    def test_local(self):
        """Testing logging run_local()"""
        print "Running: %s - %s" % (self.id(), self.shortDescription())
        g.config['log_color'] = True
        rcode, rout, rerr = g.run_local("cat %s" % self.tmp_local_unicode_file)
        self.assertEqual(rcode, 0)
        #g.log.info(u"ENCODED: %s".encode('utf8') % rout)
        #g.log.log(0, "ENCODED: %s".encode('utf8') % rout)

    # @pytest.mark.skip
    def test_remote_unicode_coloroff(self):
        """Testing logging unicode w/ color off"""
        print "Running: %s - %s" % (self.id(), self.shortDescription())
        g.config['log_color'] = False
        rcode, rout, rerr = g.run(self.masternode, "cat %s" %
                                  self.tmp_unicode_file)
        self.assertEqual(rcode, 0)
        g.log.info(rout)
        g.log.log(0, rout)

    # @pytest.mark.skip
    def test_remote_unicode_coloron(self):
        """Testing logging unicode w/ color on"""
        print "Running: %s - %s" % (self.id(), self.shortDescription())
        g.config['log_color'] = True
        rcode, rout, rerr = g.run(self.masternode, "cat %s" %
                                  self.tmp_unicode_file)
        self.assertEqual(rcode, 0)
        g.log.info(rout)
        g.log.log(0, rout)

    def tearDown(self):
        """Unittest tearDown override"""
        print "Tearing Down: %s" % self.id()

    @classmethod
    def tearDownClass(cls):
        """unittest tearDownClass override"""
        print "Tearing Down Class: %s" % cls.__name__

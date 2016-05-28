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
"""Test glusto config functionality"""
import unittest
import xmlrunner

import os

from glusto.core import Glusto as g


class TestGlustoConfigs(unittest.TestCase):
    """Glusto basics test class"""
    @classmethod
    def setUpClass(cls):
        """unittest standard setUpClass method
        Runs before all test_ methods in the class
        """
        print "Setting Up Class: %s" % cls.__name__
        # Setting class attributes for use across all test methods
        cls.yaml_file = '/tmp/testconfig.yml'
        cls.ini_file = '/tmp/testconfig.ini'
        cls.ini_ordered_file = '/tmp/testconfig_ordered.ini'

        cls.config = {}
        cls.config['defaults'] = {}
        cls.config['defaults']['this'] = 'yada1'
        cls.config['defaults']['that'] = 'yada2'
        cls.config['globals'] = {}
        cls.config['globals']['the_other'] = 'yada3'
        # to test ini substitution
        cls.config['defaults']['this_and_that'] = '%(this)s and %(that)s'

        g.show_config(cls.config)

        cls.order = ['defaults', 'globals']

        # cleanup files if they exist
        '''
        if os.path.exists(cls.yaml_file):
            os.unlink(cls.yaml_file)
        if os.path.exists(cls.ini_file):
            os.unlink(cls.ini_file)
        '''

    def setUp(self):
        """unittest standard setUp method
        Runs before each test_ method
        """
        print "Setting Up: %s" % self.id()

    def test_yaml(self):
        """Testing yaml config file"""
        print "Running: %s - %s" % (self.id(), self.shortDescription())

        # write the config file
        g.store_config(self.config, self.yaml_file)
        # TODO: does unittest have a file exists assert?
        self.assertTrue(os.path.exists(self.yaml_file))

        # read the config file
        config = g.load_config(self.yaml_file)
        g.show_config(config)
        self.assertEqual(config['defaults']['this'], 'yada1')
        self.assertEqual(config['defaults']['that'], 'yada2')
        self.assertEqual(config['globals']['the_other'], 'yada3')

    def test_ini(self):
        """Testing ini config file(s)"""
        print "Running: %s - %s" % (self.id(), self.shortDescription())

        g.store_config(self.config, self.ini_file)
        self.assertTrue(os.path.exists(self.ini_file))

        # read the config file
        config = g.load_config(self.ini_file)
        g.show_config(config)
        self.assertEqual(config['defaults']['this'], 'yada1')
        self.assertEqual(config['defaults']['that'], 'yada2')
        self.assertEqual(config['defaults']['this_and_that'],
                         'yada1 and yada2')
        self.assertEqual(config['globals']['the_other'], 'yada3')

    def test_ini_ordered(self):
        """Testing ordered ini config file(s)"""
        print "Running: %s - %s" % (self.id(), self.shortDescription())

        # ordered ini
        g.store_config(self.config, self.ini_ordered_file, order=self.order)
        self.assertTrue(os.path.exists(self.ini_ordered_file))

        # read the config file
        config = g.load_config(self.ini_ordered_file)
        g.show_config(config)
        self.assertEqual(config['defaults']['this'], 'yada1')
        self.assertEqual(config['defaults']['that'], 'yada2')
        self.assertEqual(config['defaults']['this_and_that'],
                         'yada1 and yada2')
        self.assertEqual(config['globals']['the_other'], 'yada3')

    def tearDown(self):
        """Unittest tearDown override"""
        print "Tearing Down: %s" % self.id()

        return True

    @classmethod
    def tearDownClass(cls):
        """unittest tearDownClass override"""
        print "Tearing Down Class: %s" % cls.__name__

        if os.path.exists(cls.yaml_file):
            os.unlink(cls.yaml_file)
        if os.path.exists(cls.ini_file):
            os.unlink(cls.ini_file)
        if os.path.exists(cls.ini_ordered_file):
            os.unlink(cls.ini_ordered_file)

if __name__ == '__main__':
    # TODO: make this argable
    output_junit = False
    # unittest.main(verbosity=2)
    tsuite = unittest.TestLoader().loadTestsFromTestCase(TestGlustoConfigs)
    if output_junit:
        trunner = xmlrunner.XMLTestRunner(output='/tmp/glustoreports')
    else:
        trunner = unittest.TextTestRunner(verbosity=2)
    trunner.run(tsuite)
    #results.testsRun

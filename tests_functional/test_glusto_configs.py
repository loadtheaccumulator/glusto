# Copyright 2016-2018 Jonathan Holloway <loadtheaccumulator@gmail.com>
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
from collections import OrderedDict

from glusto.core import Glusto as g


class TestGlustoConfigs(unittest.TestCase):
    """Glusto basics test class"""

    @classmethod
    def setUpClass(cls):
        """unittest standard setUpClass method
        Runs before all test methods in the class
        """
        print("Setting Up Class: %s" % cls.__name__)
        # Setting class attributes for use across all test methods
        cls.yaml_file = '/tmp/testconfig.yml'
        cls.json_file = '/tmp/testconfig.json'
        cls.ini_file = '/tmp/testconfig.ini'
        cls.ini_novalue_file = '/tmp/testconfig_novalue.ini'
        cls.ini_ordered_file = '/tmp/testconfig_ordered.ini'

        cls.yaml_noext = '/tmp/testyaml'
        cls.json_noext = '/tmp/testjson'
        cls.ini_noext = '/tmp/testini'

        cls.config = {}
        cls.config['defaults'] = {}
        cls.config['defaults']['this'] = 'yada1'
        cls.config['defaults']['that'] = 'yada2'
        cls.config['globals'] = {}
        cls.config['globals']['the_other'] = 'yada3'
        # to test ini substitution
        cls.config['defaults']['this_and_that'] = '%(this)s and %(that)s'

        g.show_config(cls.config)

        cls.config_novalue = {}
        cls.config_novalue['defaults'] = ['this', 'that']
        cls.config_novalue['globals'] = ['the_other', 'and_one_more_thing']

        g.show_config(cls.config_novalue)

        cls.ordered_config = OrderedDict()
        cls.ordered_config['defaults'] = OrderedDict()
        cls.ordered_config['defaults']['this'] = 'yada1'
        cls.ordered_config['defaults']['that'] = 'yada2'
        cls.ordered_config['globals'] = OrderedDict()
        cls.ordered_config['globals']['the_other'] = 'yada3'
        # to test ini substitution
        cls.ordered_config['defaults']['this_and_that'] = \
            '%(this)s and %(that)s'

        g.show_config(cls.ordered_config)

        # cleanup files if they exist
        '''
        if os.path.exists(cls.yaml_file):
            os.unlink(cls.yaml_file)
        if os.path.exists(cls.ini_file):
            os.unlink(cls.ini_file)
        '''

    def setUp(self):
        """unittest standard setUp method
        Runs before each test method
        """
        print("Setting Up: %s" % self.id())

    def test_yaml(self):
        """Testing yaml config file"""
        print("Running: %s - %s" % (self.id(), self.shortDescription()))

        g.show_config(self.config)

        # write the config file
        g.store_config(self.config, self.yaml_file)
        self.assertTrue(os.path.exists(self.yaml_file))

        # read the config file
        config = g.load_config(self.yaml_file)
        g.show_config(config)
        self.assertEqual(config['defaults']['this'], 'yada1')
        self.assertEqual(config['defaults']['that'], 'yada2')
        self.assertEqual(config['globals']['the_other'], 'yada3')

    def test_yaml_noext(self):
        """Testing yaml config file without extension"""
        print("Running: %s - %s" % (self.id(), self.shortDescription()))

        g.show_config(self.config)

        # write the config files
        g.store_config(self.config, self.yaml_file)
        self.assertTrue(os.path.exists(self.yaml_file))
        g.store_config(self.config, self.yaml_noext, config_type='yaml')
        self.assertTrue(os.path.exists(self.yaml_noext))

        print("--------------")
        g.show_file(self.yaml_file)
        print("--------------")
        g.show_file(self.yaml_noext)
        print("--------------")

        # read the config file
        config = g.load_config(self.yaml_file)
        g.show_config(config)
        self.assertEqual(config['defaults']['this'], 'yada1')
        self.assertEqual(config['defaults']['that'], 'yada2')
        self.assertEqual(config['globals']['the_other'], 'yada3')

        config_noext = g.load_config(self.yaml_noext, config_type='yaml')
        g.show_config(config_noext)
        self.assertEqual(config_noext['defaults']['this'], 'yada1')
        self.assertEqual(config_noext['defaults']['that'], 'yada2')
        self.assertEqual(config_noext['globals']['the_other'], 'yada3')

        self.assertEqual(config, config_noext, 'config files are not the same')

    def test_json(self):
        """Testing json config file"""
        print("Running: %s - %s" % (self.id(), self.shortDescription()))

        g.show_config(self.config)

        # write the config file
        g.store_config(self.config, self.json_file)
        self.assertTrue(os.path.exists(self.json_file))

        # read the config file
        config = g.load_config(self.json_file)
        g.show_config(config)
        self.assertEqual(config['defaults']['this'], 'yada1')
        self.assertEqual(config['defaults']['that'], 'yada2')
        self.assertEqual(config['globals']['the_other'], 'yada3')

    def test_json_noext(self):
        """Testing json config file without extension"""
        print("Running: %s - %s" % (self.id(), self.shortDescription()))

        g.show_config(self.config)

        # write the config files
        g.store_config(self.config, self.json_file)
        self.assertTrue(os.path.exists(self.json_file))
        g.store_config(self.config, self.json_noext, config_type='json')
        self.assertTrue(os.path.exists(self.json_noext))

        print("--------------")
        g.show_file(self.json_file)
        print("--------------")
        g.show_file(self.json_noext)
        print("--------------")

        # read the config file
        config = g.load_config(self.json_file)
        g.show_config(config)
        self.assertEqual(config['defaults']['this'], 'yada1')
        self.assertEqual(config['defaults']['that'], 'yada2')
        self.assertEqual(config['globals']['the_other'], 'yada3')

        config_noext = g.load_config(self.json_noext, config_type='json')
        g.show_config(config_noext)
        self.assertEqual(config_noext['defaults']['this'], 'yada1')
        self.assertEqual(config_noext['defaults']['that'], 'yada2')
        self.assertEqual(config_noext['globals']['the_other'], 'yada3')

        self.assertEqual(config, config_noext, 'config files are not the same')

    def test_ini(self):
        """Testing ini config file(s)"""
        print("Running: %s - %s" % (self.id(), self.shortDescription()))

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

    def test_ini_novalue(self):
        """Testing ini config file(s) without values"""
        print("Running: %s - %s" % (self.id(), self.shortDescription()))

        g.store_config(self.config_novalue, self.ini_novalue_file)
        self.assertTrue(os.path.exists(self.ini_novalue_file))

        print("--------------")
        g.show_file(self.ini_novalue_file)
        print("--------------")

        # read the config file
        config = g.load_config(self.ini_novalue_file)
        g.show_config(config)
        self.assertEqual(config['defaults'].get('this'), '')
        self.assertEqual(config['defaults'].get('that'), '')
        self.assertEqual(config['globals'].get('and_one_more_thing'), '')
        self.assertEqual(config['globals'].get('the_other'), '')

    def test_ini_noext(self):
        """Testing ini config file(s) without extension"""
        print("Running: %s - %s" % (self.id(), self.shortDescription()))

        g.store_config(self.config, self.ini_file)
        self.assertTrue(os.path.exists(self.ini_file))
        g.store_config(self.config, self.ini_noext, config_type='ini')
        self.assertTrue(os.path.exists(self.ini_noext))

        print("--------------")
        g.show_file(self.ini_file)
        print("--------------")
        g.show_file(self.ini_noext)
        print("--------------")

        # read the config file
        config = g.load_config(self.ini_file)
        g.show_config(config)
        self.assertEqual(config['defaults']['this'], 'yada1')
        self.assertEqual(config['defaults']['that'], 'yada2')
        self.assertEqual(config['defaults']['this_and_that'],
                         'yada1 and yada2')
        self.assertEqual(config['globals']['the_other'], 'yada3')

        config_noext = g.load_config(self.ini_file, config_type='ini')
        g.show_config(config_noext)
        self.assertEqual(config_noext['defaults']['this'], 'yada1')
        self.assertEqual(config_noext['defaults']['that'], 'yada2')
        self.assertEqual(config_noext['defaults']['this_and_that'],
                         'yada1 and yada2')
        self.assertEqual(config_noext['globals']['the_other'], 'yada3')

        self.assertEqual(config, config_noext, 'config files are not the same')

    def test_ini_ordered(self):
        """Testing ordered ini config file(s)"""
        print("Running: %s - %s" % (self.id(), self.shortDescription()))

        g.show_config(self.ordered_config)
        # ordered ini
        g.store_config(self.ordered_config, self.ini_ordered_file)
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
        print("Tearing Down: %s" % self.id())

        return True

    @classmethod
    def tearDownClass(cls):
        """unittest tearDownClass override"""
        print("Tearing Down Class: %s" % cls.__name__)

        if os.path.exists(cls.yaml_file):
            os.unlink(cls.yaml_file)
        if os.path.exists(cls.json_file):
            os.unlink(cls.json_file)
        if os.path.exists(cls.ini_file):
            os.unlink(cls.ini_file)
        if os.path.exists(cls.ini_ordered_file):
            os.unlink(cls.ini_ordered_file)

        if os.path.exists(cls.yaml_noext):
            os.unlink(cls.yaml_noext)
        if os.path.exists(cls.json_noext):
            os.unlink(cls.json_noext)
        if os.path.exists(cls.ini_noext):
            os.unlink(cls.ini_noext)


if __name__ == '__main__':
    output_junit = False
    tsuite = unittest.TestLoader().loadTestsFromTestCase(TestGlustoConfigs)
    if output_junit:
        trunner = xmlrunner.XMLTestRunner(output='/tmp/glustoreports')
    else:
        trunner = unittest.TextTestRunner(verbosity=2)
    trunner.run(tsuite)

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
"""Test glusto template functionality"""
import unittest
import os

from glusto.core import Glusto as g


class TestGlustoTemplates(unittest.TestCase):
    """Glusto basics test class"""
    @classmethod
    def setUpClass(cls):
        """unittest standard setUpClass method
        Runs before all test_ methods in the class
        """
        print "Setting Up Class: %s" % cls.__name__

        # Setting class attributes for use across all test methods
        cls.config_file = ('supporting_files/templates/'
                           'glusto_templates-vars.yml')
        config = g.load_config(cls.config_file)
        g.show_config(config)
        if config:
            g.update_config(config)

        cls.template_vars = g.config['templates']
        cls.template_file = ('templates/'
                             'glusto_templates-template.jinja')
        cls.search_path = 'supporting_files'
        cls.output_file = '/tmp/glusto_templates-output.yml'

    def setUp(self):
        """unittest standard setUp method
        Runs before each test_ method
        """
        print "Setting Up: %s" % self.id()
        # render the template
        g.render_template(self.template_file,
                          self.template_vars,
                          self.output_file,
                          self.search_path)

        # read the resulting config file built from template
        self.output_config = g.load_config(self.output_file)
        g.show_config(self.output_config)

    def test_template_include(self):
        """Testing template include"""
        # TODO: consider reading firstline from the original file
        firstline = ("# Copyright 2016 Jonathan Holloway "
                     "<loadtheaccumulator@gmail.com>")
        outfh = open(self.output_file, 'r')
        out_firstline = outfh.readline().strip()

        self.assertEqual(firstline, out_firstline,
                         'first lines do not match')

    def test_template_scalar(self):
        """Testing template scalar"""
        print "Running: %s - %s" % (self.id(), self.shortDescription())
        # compare plain scalars
        self.assertEqual(g.config['templates']['plain_scalar'],
                         self.output_config['out_templates']['plain_scalar'],
                         'plain scalars do not match')

    def test_template_forloop(self):
        """Testing template for loop"""
        print "Running: %s - %s" % (self.id(), self.shortDescription())
        # compare sequence items
        for i in range(0, 3):
            input_item = g.config['templates']['sequence'][i]
            output_item = self.output_config['out_templates']['sequence'][i]

            self.assertEqual(input_item, output_item,
                             'sequence items (%i) do not match' % i)

    def tearDown(self):
        """Unittest tearDown override"""
        print "Tearing Down: %s" % self.id()

        # removing output file
        os.unlink(self.output_file)

        return True

    @classmethod
    def tearDownClass(cls):
        """unittest tearDownClass override"""
        print "Tearing Down Class: %s" % cls.__name__

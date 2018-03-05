# Copyright 2018 Jonathan Holloway <loadtheaccumulator@gmail.com>
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
import os
import unittest

from glusto.core import Glusto as g


class shoots_with(g.CarteTestClass):
    """Decorator providing carteplex definition for carteplex functionality"""

    def __init__(self, value):
        axis_names = ['camera', 'lens', 'filter']

        available_options = [['nikon', 'olympus', 'fuji'],
                             ['20mm', '35mm', '50mm', '85mm'],
                             ['polarizer', 'uv', 'haze', 'closeup', 'none']]

        self.axis_names = g.config.get('axis_names', axis_names)

        self.available_options = g.config.get('available_options',
                                              available_options)

        shoots_with_camera = g.config.get('shooting_with_camera',
                                          self.available_options[0])
        shoots_with_lens = g.config.get('shooting_with_lens',
                                        self.available_options[1])
        shoots_with_filter = self.available_options[2]

        self.selections = [shoots_with_camera, shoots_with_lens,
                           shoots_with_filter]
        self.limits = g.config.get('limits', value)


class GlustoBaseClass(unittest.TestCase):

    camera = None
    lens = None
    filter = None

    @classmethod
    def setUpClass(cls):
        print("setUpClass BASE: %s" % cls.__name__)
        print("**IN SUPER Class name**: ", cls.__name__)
        print("***IN SUPER Class mro**: ", cls.__mro__)
        print("***IN SUPER Class bases**: ", cls.__bases__)
        print("***IN SUPER Class super**: ", cls.__mro__[1])

        if not cls.camera:
            cls.camera = "nikon"
        if not cls.lens:
            cls.lens = "50mm"
        if not cls.filter:
            cls.filter = "none"

        cls.script_dir = os.path.dirname(os.path.realpath(__file__))
        cls.config = g.load_config('%s/supporting_files/carteplex/'
                                   'glusto_tests_base.yml' % cls.script_dir)
        cls.combinations = cls.config['combinations']
        print("CLASS SCRIPT DIR: %s" % cls.script_dir)
        print("CLASS (BASE) CONFIG:\n%s" % cls.config)
        print("SETUPCLASS GLUSTO (BASE): %s with %s with %s" % (cls.camera,
                                                                cls.lens,
                                                                cls.filter))

    @classmethod
    def get_combo(cls):
        """Return the carteplex combination"""
        return('%s_%s_%s' % (cls.camera, cls.lens, cls.filter))

    def setUp(self):
        """Setting this up"""
        print("\tsetUp BASE: %s - %s" % (self.id(), self.shortDescription()))
        print("SETUP GLUSTO (BASE): %s with %s with %s" % (self.camera,
                                                           self.lens,
                                                           self.filter))

    def tearDown(self):
        print("\ttearDown BASE: %s - %s" %
              (self.id(), self.shortDescription()))
        print("TEARDOWN GLUSTO (BASE): %s with %s with %s" % (self.camera,
                                                              self.lens,
                                                              self.filter))

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass BASE: %s" % cls.__name__)
        print("TEARDOWNCLASS GLUSTO (BASE): %s with %s with %s" % (cls.camera,
                                                                   cls.lens,
                                                                   cls.filter))

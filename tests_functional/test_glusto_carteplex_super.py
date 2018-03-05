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
"""Test im_func with the carteplex class clones.
   Run with:
    glusto --pytest='-vv tests/test_glusto_carteplex_super.py --capture=no'
"""
from tests_functional.glusto_base_class import GlustoBaseClass
from tests_functional.glusto_base_class import shoots_with

import pytest


@shoots_with([['olympus', 'fuji'],
              ['35mm', '85mm'],
              ['none', 'polarizer']])
class MyGlustoTest(GlustoBaseClass):

    @classmethod
    def setUpClass(cls):
        print("Shoots with %s camera and %s lens and %s filter" % (cls.camera,
                                                                   cls.lens,
                                                                   cls.filter))
        super().setUpClass()
        print("**Class name**: ", cls.__name__)
        print("***Class mro**: ", cls.__mro__)
        print("***Class bases**: ", cls.__bases__)
        print("***Class super**: ", cls.__mro__[1])
        print("Class Config:")
        print(cls.config)

    def setUp(self):
        """Setting this up"""
        print("\tsetUp: %s - %s" % (self.id(), self.shortDescription()))
        super().setUp()
        '''
        print("**Class name**: ", self.__name__)
        print("***Class mro**: ", self.__mro__)
        print("***Class bases**: ", self.__bases__)
        print("***Class super**: ", self.__mro__[1])
        print("**Class name**: ", type(self).__name__)
        '''
        print("\tCamera: %s, Lens: %s, Filter: %s" % (self.camera, self.lens,
                                                      self.filter))
        self.combo = '%s_%s_%s' % (self.camera, self.lens, self.filter)

    @pytest.mark.test1
    def test_glusto1(self):
        """Test 1"""
        print("\t\tRunning: %s - %s" % (self.id(), self.shortDescription()))
        print("\t\t%s with %s lens through %s filter" %
              (self.camera, self.lens, self.filter))
        # combo = '%s_%s_%s' % (self.camera, self.lens, self.filter)
        class_combo = super().get_combo()
        print(class_combo)
        self.assertEqual(self.combo, class_combo)

    @pytest.mark.test2
    def test_glusto2(self):
        """Test 2"""
        print("\t\tRunning: %s - %s" % (self.id(), self.shortDescription()))
        print("\t\t%s with %s lens through %s filter" %
              (self.camera, self.lens, self.filter))
        self.assertTrue(self.combo in self.combinations,
                        'combo %s is not in combinations list' % self.combo)

    @pytest.mark.skip
    def test_glusto3(self):
        """Test 3"""
        print("\t\tRunning: %s - %s" % (self.id(), self.shortDescription()))
        print("\t\t%s with %s lens through %s filter" %
              (self.camera, self.lens, self.filter))

    # def tearDown(self):
    #    print("\ttearDown: %s - %s" % (self.id(), self.shortDescription()))
    #    GlustoBaseClass.tearDown.im_func(self)

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass: %s" % cls.__name__)
        super().tearDownClass()
        print("**Class name**: ", cls.__name__)
        print("***Class mro**: ", cls.__mro__)
        print("***Class bases**: ", cls.__bases__)
        print("***Class super**: ", cls.__mro__[1])
        print("OVER AND OUT")

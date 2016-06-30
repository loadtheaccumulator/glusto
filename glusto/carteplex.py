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
"""Cartesian product decorator class for on-the-fly creation of testcases
based on a matrix of lists.

- Handles automatic generation of cartesian product combinations based on any
    number of lists.

- Provides an 'ALL' default to populate a var with a predefined full list.

- Compares variables passed in decorator to a list of configuration options
    (e.g., specify what underlying configuration is available to the test
    via config file and specify the configurations the test is limited to...
    Glusto will only create the possible combinations based on the
    intersection).

- Passes "axis names" into test class as class attributes to make them
    available to test methods.

- Provided via the Glusto import "from glusto.core import Glusto as g"

To use,
1) Subclass CarteTestClass,
2) Override __init__ to define variables,
3) Import your subclass and add a decorator of the same name to your tests.

Carteplex is "Cartesian Multiplexing". And that's simplified from the original
Carteprodplexorator (Cartesian Product Multiplexing Decorator).

See docs for more information and use-case examples.
"""
import unittest
import sys
import itertools
import sets


class CarteTestClass(object):
    """Decorator providing cartesian product parameter-like capability
    for unittest class"""

    def __init__(self, value):
        """Override to provide data specific to your tests.

        Args:
            value (object): data automatically provided by the decorator.
        """
        self.axis_names = ['cartesian', 'product']

        self.available_options = [['A', 'B', 'C', 'D', 'E'],
                                  ['one', 'two', 'three', 'four']]

        self.selections = [['A', 'C', 'E'], ['two', 'four']]
        self.limits = value

    def __call__(self, obj):
        """The engine behind the cartesian product multiplexing (carteplex)
        goodness. Do not override.

        Args:
            obj (object): object automatically passed by the decorator.

        Returns:
            An empty object. (removes original testclass from run)
        """
        # populate with available_options where selection is ALL
        for i in range(0, len(self.selections)):
            if self.selections[i] == 'ALL':
                self.selections[i] = self.available_options[i]
            if self.limits[i] == 'ALL':
                self.limits[i] = self.available_options[i]

        intersect_set = []
        for i in range(0, len(self.selections)):
            selection_set = sets.Set(self.selections[i])
            intersect_set.append(selection_set.intersection(self.limits[i]))

        self.iterables = list(intersect_set)

        print "module name: %s" % __name__
        print "object name: %s" % obj.__name__
        print "object module name: %s" % obj.__module__

        for t in itertools.product(*self.iterables):
            print t

            suffix = '_'.join(t)

            class_name = "%s_%s" % (obj.__name__, suffix)
            print "class_name: %s" % class_name

            new_class = type(class_name, (obj,), {})
            # loop through lists and assign attributes to objects
            for i in range(0, len(t)):
                print "%s: %s" % (self.axis_names[i], t[i])
                setattr(new_class, self.axis_names[i], t[i])
            class_module = sys.modules[obj.__module__]
            setattr(class_module, class_name, new_class)

        # pytest catches the original test class, so squelch it before loader
        obj = ''

        loader = unittest.TestLoader()
        generated_suite = \
            loader.loadTestsFromModule(class_module, True)

        def load_tests(loader, standard_tests, pattern):
            print "LOAD TESTS"

            return generated_suite

        class_module.load_tests = load_tests

        return obj

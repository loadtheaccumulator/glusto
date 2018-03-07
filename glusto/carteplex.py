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
# pylint: disable=too-few-public-methods
import sys
import itertools
import sets


class Carteplex(object):
    """Main class for cartesian product classes"""

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

            # rebuild axis_names with none None list
            updated_axis_names = []
            for i in range(0, len(self.limits)):
                if self.limits[i]:
                    updated_axis_names.append(self.axis_names[i])

            print "\n\n\n\n"
            print "available_options:"
            print self.available_options
            print "selections:"
            print self.selections
            print "limits:"
            print self.limits
            print "axis names:"
            print self.axis_names
            print "updated axis_names:"
            print updated_axis_names

            intersect_set = []
            for i in range(0, len(self.selections)):
                print 'self.limits = %s' % self.limits[i]
                if self.limits[i]:
                    selection_set = sets.Set(self.selections[i])
                    ss_intersect = selection_set.intersection(self.limits[i])
                    intersect_set.append(ss_intersect)

            iterables = list(intersect_set)
            print "Iterables"
            print iterables

            print "module name: %s" % __name__
            print "object name: %s" % obj.__name__
            print "object module name: %s" % obj.__module__

            class_module = sys.modules[obj.__module__]

            for iterproduct in itertools.product(*iterables):
                print iterproduct
                print len(iterproduct)
                # string representation of cartesian product values
                suffix = '_'.join(iterproduct)
                # name to inject before suffix (can be set in decorator)
                cplex_name = getattr(self, 'cplex_name', 'cplex')

                class_name = "%s_%s_%s" % (obj.__name__, cplex_name, suffix)
                print "class_name: %s" % class_name

                """Create the new classes with the obj super instead of
                    the object. Also copy the class dict from obj to the
                    new class. This retains the guts of obj and allows
                    existing im_func() calls as well as Python2 super() calls
                    that return the true super and not the obj class used
                    as a template.

                    Usage examples:
                        In a classmethod:
                            super(cls, cls).setUpClass()
                        In an instance method:
                            super(self.__class__, self).setUp()

                    Previous type call that used object as super...
                        new_class = type(class_name, (obj,), {})
                """
                # TODO: test under Python3
                new_class = type(class_name, (obj.__bases__),
                                 dict(obj.__dict__))

                # loop through lists and assign attributes to objects
                for i in range(0, len(iterproduct)):
                    print "%s: %s" % (updated_axis_names[i],
                                      iterproduct[i])
                    setattr(new_class, updated_axis_names[i],
                            iterproduct[i])

                # change the module name for the new class. it's created
                # under carteplex and needs to be the test module in reports
                new_class.__module__ = class_module.__name__
                setattr(class_module, class_name, new_class)

            # pytest catches the original test class. squelch it before loader
            obj = ''

            # define load_tests here and then wire it to the module
            # pylint: disable=unused-argument
            def load_tests(loader, standard_tests, pattern):
                """Carteplex injects this method into the calling test module.
                The loader has already created a list of methods by the time
                the Carteplex decorator is exec'd, so this is added
                automatically to the test module to gen a new list on the fly--
                and so the test script writer doesn't have to add it.
                """
                print "LOAD TESTS"

                return standard_tests

            class_module.load_tests = load_tests

            return obj

# TODO: remove print statements.
# TODO: cartemethod and cartefunction
# TODO: load carteplex attributes from default config file

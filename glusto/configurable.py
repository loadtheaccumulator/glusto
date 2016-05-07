# Copyright 2014 Jonathan Holloway <loadtheaccumulator@gmail.com>
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


"""All things configuration.

NOTE:
    Configurable is inherited by the Glusto class
    and not designed to be instantiated.
"""
import yaml


class Configurable(object):
    """The class providing all things configuration."""

    config = {}
    """The default class attribute for storing configurations."""

    @staticmethod
    def store_config(obj, filename):
        """Writes an object to a file in yaml format.

        Args:
            obj (object): The Python object to store in yaml format.
            filename (str): Filename for output of configuration.

        Returns:
            Nothing

        Note:
            Uses custom GDumper class to strip Python object formatting.
            This is not a utility function for serialization.
        """
        # TODO: filter objects not necessary to store
        # TODO: errorcheck these calls
        configfd = file(filename, 'w')
        yaml.dump(obj, configfd, Dumper=GDumper)

    @staticmethod
    def load_config(filename):
        """Reads a yaml config from file.

        Args:
            filename (str): Filename of configuration to be read.

        Returns:
            Dict of configuration items.
        """
        configfd = file(filename, 'r')
        config = yaml.load(configfd)
        # TODO: does yaml.load return None or empty dict?

        return config

    @staticmethod
    def load_configs(filelist):
        """Reads multiple configs from a list of filenames
        into a single configuration.

        Args:
            filelist (list): List of configuration filenames to read.

        Returns:
            Dict of configuration items.
        """
        config = {}
        if isinstance(filelist, str):
            filelist = [filelist]
        for filename in filelist:
            config_part = Configurable.load_config(filename)
            # TODO: add errcheck to prevent hosing the config dict
            config.update(config_part)

        return config

    @classmethod
    def set_config(cls, config):
        """Assigns a config to the config class attribute.

        Args:
            config  (dict): A dictionary of configuration objects.

        Returns:
            Nothing

        Note:
            DESTRUCTIVE. This will assign a new dictionary on top of an
            existing config. See update_config().
        """

        cls.config = config

    @classmethod
    def update_config(cls, config):
        """Adds a config to the config class attribute.

        Args:
            config  (dict): A dictionary of configuration objects.

        Returns:
            Nothing

        Note:
            SOMEWHAT DESTRUCTIVE. This will overwrite any previously
            existing objects.

            For example, config['thisandthat'] will overwrite
            cls.config['thisandthat'], but config['subconfig']['thisandthat']
            will add the subconfig dictionary without overwriting
            cls.config['thisandthat'].
        """
        cls.config.update(config)

    @classmethod
    def log_config(cls, obj):
        """Writes a yaml formatted configuration to the log.

        Args:
            obj (dict): The configuration object to write to log.

        Returns:
            Nothing
        """
        cls.log.debug("Configuration for object type %s:\n%s" %
                      (type(obj), yaml.dump(obj, Dumper=GDumper)))

    @staticmethod
    def get_config(obj):
        """Retrieves an object in yaml format.

        Args:
            obj (object): A Python object to be converted to yaml.

        Returns:
            A yaml formatted string.
        """
        return yaml.dump(obj, Dumper=GDumper)

    @staticmethod
    def show_config(obj):
        """Outputs a yaml formatted representation of an object on stdout.

        Args:
            obj (object): A Python object to be converted to yaml.

        Returns:
            Nothing
        """
        print yaml.dump(obj, Dumper=GDumper)

    @classmethod
    def clear_config(cls):
        """Clears the config class attribute with an empty dictionary.

        Returns:
            Nothing
        """
        cls.config = {}


class GDumper(yaml.Dumper):
    """Override the alias junk normally output by Dumper.
    This is necessary because PyYaml doesn't give a simple option to 
    modify the output and ignore tags, aliases, etc.
    """
    def ignore_aliases(self, data):
        """Overriding to skip aliases."""
        return True

    def prepare_tag(self, tag):
        """Overriding to skip tags.
        e.g.,
        !!python/object:glusto.cluster.Cluster
        """
        return ''

# TODO: see if Python3 makes possible for Configuration to handle all objects
class Intraconfig(object):
    """Class to provide instances with simple configuration
    utility and introspection in yaml config format.

    Intended to be inherited.

    Example:
        To inherit Intraconfig in your custom class::

            >>> from glusto.configurable import Intraconfig
            >>> class MyClass(Intraconfig):
            >>>     myattribute = "this and that"

        To use Intraconfig to output MyClass as yaml::

            >>> myinstance = MyClass()
            >>> myinstance.show_config()
    """
    def update_config(self, config):
        """Adds a config to the config class attribute.

        Args:
            config  (dict): A dictionary of configuration objects.

        Returns:
            Nothing

        Note:
            SOMEWHAT DESTRUCTIVE. This will overwrite any previously
            existing objects.

            For example, config['thisandthat'] will overwrite
            cls.config['thisandthat'], but config['subconfig']['thisandthat']
            will add the subconfig dictionary without overwriting
            cls.config['thisandthat'].
        """
        self.__dict__.update(config)

    def show_config(self):
        """Outputs a yaml formatted representation of an instance on stdout.

        Returns:
            Nothing
        """
        Configurable.show_config(self)

    def get_config(self):
        """Retrieves an instance object in yaml format.

        Returns:
            A yaml formatted string.
        """
        return Configurable.get_config(self)

    def load_config(self, filename):
        """Reads a yaml config from file and assigns to the config
        instance attribute.

        Args:
            filename (str): Filename of configuration to be read.

        Returns:
            Nothing
        """
        config =  Configurable.load_config(filename)
        self.set_config(config)


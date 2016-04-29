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


"""All things configuration"""
import yaml


class Configurable(object):
    config = {}

    @staticmethod
    def store_config(obj, filename):
        # TODO: filter objects not necessary to store
        # TODO: errorcheck these calls
        configfd = file(filename, 'w')
        yaml.dump(obj, configfd, Dumper=GDumper)

    @staticmethod
    def load_config(filename):
        configfd = file(filename, 'r')
        config = yaml.load(configfd)
        # TODO: does yaml.load return None or empty dict?

        return config

    @staticmethod
    def load_configs(filelist):
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
        cls.config = config

    @classmethod
    def update_config(cls, config):
        cls.config.update(config)

    @classmethod
    def log_config(cls, obj):
        cls.log.debug("Configuration for object type %s:\n%s" %
                      (type(obj), yaml.dump(obj, Dumper=GDumper)))

    @staticmethod
    def get_config(obj):
        return yaml.dump(obj, Dumper=GDumper)

    @staticmethod
    def show_config(obj):
        print yaml.dump(obj, Dumper=GDumper)

    @classmethod
    def clear_config(cls):
        cls.config = {}


class GDumper(yaml.Dumper):
    """override the alias junk
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
    def update_config(self, config):
        self.__dict__.update(config)

    def show_config(self):
        Configurable.show_config(self)

    def get_config(self):
        return Configurable.get_config(self)

    def load_config(self, filename):
        config =  Configurable.load_config(filename)
        self.set_config(config)


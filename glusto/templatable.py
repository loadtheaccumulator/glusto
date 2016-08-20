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
"""All things Jinja templates.

NOTE:
    Templatable is inherited by the Glusto class
    and not designed to be instantiated.
"""
import jinja2


class Templatable(object):
    """The class providing Jinja template functionality."""

    @staticmethod
    def render_template(template_filename, template_vars={},
                        output_file=None, searchpath=None):
        """Render a template into text file

        Args:
            template_filename (str): Fully qualified template filename.
            template_vars (dict): A dictionary of variables.
            output_file (str) [optional]: Fully qualified output filename.
            searchpath (str) [optional]: The root path to begin file searches.
                Default is the current path.

        Returns:
            String containing template rendering result if successful.
        """
        if not searchpath:
            if template_filename.startswith('/'):
                searchpath = "/"
            else:
                searchpath = "."

        template_loader = jinja2.FileSystemLoader(searchpath=searchpath)
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(template_filename)
        output_text = template.render(template_vars)

        if output_file:
            with open(output_file, 'wb') as fh:
                fh.write(output_text)

        # TODO: return True or False. add error checking above
        return output_text

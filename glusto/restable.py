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
"""All things REST API related.

NOTE:
    Restable is inherited by the Glusto class
    and not designed to be instantiated.
"""

from urllib import urlencode
from urllib2 import Request, urlopen, URLError


class Restable(object):
    """The class providing REST API functionality."""

    @classmethod
    def rest_get(cls, url):
        """Submit a REST API GET request.

        Args:
            url (str): The HTTP protocol standard url for the request.

        Returns:
            returncode (int): The HTTP protocol standard return code.
            Zero on success.
            response output (str): The output text from the response.
            response error (str): The error text on failure.
        """
        #request = Request('http://placekitten.com/')
        request = Request(url)

        try:
            response = urlopen(request)
            # TODO: catch other error
            restout = response.read()
            #print kittens[559:1000]
            retcode = 0
            resterr = None
        except URLError, e:
            resterr = e.reason
            restout = None
            retcode = e.code

        # return a connectible-like tuple
        return (retcode, restout, resterr)

    @classmethod
    def rest_post(cls, url, data):
        """Submit a REST API POST request.

        Args:
            url (str): The HTTP protocol standard url for the request.
            data (dict): A dictionary of key:value pairs

        Returns:
            returncode (int): The HTTP protocol standard return code.
            Zero on success.
            response output (str): The output text from the response.
            response error (str): The error text on failure.
        """
        post_data = urlencode(data)
        request = Request(url, post_data)

        try:
            response = urlopen(request)
            restout = response.read()
            retcode = 0
            resterr = None
        except URLError, e:
            resterr = e.reason
            restout = None
            retcode = e.code

        # return a connectible-like tuple
        return (retcode, restout, resterr)

    @classmethod
    def rest_put(cls, url, data):
        """Submit a REST API PUT request.

        Args:
            url (str): The HTTP protocol standard url for the request.
            data (dict): A dictionary of key:value pairs

        Returns:
            returncode (int): The HTTP protocol standard return code.
            Zero on success.
            response output (str): The output text from the response.
            response error (str): The error text on failure.
        """
        put_data = urlencode(data)
        request = Request(url, put_data)
        request.get_method = lambda: 'PUT'
        try:
            response = urlopen(request)
            restout = response.read()
            retcode = 0
            resterr = None
        except URLError, e:
            resterr = e.reason
            restout = None
            retcode = e.code

        # return a connectible-like tuple
        return (retcode, restout, resterr)

    @classmethod
    def rest_delete(cls, url, data):
        """Submit a REST API DELETE request.

        Args:
            url (str): The HTTP protocol standard url for the request.
            data (dict): A dictionary of key:value pairs

        Returns:
            returncode (int): The HTTP protocol standard return code.
            Zero on success.
            response output (str): The output text from the response.
            response error (str): The error text on failure.
        """
        delete_data = urlencode(data)
        request = Request(url, delete_data)
        request.get_method = lambda: 'DELETE'
        try:
            response = urlopen(request)
            restout = response.read()
            retcode = 0
            resterr = None
        except URLError, e:
            resterr = e.reason
            restout = None
            retcode = e.code

        # return a connectible-like tuple
        return (retcode, restout, resterr)

# TODO: add authentication capability

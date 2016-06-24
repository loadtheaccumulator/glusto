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
from __builtin__ import classmethod
"""All things rpyc connection.

NOTE:
    Rpycable is inherited by the Glusto class
    and not designed to be instantiated.

WARNING:
    Rpyc breaks in mixed Python 2.x/3.x environments.
    When using rpyc, you will only be able to successfully make rpyc calls
    against a system running the same version of Python.
    (see rpyc module docs for more information)
"""
from rpyc.utils.zerodeploy import DeployedServer


class Rpycable(object):

    _rpyc_connections = {}
    _deployed_servers = {}

    @classmethod
    def _rpyc_get_connection_name(cls, host, user=None, instance=None):
        if not user:
            user = cls.user

        if instance:
            connection_name = "%s@%s:%i" % (user, host, instance)
        else:
            connection_name = "%s@%s" % (user, host)

        return connection_name

    @classmethod
    def _rpyc_get_deployed_server(cls, name, ssh_connection):
        print "getting deployed server"
        if name not in cls._deployed_servers:
            deployed_server = DeployedServer(ssh_connection)
            cls._deployed_servers[name] = deployed_server
            print "cached deployed server %s" % name
        else:
            print "getting deployed server %s from cache" % name
            deployed_server = cls._deployed_servers[name]

        if deployed_server:
            return deployed_server

        return None

    @classmethod
    def _rpyc_get_classic_connection(cls, name, deployed_server):
        print "getting classic connection"
        if name not in cls._rpyc_connections:
            classic_connection = deployed_server.classic_connect()
            cls._rpyc_connections[name] = classic_connection
            print 'Cached connection for %s' % name
        else:
            classic_connection = cls._rpyc_connections[name]

        if classic_connection:
            return classic_connection

        return None

    @classmethod
    def rpyc_get_connection(cls, host, user=None, instance=1):
        """Setup a connection via rpyc"""

        conn_name = cls._rpyc_get_connection_name(host, user, instance)
        deployed_server_name = cls._rpyc_get_connection_name(host, user)
        classic_connection = None

        print "Conn name: %s" % conn_name
        # if no existing connection, create one
        if conn_name not in cls._rpyc_connections:
            print("Creating rpyc connection: %s" % conn_name)
            ssh_connection = cls._get_ssh_connection(host, user)

            if ssh_connection:
                print "deployed server setup"
                deployed_server = \
                    cls._rpyc_get_deployed_server(deployed_server_name,
                                                  ssh_connection)

                if deployed_server:
                    print "class connect"
                    classic_connection = \
                        cls._rpyc_get_classic_connection(conn_name,
                                                         deployed_server)

                    if not classic_connection:
                        print "Classic rpyc connection failed"
                else:
                    print "Deploying rpyc failed"
            else:
                print "SSH Connection Failed"
        else:
            print("Retrieved connection from cache: %s" % conn_name)
            classic_connection = cls._rpyc_connections[conn_name]

        #print classic_connection.modules.os.environ
        #print cls._rpyc_connections[conn_name].modules.os.environ

        if classic_connection:
            return classic_connection

        print("oops. did not get rpyc for %s", conn_name)

        return None

    @classmethod
    def rpyc_list_connections(cls):
        """Display the list of existing ssh connections on stdout."""
        for name in cls._rpyc_connections.keys():
            print (name)

    @classmethod
    def rpyc_list_deployed_servers(cls):
        for name in cls._deployed_servers.keys():
            print (name)

    @classmethod
    def rpyc_check_connection(cls, host, user=None, instance=1):

        conn_name = cls._rpyc_get_connection_name(host, user, instance)

        connection = cls.rpyc_get_connection(host, user, instance)
        status = "open"
        if connection.closed:
            status = "closed"
        print "%s is %s" % (conn_name, status)

    @classmethod
    def rpyc_ping_connection(cls, host, user=None, instance=1):
        connection = cls.rpyc_get_connection(host, user, instance)
        try:
            connection.ping()

            return True
        except:
            return False

    @classmethod
    def rpyc_close_connection(cls, host=None, user=None, instance=1):
        connection = cls.rpyc_get_connection(host, user, instance)
        name = cls._rpyc_get_connection_name(host, user, instance)
        print "closing rpyc connection %s" % name
        del cls._rpyc_connections[name]
        connection.close()

    @classmethod
    def rpyc_close_connections(cls):
        for key in cls._rpyc_connections.keys():
            print "closing rpyc connection %s" % key
            connection = cls._rpyc_connections[key]
            del cls._rpyc_connections[key]
            connection.close()

# TODO: log instead of print
# TODO: more robust error checking

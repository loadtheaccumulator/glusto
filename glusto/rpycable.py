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
"""All things rpyc connection.

NOTE:
    Rpycable is inherited by the Glusto class
    and not designed to be instantiated.

WARNING:
    Rpyc breaks in mixed Python 2.x/3.x environments.
    When using rpyc, you will only be able to successfully make rpyc calls
    against a system running the same version of Python.
    (see rpyc module install docs for more information)
"""
import inspect
import types

from rpyc.utils.zerodeploy import DeployedServer


class Rpycable(object):

    _rpyc_connections = {}
    _deployed_servers = {}

    @classmethod
    def _rpyc_get_connection_name(cls, host, user=None, instance=None):
        """Create a name for the connection.

        Args:
            host (str): The hostname or IP of the remote system.
            user (str): A user on the remote system. Default: root
            instance (int): The number of the instance when multiple
                connections are used.

        Returns:
            A string representing the name for the connection.
        """
        if not user:
            user = cls.user

        if instance:
            connection_name = "%s@%s:%i" % (user, host, instance)
        else:
            connection_name = "%s@%s" % (user, host)

        return connection_name

    @classmethod
    def _rpyc_get_deployed_server(cls, name, ssh_connection=None):
        """Create and cache a deployed server object.

        Args:
            name (str): The name for the deployed server cache.
            ssh_connection (obj): An ssh_connection object.

        Returns:
            A new or cached deployed_server object.
        """
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
        """Create and cache an rpyc classic connection object.

        Args:
            name (str): The name for the classic connection cache.
            deployed_server (obj): A deployed server object.

        Returns:
            A new or cached classic connection object.
        """
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
        """Setup and cache a connection via rpyc.

        Args:
            host (str): The hostname or IP of the remote system.
            user (str): A user on the remote system. Default: root
            instance (int): The number of the instance when multiple
                connections are used.

        Returns:
            A new or cached rpyc connection object.
        """
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

        if classic_connection:
            return classic_connection

        print("oops. did not get rpyc for %s", conn_name)

        return None

    @classmethod
    def rpyc_create_connections(cls, hosts, user=None, num_instances=1):
        """Setup and cache multiple connections via rpyc.

        Args:
            host (str): The hostname or IP of the remote system.
            user (str): A user on the remote system. Default: root
            num_isntances (int): The number of the instances to create.

        Returns:
            Nothing.
        """
        for i in range(1, num_instances + 1):
            for host in hosts:
                cls.rpyc_get_connection(host, user=user, instance=i)

        # TODO: what to return here. a dictionary of connections created ???

    @classmethod
    def rpyc_get_connections(cls):
        """Get the connection dictionary.

        Args:
            None

        Returns:
            The dictionary of rpyc connections.
        """
        return cls._rpyc_connections

    @classmethod
    def rpyc_list_connections(cls):
        """Display the list of existing ssh connections on stdout.

        Args:
            None

        Returns:
            Nothing
        """
        for name in cls._rpyc_connections.keys():
            print (name)

    @classmethod
    def rpyc_list_deployed_servers(cls):
        for name in cls._deployed_servers.keys():
            print (name)

    @classmethod
    def rpyc_check_connection(cls, host, user=None, instance=1):
        """Check whether a connection is open or closed.

        Args:
            host (str): The hostname or IP of the remote system.
            user (str): A user on the remote system. Default: root
            instance (int): The number of the instance when multiple
                connections are used.

        Returns:
            Nothing
        """
        conn_name = cls._rpyc_get_connection_name(host, user, instance)

        connection = cls.rpyc_get_connection(host, user, instance)
        status = "open"
        if connection.closed:
            status = "closed"
        print "%s is %s" % (conn_name, status)

    @classmethod
    def rpyc_ping_connection(cls, host, user=None, instance=1):
        """Ping an rpyc connection.

        Args:
            host (str): The hostname or IP of the remote system.
            user (str): A user on the remote system. Default: root
            instance (int): The number of the instance when multiple
                connections are used.

        Returns:
            True if pingable. False if does not ping.
        """
        connection = cls.rpyc_get_connection(host, user, instance)
        try:
            connection.ping()

            return True
        except:
            return False

    @classmethod
    def rpyc_close_connection(cls, host=None, user=None, instance=1):
        """Close an rpyc connection.

        Args:
            host (str): The hostname or IP of the remote system.
            user (str): A user on the remote system. Default: root
            instance (int): The number of the instance when multiple
                connections are used.

        Returns:
            Nothing.
        """
        connection = cls.rpyc_get_connection(host, user, instance)
        name = cls._rpyc_get_connection_name(host, user, instance)
        print "closing rpyc connection %s" % name
        del cls._rpyc_connections[name]
        connection.close()

    @classmethod
    def rpyc_close_connections(cls):
        """Close all rpyc connections.

        Args:
            None

        Returns:
            Nothing
        """
        for key in cls._rpyc_connections.keys():
            print "closing rpyc connection %s" % key
            connection = cls._rpyc_connections[key]
            del cls._rpyc_connections[key]
            connection.close()

    @classmethod
    def rpyc_close_deployed_servers(cls):
        """Close all deployed server connections.

        Args:
            None

        Returns:
            Nothing
        """
        cls.rpyc_close_connections()

        for key in cls._deployed_servers.keys():
            print "closing rpyc deployed server %s" % key
            deployed_server = cls._deployed_servers[key]
            del cls._deployed_servers[key]
            deployed_server.close()

    @classmethod
    def rpyc_close_deployed_server(cls, host=None, user=None):
        """Close a deployed server connection.

        Args:
            host (str): The hostname or IP of the remote system.
            user (str): A user on the remote system. Default: root

        Returns:
            Nothing.
        """
        name = cls._rpyc_get_connection_name(host, user)
        ds_search = '%s:' % name

        for rpyckey in cls._rpyc_connections.keys():
            if ds_search in rpyckey:
                connection = cls._rpyc_connections[rpyckey]
                del cls._rpyc_connections[rpyckey]
                connection.close()

        deployed_server = cls._rpyc_get_deployed_server(name)
        print "closing rpyc connection %s" % name
        del cls._deployed_servers[name]
        deployed_server.close()

    @classmethod
    def rpyc_define_module(cls, connection, local_module):
        """Define a local module on the remote system

        Args:
            connection (obj): An rpyc connection object.
            local_module (obj): The module object being defined on the remote.

        Returns:
            A module object representing the local module defined on remote
        """
        sourcecode = inspect.getsource(local_module)
        members = inspect.getmembers(local_module)
        remote_module = types.ModuleType('remote_module', 'remote module')

        connection.execute(sourcecode)
        for name, _ in members:
            try:
                robject = connection.namespace[name]
                setattr(remote_module, name, robject)
            except:
                pass

        return remote_module


# TODO: log instead of print
# TODO: more robust error checking

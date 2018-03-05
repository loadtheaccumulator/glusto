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


class Rpycable():
    """Provides an RPyC object for managing connections and remote execs"""
    # pylint: disable=no-member,bare-except
    # TODO: try to handle possible exceptions RPyC might throw

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
        cls.log.debug("getting deployed server")
        if name not in cls._deployed_servers:
            deployed_server = DeployedServer(ssh_connection)
            cls._deployed_servers[name] = deployed_server
            cls.log.debug("cached deployed server %s" % name)
        else:
            cls.log.debug("getting deployed server %s from cache" % name)
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
        cls.log.debug("getting classic connection")
        if name not in cls._rpyc_connections:
            classic_connection = deployed_server.classic_connect()
            cls._rpyc_connections[name] = classic_connection
            cls.log.debug('Cached connection for %s' % name)
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

        cls.log.debug("Conn name: %s" % conn_name)
        # if no existing connection, create one
        if conn_name not in cls._rpyc_connections:
            cls.log.debug("Creating rpyc connection: %s" % conn_name)
            ssh_connection = cls._get_ssh_connection(host, user)

            if ssh_connection:
                cls.log.debug("deployed server setup")
                deployed_server = \
                    cls._rpyc_get_deployed_server(deployed_server_name,
                                                  ssh_connection)

                if deployed_server:
                    cls.log.debug("class connect")
                    classic_connection = \
                        cls._rpyc_get_classic_connection(conn_name,
                                                         deployed_server)

                    if not classic_connection:
                        cls.log.error("Classic rpyc connection failed")
                else:
                    cls.log.error("Deploying rpyc failed")
            else:
                cls.log.error("SSH Connection Failed")
        else:
            cls.log.debug("Retrieved connection from cache: %s" % conn_name)
            classic_connection = cls._rpyc_connections[conn_name]

        if classic_connection:
            return classic_connection

        cls.log.error("oops. did not get rpyc for %s", conn_name)

        return None

    @classmethod
    def rpyc_create_connections(cls, hosts, user=None, num_instances=1):
        """Setup and cache multiple connections via rpyc.

        Args:
            host (str): The hostname or IP of the remote system.
            user (str): A user on the remote system. Default: root
            num_instances (int): The number of the instances to create.

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
        for name in cls._rpyc_connections:
            print(name)

    @classmethod
    def rpyc_list_deployed_servers(cls):
        """Display the list of deployed servers

        Args:
            None

        Returns:
            Nothing
        """
        for name in cls._deployed_servers:
            print(name)

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
        print("%s is %s" % (conn_name, status))

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

            print("connection is alive")
            return True
        except:  # noqa: E722
            print("connection is dead")
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
        cls.log.debug("closing rpyc connection %s" % name)
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
        for key in list(cls._rpyc_connections):
            cls.log.debug("closing rpyc connection %s" % key)
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

        for key in list(cls._deployed_servers):
            cls.log.debug("closing rpyc deployed server %s" % key)
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

        for rpyckey in cls._rpyc_connections:
            if ds_search in rpyckey:
                connection = cls._rpyc_connections[rpyckey]
                del cls._rpyc_connections[rpyckey]
                connection.close()

        deployed_server = cls._rpyc_get_deployed_server(name)
        cls.log.debug("closing rpyc connection %s" % name)
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
            except:  # noqa: E722
                pass

        return remote_module


# TODO: log instead of print
# TODO: more robust error checking

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
"""All things remote connection and local shell.

NOTE:
    Connectible is inherited by the Glusto class
    and not designed to be instantiated.
"""
import subprocess
import os

from plumbum import SshMachine


class Connectible(object):
    """The class provding remote connections and local commands."""

    _ssh_connections = {}
    """The dictionary of ssh connections used by the inheriting class"""
    # TODO: config override
    use_controlpersist = True
    user = "root"
    #log_color = True

    @classmethod
    def _get_ssh_connection(cls, host, user=None):
        """Setup an SshMachine connection.

        Args:
            host (str): Hostname of the system.
            user (optional[str]): User to use for connection.

        Returns:
            An ssh connection object on success.
            None on failure.
        """
        if not user:
            user = cls.user

        ssh_opts = ()
        ssh_opts += ('-T',
                     '-oPasswordAuthentication=no',
                     '-oStrictHostKeyChecking=no',
                     '-oPort=22',
                     '-oConnectTimeout=10')

        keyfile = None
        if 'ssh_keyfile' in cls.config:
            keyfile = cls.config['ssh_keyfile']

            ssh_opts += ('-o', 'IdentityFile=%s' % keyfile)

        if cls.use_controlpersist:
            ssh_opts += ('-oControlMaster=auto',
                         '-oControlPersist=4h',
                         '-oControlPath=~/.ssh/glusto-ssh-%r@%h:%p')

        conn_name = "%s@%s" % (user, host)
        # if no existing connection, create one
        if conn_name not in cls._ssh_connections:
            cls.log.debug("Creating connection: %s" % conn_name)
            try:
                ssh = SshMachine(host, user, ssh_opts=ssh_opts)
            except:
                cls.log.error("Exception trying to establish SshMachine")
                return None
            cls._ssh_connections[conn_name] = ssh
        else:
            cls.log.debug("Retrieved connection from cache: %s" % conn_name)
            ssh = cls._ssh_connections[conn_name]

        if ssh:
            return ssh

        print("oops. did not get ssh for %s", conn_name)
        return None

    @classmethod
    def run(cls, host, command, user=None):
        """Run a command on a remote host via ssh.

        Args:
            host (str): The hostname of the system.
            command (str): The command to run on the system.
            user (optional[str]): The user to use for connection.

        Returns:
            A tuple consisting of the command return code, stdout, and stderr.
            None on error.

        Example:
            To run the uname command on a remote host named "bunkerhill"...

                >>> from glusto.core import Glusto as g
                >>> results = g.run("bunkerhill", "uname -a")
        """
        '''
        if isinstance(hosts, str):
            ssh = cls._get_ssh_connection(hosts, user)


        results = {}
        for host in hosts:
            ssh = cls._get_ssh_connection(host, user)
            results[ssh] = "result from %s on %s" % (command, ssh)
        '''
        if not user:
            user = cls.user

        ctlpersist = ''
        if cls.use_controlpersist:
            ctlpersist = " (cp)"

        # output command
        cls.log.info("%s@%s%s: %s" % (user, host, ctlpersist, command))
        # run the command
        ssh = cls._get_ssh_connection(host, user)
        if not ssh:
            cls.log.error("ERROR: No ssh connection")
            return None

        p = ssh.popen(command)
        stdout, stderr = p.communicate()
        retcode = p.returncode

        # output command results
        identifier = "%s@%s" % (user, host)
        cls._log_results(identifier, retcode, stdout, stderr)

        return (retcode, stdout, stderr)

    @classmethod
    def _log_results(cls, identifier, retcode, stdout, stderr):
        """Logs the return code, stdout, and stderr returned from a command.

        Args:
            identifier (str): A representative name for the messages to be
                displayed in the log entry.
            retcode (str): the return code from the command resuls.
            stdout (str): the stdout from the command results.
            stderr (str): the stderr from the command results.

        Returns:
            Nothing
        """
        # output command results
        cls.log.debug(cls.colorfy(cls.COLOR_RCODE, "RETCODE (%s): %s" %
                                  (identifier, retcode)))
        if stdout:
            cls.log.debug(cls.colorfy(cls.COLOR_STDOUT, "STDOUT (%s)...\n%s" %
                                      (identifier, stdout)))
        if stderr:
            cls.log.debug(cls.colorfy(cls.COLOR_STDERR, "STDERR (%s)...\n%s" %
                                      (identifier, stderr)))

    @classmethod
    def run_async(cls, host, command, user=None):
        """Run remote commands asynchronously.

        Args:
            host (str): The hostname of the system.
            command (str): The command to run on the system.
            user (optional[str]): The user to use for connection.

        Returns:
            An open connection descriptor to be used by the calling function.
            None on error.

        Example:
            To run a command asynchronously on remote hosts
            named "bunkerhill" and "breedshill"...

                >>> from glusto.core import Glusto as g

                >>> command = "ls -R /etc"
                >>> proc1 = g.run_async("bunkerhill", command)
                >>> proc2 = g.run_async("breedshill", command)

                >>> results1 = proc1.async_communicate()
                >>> results2 = proc2.async_communicate()

            This can also be used to run a command against the same system
            asynchronously as different users...

                >>> command = "ls -R /etc"
                >>> proc1 = g.run_async("breedshill", command, user="howe")
                >>> proc2 = g.run_async("breedshill", command, user="pigot")

                >>> results1 = proc1.async_communicate()
                >>> results2 = proc2.async_communicate()

        Note:
            run_async() runs commands asynchronously, but blocks on
            async_communicate() and reads output sequentially.
            This might not be a good fit for run-and-forget commands."""
        if not user:
            user = cls.user

        if cls.use_controlpersist:
            ctlpersist = " (cp)"

            # output command
            cls.log.info(cls.colorfy(cls.COLOR_COMMAND, "%s@%s%s: %s" %
                                     (user, host, ctlpersist, command)))
            # run the command
            ssh = cls._get_ssh_connection(host, user)
            if not ssh:
                print "ERROR: No ssh connection"
                return None

            p = ssh.popen(command)

        def async_communicate():
            stdout, stderr = p.communicate()
            retcode = p.returncode

            # output command results
            identifier = "%s@%s" % (user, host)
            cls._log_results(identifier, retcode, stdout, stderr)

            return (retcode, stdout, stderr)

        p.async_communicate = async_communicate
        return p

    @classmethod
    def run_local(cls, command):
        """Run a command on the local management system.

        Args:
            command (str): Command to run locally.

        Returns:
            A tuple consisting of the command return code, stdout, and stderr.

        Example:
            To run a command locally...

                >>> from glusto.core import Glusto as g
                >>> retcode, stdout, stderr = g.run_local("uname -a")
        """
        # output command
        cls.log.info("local: %s" % command)

        p = subprocess.Popen(command, shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        retcode = p.returncode

        # output command results
        cls._log_results('local', retcode, stdout, stderr)

        return (retcode, stdout, stderr)

    @classmethod
    def run_serial(cls, hosts, command, user=None):
        """Sequentially runs a command against a list of hosts.

        Args:
            hosts (list): A list of hostnames to run command against.
            command (str): The command to run on the system.
            user (optional[str]): The user to use for connection.

        Returns:
            A dictionary of tuples containing returncode, stdout, and stderr.
            Labeled by the host.

        Example:
            To run a command against a list of hosts...

                >>> from glusto.core import Glusto as g
                >>> hosts = ["bunkerhill", "breedshill"]
                >>> results = g.run_serial(hosts, "ls -Rail /etc")
        """
        results = {}
        for host in hosts:
            rcode, rout, rerr = cls.run(host, command, user)

            results[host] = (rcode, rout, rerr)

        return results

    @classmethod
    def run_parallel(cls, hosts, command, user=None):
        """Sequentially runs a command against a list of hosts.

        Args:
            hosts (list): A list of hostnames to run command against.
            command (str): The command to run on the system.
            user (optional[str]): The user to use for connection.

        Returns:
            A dictionary of tuples containing returncode, stdout, and stderr.
            Labeled by the host.

        Example:
            To run a command against a list of hosts in parallel...

                >>> from glusto.core import Glusto as g
                >>> hosts = ["bunkerhill", "breedshill"]
                >>> results = g.run_serial(hosts, "ls -Rail /etc")
        """
        '''
        results = {}
        for host in hosts:
            rcode, rout, rerr = cls.run(host, command, user)

            results[host] = (rcode, rout, rerr)

        return results
        '''
        results = {}
        rasyncs = {}
        # run the commands async and record the returned communicate object
        for host in hosts:
            rasyncs[host] = cls.run_async(host, command, user)

        # loop through communicate() calls and record results
        for host, proc in rasyncs.items():
            results[host] = proc.async_communicate()

        return results

    @classmethod
    def upload(cls, host, localpath, remotepath, user=None):
        """Uploads a file to a remote system.

        Args:
            host (str): Hostname of the remote system.
            localpath (str): The source path for the file on the local system.
            remotepath (str): The target path on the remote server.
            user (optional[str]): The user to use for the remote connection.

        Returns:
            None on failure.
        """
        # TODO: consider a noclobber option to backup existing files

        if not user:
            user = cls.user

        # run the command
        ssh = cls._get_ssh_connection(host, user)
        if not ssh:
            print "ERROR: No ssh connection"
            return None

        # TODO: catch exceptions thrown by SshMachine.upload()
        ssh.upload(localpath, remotepath)

    @classmethod
    def download(cls, host, remotepath, localpath, user=None):
        """Uploads a file to a remote system.

        Args:
            host (str): Hostname of the remote system.
            remotepath (str): The source path on the remote server.
            localpath (str): The target path for the file on the local system.
            user (optional[str]): The user to use for the remote connection.

        Returns:
            None on failure.
        """
        # TODO: consider a noclobber option to backup existing files

        if not user:
            user = cls.user

        # run the command
        ssh = cls._get_ssh_connection(host, user)
        if not ssh:
            print "ERROR: No ssh connection"
            return None

        # TODO: catch exceptions thrown by SshMachine.download()
        ssh.download(remotepath, localpath)

    @classmethod
    def transfer(cls, sourcehost, sourcefile,
                 targethost, targetfile, user=None):
        """Transfer a file between remote systems (scp)
        Requires keys to be set up between remote systems.

        Args:
            sourcehost (str): Hostname of the remote system copying from.
            sourcefile (str): The source path on a remote system.
            targethost (str): Hostname of the remote system copying to.
            targetfile (str): The target path for the file on a remote system.
            user (optional[str]): The user to use for the remote connection.

        Returns:
            Nothing
        """

        if not user:
            user = cls.user

        # TODO: add scp options (keyfile, etc)
        command = 'scp %s %s@%s:%s' % (sourcefile,
                                       user, targethost, targetfile)
        cls.run(sourcehost, command)

    @classmethod
    def ssh_list_connections(cls):
        """Display the list of existing ssh connections on stdout."""
        for name in cls._ssh_connections.keys():
            print (name)

    @classmethod
    def ssh_get_connections(cls):
        """Retrieves the dictionary of ssh connections.

        Returns:
            A dictionary of ssh connections.
        """
        return cls._ssh_connections

    @classmethod
    def ssh_close_connection(cls, host, user=None):
        """Close an SshMachine connection.

        Args:
            host (str): Hostname of the system.
            user (optional[str]): User to use for connection.

        Returns:
            Nothing
        """
        if not user:
            user = cls.user

        conn_name = "%s@%s" % (user, host)
        connection = cls._get_ssh_connection(host, user)
        del cls._ssh_connections[conn_name]
        connection.close()

    @classmethod
    def ssh_close_connections(cls):
        """Close all ssh connections.

        Args:
            None

        Returns:
            Nothing
        """
        for key in cls._ssh_connections.keys():
            print "closing ssh connection %s" % key
            connection = cls._ssh_connections[key]
            del cls._ssh_connections[key]
            connection.close()

    @classmethod
    def ssh_set_keyfile(cls, keyfile):
        if keyfile.startswith('~'):
            keyfile = keyfile.replace('~', os.environ['HOME'])
        if os.path.exists(keyfile):
            cls.config['ssh_keyfile'] = keyfile

            return True

        cls.log.error("Keyfile %s does not exist" % keyfile)
        return False

    @classmethod
    def ssh_get_keyfile(cls):

        return cls.config.get('ssh_keyfile', None)


# TODO: add color logging to all methods with retcode, rout, rerr
# TODO: check connections to see if they are current.

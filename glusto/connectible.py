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

"""All things remote connection and local shell"""
import subprocess

from plumbum import SshMachine
from decorator import contextmanager


class Connectible(object):
    _ssh_connections = {}
    # TODO: config override
    use_ssh = True
    use_controlpersist = True
    user = "root"
    #log_color = True

    @classmethod
    def _get_ssh_connection(cls, host, user=None):
        """Setup an SshMachine connection for non-rpyc connections"""
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

        #cls.show_object(ssh_opts)

        conn_name = "%s@%s" % (user, host)
        # if no existing connection, create one
        if conn_name not in cls._ssh_connections:
            cls.log.debug("Creating connection: %s" % conn_name)
            # we already have plumbum imported for rpyc, so let's use it
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
    def run_test(cls, host=None, command=None, user=None, mode=None):
        if not host or mode == 'local':
            cls.run_local(command)
        else:
            cls.run(host, command, user)

    @classmethod
    def run(cls, host, command, user=None):
        """
        if isinstance(hosts, str):
            ssh = cls._get_ssh_connection(hosts, user)


        results = {}
        for host in hosts:
            ssh = cls._get_ssh_connection(host, user)
            results[ssh] = "result from %s on %s" % (command, ssh)
        """
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
        NOTE: runs commands asynchronously, but blocks on async_communicate()
                and reads output sequentially. This might not be a good fit
                for run-and-forget commands"""
        if not user:
            user = cls.user

        if cls.use_ssh:
            ctlpersist = ''
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

    # TODO: do we need the contextmanager method for doing this?
    @classmethod
    @contextmanager
    def run_background(cls, host, command, user=None):
        """Run a command in the background and return without results.
        """
        if not user:
            user = cls.user

        if cls.use_ssh:
            ctlpersist = ''
            if cls.use_controlpersist:
                ctlpersist = " (cp)"

        # output command
        cls.log.info("%s@%s%s: %s" % (user, host, ctlpersist, command))
        # run the command
        ssh = cls._get_ssh_connection(host, user)

        p = ssh.popen(command)
        print "pre-yield"
        try:
            yield
        except Exception:
            p.kill()
        print "post-yield"
        stdout, stderr = p.communicate()
        retcode = p.returncode
        # TODO: add return capability and test for hangs
        print retcode, stdout, stderr

    @classmethod
    def run_local(cls, command):
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
        results = {}
        for host in hosts:
            rcode, rout, rerr = cls.run(host, command, user)

            results[host] = (rcode, rout, rerr)

        return results

    @classmethod
    def upload(cls, host, localpath, remotepath, user=None):
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
    def transfer(cls, sourcehost, targethost,
                 sourcefile, targetfile, user=None):
        """Transfer a file between remote systems (scp)
        Requires keys to be set up between remote systems."""

        if not user:
            user = cls.user

        # TODO: add scp options (keyfile, etc)
        command = 'scp %s %s@%s:%s' % (sourcefile,
                                       user, targethost, targetfile)
        cls.run(sourcehost, command)

    @classmethod
    def list_ssh_connections(cls):
        for name in cls._ssh_connections.keys():
            print (name)

    @classmethod
    def get_ssh_connections(cls):
        return cls._ssh_connections

# TODO: add color logging to all methods with retcode, rout, rerr

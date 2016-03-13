""" glusto brains """
from pprint import PrettyPrinter

from plumbum import SshMachine


class Glusto(object):
    """Glusto class
    The locker for all things Glusto
    """
    config = {}
    _ssh_connections = {}
    use_ssh = True
    use_controlpersist = True
    user = "jhollowa"
    #config["ssh_keyfile"] = "~/.ssh/id_rsa"

    def __init__(self):
        """ Might not need an instance yet """
        return None

    @classmethod
    def _get_ssh_connection(cls, node, user):
        """Setup an SshMachine connection for non-rpyc connections"""
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

        conn_name = "%s@%s" % (user, node)
        # if no existing connection, create one
        if conn_name not in cls._ssh_connections:
            # we already have plumbum imported for rpyc, so let's use it
            ssh = SshMachine(node, user, ssh_opts=ssh_opts)
            cls._ssh_connections[conn_name] = ssh
        else:
            ssh = cls._ssh_connections[conn_name]

        if ssh:
            return ssh

        print("oops. did not get ssh for %s", conn_name)
        return None

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

        if cls.use_ssh:
            ctlpersist = ''
            if cls.use_controlpersist:
                ctlpersist = " (cp)"

            # output command
            print("%s@%s%s: %s" % (user, host, ctlpersist, command))
            # run the command
            ssh = cls._get_ssh_connection(host, user)
            #p = ssh.popen(command)

            p = ssh.popen(command)
            stdout, stderr = p.communicate()
            retcode = p.returncode

            # output command results
            print("RETCODE: %s" % retcode)
            if stdout:
                print("STDOUT...\n%s" % stdout)
            if stderr:
                print("STDERR...\n%s" % stderr)

            return (retcode, stdout, stderr)

    @classmethod
    def list_ssh_connections(cls):
        for name in cls._ssh_connections.keys():
            print (name)

    @classmethod
    def get_ssh_connections(cls):
        return cls._ssh_connections

    @classmethod
    def _read_configs(cls):
        pass

    @classmethod
    def log_object(cls, obj):
        pp = PrettyPrinter()
        # TODO: change this to logging
        pp.pprint(obj)

    @classmethod
    def show_object(clscls, obj):
        pp = PrettyPrinter()
        pp.pprint(obj)

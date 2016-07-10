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
"""Test glusto SSH functionality"""
import unittest
import pytest

from glusto.core import Glusto as g


class TestGlustoBasics(unittest.TestCase):
    """Glusto basics test class"""
    @classmethod
    def setUpClass(cls):
        """unittest standard setUpClass method
        Runs before all test_ methods in the class
        """
        print "Setting Up Class: %s" % cls.__name__
        config = g.load_configs(["../examples/systems.yml",
                                 "../examples/glusto.yml"])
        g.update_config(config)

        cls.hosts = g.config['nodes']
        cls.primary_host = g.config['nodes'][0]
        cls.client = g.config["clients"][0]

        cls.test_string = 'Go for the Glusto!'

    def setUp(self):
        """unittest standard setUp method
        Runs before each test_ method
        """
        print "Setting Up: %s" % self.id()

    def test_run_local(self):
        """Testing SSH run_local() method"""
        print "Running: %s - %s" % (self.id(), self.shortDescription())
        rcode, rout, rerr = g.run_local('echo -n %s' % self.test_string)
        self.assertEqual(rcode, 0)
        self.assertEqual(rout, self.test_string)
        print rout
        self.assertEqual(rerr, '')

    def test_run(self):
        """Testing SSH run() method"""
        print "Running: %s - %s" % (self.id(), self.shortDescription())
        rcode, rout, rerr = g.run(self.primary_host,
                                  'echo -n %s' % self.test_string)
        self.assertEqual(rcode, 0)
        self.assertEqual(rout, self.test_string)
        print rout
        self.assertEqual(rerr, '')

    def test_run_serial(self):
        """Testing SSH run_serial() method"""
        print "Running: %s - %s" % (self.id(), self.shortDescription())
        results = g.run_serial(self.hosts, 'echo -n %s' % self.test_string)
        for host, result in results.iteritems():
            self.assertIn(host, self.hosts)
            print host
            rcode, rout, rerr = result
            self.assertEqual(rcode, 0)
            self.assertEqual(rout, self.test_string)
            print rout
            self.assertEqual(rerr, '')

    def test_run_parallel(self):
        """Testing SSH run_parallel() method"""
        print "Running: %s - %s" % (self.id(), self.shortDescription())
        results = g.run_parallel(self.hosts, 'echo -n %s' % self.test_string)
        hosts_already_tested = []
        for host, result in results.iteritems():
            # test host is in list of hosts to test
            self.assertIn(host, self.hosts)
            # test host has not already been tested
            self.assertNotIn(host, hosts_already_tested)
            hosts_already_tested.append(host)
            print host
            rcode, rout, rerr = result
            self.assertEqual(rcode, 0)
            self.assertEqual(rout, self.test_string)
            print rout
            self.assertEqual(rerr, '')

    def test_upload(self):
        """Testing SSH upload() method"""
        print "Running: %s - %s" % (self.id(), self.shortDescription())
        g.run(self.primary_host, 'rm -f /tmp/upload_test_file')
        rcode, rout, _ = g.run_local('md5sum /etc/hosts | awk \'{print $1}\'')
        if rcode == 0:
            md5sum = rout.strip()
        g.upload(self.primary_host,
                 '/etc/hosts', '/tmp/upload_test_file')
        command = 'md5sum /tmp/upload_test_file | awk \'{print $1}\''
        rcode,  rout, _ = g.run(self.primary_host, command)
        if rcode == 0:
            md5sum_up = rout.strip()
        self.assertEqual(md5sum, md5sum_up, '')

    def test_download(self):
        """Testing SSH download() method"""
        print "Running: %s - %s" % (self.id(), self.shortDescription())

        remote_file = '/etc/hosts'
        local_file = '/tmp/download_test_file'

        # remove local test file (ignore error if not exist)
        g.run_local('rm -f %s' % local_file)

        # md5sum remote file
        command = 'md5sum %s| awk \'{print $1}\'' % remote_file
        rcode,  rout, _ = g.run(self.primary_host, command)
        if rcode == 0:
            md5sum_up = rout.strip()

        # download it
        g.download(self.primary_host,
                   '/etc/hosts', '/tmp/download_test_file')

        # md5sum local copy
        command = 'md5sum %s | awk \'{print $1}\'' % local_file
        rcode, rout, _ = g.run_local(command)
        if rcode == 0:
            md5sum_down = rout.strip()

        # compare the md5sums
        self.assertEqual(md5sum_down, md5sum_up, 'md5sums do not match')

    def test_transfer(self):
        """Testing SSH transfer() method"""
        print "Running: %s - %s" % (self.id(), self.shortDescription())

        remote_file = '/etc/hosts'
        remote_file_copy = '/tmp/transfer_test_file'
        host1 = self.hosts[0]
        host2 = self.hosts[1]

        # remove remote test file copy(ignore error if not exist)
        g.run(host2, 'rm -f %s' % remote_file_copy)

        # md5sum remote file
        command = 'md5sum %s| awk \'{print $1}\'' % remote_file
        rcode,  rout, _ = g.run(self.primary_host, command)
        if rcode == 0:
            md5sum_orig = rout.strip()

        # transfer it
        g.transfer(host1, remote_file, host2, remote_file_copy)

        # md5sum remote file copy
        command = 'md5sum %s | awk \'{print $1}\'' % remote_file_copy
        rcode, rout, _ = g.run(host2, command)
        if rcode == 0:
            md5sum_copy = rout.strip()

        # compare the md5sums
        self.assertEqual(md5sum_orig, md5sum_copy, 'md5sums do not match')

    #@unittest.skip('generates a lot of traffic on stdout')
    @pytest.mark.skip(reason='generates a lot of traffic on stdout')
    def test_stress_stdout(self):
        """"Send load of text output to stdout"""
        command = '''ls -Rail /etc > /tmp/railetc
            for i in $(seq 1 1000)
            do
                cat /tmp/railetc
            done
            echo "Complete"
            '''
        g.disable_log_levels('INFO')
        rcode, rout, rerr = g.run(self.primary_host, command)
        g.reset_log_levels()
        self.assertEqual(rcode, 0, 'stressing stdout failed')
        self.assertNotEqual(rout, '', 'stdout has no content.')
        self.assertEqual(rerr, '', 'stderr has content.')

    #@unittest.skip('generates a lot of traffic on stderr')
    @pytest.mark.skip(reason='generates a lot of traffic on stderr')
    def test_stress_stderr(self):
        """Send load of text output to stderr"""
        command = '''ls -Rail /etc > /tmp/railetc
            for i in $(seq 1 1000)
            do
                cat /tmp/railetc >&2
            done
            echo "Complete" >&2
            '''
        g.disable_log_levels('INFO')
        rcode, rout, rerr = g.run(self.primary_host, command)
        g.reset_log_levels()
        self.assertEqual(rcode, 0, 'stressing stderr failed')
        self.assertEqual(rout, '', 'sdtout has content.')
        self.assertNotEqual(rerr, '', 'stderr has no content.')

    def tearDown(self):
        """Unittest tearDown override"""
        print "Tearing Down: %s" % self.id()

        return True

    @classmethod
    def tearDownClass(cls):
        """unittest tearDownClass override"""
        print "Tearing Down Class: %s" % cls.__name__
        g.run(cls.primary_host, 'rm -f /tmp/railetc')
        g.run(cls.primary_host, 'rm -f /tmp/upload_test_file')
        g.run(cls.hosts[1], 'rm -f /tmp/transfer_test_file')

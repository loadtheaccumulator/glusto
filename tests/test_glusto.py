""" test glusto basic functionality """
import unittest
import xmlrunner

from glusto.core import Glusto as g
# from glusto.volumes import Volumes as v

class TestGlustoBasics(unittest.TestCase):
    """Glusto basics test class"""
    @classmethod
    def setUpClass(cls):
        """unittest standard setUpClass method
        Runs before all test_ methods in the class
        """
        print "Setting Up Class: %s" % cls.__name__

    def setUp(self):
        """unittest standard setUp method
        Runs before each test_ method
        """
        print "Setting Up: %s" % self.id()
        config = g.load_configs(["../working/systems.yml",
                                 "../working/glusto.yml"])
        g.update_config(config)

        self.masternode = g.config["nodes"][0]
        self.client = g.config["clients"][0]

    def test_stderr(self):
        """Testing output to stderr"""
        print "Running: %s - %s" % (self.id(), self.shortDescription())
        rcode, rout, rerr = g.run(self.masternode, "uname -a >&2")
        self.assertEqual(rcode, 0)
        self.assertFalse(rout)
        self.assertTrue(rerr)

    def test_stdout(self):
        """Testing output to stdout"""
        print "Running: %s - %s" % (self.id(), self.shortDescription())
        # add a cleanup method to run after tearDown()
        self.addCleanup(self.cleanup_remote_commands)
        for node in g.config["nodes"]:
            rcode, rout, rerr = g.run(node, "ls -ld /etc")
        self.assertEqual(rcode, 0)
        self.assertTrue(rout)
        self.assertFalse(rerr)

    def cleanup_remote_commands(self):
        """Cleanup remote commands method
        Called after teardown for additional cleanup specific to this test
        """
        print "Cleaning up after setup on fail or after teardown"

    def test_return_code(self):
        """Testing the return code"""
        print "Running: %s - %s" % (self.id(), self.shortDescription())
        rcode, rout, rerr = g.run(self.masternode, "cat /etc/fstab")
        self.assertEqual(rcode, 0)
        self.assertTrue(rout)
        self.assertFalse(rerr)

    @unittest.skip("Example test skip")
    def test_skip_me(self):
        """Testing the unittest skip feature"""
        print "Running: %s - %s" % (self.id(), self.shortDescription())
        rcode, _, _ = g.run(self.masternode, "cat /etc/hosts")
        self.assertEqual(rcode, 0)

    def test_negative_test(self):
        """Testing an expected failure as negative test"""
        rcode, _, _ = g.run(self.masternode, "false")
        self.assertEqual(rcode, 1)

    def test_expected_fail(self):
        """Testing an expected failure. This test should fail"""
        rcode, _, _ = g.run(self.masternode, "false")
        self.assertEqual(rcode, 0)

    def tearDown(self):
        """Unittest tearDown override"""
        print "Tearing Down: %s" % self.id()

        return True

    @classmethod
    def tearDownClass(cls):
        """unittest tearDownClass override"""
        print "Tearing Down Class: %s" % cls.__name__

if __name__ == '__main__':
    # TODO: make this argable
    output_junit = False
    # unittest.main(verbosity=2)
    tsuite = unittest.TestLoader().loadTestsFromTestCase(TestGlustoBasics)
    if output_junit:
        trunner = xmlrunner.XMLTestRunner(output='/tmp/glustoreports')
    else:
        trunner = unittest.TextTestRunner(verbosity=2)
    trunner.run(tsuite)
    #results.testsRun

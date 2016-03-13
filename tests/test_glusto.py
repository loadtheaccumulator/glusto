""" test glusto basic functionality """
import unittest

from glusto.glusto import Glusto as g

class TestGlustoBasics(unittest.TestCase):
    """Glusto basics test class"""
    @classmethod
    def setUpClass(cls):
        """unittest standard setUpClass method
        Runs before all test_ methods in the class
        """
        print("Setting Up Class: %s" % cls.__name__)

    def setUp(self):
        """unittest standard setUp method
        Runs before each test_ method
        """
        print("Setting Up: %s" % self.id())
        pass

    def test_stderr(self):
        print("Running: %s - %s" % (self.id(), self.shortDescription()))
        rcode, _, _ = g.run("localhost", "uname -a >&2")
        self.assertEqual(rcode, 0)

    def test_stdout(self):
        """Remote Commands"""
        print("Running: %s - %s" % (self.id(), self.shortDescription()))
        # add a cleanup method to run after tearDown()
        self.addCleanup(self.cleanup_remote_commands)
        rcode, _, _ = g.run("localhost", "ls -ld /etc")
        self.assertEqual(rcode, 0)

    def cleanup_remote_commands(self):
        """Cleanup remote commands method
        Called after teardown for additional cleanup specific to this test
        """
        print("Cleaning up after setup on fail or after teardown")

    def test_return_code(self):
        print("Running: %s - %s" % (self.id(), self.shortDescription()))
        rcode, _, _ = g.run("localhost", "cat /etc/fstab")
        self.assertEqual(rcode, 0)

    def tearDown(self):
        print("Tearing Down: %s" % self.id())

        return True

    @classmethod
    def tearDownClass(cls):
        print("Tearing Down Class: %s" % cls.__name__)

if __name__ == '__main__':
    #unittest.main(verbosity=2)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGlustoBasics)
    unittest.TextTestRunner().run(suite)

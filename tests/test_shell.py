import unittest
import sys
from io import StringIO

from klickbrick import shell


class TestShell(unittest.TestCase):
    def setUp(self):
        self.held, sys.stdout = sys.stdout, StringIO()

    def test_execute_happy_path(self):
        return_value_code, return_value_stdout = shell.execute(
            ["echo", "hello"]
        )
        stdout_output = sys.stdout.getvalue()
        self.assertTrue("hello" in stdout_output)
        self.assertEqual(return_value_code, 0)
        self.assertTrue("hello" in return_value_stdout)

    def test_execute_sad_path(self):
        return_value_code, return_value_stdout = shell.execute(["foo"])
        stdout_output = sys.stdout.getvalue()
        self.assertTrue("Failed to execute" in stdout_output)
        self.assertGreater(return_value_code, 0)
        self.assertTrue("No such file or directory" in return_value_stdout)

    def test_execute_sad_path_ls(self):
        return_value_code, return_value_stdout = shell.execute(["ls", "foo"])
        stdout_output = sys.stdout.getvalue()
        self.assertTrue("No such file or directory" in stdout_output)
        self.assertGreater(return_value_code, 0)
        self.assertFalse(return_value_stdout)


if __name__ == "__main__":
    unittest.main()

import unittest
import sys

from klickbrick import klickbrick
from klickbrick import scripts


class TestCLI(unittest.TestCase):
    def test_construct_greeting(self):
        assert scripts.construct_greeting("david") == "Hello david"

    def test_parse_args(self):

        args = ["hello", "--name", "david"]
        old_sys_argv = sys.argv
        sys.argv = [old_sys_argv[0]] + args

        klickbrick.KlickBrick()

        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")
        output = (
            sys.stdout.getvalue().strip()
        )  # because stdout is a StringIO instance
        self.assertEquals(output, "Hello david")


if __name__ == "__main__":
    unittest.main()

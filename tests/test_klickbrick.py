import unittest
import sys

from klickbrick import klickbrick
from klickbrick import scripts


class TestCLI(unittest.TestCase):
    def test_construct_greeting(self):
        assert scripts.construct_greeting("Ole") == "Hello Ole"

    def test_parse_args(self):
        args = ["hello", "--name", "Ole"]
        klickbrick.KlickBrick(args)

        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")
        output = (
            sys.stdout.getvalue().strip()
        )  # because stdout is a StringIO instance
        self.assertEquals(output, "Hello Ole")


if __name__ == "__main__":
    unittest.main()

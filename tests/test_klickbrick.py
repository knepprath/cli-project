import unittest
from klick_brick_cli import klickbrick

class TestCLI(unittest.TestCase):

    def test_construct_greeting(self):
        assert klickbrick.construct_greeting("hello", "david") == "hello david"

    def test_parse_args(self):
        args = klickbrick.parse_args(['hello', '--name', 'david'])
        assert args.hello == 'hello'
        assert args.name == 'david'

if __name__ == '__main__':
    unittest.main()
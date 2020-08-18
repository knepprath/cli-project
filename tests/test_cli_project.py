import unittest
from cli_project import klick_brick_cli

class TestCLI(unittest.TestCase):

    def test_construct_greeting(self):
        assert klick_brick_cli.construct_greeting("hello", "david") == "hello david"

    def test_parse_args(self):
        args = klick_brick_cli.parse_args(['hello', '--name', 'david'])
        assert args.hello == 'hello'
        assert args.name == 'david'

if __name__ == '__main__':
    unittest.main()
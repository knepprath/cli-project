import argparse
import sys

from klickbrick import scripts


class KlickBrick(object):
    def __init__(self, arguments):
        self.parser = argparse.ArgumentParser(prog="klickbrick")
        self.subparsers = self.parser.add_subparsers()

        hello_parser = self.subparsers.add_parser(name="hello", description="A friendly Hello World")
        hello_parser.add_argument(
            "-n",
            "--name",
            type=str,
            default="World",
            help="Optional flag to be more friendly",
        )

        options = self.parser.parse_args(arguments)

        # invoke command with options
        getattr(self, arguments[0])(options)

    def hello(self, options):
        print(scripts.construct_greeting(options.name))


# Entry point for poetry so package is executable
def main():
    KlickBrick(sys.argv[1:])


# Support invoking the script directly from source
if __name__ == "__main__":
    main()

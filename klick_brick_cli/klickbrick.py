import argparse
import sys

class KlickBrick(object):

    def __init__(self):
        parser = argparse.ArgumentParser(prog='klickbrick')
        parser.add_argument('command')

        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def hello(self):
        parser = argparse.ArgumentParser(
            description='Record changes to the repository')
        parser.add_argument('--name',
                            '-n',
                            type=str,
                            default="world",
                            help="Optional flag to be more personal")

        args = parser.parse_args(sys.argv[2:])
        print(construct_greeting(args.name))

    def onboard(self):
        print("creating checklist")


def construct_greeting(name):
    return f"Hello {name}"


if __name__ == '__main__':
    KlickBrick()
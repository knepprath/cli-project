import argparse
import sys

def parse_args(args):
    parser = argparse.ArgumentParser()

    parser.add_argument('hello',
                        type=str,
                        help="Friendly command that says hello")
    parser.add_argument('--name',
                        '-n',
                        type=str,
                        default="world",
                        help="Optional flag to be more personal")
    return parser.parse_args(args)

def construct_greeting(message, name):
    return f"{message} {name}"

def main():
    args = parse_args(sys.argv[1:])

    if args.hello == "hello":
        print(construct_greeting(args.hello, args.name))

if __name__ == '__main__':
    main()
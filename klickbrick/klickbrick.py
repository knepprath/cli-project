import argparse
import sys
import os
import requests
import inspect
from pathlib import Path

from klickbrick import shell
from klickbrick import scripts

# TODO optimize imports
# TODO add proper logger

FRAMEWORKS = ["python"]


class KlickBrick(object):
    command_args = []

    def __init__(self):
        parser = argparse.ArgumentParser(prog="klickbrick")

        # Create base_subparser so subparsers can consume as parent and share common arguments
        self.base_subparser = argparse.ArgumentParser(add_help=False)
        self.base_subparser.add_argument(
            "-v",
            "--version",
            action="version",
            version=f"klickbrick {scripts.package_version()}",
        )
        self.base_subparser.add_argument(
            "-d",
            "--dry-run",
            action="store_true",
            help="Inspect what the result of the command will be without any side effects",
        )
        self.subparsers = parser.add_subparsers()

        # TODO config to enable metrics
        # send_metric(
        #     {
        #         "userId": "DK",
        #         "osPlatform": "mac os x",
        #         "osVersion": "10.15.6",
        #         "pythonVersion": "3.8.9",
        #         "command": {
        #             "input": " ".join(sys.argv[1:]),
        #             "exitReason": "blah",
        #             "exitCode": "0",
        #             "duration": "0m0.001s",
        #         },
        #     }
        # )

        # handle no arguments
        if len(sys.argv) <= 1:
            self.help()
        else:
            command = sys.argv[1]
            self.command_args = sys.argv[1:]
            # handle undefined arguments
            if not hasattr(self, command):
                self.help()
            else:
                # use dispatch pattern to invoke method with same name so it's easy to add new subcommands
                getattr(self, command)()

    # acknowladge the tradoff in my design here. I'm optimizing for it to be very easy to add new commands
    # that means I'm working a little bit against the built in help functinoality that is targeting a more straightforward approach.
    # But I still want a really robust help command. This is something that I build once, but new commands will be added more frequently.
    def help(self):
        parser = self.subparsers.add_parser(
            "help", parents=[self.base_subparser], add_help=False
        )
        parser.add_argument("help", nargs="?", help=argparse.SUPPRESS)
        parser.add_argument(
            "command",
            nargs="?",
            help="name of command to show usage for",
        )

        args, unknown = parser.parse_known_args()

        if args.help is None and args.command is None:
            print_available_commands(self)
        elif unknown:
            print(f"'{unknown}' is not a valid argument")
            parser.print_help()
            print_available_commands(self)
        elif args.help == "help" and args.command is None:
            parser.print_help()
            print_available_commands(self)
        elif "help" not in args.help:
            print(f"'{args.help}' is not a valid command")
            print_available_commands(self)
        elif not hasattr(self, args.command):
            print(f"{args.command} is not a valid argument")
            print_available_commands(self)
        else:
            self.command_args.append("-h")
            getattr(self, args.command)()

    def hello(self):
        parser = self.subparsers.add_parser(
            "hello", parents=[self.base_subparser]
        )
        parser.add_argument(
            "-n",
            "--name",
            type=str,
            default="world",
            help="optional flag to be more personal",
        )
        args = parser.parse_args(self.command_args[1:])
        print(scripts.construct_greeting(args.name))

    def init(self):
        parser = self.subparsers.add_parser(
            "init",
            parents=[self.base_subparser],
            description="Initialize a new code repository with standard conventions",
        )
        parser.add_argument(
            "-p",
            "--path",
            type=str,
            default=os.getcwd(),
            help="Path to location that the code repository should be created. Defaults to the current working directory",
        )
        parser.add_argument(
            "-f",
            "--framework",
            type=str,
            default="python",
            help="Language framework that this code repository will use",
        )
        required_arguments = parser.add_argument_group("required arguments")
        required_arguments.add_argument(
            "-n",
            "--name",
            type=str,
            required=True,
            help="Name of the new code repository",
        )

        args = parser.parse_args(self.command_args[1:])

        if args.framework in FRAMEWORKS:
            getattr(self, "init_" + args.framework)(args.path, args.name)
        else:
            print(
                f"the supported frameworks for the init command are {FRAMEWORKS}"
            )

    # TODO we don't want this in the class because we don't want to treat it like an actual subcommand
    def init_python(self, parent, name):
        path = parent + "/" + name
        path = os.path.expanduser(path)
        print(f"creating python project at {path}")

        try:
            Path(path).mkdir(parents=True)
        except FileExistsError:
            print(
                f"ERROR: Cannot create project. The directory already exits: {path}"
            )
            return

        return_code, output = shell.execute(["git", "init", f"{path}"])

    def onboard(self):
        parser = self.subparsers.add_parser(
            "onboard",
            parents=[self.base_subparser],
            description="Installs and configures all software needed by new developers",
        )
        parser.add_argument(
            "--checklist",
            action="store_true",
            help="Generate a checklist for new developers to effectively complete onboarding process",
        )
        parser.add_argument(
            "--it-request",
            action="store_true",
            help="Creates and email draft with for the IT department to complete onboarding process with custom information provided by new employee",
        )
        parser.add_argument(
            "--dev-tools",
            nargs="?",
            default=False,
            const=True,
            help="[DEV_TOOLS] is optional argument to install and configure a single tool",
        )

        required_arguments = parser.add_argument_group(
            "required arguments for --it-request and --dev-tools"
        )
        required_arguments.add_argument("--first-name")
        required_arguments.add_argument("--last-name")

        args = parser.parse_args(self.command_args[1:])

        if args.checklist is True:
            print("creating checklist")
            scripts.write_checklist()
        # All other options require additional flags
        elif args.first_name is not None and args.last_name is not None:
            if args.it_request is True:
                print("submitting it request")
                scripts.send_it_email(args.first_name, args.last_name)
            elif args.dev_tools is not False:
                print("installing dev tools")
                scripts.install_dev_tools(
                    args.dev_tools, args.first_name, args.last_name
                )
            else:
                # TODO better algo to solve this so it's more maintainable
                print(
                    "creating checklist, submitting it request, and installing dev tools"
                )
                scripts.write_checklist()
                scripts.send_it_email(args.first_name, args.last_name)
                scripts.install_dev_tools(
                    True, args.first_name, args.last_name
                )
        else:
            print("missing required args")


def send_metric(metric):
    payload = {"metrics": [metric]}

    try:
        requests.post(
            "http://localhost:8080/metrics", json=payload, timeout=2000
        )
    except requests.exceptions.Timeout as ex:
        print(str(ex))


def print_available_commands(cli):
    print("List of available subcommands are:")
    print(
        [attr for attr in dir(cli) if inspect.ismethod(getattr(cli, attr))][1:]
    )


# Entry point for poetry so package is executable
def main():
    KlickBrick()


# Support invoking the script directly from source
if __name__ == "__main__":
    main()

import argparse
import sys
import os
import requests
import inspect
import logging

from klickbrick import config
from klickbrick import scripts

# TODO optimize imports

# TODO Make log level configurable
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class KlickBrick(object):
    command_args = []

    def __init__(self, arguments):
        self.arguments = arguments
        parser = argparse.ArgumentParser(prog="klickbrick")
        # Create base_subparser so subparsers can consume as parent and share common arguments
        self.base_subparser = argparse.ArgumentParser(add_help=False)
        self.base_subparser.add_argument(
            "-v",
            "--version",
            action="version",
            version=f"%(prog)s {scripts.package_version()}",
        )
        self.base_subparser.add_argument(
            "-d",
            "--dry-run",
            action="store_true",
            help="Inspect what the result of the command will be without any side effects",
        )

        args, unknown = self.base_subparser.parse_known_args(self.arguments)
        if args.dry_run is True:
            logging.debug("Enabling dry run mode")
            config.DRY_RUN = True

        self.subparsers = parser.add_subparsers()

        # TODO config to enable metrics
        # send_metric(
        #     {
        #         "userId": "DK",
        #         "osPlatform": "mac os x",
        #         "osVersion": "10.15.6",
        #         "pythonVersion": "3.8.9",
        #         "command": {
        #             "input": " ".join(arguments[1:]),
        #             "exitReason": "blah",
        #             "exitCode": "0",
        #             "duration": "0m0.001s",
        #         },
        #     }
        # )

        # handle no arguments
        if len(arguments) == 0:
            self.help()
        else:
            command = arguments[0]
            self.command_args = arguments[1:]
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

        args, unknown = parser.parse_known_args(self.arguments)

        if args.help is None and args.command is None:
            print_available_commands(self)
        elif unknown:
            logging.error(f"'{unknown}' is not a valid argument")
            parser.print_help()
            print_available_commands(self)
        elif args.help == "help" and args.command is None:
            parser.print_help()
            print_available_commands(self)
        elif "help" not in args.help:
            logging.error(f"'{args.help}' is not a valid command")
            print_available_commands(self)
        elif not hasattr(self, args.command):
            logging.error(f"'{args.command}' is not a valid argument")
            print_available_commands(self)
        else:
            self.command_args.append("-h")
            try:
                getattr(self, args.command)()
            # TODO Because I am augmenting argparse help I don't want argparse to do system exit as this breaks ability to test
            # Consider a better solution https://stackoverflow.com/questions/5943249/python-argparse-and-controlling-overriding-the-exit-status-code
            except SystemExit:
                pass

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
        args = parser.parse_args(self.command_args)
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

        args = parser.parse_args(self.command_args)

        if "python" in args.framework:
            scripts.init_python(args.path, args.name)
        else:
            logging.warning(f"Python is currently the only supported language")

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

        args = parser.parse_args(self.command_args)

        if args.checklist is True:
            logging.info("creating checklist")
            scripts.write_checklist()
        # All other options require additional flags
        elif args.first_name is not None and args.last_name is not None:
            if args.it_request is True:
                logging.info("submitting it request")
                scripts.send_it_email(args.first_name, args.last_name)
            elif args.dev_tools is not False:
                logging.info("installing dev tools")
                scripts.install_dev_tools(
                    args.dev_tools, args.first_name, args.last_name
                )
            else:
                # TODO better algo to solve this so it's more maintainable
                logging.info(
                    "creating checklist, submitting it request, and installing dev tools"
                )
                scripts.write_checklist()
                scripts.send_it_email(args.first_name, args.last_name)
                scripts.install_dev_tools(
                    True, args.first_name, args.last_name
                )
        else:
            logging.error("missing required args")


def send_metric(metric):
    payload = {"metrics": [metric]}

    try:
        requests.post(
            "http://localhost:8080/metrics", json=payload, timeout=2000
        )
    except requests.exceptions.Timeout as ex:
        logging.error(str(ex))


def print_available_commands(cli):
    print("List of available commands are:")
    print(
        [attr for attr in dir(cli) if inspect.ismethod(getattr(cli, attr))][1:]
    )


# Entry point for poetry so package is executable
def main():
    config.initialize()
    KlickBrick(sys.argv[1:])


# Support invoking the script directly from source
if __name__ == "__main__":
    main()

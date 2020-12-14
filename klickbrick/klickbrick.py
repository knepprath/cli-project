import argparse
import sys
import os
import inspect
import logging

import requests

from klickbrick import config
from klickbrick import scripts

# TODO Make log level configurable
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class KlickBrick(object):
    def __init__(self, arguments):
        parser = argparse.ArgumentParser(prog="klickbrick")
        # Create base subparser so parsers can consume it as parent and share common arguments
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

        args, unknown = self.base_subparser.parse_known_args(arguments)
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
            self.help(arguments)
        else:
            command = arguments[0]
            # handle undefined command
            if not hasattr(self, command):
                self.help(arguments)
            else:
                # use dispatch pattern to invoke method with same name so it's easy to add new subcommands
                getattr(self, command)(arguments)

    # Design Decision Tradeoff
    # Optimizing for being easy to add new commands but with robust help functionality.
    # Augmenting the default help adds one time complexity, but all new commands will benefit.
    def help(self, arguments):
        parser = self.__create_parser(
            "help", "Instructions for using the klickbrick CLI"
        )
        parser.add_argument("help", nargs="?", help=argparse.SUPPRESS)
        parser.add_argument(
            "command",
            nargs="?",
            help="name of command to show usage for",
        )

        # Handle unknown arguments
        args, unknown = parser.parse_known_args(arguments)

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
            arguments.append("-h")
            try:
                getattr(self, args.command)(arguments)
            # TODO Because I am augmenting the built in help I don't want argparse to do system exit as this breaks ability to test
            # Consider a better solution https://stackoverflow.com/questions/5943249/python-argparse-and-controlling-overriding-the-exit-status-code
            except SystemExit:
                pass

    def hello(self, arguments):
        parser = self.__create_parser("hello", "A friendly Hello World")
        parser.add_argument(
            "-n",
            "--name",
            type=str,
            default="world",
            help="Optional flag to be more friendly",
        )
        args = parser.parse_args(arguments[1:])
        print(scripts.construct_greeting(args.name))

    def init(self, arguments):
        parser = self.__create_parser(
            "init",
            "Initialize a new code repository with standard conventions",
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

        args = parser.parse_args(arguments[1:])

        if "python" in args.framework:
            scripts.init_python(args.path, args.name)
        else:
            logging.warning(f"Python is currently the only supported language")

    def onboard(self, arguments):
        parser = self.__create_parser(
            "onboard",
            "Installs and configures all software needed by new developers",
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

        args = parser.parse_args(arguments[1:])

        if args.checklist is True:
            logging.info("creating checklist")
            scripts.write_checklist()
        # All other options require additional flags
        # TODO refactor to be more maintainable
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

    def __create_parser(self, name, description):
        parser = self.subparsers.add_parser(
            name=name,
            parents=[self.base_subparser],
            description=description,
        )
        return parser


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

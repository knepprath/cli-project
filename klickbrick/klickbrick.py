import argparse
import sys
import os
import logging
import platform
from datetime import datetime

import requests

from klickbrick import config
from klickbrick import scripts

# TODO Make log level user configurable
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# TODO make telemetry user configurable
ENABLE_TELEMETRY = True


class KlickBrick(object):
    def __init__(self, arguments):
        self.parser = argparse.ArgumentParser(prog="klickbrick")
        self.parser.add_argument(
            "-v",
            "--version",
            action="version",
            version=f"%(prog)s {scripts.package_version()}",
        )
        # Create base subparser so parsers can consume it as parent and share common arguments
        base_subparser = argparse.ArgumentParser(add_help=False)
        base_subparser.add_argument(
            "-d",
            "--dry-run",
            action="store_true",
            help="Inspect what the result of the command will be without any side effects",
        )

        self.subparsers = self.parser.add_subparsers()
        self.subparsers.add_parser(
            name="help",
            parents=[base_subparser],
            description="Document usage of the CLI",
        )

        hello_parser = self.subparsers.add_parser(
            name="hello",
            parents=[base_subparser],
            description="A friendly Hello World",
        )
        hello_parser.add_argument(
            "-n",
            "--name",
            type=str,
            default="World",
            help="Optional flag to be more friendly",
        )

        init_parser = self.subparsers.add_parser(
            name="init",
            parents=[base_subparser],
            description="Initialize a new code repository with standard conventions",
        )
        init_parser.add_argument(
            "-p",
            "--path",
            type=str,
            default=os.getcwd(),
            help="Path to location that the code repository should be created. Defaults to the current working directory",
        )
        init_required_arguments = init_parser.add_argument_group(
            "required arguments"
        )
        init_required_arguments.add_argument(
            "-n",
            "--name",
            type=str,
            required=True,
            help="Name of the new code repository",
        )

        onboard_parser = self.subparsers.add_parser(
            name="onboard",
            parents=[base_subparser],
            description="Configures all software needed by new developers",
        )
        onboard_parser.add_argument(
            "--dev-tools",
            nargs="?",
            default=False,
            const=True,
            help="[DEV_TOOLS] is optional argument to install and configure a single tool",
        )

        onboard_required_arguments = onboard_parser.add_argument_group(
            "required arguments for --dev-tools"
        )
        onboard_required_arguments.add_argument("--first-name")
        onboard_required_arguments.add_argument("--last-name")

        # Handle no arguments
        if len(arguments) == 0:
            self.parser.print_help(sys.stderr)
            sys.exit(1)

        try:
            options = self.parser.parse_args(arguments)
        # Handle invalid arguments
        except AttributeError:
            self.parser.print_help()
            sys.exit(0)

        if options.dry_run is True:
            logging.debug("Enabling dry run mode")
            config.DRY_RUN = True

        getattr(self, arguments[0])(options)

        if ENABLE_TELEMETRY:
            send_metric(arguments)

    def hello(self, options):
        print(scripts.construct_greeting(options.name))

    def help(self, options):
        self.parser.print_help()

    def init(self, options):
        scripts.init_generic(options.path, options.name)

    def onboard(self, options):
        # TODO refactor to be more maintainable
        if options.first_name is not None and options.last_name is not None:
            if options.dev_tools is not False:
                scripts.config_dev_tools(
                    options.dev_tools, options.first_name, options.last_name
                )
            else:
                logging.info("Performing all onboarding tasks")
                scripts.config_dev_tools(
                    True, options.first_name, options.last_name
                )
        else:
            logging.error("missing required args")


def send_metric(cli_input):
    # TODO capture exit reason and duration
    payload = {
        "metrics": [
            {
                "userId": os.getlogin(),
                "osPlatform": platform.system(),
                "osVersion": platform.version(),
                "pythonVersion": sys.version,
                "command": {
                    "input": " ".join(cli_input),
                    "exitReason": "Not Implemented",
                    "exitCode": "Not Implemented",
                    "duration": "Not Implemented",
                    "timestamp": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                },
            }
        ]
    }

    try:
        requests.post(
            "http://localhost:8080/metrics", json=payload, timeout=2000
        )
    except requests.exceptions.RequestException as exception:
        logging.debug(str(exception))


# Entry point for poetry so package is executable
def main():
    config.initialize()
    KlickBrick(sys.argv[1:])


# Support invoking the script directly from source
if __name__ == "__main__":
    main()

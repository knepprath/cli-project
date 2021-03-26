import argparse
import sys

from klickbrick import config
from klickbrick import scripts


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
        # This allows all commands to inherit the --dry-run flag as if it's their own argument
        self.base_subparser = argparse.ArgumentParser(add_help=False)
        self.base_subparser.add_argument(
            "-d",
            "--dry-run",
            action="store_true",
            help="Inspect what the result of the command will be without any side effects",
        )

        self.subparsers = self.parser.add_subparsers()

        self.add_hello_parser()
        self.add_onboard_parser()

        options = self.parser.parse_args(arguments)

        if options.dry_run is True:
            config.DRY_RUN = True

        # invoke command with options
        getattr(self, arguments[0])(options)

    def create_parser(self, name, description):
        return self.subparsers.add_parser(
            name=name, parents=[self.base_subparser], description=description
        )

    def add_hello_parser(self):
        hello_parser = self.create_parser("hello", "A friendly Hello World")
        hello_parser.add_argument(
            "-n",
            "--name",
            type=str,
            default="World",
            help="Optional flag to be more friendly",
        )

    def add_onboard_parser(self):
        onboard_parser = self.create_parser(
            "onboard", "Configures all software needed by new developers"
        )
        onboard_parser.add_argument(
            "--dev-tools",
            nargs="?",
            choices=["git"],
            default=False,
            const=True,
            help="[DEV_TOOLS] is optional argument to install and configure a single tool",
        )

        onboard_required_arguments = onboard_parser.add_argument_group(
            "required arguments for --dev-tools"
        )
        onboard_required_arguments.add_argument(
            "--first-name", type=str, required=True
        )
        onboard_required_arguments.add_argument(
            "--last-name", type=str, required=True
        )

    def hello(self, options):
        print(scripts.construct_greeting(options.name))

    def onboard(self, options):
        if options.dev_tools is not False:
            scripts.config_dev_tools(
                options.dev_tools, options.first_name, options.last_name
            )
        else:
            scripts.config_dev_tools(
                True, options.first_name, options.last_name
            )
            # ...invoke scripts for additional onboarding tasks


# Entry point for poetry so package is executable
def main():
    config.initialize()
    KlickBrick(sys.argv[1:])


# Support invoking the script directly from source
if __name__ == "__main__":
    main()

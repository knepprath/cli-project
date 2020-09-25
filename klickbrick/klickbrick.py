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
    def __init__(self):
        parser = argparse.ArgumentParser(prog="klickbrick")
        parser.add_argument(
            "invoke", nargs="?", help="you must provide a valid subcommand"
        )
        parser.add_argument(
            "-v",
            "--version",
            action="version",
            version=f"%(prog)s {scripts.package_version()}",
        )

        # TODO add scenario for invalid arg
        # TODO if no arg print message accordingly and invoke help, add scenario for this too

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

        subcommand = parser.parse_args(sys.argv[1:2])
        self.subcommand_args = sys.argv[1:]

        if not sys.argv[1:2]:
            self.help()
        elif not hasattr(self, subcommand.invoke):
            self.subcommand_args.append(subcommand.invoke)
            self.help()
        else:
            # use dispatch pattern to invoke method with same name
            getattr(self, subcommand.invoke)()

    def help(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "help", nargs="?", help="show usage for subcommands"
        )
        parser.add_argument(
            "subcommand",
            nargs="?",
            help="name of subcommand to show usage for",
        )
        args = parser.parse_args(self.subcommand_args)

        if args.subcommand is None:
            parser.print_help()
            print("List of available commands:")
            print(
                [
                    attr
                    for attr in dir(self)
                    if inspect.ismethod(getattr(self, attr))
                ][1:]
            )
        elif not hasattr(self, args.subcommand):
            print(f"{args.subcommand} is invalid command")
            print("List of available commands:")
            print(
                [
                    attr
                    for attr in dir(self)
                    if inspect.ismethod(getattr(self, attr))
                ][1:]
            )
        else:
            self.subcommand_args.append("-h")
            getattr(self, args.subcommand)()

    def hello(self):
        parser = argparse.ArgumentParser(description="Hello World command")
        parser.add_argument(
            "-n",
            "--name",
            type=str,
            default="world",
            help="optional flag to be more personal",
        )

        args = parser.parse_args(self.subcommand_args[1:])
        print(scripts.construct_greeting(args.name))

    def init(self):
        parser = argparse.ArgumentParser(
            description="Initialize a new code repository according with standard conventions"
        )
        parser.add_argument(
            "-n",
            "--name",
            type=str,
            required=True,
            help="Name of the new code repository",
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

        args = parser.parse_args(self.subcommand_args[1:])

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
        parser = argparse.ArgumentParser(
            description="Installs and configures all software needed by new developers"
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

        parser.add_argument("--first-name")
        parser.add_argument("--last-name")

        args = parser.parse_args(self.subcommand_args[1:])

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


# Entry point for poetry so package is executable
def main():
    KlickBrick()


# Support invoking the script directly from source
if __name__ == "__main__":
    main()

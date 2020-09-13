import argparse
import sys
import os
import shutil
import requests
import urllib.request
import inspect
from pathlib import Path

import shell
import brew

# TODO optimize imports
# TODO add proper logger

PYTHON_VERSION = "3.8.0"

FRAMEWORKS = ["python"]


class KlickBrick(object):
    def __init__(self):
        parser = argparse.ArgumentParser(prog="klickbrick")
        parser.add_argument("invoke")

        send_metric(
            {
                "userId": "DK",
                "osPlatform": "mac os x",
                "osVersion": "10.15.6",
                "pythonVersion": "3.8.9",
                "command": {
                    "input": " ".join(sys.argv[1:]),
                    "exitReason": "blah",
                    "exitCode": "0",
                    "duration": "0m0.001s",
                },
            }
        )

        subcommand = parser.parse_args(sys.argv[1:2])
        self.subcommand_args = sys.argv[1:]

        if not hasattr(self, subcommand.invoke):
            print("Unrecognized command")
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, subcommand.invoke)()

    def help(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("help", help="Optional flag to be more personal")
        parser.add_argument("name", nargs="?", help="Command to show help for")
        args = parser.parse_args(self.subcommand_args)

        if args.name:
            self.subcommand_args.append("-h")
            getattr(self, args.name)()
        else:
            print("Use help [name] to show help for given command")
            print("List of available commands:")
            print(
                [
                    attr
                    for attr in dir(self)
                    if inspect.ismethod(getattr(self, attr))
                ][1:]
            )

    def hello(self):
        parser = argparse.ArgumentParser(
            description="Record changes to the repository"
        )
        parser.add_argument(
            "--name",
            "-n",
            type=str,
            default="world",
            help="Optional flag to be more personal",
        )

        args = parser.parse_args(self.subcommand_args[1:])
        print(construct_greeting(args.name))

    def init(self):
        parser = argparse.ArgumentParser(
            description="Initialize a new code repository according with standard conventions"
        )
        parser.add_argument(
            "--name",
            "-n",
            type=str,
            required=True,
            help="Name of the new code repository",
        )
        parser.add_argument(
            "--path",
            "-p",
            type=str,
            default=os.getcwd(),
            help="Path to location that the code repository should be created. Defaults to the current working directory",
        )
        parser.add_argument(
            "--framework",
            "-f",
            type=str,
            default="python",
            help="Language framework that this code repository will use",
        )

        args = parser.parse_args(self.subcommand_args[1:])

        if args.framework in FRAMEWORKS:
            getattr(self, "init_" + args.framework)(args.path, args.name)
        else:
            print(
                f"the suppored frameworks for the init command are {FRAMEWORKS}"
            )

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
            write_checklist()
        # All other options require additional flags
        elif args.first_name is not None and args.last_name is not None:
            if args.it_request is True:
                print("submitting it request")
                send_it_email(args.first_name, args.last_name)
            elif args.dev_tools is not False:
                print("installing dev tools")
                install_dev_tools(
                    args.dev_tools, args.first_name, args.last_name
                )
            else:
                # TODO better algo to solve this so it's more maintainable
                print(
                    "creating checklist, submitting it request, and installing dev tools"
                )
                write_checklist()
                send_it_email(args.first_name, args.last_name)
                install_dev_tools(True, args.first_name, args.last_name)
        else:
            print("missing required args")


def construct_greeting(name):
    return f"Hello {name}"


def write_checklist():
    shutil.copyfile(
        f"{os.path.dirname(os.path.abspath(__file__))}/resources/onboard_checklist_template.md",
        f"{os.getcwd()}/onboarding_checklist.md",
    )


def send_it_email(first_name, last_name):
    address = "it@example.com"
    subject = "subject of email"

    body = f"The user {first_name} {last_name} is being onboarded"
    print(body)

    url = "mailto:{}?subject={}&body={}"
    url = url.format(address, subject, body)

    # TODO put this in a try and assert that exception is not thrown in test
    if sys.platform == "darwin":
        return_code, output = shell.execute(["open", url])


def install_dev_tools(selection, first_name, last_name):
    install_brew()

    if selection == "git" or selection is True:
        brew.install("git")
        configure_git(first_name, last_name)
    elif selection == "pyenv" or selection is True:
        brew.install("pyenv")
        configure_python()
    elif selection == "poetry" or selection is True:
        install_poetry()
        configure_poetry_repository()


def install_brew():
    return_code, output = shell.execute(["brew", "--version"])

    if return_code == 0:
        print("WARNING : brew is already installed")
    else:
        (fn, hd) = urllib.request.urlretrieve(
            "https://raw.githubusercontent.com/Homebrew/install/master/install.sh"
        )
        return_code, output = shell.execute(["bash", fn])


def configure_git(first_name, last_name):
    return_code, output = shell.execute(
        [
            "git",
            "config",
            "--global",
            "user.name",
            first_name + " " + last_name,
        ]
    )

    if return_code != 0:
        print("ERROR : git user.name was not configured")

    shutil.copyfile(
        f"{os.path.dirname(os.path.abspath(__file__))}/resources/git_commit_template",
        f"{str(Path.home())}/.gitmessage",
    )

    return_code, output = shell.execute(
        [
            "git",
            "config",
            "--global",
            "commit.template",
            f"{str(Path.home())}/.gitmessage",
        ]
    )

    if return_code != 0:
        print("ERROR : git commit.template was not configured")


def configure_python():
    return_code, output = shell.execute(["pyenv", "global"])

    if PYTHON_VERSION in output:
        print(f"Python {PYTHON_VERSION} is already configured as global")
    else:
        f = open(f"{str(Path.home())}/.zshrc", "a")
        f.write("# *** pyenv configuration ***\n")
        f.write('export PYENV_ROOT="$HOME/.pyenv"\n')
        f.write('export PATH="$PYENV_ROOT/bin:$PATH"\n')
        f.write(
            'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi\n'
        )
        f.close()

        return_code, output = shell.execute(
            ["pyenv", "install", PYTHON_VERSION]
        )

        return_code, output = shell.execute(
            ["pyenv", "global", PYTHON_VERSION]
        )


def install_poetry():
    (fn, hd) = urllib.request.urlretrieve(
        "https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py"
    )

    return_code, output = shell.execute(["python", fn])

    f = open(f"{str(Path.home())}/.zshrc", "a")
    f.write("# *** poetry configuration ***\n")
    f.write('export PATH="$HOME/.poetry/bin:$PATH"\n')
    f.close()


def configure_poetry_repository():
    return_code, output = shell.execute(
        [
            f"{str(Path.home())}/.poetry/bin/poetry",
            "config",
            "repositories.klickbrick",
            "https://klick.brick/simple/",
        ]
    )


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

import argparse
import sys
import os
import shutil
import subprocess
import urllib.request
import inspect
from pathlib import Path

# TODO optimize imports
# TODO add proper logger

PYTHON_VERSION = "3.8.0"


class KlickBrick(object):

    def __init__(self):
        parser = argparse.ArgumentParser(prog='klickbrick')
        parser.add_argument('invoke')

        subcommand = parser.parse_args(sys.argv[1:2])
        self.subcommand_args = sys.argv[1:]

        if not hasattr(self, subcommand.invoke):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, subcommand.invoke)()

    def help(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('help',
                            help="Optional flag to be more personal")
        parser.add_argument(
            'name',
            nargs='?',
            help='Command to show help for'
        )
        args = parser.parse_args(self.subcommand_args)

        if args.name:
            self.subcommand_args.append('-h')
            getattr(self, args.name)()
        else:
            print("Use help [name] to show help for given command")
            print("List of available commands:")
            print([attr for attr in dir(self) if inspect.ismethod(getattr(self, attr))][1:])

    def hello(self):
        parser = argparse.ArgumentParser(
            description='Record changes to the repository')
        parser.add_argument('--name',
                            '-n',
                            type=str,
                            default="world",
                            help="Optional flag to be more personal")

        args = parser.parse_args(self.subcommand_args[1:])
        print(construct_greeting(args.name))

    def onboard(self):
        parser = argparse.ArgumentParser(description='Installs and configures all software needed by new developers')
        parser.add_argument('--checklist',
                            action='store_true',
                            help="Generate a checklist for new developers to effectively complete onboarding process")
        parser.add_argument('--it-request',
                            action='store_true',
                            help="Creates and email draft with for the IT department to complete onboarding process with custom information provided by new employee")
        parser.add_argument('--dev-tools',
                            nargs='?',
                            default=False,
                            const=True,
                            help="[DEV_TOOLS] is optional argument to install and configure a single tool")

        parser.add_argument('--first-name')
        parser.add_argument('--last-name')

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
                install_dev_tools(args.dev_tools, args.first_name, args.last_name)
            else:
                # TODO better algo to solve this so it's more maintainable
                print("creating checklist, submitting it request, and installing dev tools")
                write_checklist()
                send_it_email(args.first_name, args.last_name)
                install_dev_tools(True, args.first_name, args.last_name)
        else:
            print("missing required args")


def construct_greeting(name):
    return f"Hello {name}"


def write_checklist():
    shutil.copyfile(f"{os.path.dirname(os.path.abspath(__file__))}/resources/onboard_checklist_template.md", f"{os.getcwd()}/onboarding_checklist.md")


def send_it_email(first_name, last_name):
    address = "it@example.com"
    subject = "subject of email"

    body = f"The user {first_name} {last_name} is being onboarded"
    print(body)

    url = "mailto:{}?subject={}&body={}"
    url = url.format(address, subject, body)

    # TODO put this in a try and assert that exception is not thrown in test
    if sys.platform=='darwin':
        subprocess.Popen(['open', url])


def install_dev_tools(selection, first_name, last_name):
    install_brew()

    if selection == "git" or selection is True:
        brew_install("git")
        configure_git(first_name, last_name)
    elif selection == "pyenv" or selection is True:
        brew_install("pyenv")
        configure_python()
    elif selection == "poetry" or selection is True:
        install_poetry()
        configure_poetry_repository()


def install_brew():
    output_brew_version= subprocess.check_output(['brew','--version'])
    print(output_brew_version)

    process = subprocess.Popen(["brew", "--version"],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode == 0:
        print("brew is already installed")
    else:
        (fn,hd) = urllib.request.urlretrieve('https://raw.githubusercontent.com/Homebrew/install/master/install.sh')
        process = subprocess.Popen(['bash', fn],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        print(stdout)


def configure_git(first_name, last_name):
    process = subprocess.Popen(['git', 'config', '--global', 'user.name', first_name + " " + last_name],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        print(stderr)
    else:
        print("git user.name configured")

    shutil.copyfile(f"{os.path.dirname(os.path.abspath(__file__))}/resources/git_commit_template", f"{str(Path.home())}/.gitmessage")

    process = subprocess.Popen(['git', 'config', '--global', 'commit.template', f"{str(Path.home())}/.gitmessage"],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print(stdout)


def configure_python():
    process = subprocess.Popen(["pyenv", "global"],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if (PYTHON_VERSION in stdout.decode("utf-8")):
        print(f"Python {PYTHON_VERSION} is already configured as global")
    else:
        f = open(f"{str(Path.home())}/.zshrc", "a")
        f.write("# *** pyenv configuration ***\n")
        f.write('export PYENV_ROOT=\"$HOME/.pyenv\"\n')
        f.write('export PATH=\"$PYENV_ROOT/bin:$PATH\"\n')
        f.write('if command -v pyenv 1>/dev/null 2>&1; then\n  eval \"$(pyenv init -)\"\nfi\n')
        f.close()

        process = subprocess.Popen(["pyenv", "install", PYTHON_VERSION],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        print(stdout)

        process = subprocess.Popen(["pyenv", "global", PYTHON_VERSION],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        print(stdout)


def install_poetry():
    (fn,hd) = urllib.request.urlretrieve('https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py')
    process = subprocess.Popen(['python', fn],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    f = open(f"{str(Path.home())}/.zshrc", "a")
    f.write("# *** poetry configuration ***\n")
    f.write('export PATH=\"$HOME/.poetry/bin:$PATH\"\n')
    f.close()


def configure_poetry_repository():
    process = subprocess.Popen([f"{str(Path.home())}/.poetry/bin/poetry", "config", "repositories.klickbrick", "https://klick.brick/simple/"],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print(stdout)


def brew_install(package_name):
    process = subprocess.Popen([package_name],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode == 0:
        print(f"The package {package_name} is already installed")
    else:
        process = subprocess.Popen(['brew', 'install', package_name],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print(stderr)
        else:
            print(f"{package_name} installed")
            process = subprocess.Popen([package_name, '--version'],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            print(stdout)


# Entry point for poetry so package is executable
def main():
    KlickBrick()


# Support invoking the script directly from source
if __name__ == '__main__':
    main()
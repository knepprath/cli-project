import argparse
import sys
import os
import shutil
import subprocess

# TODO optimize imports
# TODO add proper logger

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
        parser = argparse.ArgumentParser(
            description='Record changes to the repository')
        parser.add_argument('--checklist', action='store_true')
        parser.add_argument('--it-request', action='store_true')
        parser.add_argument('--dev-tools', action='store_true')

        parser.add_argument('--first-name')
        parser.add_argument('--last-name')

        args = parser.parse_args(sys.argv[2:])

        if args.checklist is True:
            print("creating checklist")
            write_checklist()
        # All other options require additional flags
        elif args.first_name is not None and args.last_name is not None:
            if args.it_request is True:
                print("submitting it request")
                send_it_email(args.first_name, args.last_name)
            elif args.dev_tools is True:
                print("installing dev tools")
                install_dev_tools()
            else:
                print("creating checklist, submitting it request, and installing dev tools")
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

    # TODO put this in a try and assert that exception is not thrown
    if sys.platform=='darwin':
        subprocess.Popen(['open', url])


def install_dev_tools():
    try:
        output_brew_version= subprocess.check_output(['brew','--version'])
        print(output_brew_version)
    except:
        print("please first install brew") #TODO install brew with curl requires sudo prompt

    process = subprocess.Popen(['brew', 'install', 'git'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(stderr)
    else:
        print("git installed")
        process = subprocess.Popen(['git', '--version'],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        print(stdout)


if __name__ == '__main__':
    KlickBrick()
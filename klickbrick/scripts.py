import sys
import os
from pathlib import Path

from klickbrick import brew
from klickbrick import shell

PYTHON_VERSION = "3.8.0"
USER_HOME_DIRECTORY = str(Path.home())
USER_CURRENT_WORKING_DIRECTORY = os.getcwd()


def construct_greeting(name):
    return f"Hello {name}"


def write_checklist():
    shell.copy_file(
        source="onboard_checklist_template.md",
        destination=f"{USER_CURRENT_WORKING_DIRECTORY}/onboarding_checklist.md",
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
        shell.install_from_url(
            executor="bash",
            url="https://raw.githubusercontent.com/Homebrew/install/master/install.sh",
        )


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

    shell.copy_file(
        source="git_commit_template",
        destination=f"{USER_HOME_DIRECTORY}/.gitmessage",
    )

    return_code, output = shell.execute(
        [
            "git",
            "config",
            "--global",
            "commit.template",
            f"{USER_HOME_DIRECTORY}/.gitmessage",
        ]
    )

    if return_code != 0:
        print("ERROR : git commit.template was not configured")


def configure_python():
    return_code, output = shell.execute(["pyenv", "global"])

    if PYTHON_VERSION in output:
        print(f"Python {PYTHON_VERSION} is already configured as global")
    else:
        f = open(f"{USER_HOME_DIRECTORY}/.zshrc", "a")
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
    shell.install_from_url(
        executor="python",
        url="https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py",
    )

    f = open(f"{USER_HOME_DIRECTORY}/.zshrc", "a")
    f.write("# *** poetry configuration ***\n")
    f.write('export PATH="$HOME/.poetry/bin:$PATH"\n')
    f.close()


def configure_poetry_repository():
    return_code, output = shell.execute(
        [
            f"{USER_HOME_DIRECTORY}/.poetry/bin/poetry",
            "config",
            "repositories.klickbrick",
            "https://klick.brick/simple/",
        ]
    )

import os
from pathlib import Path
import pkg_resources
import logging

from klickbrick import brew
from klickbrick import shell

PYTHON_VERSION = "3.8.0"
USER_HOME_DIRECTORY = str(Path.home())
USER_CURRENT_WORKING_DIRECTORY = os.getcwd()


def package_version():
    return pkg_resources.get_distribution("klickbrick").version


def construct_greeting(name):
    return f"Hello {name}"


def write_checklist():
    logging.info("Generating onboarding checklist")
    shell.copy_file(
        source="onboard_checklist_template.md",
        destination=f"{USER_CURRENT_WORKING_DIRECTORY}/onboarding_checklist.md",
    )


def send_it_email(first_name, last_name):
    logging.info("Sending onboarding request to the IT Department")
    address = "it@example.com"
    subject = "subject of email"

    body = f"The user {first_name} {last_name} is being onboarded"

    url = "mailto:{}?subject={}&body={}"
    url = url.format(address, subject, body)

    shell.execute(["open", url])


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
    logging.info("Installing Brew")
    shell.install_from_url(
        executor="bash",
        url="https://raw.githubusercontent.com/Homebrew/install/master/install.sh",
    )


def configure_git(first_name, last_name):
    logging.info("Configuring git user and commit template")
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
        logging.error("git user.name was not configured")

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
        logging.error("git commit.template was not configured")


def configure_python():
    logging.info("Configuring standard Python version using pyenv")

    # TODO push to a append_to_file helper function that uses DRY_RUN flag
    f = open(f"{USER_HOME_DIRECTORY}/.zshrc", "a")
    f.write("# *** pyenv configuration ***\n")
    f.write('export PYENV_ROOT="$HOME/.pyenv"\n')
    f.write('export PATH="$PYENV_ROOT/bin:$PATH"\n')
    f.write(
        'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi\n'
    )
    f.close()

    shell.execute(["pyenv", "install", PYTHON_VERSION])
    shell.execute(["pyenv", "global", PYTHON_VERSION])


def install_poetry():
    logging.info("Installing Poetry")
    shell.install_from_url(
        executor="python",
        url="https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py",
    )

    # TODO use append_to_file helper function
    f = open(f"{USER_HOME_DIRECTORY}/.zshrc", "a")
    f.write("# *** poetry configuration ***\n")
    f.write('export PATH="$HOME/.poetry/bin:$PATH"\n')
    f.close()


def configure_poetry_repository():
    logging.info("Configuring Poetry to use klickbrick repository")
    shell.execute(
        [
            f"{USER_HOME_DIRECTORY}/.poetry/bin/poetry",
            "config",
            "repositories.klickbrick",
            "https://klick.brick/simple/",
        ]
    )

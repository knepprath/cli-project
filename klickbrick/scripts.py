import logging
import os
from pathlib import Path
import pkg_resources

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

    shell.execute(f"open {url}")


def install_dev_tools(selection, first_name, last_name):
    logging.info("Installing dev tools")
    if selection == "brew" or selection is True:
        install_brew()
    if selection == "git" or selection is True:
        brew.install("git")
        configure_git(first_name, last_name)
    if selection == "pyenv" or selection is True:
        brew.install("pyenv")
        configure_python()
    if selection == "poetry" or selection is True:
        install_poetry()
        configure_poetry_repository()


def install_brew():
    logging.info("Installing Brew")
    shell.install_from_url(
        executor="/bin/bash",
        url="https://raw.githubusercontent.com/Homebrew/install/master/install.sh",
    )


def configure_git(first_name, last_name):
    logging.info("Configuring git user and commit template")
    return_code, output = shell.execute(
        f"git config --global user.name {first_name} {last_name}"
    )

    if return_code != 0:
        logging.error("git user.name was not configured")

    shell.copy_file(
        source="git_commit_template",
        destination=f"{USER_HOME_DIRECTORY}/.gitmessage",
    )

    return_code, output = shell.execute(
        f"git config --global commit.template {USER_HOME_DIRECTORY}/.gitmessage"
    )

    if return_code != 0:
        logging.error("git commit.template was not configured")


def configure_python():
    logging.info(f"Configuring Python {PYTHON_VERSION} using pyenv")

    content = """# *** pyenv configuration ***
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
if command -v pyenv 1>/dev/null 2>&1; then
    eval "$(pyenv init -)"
fi\n"""

    shell.append_to_file(f"{USER_HOME_DIRECTORY}/.bash_profile", content)

    shell.execute(f"pyenv install --skip-existing {PYTHON_VERSION}")
    shell.execute(f"pyenv global {PYTHON_VERSION}")


def install_poetry():
    logging.info("Installing Poetry")
    shell.install_from_url(
        executor="python",
        url="https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py",
        args="--yes --no-modify-path",
    )

    content = """# *** poetry configuration ***
export PATH="$HOME/.poetry/bin:$PATH"\n
"""

    shell.append_to_file(f"{USER_HOME_DIRECTORY}/.bash_profile", content)


def configure_poetry_repository():
    logging.info("Configuring Poetry to use klickbrick repository")
    shell.execute(
        f"{USER_HOME_DIRECTORY}/.poetry/bin/poetry config repositories.klickbrick https://klick.brick/simple/"
    )

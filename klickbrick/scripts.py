import logging
import os
from pathlib import Path
import pkg_resources

from klickbrick import shell

PYTHON_VERSION = "3.8.0"
USER_HOME_DIRECTORY = str(Path.home())
USER_CURRENT_WORKING_DIRECTORY = os.getcwd()


def package_version():
    return pkg_resources.get_distribution("klickbrick").version


def construct_greeting(name):
    return f"Hello {name}"


def config_dev_tools(selection, first_name, last_name):
    logging.info("Configuring dev tools")
    if selection == "git" or selection is True:
        configure_git(first_name, last_name)


def configure_git(first_name, last_name):
    logging.info("Configuring git user and commit template")
    return_code, output = shell.execute(
        f"git config --global user.name {first_name} {last_name}"
    )

    if return_code != 0:
        logging.error("git user.name was not configured")

    shell.copy_file(
        source=f"{os.path.dirname(os.path.abspath(__file__))}/resources/onboard/git_commit_template",
        destination=f"{USER_HOME_DIRECTORY}/.gitmessage",
    )

    return_code, output = shell.execute(
        f"git config --global commit.template {USER_HOME_DIRECTORY}/.gitmessage"
    )

    if return_code != 0:
        logging.error("git commit.template was not configured")


def init_generic(parent, name):
    path = construct_project_path(parent, name)
    logging.info(f"creating project at `{path}`")
    shell.create_directory(path)

    logging.info(f"add .gitignore config at `{path}`")
    shell.copy_file(
        source=f"{os.path.dirname(os.path.abspath(__file__))}/resources/init/gitignore_config",
        destination=f"{path}/.gitignore",
    )

    logging.info(f"add README from template at `{path}`")
    with open(
        f"{os.path.dirname(os.path.abspath(__file__))}/resources/init/readme_template"
    ) as file:
        readme_content = file.read()
    readme_content = readme_content.format(name)
    shell.append_to_file(f"{path}/README", readme_content)

    logging.info(f"add generic .travis.yml at `{path}`")
    shell.copy_file(
        source=f"{os.path.dirname(os.path.abspath(__file__))}/resources/init/travis_template",
        destination=f"{path}/.travis.yml",
    )

    logging.info(f"creating a features directory for BDD process at `{path}`")
    shell.create_directory(f"{path}/features/steps")


def construct_project_path(parent, name):
    path = parent + "/" + name
    path = os.path.expanduser(path)
    return path


def get_username():
    return shell.execute("whoami")

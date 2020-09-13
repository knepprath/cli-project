import os
import shlex
from behave import *
from pathlib import Path

from klickbrick.shell import execute


@when("the user runs KlickBrick '{command}'")
def step_impl(context, command):
    args = shlex.split(command)
    response_code, output = execute(
        ["python", f"{os.getcwd()}/klickbrick/klickbrick.py"] + args
    )
    print(output)
    context.response = output


@then("an onboarding checklist is generated")
def step_impl(context):
    assert "creating checklist" in context.response


@then("the checklist is in Markdown format")
def step_impl(context):
    assert os.path.isfile("onboarding_checklist.md")


@then("an IT onboarding request has been created")
def step_impl(context):
    assert "Christiansen" in context.response


@then("git is installed")
def step_impl(context):
    response_code, output = execute(["git", "--version"])
    assert response_code == 0
    assert "git version" in output


@then("git user profile is set with users name")
def step_impl(context):
    response_code, output = execute(["git", "config", "--global", "user.name"])
    assert response_code == 0
    assert "Ole Kirk Christiansen" in output


@then("git commit template is configured")
def step_impl(context):
    response_code, output = execute(
        ["git", "config", "--global", "commit.template"]
    )
    assert response_code == 0
    assert ".gitmessage" in output


@then("pyenv is installed")
def step_impl(context):
    response_code, output = execute(["pyenv", "versions"])
    assert response_code == 0


@then("Python version 3.8.0 is set as Global default")
def step_impl(context):
    response_code, output = execute(["pyenv", "global"])
    assert response_code == 0
    assert "3.8.0" in output


@then("poetry is installed")
def step_impl(context):
    response_code, output = execute([f"{str(Path.home())}/.poetry/bin/poetry"])
    assert response_code == 0


@then("the KlickBrick repository is configured")
def step_impl(context):
    response_code, output = execute(
        [
            f"{str(Path.home())}/.poetry/bin/poetry",
            "config",
            "repositories.klickbrick",
        ]
    )
    assert response_code == 0
    assert "klick.brick" in output


@then("git is installed and configured")
def step_impl(context):
    context.execute_steps(
        """
        Then git is installed
        And git user profile is set with users name
        And git commit template is configured
    """
    )


@then("pyenv is installed and configured")
def step_impl(context):
    context.execute_steps(
        """
        Then pyenv is installed
        And Python version 3.8.0 is set as Global default
    """
    )


@then("poetry is installed and configured")
def step_impl(context):
    context.execute_steps(
        """
        Then poetry is installed
        And the KlickBrick repository is configured
    """
    )


@then("all developer tools are installed and configured")
def step_impl(context):
    context.execute_steps(
        """
        Then git is installed and configured
        And pyenv is installed and configured
        And poetry is installed and configured
    """
    )

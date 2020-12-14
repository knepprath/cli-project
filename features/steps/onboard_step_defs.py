import os
from behave import *
from pathlib import Path


@then("an onboarding checklist is generated")
def step_impl(context):
    assert "creating checklist" in context.response


@then("the checklist is in Markdown format")
def step_impl(context):
    assert (
        f"cp onboard_checklist_template.md {os.getcwd()}/onboarding_checklist.md"
        in context.response
    )
    # end-to-end with side effects
    # assert os.path.isfile("onboarding_checklist.md")


@then("an IT onboarding request has been created")
def step_impl(context):
    assert "Christiansen" in context.response


@then("git is installed")
def step_impl(context):
    assert "brew install git" in context.response
    # end-to-end with side effects
    # response_code, output = execute("git --version")
    # assert response_code == 0
    # assert "git version" in output


@then("git user profile is set with users name")
def step_impl(context):
    assert "git config --global user.name Ole Christiansen" in context.response
    # end-to-end with side effects
    # response_code, output = execute("git config --global user.name")
    # assert response_code == 0
    # assert "Ole Christiansen" in output


@then("git commit template is configured")
def step_impl(context):
    assert (
        f"git config --global commit.template {str(Path.home())}/.gitmessage"
        in context.response
    )
    # end-to-end with side effects
    # response_code, output = execute("git config --global commit.template")
    # assert response_code == 0
    # assert ".gitmessage" in output


@then("pyenv is installed")
def step_impl(context):
    assert "brew install pyenv" in context.response
    # end-to-end with side effects
    # response_code, output = execute("pyenv versions")
    # assert response_code == 0


@then("Python version 3.8.0 is set as Global default")
def step_impl(context):
    assert "pyenv install --skip-existing 3.8.0" in context.response
    # end-to-end with side effects
    # response_code, output = execute("pyenv global")
    # assert response_code == 0
    # assert "3.8.0" in output


@then("poetry is installed")
def step_impl(context):
    assert (
        'python -c "$(curl -fsSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py)" --yes --no-modify-path'
        in context.response
    )
    # end-to-end with side effects
    # response_code, output = execute(f"{str(Path.home())}/.poetry/bin/poetry")
    # assert response_code == 0


@then("the KlickBrick repository is configured")
def step_impl(context):
    assert (
        f"{str(Path.home())}/.poetry/bin/poetry config repositories.klickbrick https://klick.brick/simple/"
        in context.response
    )
    # end-to-end with side effects
    # response_code, output = execute(f"{str(Path.home())}/.poetry/bin/poetry config repositories.klickbrick")
    # assert response_code == 0
    # assert "klick.brick" in output


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

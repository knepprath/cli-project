import os
from pathlib import Path

from behave import *


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


@then("git is configured")
def step_impl(context):
    context.execute_steps(
        """
        Then git user profile is set with users name
        And git commit template is configured
    """
    )


@then("all developer tools are installed and configured")
def step_impl(context):
    context.execute_steps(
        """
        Then git is configured
    """
    )

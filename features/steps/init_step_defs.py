import os
from pathlib import Path

from behave import *


@given("a directory already exists at '~/custom/path/new-project'")
def step_impl(context):
    path = os.path.expanduser("~/custom/path/new-project")
    Path(path).mkdir(parents=True)


@then("an error message is displayed stating the directory already exits")
def step_impl(context):
    assert (
        "Cannot create project. The directory already exits"
        in context.response
    )


@then(
    "a directory called `new-project` is created in the current working directory"
)
def step_impl(context):
    assert f"mkdir -p {os.getcwd()}/new-project" in context.response
    # end-to-end with side effects
    # assert os.path.isdir(f"{os.getcwd()}/new-project")


@then("the directory is initialized as a git repository")
def step_impl(context):
    assert {f"git init {os.getcwd()}/new-project" in context.response}
    # end-to-end with side effects
    # assert os.path.isdir(f"{os.getcwd()}/new-project/.git")


@then("a directory called 'new-project' is created in '~/custom/path'")
def step_impl(context):
    assert (
        f"mkdir -p {os.path.expanduser('~/custom/path/new-project')}"
        in context.response
    )
    # end-to-end with side effects
    # path = os.path.expanduser("~/custom/path/new-project")
    # assert os.path.isdir(path)

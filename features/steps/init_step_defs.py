from behave import *
import os
import sys
from pathlib import Path


@given("a directory already exits at '~/custom/path/new-project'")
def step_impl(context):
    path = os.path.expanduser("~/custom/path/new-project")
    Path(path).mkdir(parents=True)


@then("an error message is displayed stating the directory already exits")
def step_impl(context):
    output = (
        sys.stdout.getvalue().strip()
    )  # because stdout is a StringIO instance
    assert (
        "ERROR: Cannot create project. The directory already exits" in output
    )
    print(output)


@then(
    "a directory called `new-project` is created in the current working directory"
)
def step_impl(context):
    assert os.path.isdir(f"{os.getcwd()}/new-project")


@then("the directory is initialized as a git repository")
def step_impl(context):
    assert os.path.isdir(f"{os.getcwd()}/new-project/.git")


@then("a directory called 'new-project' is created in '~/custom/path'")
def step_impl(context):
    path = os.path.expanduser("~/custom/path/new-project")
    assert os.path.isdir(path)

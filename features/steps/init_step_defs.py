import os
from pathlib import Path

from behave import *


@given("a directory already exists at '~/custom/path/new-project'")
def step_impl(context):
    path = os.path.expanduser("~/custom/path/new-project")
    Path(path).mkdir(parents=True)


@then("an error message is displayed stating the directory already exists")
def step_impl(context):
    assert "The directory already exists" in context.response


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


@then("there is a black config in pyproject.toml")
def step_impl(context):
    assert (
        f"( cd {os.getcwd()}/new-project ; pyenv local 3.8.0 )"
        in context.response
    )


@then("there is a .flake8 config file")
def step_impl(context):
    assert (
        f"cp init/python/flake8_config {os.getcwd()}/new-project/.flake8"
        in context.response
    )


@then("there is a .pre-commit-config.yaml")
def step_impl(context):
    assert (
        f"cp init/python/pre_commit_config {os.getcwd()}/new-project/.pre-commit-config"
        in context.response
    )


@then("there is a .python-version file")
def step_impl(context):
    assert (
        f"cd {os.getcwd()}/new-project ; pyenv local 3.8.0" in context.response
    )


@then("the project is initialized with poetry")
def step_impl(context):
    assert (
        f"cd {os.getcwd()}/new-project ; poetry init --name new-project --python 3.8.0"
        in context.response
    )


@then("there is a default .gitignore")
def step_impl(context):
    assert (
        f"cp init/gitignore_config {os.getcwd()}/new-project/.gitignore"
        in context.response
    )


@then("there is a README template")
def step_impl(context):
    assert f">> {os.getcwd()}/new-project/README" in context.response


@then("there is a .travis.yml template")
def step_impl(context):
    assert (
        f"cp init/travis_template {os.getcwd()}/new-project/.travis.yml"
        in context.response
    )


@then("there is a features directory")
def step_impl(context):
    assert (
        f"mkdir -p {os.getcwd()}/new-project/features/steps"
        in context.response
    )


@then("the python specific config is added to .gitignore")
def step_impl(context):
    assert f">> {os.getcwd()}/new-project/README" in context.response

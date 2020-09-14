from behave import *
import shlex
from klickbrick.shell import execute
from klickbrick.scripts import package_version


@when("the user runs KlickBrick '{command}'")
def step_impl(context, command):
    args = shlex.split(command)
    response_code, output = execute(["poetry", "run", "klickbrick"] + args)
    print(output)
    context.response = output


@then("the current version of the CLI is identified")
def step_impl(context):
    assert f"klickbrick {package_version()}" in context.response

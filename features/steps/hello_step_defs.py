import os
from behave import *

from klickbrick.shell import execute


@given("we run the hello command")
def step_impl(context):
    response_code, output = execute(
        [
            "python3",
            f"{os.getcwd()}/klickbrick/klickbrick.py",
            "hello",
            "--name",
            "david",
        ]
    )
    context.response = output


@then('the command returns "hello world"')
def step_impl(context):
    print(context.response)
    assert "Hello david" in context.response

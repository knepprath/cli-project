import os
from behave import *
import subprocess


@given("we run the hello command")
def step_impl(context):
    process = subprocess.Popen(
        [
            "python3",
            f"{os.getcwd()}/klickbrick/klickbrick.py",
            "hello",
            "--name",
            "david",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = process.communicate()
    context.response = stdout.decode("utf-8")


@then('the command returns "hello world"')
def step_impl(context):
    print(context.response)
    assert "Hello david" in context.response

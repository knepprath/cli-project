import sys
from behave import *


@then("list all available commands")
def step_impl(context):
    assert "hello" in context.response
    assert "init" in context.response
    assert "help" in context.response
    assert "onboard" in context.response


@then(u"document the usage of the command")
def step_impl(context):
    assert "usage: klickbrick.py [-h] [--name NAME]" in context.response

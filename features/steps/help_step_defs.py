from behave import *


@then("list all available commands")
def step_impl(context):
    assert "hello" in context.response
    assert "init" in context.response
    assert "help" in context.response
    assert "onboard" in context.response


@then(u"document the usage of the command")
def step_impl(context):
    assert "show this help message and exit" in context.response


@then("the argument is identified as invalid")
def step_impl(context):
    assert "is not a valid argument" "" in context.response

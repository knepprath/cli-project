from behave import *


@then("list all available commands")
def step_impl(context):
    assert (
        "positional arguments:" in context.response
        or "choose from" in context.response
    )


@then(u"document the usage of the command")
def step_impl(context):
    assert "usage: klickbrick hello [-h] [-d] [-n NAME]" in context.response


@then("the argument is identified as invalid")
def step_impl(context):
    assert "klickbrick: error: unrecognized arguments:" in context.response

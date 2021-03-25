from behave import *


@then('the command returns "Hello World"')
def step_impl(context):
    print(context.response)
    assert "Hello World" in context.response


@then('the command returns "Hello Ole"')
def step_impl(context):
    print(context.response)
    assert "Hello Ole" in context.response

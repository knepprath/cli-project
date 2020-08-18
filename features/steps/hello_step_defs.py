from behave import *
from cli_project.klick_brick_cli import parse_args

@given('we run the hello command')
def step_impl(context):
    context.cli = parse_args(['hello', '--name', 'david'])

@then('the command returns "hello world"')
def step_impl(context):
    args = context.cli
    assert args.hello == 'hello'
    assert args.name == 'david'

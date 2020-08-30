import sys
from behave import *
from klickbrick import klickbrick

@given('we run the hello command')
def step_impl(context):
    args = ['hello', '--name', 'david']
    old_sys_argv = sys.argv
    sys.argv = [old_sys_argv[0]] + args

    klickbrick.KlickBrick()

@then('the command returns "hello world"')
def step_impl(context):
    output = sys.stdout.getvalue().strip() # because stdout is a StringIO instance
    assert output == "Hello david"
    print(output)

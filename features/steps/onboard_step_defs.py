import sys
from behave import *
from klick_brick_cli import klickbrick

@when(u'the user runs `KlickBrick onboard --checklist`')
def step_impl(context):
    args = ['onboard', '--checklist']
    old_sys_argv = sys.argv
    sys.argv = [old_sys_argv[0]] + args

    klickbrick.KlickBrick()

@then(u'an onboarding checklist is generated')
def step_impl(context):
    output = sys.stdout.getvalue().strip() # because stdout is a StringIO instance
    assert output == "creating checklist"
    print(output)

@then(u'the checklist is in Markdown format')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the checklist is in Markdown format')
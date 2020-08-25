import sys
import os
import shlex
from behave import *
from klick_brick_cli import klickbrick

@when(u"the user runs KlickBrick '{command}'")
def step_impl(context, command):
    args = shlex.split(command)
    old_sys_argv = sys.argv
    sys.argv = [old_sys_argv[0]] + args

    print(args)
    klickbrick.KlickBrick() # TODO evaluate how to invoke more realistically to a pip install of the module, but in environment that can be cleaned up

@then(u'an onboarding checklist is generated')
def step_impl(context):
    output = sys.stdout.getvalue().strip() # because stdout is a StringIO instance
    assert output == "creating checklist"
    print(output)

@then(u'the checklist is in Markdown format')
def step_impl(context):
    assert os.path.isfile('onboarding_checklist.md')

@then(u'the email template is updated with the users name')
def step_impl(context):
    output = sys.stdout.getvalue().strip() # because stdout is a StringIO instance
    assert "Christiansen" in output
    print(output)

import sys
from behave import *


@then("list all available commands")
def step_impl(context):
    output = sys.stdout.getvalue().strip()  # because stdout is a StringIO instance
    assert "['hello', 'help', 'onboard']" in output


@then(u"document the usage of the command")
def step_impl(context):
    output = sys.stdout.getvalue().strip()  # because stdout is a StringIO instance
    print(output)

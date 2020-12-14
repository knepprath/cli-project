from behave import *

from klickbrick.shell import execute
from klickbrick.scripts import package_version

# Imports used during alternative options for invoking the CLI
# import shlex
# import sys
# from klickbrick.klickbrick import KlickBrick


@when("the user runs KlickBrick '{command}'")
def step_impl(context, command):
    # Option 1: Invoke Python code directly
    # KlickBrick(shlex.split(command))
    # output = sys.stdout.getvalue().strip() # because stdout is a StringIO instance

    # Option 2: Invoke package using Poetry so it's closer to an end-to-end test,
    # but using the --dry-run flag so that there is no side effects in environment
    response_code, output = execute(
        f"poetry run klickbrick {command} --dry-run"
    )

    # Option 3: True end to end test with side effects
    # args = shlex.split(command)
    # response_code, output = execute(f"poetry run klickbrick {command}")

    # Behave only shows print statements on Scenario failure to help with debugging
    print(output)
    # Pass output in context so assertions can be made against it in "Then" steps
    context.response = output


@when("the user runs KlickBrick without any arguments")
def step_impl(context):
    context.execute_steps(
        """
        When the user runs KlickBrick ' '
    """
    )


@then("the current version of the CLI is identified")
def step_impl(context):
    assert f"klickbrick {package_version()}" in context.response


@then("the command is identified as invalid")
def step_impl(context):
    assert "'nonexistent' is not a valid command" "" in context.response

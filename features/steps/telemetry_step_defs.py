from behave import *


@given(u"the server is running to receive CLI metrics")
def step_impl(context):
    raise NotImplementedError(
        u"STEP: Given the server is running to receive CLI metrics"
    )


@when(u"user executes a command with the CLI")
def step_impl(context):
    raise NotImplementedError(
        u"STEP: When user executes a command with the CLI"
    )


@then(u"the metric is emitted contains the command")
def step_impl(context):
    raise NotImplementedError(
        u"STEP: Then the metric is emitted contains the command"
    )


@then(u"the metric is emitted contains the OS")
def step_impl(context):
    raise NotImplementedError(
        u"STEP: Then the metric is emitted contains the OS"
    )


@then(u"the metric is emitted contains the Python version")
def step_impl(context):
    raise NotImplementedError(
        u"STEP: Then the metric is emitted contains the Python version"
    )


@then(u"the metric is emitted contains the user config")
def step_impl(context):
    raise NotImplementedError(
        u"STEP: Then the metric is emitted contains the user config"
    )

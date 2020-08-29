import sys
import os
import shlex
import subprocess
from behave import *
from klick_brick_cli import klickbrick
from pathlib import Path



@when(u"the user runs KlickBrick '{command}'")
def step_impl(context, command):
    args = shlex.split(command)
    old_sys_argv = sys.argv
    sys.argv = [old_sys_argv[0]] + args

    # print(args)
    klickbrick.KlickBrick() # TODO evaluate how to invoke more realistically to a pip install of the module, but in environment that can be cleaned up


@then(u'an onboarding checklist is generated')
def step_impl(context):
    output = sys.stdout.getvalue().strip() # because stdout is a StringIO instance
    assert "creating checklist" in output
    print(output)


@then(u'the checklist is in Markdown format')
def step_impl(context):
    assert os.path.isfile('onboarding_checklist.md')


@then(u'an IT onboarding request has been created')
def step_impl(context):
    output = sys.stdout.getvalue().strip() # because stdout is a StringIO instance
    assert "Christiansen" in output
    print(output)


@then(u'git is installed')
def step_impl(context):
    process = subprocess.Popen(['git', '--version'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    assert process.returncode == 0
    assert "git version" in stdout.decode("utf-8")


@then(u'git user profile is set with users name')
def step_impl(context):
    process = subprocess.Popen(['git', 'config', '--global', 'user.name'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    assert process.returncode == 0
    assert "Ole Kirk Christiansen" in stdout.decode("utf-8")


@then(u'git commit template is configured')
def step_impl(context):
    process = subprocess.Popen(['git', 'config', '--global', 'commit.template'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    assert process.returncode == 0
    assert ".gitmessage" in stdout.decode("utf-8")


@then(u'pyenv is installed')
def step_impl(context):
    process = subprocess.Popen(["pyenv", "versions"],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    assert process.returncode == 0


@then(u'Python version 3.8.0 is set as Global default')
def step_impl(context):
    process = subprocess.Popen(["pyenv", "global"],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    assert process.returncode == 0
    assert "3.8.0" in stdout.decode("utf-8")


@then(u'poetry is installed')
def step_impl(context):
    process = subprocess.Popen([f"{str(Path.home())}/.poetry/bin/poetry"],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    assert process.returncode == 0


@then(u'the KlickBrick repository is configured')
def step_impl(context):
    process = subprocess.Popen([f"{str(Path.home())}/.poetry/bin/poetry", "config", "repositories.klickbrick"],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    assert process.returncode == 0
    assert "klick.brick" in stdout.decode("utf-8")


@then(u'git is installed and configured')
def step_impl(context):
    context.execute_steps(u"""
        Then git is installed
        And git user profile is set with users name
        And git commit template is configured
    """)


@then(u'pyenv is installed and configured')
def step_impl(context):
    context.execute_steps(u"""
        Then pyenv is installed
        And Python version 3.8.0 is set as Global default
    """)


@then(u'poetry is installed and configured')
def step_impl(context):
    context.execute_steps(u"""
        Then poetry is installed
        And the KlickBrick repository is configured
    """)


@then(u'all developer tools are installed and configured')
def step_impl(context):
    context.execute_steps(u"""
        Then git is installed and configured
        And pyenv is installed and configured
        And poetry is installed and configured
    """)

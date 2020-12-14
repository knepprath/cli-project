import os
import sys
import shutil

from behave.tag_matcher import ActiveTagMatcher

from klickbrick import config

# -- MATCHES ANY TAGS: @use.with_{category}={value}
# NOTE: active_tag_value_provider provides category values for active tags.
active_tag_value_provider = {
    "os": sys.platform,  # e.g. for scenario that can only be run on macOS tag with @use.with_os=darwin
}
print(sys.platform)
active_tag_matcher = ActiveTagMatcher(active_tag_value_provider)


def setup_active_tag_values(active_tag_values, data):
    for category in active_tag_values.keys():
        if category in data:
            active_tag_values[category] = data[category]


def before_all(context):
    config.initialize()
    # -- SETUP ACTIVE-TAG MATCHER (with userdata):
    # USE: behave -D with_os=darwin ...
    setup_active_tag_values(active_tag_value_provider, context.config.userdata)


def before_feature(context, feature):
    if active_tag_matcher.should_exclude_with(feature.tags):
        feature.skip(reason="DISABLED ACTIVE-TAG")
    if "skip" in feature.tags:
        feature.skip("Marked with @skip")
        return

    # Whatever other things you might want to do in this hook go here.


def before_scenario(context, scenario):
    if active_tag_matcher.should_exclude_with(scenario.effective_tags):
        scenario.skip("DISABLED ACTIVE-TAG")
    if "skip" in scenario.effective_tags:
        scenario.skip("Marked with @skip")
        return

    # TODO cleanup state better
    # TODO Uninstall all the things that get installed by the CLI, should this be a CLI command too?
    try:
        shutil.rmtree(f"{os.getcwd()}/new-project")
    except FileNotFoundError:
        pass
    try:
        shutil.rmtree(os.path.expanduser("~/custom/path/new-project"))
    except FileNotFoundError:
        pass

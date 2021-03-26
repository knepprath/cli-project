Feature: Core Functionality of the CLI

#  TODO add a tag to these scenarios to identify them as end to end which are run
#  all the other scenarios should tests using the dry run flag?

  Scenario Outline: CLI -Version
    When the user runs KlickBrick '<input>'
    Then the current version of the CLI is identified

  Examples: Version Flag
    | input       |
    | --version |
    | -v        |
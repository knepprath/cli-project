Feature: Core Functionality of the CLI

  Scenario Outline: CLI -Version
    When the user runs KlickBrick '<input>'
    Then the current version of the CLI is identified

  Examples: Version Flag
    | input       |
    | --version |
    | -v        |

  @skip
  Scenario: Executed with no arguments
    When the user runs KlickBrick without any arguments
    Then list all available commands

  @skip
  Scenario: Executed with non-existent subcommand
    When the user runs KlickBrick 'nonexistent'
    Then the command is identified as invalid
    And list all available commands
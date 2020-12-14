Feature: Core Functionality of the CLI

#  TODO add a tag to these scenarios to identify them as end to end which are run
#  all the other scenarios should tests using the dry run flag?

  Scenario: Executed with no arguments
    When the user runs KlickBrick without any arguments
    Then list all available commands

  Scenario: Executed with non-existent subcommand
    When the user runs KlickBrick 'nonexistent'
    Then the command is identified as invalid
    And list all available commands
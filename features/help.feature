Feature: Document usage of commands

  Scenario: Document Available Commands
    When the user runs KlickBrick 'help'
    Then list all available commands

  Scenario: Usage for specific command
    When the user runs KlickBrick 'help hello'
    Then document the usage of the command

  @skip
  Scenario: Usage for non-existent command
    When the user runs KlickBrick 'help nonexistent'
    Then indicate that 'nonexistent' is an invalid command
    And list all available commands
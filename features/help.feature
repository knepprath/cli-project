Feature: Document usage of commands

  Scenario: Document Available Commands
    When the user runs KlickBrick 'help'
    Then list all available commands

  Scenario: Usage for specific command
    When the user runs KlickBrick 'help hello'
    Then document the usage of the command

  Scenario: Usage for non-existent command
    When the user runs KlickBrick 'help nonexistent'
    Then the argument is identified as invalid
    And list all available commands

  Scenario: Usage for invalid argument
    When the user runs KlickBrick 'help --invalid'
    Then the argument is identified as invalid
    And list all available commands
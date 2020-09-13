Feature: Document usage of commands

  Scenario: Document Available Commands
    When the user runs KlickBrick 'help'
    Then list all available commands

  Scenario: Document usage of specific command
    When the user runs KlickBrick 'help hello'
    Then document the usage of the command
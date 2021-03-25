Feature: Document usage of commands

  Scenario: Document Available Commands
    When the user runs KlickBrick 'help'
    Then list all available commands

  Scenario: Usage for specific command
    When the user runs KlickBrick 'hello --help'
    Then document the usage of the command

  Scenario: Usage for non-existent command
    When the user runs KlickBrick 'nonexistent --help'
    Then the command is identified as invalid
    And list all available commands

  Scenario: Usage for invalid argument
    When the user runs KlickBrick '--invalid --help'
    Then document KlickBrick usage
    And list all available commands
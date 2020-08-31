@skip
Feature: Document usage of commands

  Scenario: Document Available Commands
    When the user runs KlickBrick 'help'
    Then list all available commands

  #TODO the way that argparse is logging -h is not registering as a valid command during scenario execution. It exits, "differently"?
  # "help onboard" leverages -h, so it's broken the same way.
  @skip
  Scenario: Document usage of specific command
    When the user runs KlickBrick 'help hello'
    Then document the usage of the command
Feature: Document usage of commands

  Scenario: Document Available Commands
    When the user runs KlickBrick 'help'
    Then list all available commands

  #TODO the way that argparse is logging -h is breaking the test for some reason. It exits differently? "help onboard" leverages -h, so it's broken the same way
  @skip
  Scenario: Document usage of specific command
    When the user runs KlickBrick 'onboard -h'
    Then document the usage of the command
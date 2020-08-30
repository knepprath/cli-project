Feature: showing off behave
@skip
  Scenario: run hello command
     Given we run the hello command
     Then the command returns "hello world"
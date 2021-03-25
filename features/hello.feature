Feature: showing off behave

  Scenario: Hello World
    When the user runs KlickBrick 'hello'
    Then the command returns "Hello World"

  Scenario: Friendly Hello
    When the user runs KlickBrick 'hello --name Ole'
    Then the command returns "Hello Ole"
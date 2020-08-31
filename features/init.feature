Feature: Initialize a code repository for a new project

  Scenario: Initialize new directory as git repository
    When the user runs KlickBrick 'init --name new-project'
    Then a directory called `new-project` is created in the current working directory
    And the directory is initialized as a git repository

  Scenario: Specify the path for new project
    When the user runs KlickBrick 'init --name new-project --path ~/custom/path'
    Then a directory called 'new-project' is created in '~/custom/path'

  Scenario: Specify the path for new project which already exits
    Given a directory already exits at '~/custom/path/new-project'
    When the user runs KlickBrick 'init --name new-project --path ~/custom/path'
    Then an error message is displayed stating the directory already exits

  @skip
  Scenario: Create pyenv with dependencies
    When the user runs KlickBrick 'init --name new-project'
    Then the project has a python environment created

    # TODO poetry? or what would it look like to initialize for a Django project?
  @skip
  Scenario: Initialize poetry
    When the user runs KlickBrick 'init --name new-project'
    Then the project is initialized with poetry

    # TODO scenario for initialize with all of the company specific files/folder structure?
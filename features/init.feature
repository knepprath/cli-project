Feature: Initialize a code repository for a new project

  Scenario: Initialize new directory as git repository
    When the user runs KlickBrick 'init --name new-project'
    Then a directory called `new-project` is created in the current working directory
    And the directory is initialized as a git repository

  Scenario: Specify the path for new project
    When the user runs KlickBrick 'init --name new-project --path ~/custom/path'
    Then a directory called 'new-project' is created in '~/custom/path'

  Scenario: Specify the path for new project which already exits
    Given a directory already exists at '~/custom/path/new-project'
    When the user runs KlickBrick 'init --name new-project --path ~/custom/path'
    Then an error message is displayed stating the directory already exists

  Scenario: Initialize with standard config files
    When the user runs KlickBrick 'init --name new-project'
    Then there is a default .gitignore
    Then there is a README template
    Then there is a .travis.yml template
    Then there is a features directory

  Scenario: Initialize python project with standard config files
    When the user runs KlickBrick 'init --name new-project --framework python'
    Then the project is initialized with poetry
    Then the python specific config is added to .gitignore
    Then there is a black config in pyproject.toml
    Then there is a .flake8 config file
    Then there is a .pre-commit-config.yaml
    Then there is a .python-version file

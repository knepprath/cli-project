Feature: Automate the onboarding workflow for new developers

  Scenario: New Developer Checklist
    When the user runs KlickBrick 'onboard --checklist'
    Then an onboarding checklist is generated
    And the checklist is in Markdown format

  Scenario: New Developer IT Onboarding Request
    When the user runs KlickBrick 'onboard --it-request --first-name Ole --last-name Christiansen'
    Then an IT onboarding request has been created

  Scenario: New Developer Tools Installation - git
    When the user runs KlickBrick 'onboard --dev-tools git --first-name Ole --last-name Christiansen'
    Then git is installed
    And git user profile is set with users name
    And git commit template is configured

  Scenario: New Developer Tools Installation - python
    When the user runs KlickBrick 'onboard --dev-tools pyenv --first-name Ole --last-name Christiansen'
    Then pyenv is installed
    And Python version 3.8.0 is set as Global default

  Scenario: New Developer Tools Installation - poetry
    When the user runs KlickBrick 'onboard --dev-tools poetry --first-name Ole --last-name Christiansen'
    Then poetry is installed
    And the KlickBrick repository is configured

  Scenario: New Developer Tools Installation - ALL
    When the user runs KlickBrick 'onboard --dev-tools --first-name Ole --last-name Christiansen'
    Then git is installed and configured
    And pyenv is installed and configured
    And poetry is installed and configured

  Scenario: New Developer Onboard
    When the user runs KlickBrick 'onboard --first-name Ole --last-name Christiansen'
    Then an onboarding checklist is generated
    And an IT onboarding request has been created
    And all developer tools are installed and configured

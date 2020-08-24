Feature: Automate the onboarding workflow for new developers

  Scenario: New Developer Checklist
    When the user runs KlickBrick "onboard --checklist"
    Then an onboarding checklist is generated
#    And the checklist is in Markdown format

  @skip
  Scenario: New Developer IT Onboarding Request
    When the user runs `KlickBrick onboard --it-request --first-name Ole Kirk --last-name Christiansen`
    Then the email template is updated with the users name
    And the email client is successfully invoked

  @skip
  Scenario: New Developer Tools Installation - git
    When the user runs `KlickBrick onboard --dev-tools --first-name Ole Kirk --last-name Christiansen`
    Then git is installed
    And git user profile is set with users name
    And git commit template is configured

  @skip
  Scenario: New Developer Tools Installation - pyenv
    When the user runs `KlickBrick onboard --dev-tools --first-name Ole Kirk --last-name Christiansen`
    And pyenv is installed
    And Python version 3.8.1 is set as Global default

  @skip
  Scenario: New Developer Tools Installation - poetry
    When the user runs `KlickBrick onboard --dev-tools --first-name Ole Kirk --last-name Christiansen`
    And poetry is installed
    And the KlickBrick repository is configured

  @skip
  Scenario: New Developer Onboard
    When the user runs `KlickBrick onboard --first-name Ole Kirk --last-name Christiansen`
    Then an onboarding checklist is generated
    And an IT onboarding request has been created
    And all developer tools are installed and configured

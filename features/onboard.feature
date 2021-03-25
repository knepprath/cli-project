Feature: Automate the onboarding workflow for new developers

  Scenario: New Developer Tools Installation - git
    When the user runs KlickBrick 'onboard --dev-tools git --first-name Ole --last-name Christiansen'
    Then git user profile is set with users name
    And git commit template is configured

  Scenario: New Developer Tools Installation - ALL
    When the user runs KlickBrick 'onboard --dev-tools --first-name Ole --last-name Christiansen'
    Then git is configured

  Scenario: New Developer Onboard
    When the user runs KlickBrick 'onboard --first-name Ole --last-name Christiansen'
    Then all developer tools are installed and configured

Feature: Usage telemtry is reported to backend server

  Scenario: CLI reports usage and context
    When user executes a command with the CLI
    Then the CLI reports the command
    And the CLI reports the OS
    And the CLI reports the Python version
    And the CLI reports the user config

  Scenario: CLI Telemetry fails gracefully
    Given connection to the backend server is interuptted
    When user executes a command with the CLI
    Then the command is run successfully
    And the telemetry failure is logged in DEBUG

  # TODO Future requirement
  # Scenario: Buffer the telemetry data
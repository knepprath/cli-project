@skip
Feature: Usage telemetry is reported to backend server

  Scenario: CLI emits metrics with usage and context
    Given the server is running to receive CLI metrics
    When user executes a command with the CLI
    Then the metric is emitted contains the command
    And the metric is emitted contains the OS
    And the metric is emitted contains the Python version
    And the metric is emitted contains the user config

  @skip
  Scenario: CLI Telemetry fails gracefully
    Given connection to the backend server is interuptted
    When user executes a command with the CLI
    Then the command is run successfully
    And the telemetry failure is logged in DEBUG

  # TODO Future requirement
  # Scenario: Buffer the telemetry data
# features/healthz.feature
# Q1-Q5: the five questions in docs/want-to-done.md
Feature: healthz endpoint
  As a client
  I want to reach the server
  So that I can know it's up

  # one Scenario per When; the title becomes the test name
  # title: situation first, what the client sees last
  Scenario: GET /healthz
    # Q5 (test) items, one per line
    Given nothing else is listening on PORT
    And the service is running
    # Q2: the one action under test
    When the client requests GET /healthz
    # Q3 checks, one per line
    Then they receive an http response  # delete?
    And the status line is "HTTP/1.1 200 OK"
    And the body is "UP"

  # Q4 gets its own Scenario when checking it takes another action
  Scenario: After a correct http response
    Given nothing else is listening on PORT
    And the service is running
    # what the client already did becomes a Given
    And the client requested Get /healthz
    When the client receives the response
    Then the server is still up
    And the server still answers requests
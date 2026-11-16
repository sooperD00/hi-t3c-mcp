# features/<story>.feature
Feature: <the want, in a few words>
  As a <Q1>
  I want <...>
  So that <...>

  # one Scenario per When; the title becomes the test name
  # title: situation first, what the client sees last
  Scenario: <title>
    # Q5 (test) items, one per line
    Given <Q5 (test) item>
    And <Q5 (test) item>
    # Q2: the one action under test
    When <Q2>
    # Q3 checks, one per line
    Then <Q3 check>
    And <Q3 check>

  # Q4 gets its own Scenario when checking it takes another action
  Scenario: <title>
    Given <Q5 (test) items>
    # what the client already did becomes a Given
    And <the earlier action, past tense>
    When <the action that checks Q4>
    Then <Q4, as what the client sees>
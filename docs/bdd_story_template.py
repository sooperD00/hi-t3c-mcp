"""
Q1-Q5: the five questions in docs/want-to-done.md

BDD Rules:
- One `When` per scenario
- Anything the client did earlier becomes a `Given`
- One condition per line
- Q5 (code) items stay out of the feature file -> They become plain unit tests
- Comments go on their own line
- Stub with `NotImplementedError`, not ...

At automation:
- A missing step definition errors out with `StepDefinitionNotFoundError`; 
this is not a real RED. A real RED is an assert failing, or NotImplementedError.
- The service has to stay up across steps, but each step is a plain function.
Solve that here, not while you're formulating.

References:
- pytest-bdd documentation: https://pytest-bdd.readthedocs.io/en/latest/
- "Cucumber: Discovery, the first practice of BDD": https://cucumber.io/blog/discovery-the-first-practice-of-bdd/
- "Test Automation University: the Formulation phase": https://testautomationu.applitools.com/bdd-with-specflow/chapter3.html
"""

# test_<story>.py
from pytest_bdd import scenarios, given, when, then

scenarios("features/<story>.feature")   # one test per Scenario

@given("<Q5 (test) line, word for word>", target_fixture="situation")
def _():
    raise NotImplementedError   # set it up (arrange); return what the When needs

@when("<Q2 line, word for word>", target_fixture="reply")
def _(situation):
    raise NotImplementedError   # call it (act); return what the Thens check

@then("<Q3 line, word for word>")
def _(reply):
    raise NotImplementedError   # check it (assert)


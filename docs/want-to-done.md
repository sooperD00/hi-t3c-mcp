# From a want to done

A method for any project: start from something a client wants, end with code that does it. It is the outer loop around [red, green, refactor](test-first-method.md). The usual name is *double-loop TDD*.

- **Outer loop:** one scenario per want, written before the code. It fails until the whole want works.
- **Inner loop:** red, green, refactor on each piece the scenario needs.

## The commit cycle

```
want(feat), docs(plan)[, test(plan), test(WIP)], test(RED)[, feat(WIP)], feat(GREEN), chore(refactor), docs(cleanup), docs(learn), repeat
```

Brackets mark optional commits. Three of the steps are BDD's three practices:

| BDD practice | Step | Output | Commit |
|---|---|---|---|
| Discovery | the five questions | answers in the devlog | `docs(plan)` |
| Formulation | answers → scenarios | `.feature` file | `test(plan)` |
| Automation | step definitions | `test_*.py` | `test(RED)` |

GREEN and refactor stay the same.

## 1. Write the want

- **The user story:** "As a (who), I want to (what), so that (why)." Commit it as `want(feat)`.
- **A nametag:** one short word for the want (`healthz`), so you can grep for it instead of the whole story.
- **The story sets the scope, not the roadmap.** Write every test the story needs, even one that belongs to a later roadmap step. Combine overlaps at refactor.

## 2. Discovery: the five questions

Answer them in this order: Who → When → Then → Given. Decide what the client sees before you ask what has to be true for it. (Kent Beck calls this *assert first*.)

| # | Question | Watch for | Gherkin line |
|---|---|---|---|
| Q1 | Who is outside? | the observer, never the code itself | `As a` in the Feature; the subject of each line |
| Q2 | What do they do? | the action | When |
| Q3 | What can they see afterward? | only what's visible: status line, headers, body, connection closing | Then |
| Q4 | What must not happen? | often the real point | Then; its own Scenario if checking it takes another action |
| Q5 | What's true beforehand? | the situation; often per key (per access code) | Given (test items); code items become plain unit tests |

Tag each Q5 answer:

- **(test):** the test sets it up. It becomes a `Given`.
- **(code):** GREEN has to build it. It stays out of the `.feature` file and gets its own unit test in the inner loop.

Q4 found the real point every time:

- 403: the reading must not leak.
- 410: the sequence must not start over.
- bad request: the server must keep serving the next client.
- 429: one access code must not block another.

Two more habits:

- **Name the setting, not the number** (read timeout, sensor period), so the test can shrink it and the promise survives a config change.
- **Use "beforehand" to isolate the cause.** A bad-request test runs with a reading present, so the only reason to reject is the request.

## 3. Formulation: answers → scenarios

Copy [template.feature](template.feature) to `features/<story>.feature`.

- **One `When` per scenario.** A second action is a second scenario.
- **Anything the client did earlier becomes a `Given`,** in past tense.
- **One condition per line.**
- **Comments go on their own line.** A `#` after a step becomes part of the step's text, and no step definition matches it.

### Name the scenario

pytest-bdd turns each scenario title into its test name (`test_` + the title, in snake case), so titles follow the test-name rules:

`test_<interface>_<situation>_<what the client sees>`

```
test_http_get_temperature_returns_200_with_the_reading
test_http_sixth_request_in_one_second_returns_429
test_http_slow_client_is_disconnected
```

- **Shared prefix per interface** (`test_http_`), so `pytest -k http` runs exactly that group.
- **Situation first, result last.** A failing name reads like a bug report, and the codes line up at the end.
- **Name what the test exercises** (the request), not an internal function it happens to reach.
- **Name the promise, not the courtesy.** The 408 test is "is disconnected"; the 408 itself is optional.
- **Name the boundary** when there is one: "sixth request in one second."

## 4. Automation: step definitions

Copy [bdd_story_template.py](bdd_story_template.py) to `test_<story>.py`.

- **Paste each `.feature` line into its decorator, word for word.**
- **Hand values between steps with `target_fixture`.** See pytest-bdd in [stack-notes-python.md](stack-notes-python.md).
- **Stub every step with `raise NotImplementedError`.**
- **A missing step definition is not a real RED.** It errors with `StepDefinitionNotFoundError`. A real RED is a failing assert or a `NotImplementedError`.

## 5. Red, green, refactor

Make the scenario pass one piece at a time with [test-first-method.md](test-first-method.md). Each Q5 (code) item gets its own unit test there.

## 6. Close the loop

- `chore(refactor)`: remove duplication, duplicated tests included. Combine tests that overlap.
- `docs(cleanup)`: sync the layout, roadmap, and spec with the code.
- `docs(learn)`: distill the devlog into the method docs and stack notes.
- Repeat with the next want.

## From the error model to a test

The error model is a second source of wants. Start from the status-code table in the interface spec.

### 1. One test per category

The table's "Test category" column is the list of tests. A category groups situations that share a setup. If only the bytes sent change, it's one parametrized test.

### 2. Name it

Use the rules in [Name the scenario](#name-the-scenario).

### 3. Answer the five questions

See [step 2](#2-discovery-the-five-questions).

### 4. Write the docstring

- **Line 1, the trace:** the table row, `code name | condition`. Matching on the code leads straight back to the spec.
- **Line 2, the promise:** the parts the name can't hold.
- Don't repeat the name word for word. If a docstring would add nothing, skip it.

```python
"""403 Forbidden | access code missing or not on the list
a client asking for a reading without a valid access code gets 403 and no reading"""
```

### 5. Stub it until its step on the roadmap

```python
@pytest.mark.xfail(reason="access codes not built yet", strict=True)
def test_http_reading_without_valid_access_code_returns_403():
	"""..."""
	raise NotImplementedError("test not written yet")
```

- `reason=` is the table's "Built in" column. `pytest -rx` lists every stub with its reason, which is the remaining roadmap.
- `strict=True` makes an unexpected pass fail, so pytest tells you when to delete the mark.
- `raise NotImplementedError` keeps the stub honestly red under the mark.

## References

- Dan North, "What's in a Story?": the user story and Given / When / Then
- Kent Beck, *Test-Driven Development: By Example*: assert first; refactoring removes duplication, duplicated tests included
- Seb Rose, [Discovery, the first practice of BDD](https://cucumber.io/blog/discovery-the-first-practice-of-bdd/): BDD is three practices, discovery, formulation, and automation
- Steve Freeman and Nat Pryce, *Growing Object-Oriented Software, Guided by Tests* (2009): double-loop TDD
- [pytest-bdd documentation](https://pytest-bdd.readthedocs.io/en/latest/)

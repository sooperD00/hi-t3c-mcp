11/6/26 2:07p
hi-t3c-mcp 20261106: discovery
hi-t3c-mcp 20261112: part deux

---

REFERENCES:
- Dan North, BDD: “What’s in a Story?”
    - "user-stories" and the "Given / When / Then" template
- Kent Beck, TDD:
    - "test list": the list of tests you write down before you start
    - "assert first": Decide what the client should see (Then) and what they do (When). Then ask what has to be true for that to happen (Given).
        - Writing order (your plan): Who → When → Then → Given
        - Reading and running order (test code):
            - Given → When → Then == arrange → act → assert.
    - "TDD by Example", the refactor step’s main job is removing duplication, and that includes duplicated tests. Sorting before you’ve written anything is a refactor done blind.
- Seb Rose, BDD
    - Behaviour-Driven Development is made of three practices; discovery, formulation, automation. **Formulation:** convert the examples that we have gathered in the Discovery phase into a format that is readable to human beings but that can also be parsed and interpreted by code.
- pytest-bdd, https://pytest-bdd.readthedocs.io/en/latest/
- Growing Object-Oriented Software, Guided by Tests by Freeman and Pryce, 2009
    - **double-loop TDD** -- the outer loop is the scenario, which fails until the whole want works. The inner loop is RGR on each small piece.
- Gherkin Reference
    - https://docs.reqnroll.net/latest/gherkin/gherkin-reference.html
- Not sure I like this one yet but putting it here: Chris Matts suggested that “hunting the value” was the first step, and flipped the template to put the benefit first: `“In order to <receive benefit> as a <role>, I can <goal/desire>”.` https://www.gov.uk/service-manual/agile-delivery/writing-user-stories

---

WORKFLOW:

x want(feat), docs(plan)[, test(plan), test(WIP)], test(RED)[, feat(WIP)], feat(GREEN), chore(refactor), docs(cleanup), docs(learn), repeat

BDD practice    Your step   Output  Commit
Discovery   the five questions  answers in the devlog   docs(plan)
Formulation answers → scenarios .feature file   test(plan)
Automation  step definitions    test_*.py   test(RED)

GREEN and refactor stay the same.

---

BACK BURNER:

- [ ] Unhappy paths: remove xfail -> RED -> GREEN -> refactor
- [ ] PLAN: /temperature


---

11/13/2026 4:38p -- PLAN

WORKFLOW:
x want(feat), docs(plan)[, test(plan), test(WIP)], test(RED)[, feat(WIP)], feat(GREEN), chore(refactor), docs(cleanup), docs(learn), repeat

"As a client, I want to ask for temperature, so I know if my pet is OK"

PLAN: healthz
"As a client, I want to reach the server, so that I can ask for the temperature"
docs(plan): the five questions, the promise, the test name
1. (`As a ____`) Who does it?
    - this is who you're gonna pretend to be in the test
    - [x] the client
2. (`When ____`) What do they do?
    - `# call it (act)`
    - [ ] request GET /healthz
    - [ ] request GET /temperature
3. (`Then ____`) What do they see?
    - `# check it (assert)`
    - test checks: proof that your setup worked
    - [ ] the valid http responses:
```
HTTP/1.1 200 OK            <- status line: version, code, reason phrase
Content-Type: text/plain
Content-Length: 2
                           <- blank line: headers are done
UP                         <- body
```
```
HTTP/1.1 200 OK            <- status line: version, code, reason phrase
Content-Type: text/plain
Content-Length: <bytes in the reading>
                           <- blank line: headers are done
<a valid reading>          <- body
```
4. (`Given ____`) What’s true beforehand (the situation the client walks into)?
    - what *I* the builder either build in GREENm or `# set it up (arrange)` in a test
    - [ ] the port is wired (code)
        (code connects port, host, and handler;
        you've chosen the start_server() arguments)
    - [ ] the server is listening (the port is turned on) (code)
    - [ ] /healthz and /temperature have routing (or, routing exists) (code)
    - [ ] a valid temperature reading is ready for serving (code)
    - [ ] something can produce valid http response text from inputs like code and body (code)
    - [ ] main() is running (test)
5. What must not happen?
    - `# check it (assert)`
    - more checks
    - [ ] no response
    - [ ] the server, port, or temperature sensor loop stops


---

# RGR -- healthz

RED:
- [ ] git commit -m "test(RED): "

GREEN:
- [ ] git commit -m "feat(GREEN): "

REFACTOR:
- [ ] DRY cleanup
- [ ] opens
- [ ] housekeeping / do now
- [ ] check each answer against the roadmap item
- [ ] git commit -m "chore(refactor):"
- [ ] docs(cleanup)
- [ ] docs(learn)
- [ ] repeat ;)

---

WORKFLOW:
x want(feat): this is feature discovery in BDD # devlog
[x docs(plan) -- general planning, e.g. this time it was documenting the BDD method]
x form(WIP) / form(plan): formulation in BDD -> .feature file
? test(WIP) / test(RED): if you are writing plain tests, no BDD
? feat(WIP) / feat(GREEN)
? chore(refactor): DRY and other code stuff; then 
? docs(cleanup): sometimes things change after you do the work
? docs(learn): the WIP -> done diff, plus any questions and realizations

---

# 11/20/2026 1:48p -- BDD -- features/healthz.feature
Claude.ai: hi-t3c-mcp-20261120: features/healthz.feature review

x "As a (client), I want to (reach the server), so that I can (know it's up)"
-> "As a tarantula keeper, I want to reach the server, So that I know my tarantula's monitor is still running"


> p: Don't look in memory or past chats. Read LINK_BDD_DOCS, LINK_GHERKIN_DOCS, and READING_LIST and review features/FILENAME.feature line by line with me. Check against the official docs and my own documentation and let's discuss options, misses, and reasonings, then make a decision before we move forward with running the tests using pytest_bdd.

1. `Feature: healthz endpoint`
    - ? heathz, healthz endpoint, Heath check, Know the server is up
    - decision: keep `healthz endpoint`
        - BDD docs examples mostly name a thing (Blog, Login)
    - [ ] add the template's "the want" wording to project docs
    - [x] git commit -m "form(plan): Feature title -- healthz" \
            -m "Feature title, user story, ???"





- [ ] git commit -m "form(plan): healthz .feature"

---

# 11/16/2026 1:50p -- BDD -- healthz
Claude.ai: Gherkin name origin
Claude.ai: TDD plan for hi-t3c-mpc main()

WORKFLOW:
x want(feat): this is feature discovery in BDD # devlog
[x docs(plan) -- general planning, e.g. this time it was documenting the BDD method]
x form(WIP) / form(plan): formulation in BDD -> .feature file
? test(WIP) / test(RED): if you are writing plain tests, no BDD
? feat(WIP) / feat(GREEN)
? chore(refactor): DRY and other code stuff; then 
? docs(cleanup): sometimes things change after you do the work
? docs(learn): the WIP -> done diff, plus any questions and realizations

## Bring Forward the User Story:
"As a (client), I want to (reach the server), so that I can (know it's up)"

## feature nametag

- [c] healthz -> features/healthz.feature, starting with docs/template.feature

## The Five Questions (from the user perspective except for #5)
Who → When → Then → Given
1. Who does it? (As a ...) [x] the client
2. What do they do (When ...) (# call it (act))?
    - [c] request GET /healthz
3. What do they see (Then ...) (# check it (assert))?
    - [-] (code) this http response
    - [c] (test) check status line and body only (for FastAPI swap later)
```
HTTP/1.1 200 OK            <- status line: version, code, reason phrase
Content-Type: text/plain
Content-Length: 2
                           <- blank line: headers are done
UP                         <- body
```
4. What must not happen (Then ...) (# check it (assert))?
    - [c] (test) the server stops answering after the first reply
5. What’s true beforehand (Given ...)
    (code): what GREEN must build; or (test): # set it up (arrange)
    - [c] (test) main() is running
    - [c] (test) nothing else is listening on PORT
    - [-] (code) the port is wired
        - the code connects port, host, and handler, start_server() arguments
    - [-] (code) the server is listening
        - the port is turned on
    - [-] (code) /healthz routing exists
        - decision: eventually this will be a routing table
    - [-] (code) a function produces valid http response text from e.g. code/body inputs
        - `_build_reply()` exists but needs its own test(s)
    - [-] (code) main() keeps running after it starts

- [x] git commit -m "form(WIP): healthz .feature; BDD workflow refinement"

---

# 11/16/2026 2:47p -- BDD "double-loop TDD" documentation -- healthz

- [x] Claude.ai "Gherkin name origin" PR#3

---

# 11/16/2026 1:50p -- BDD setup -- healthz

## Formulation
- [x] this is how typing the who/when/then/given results -> next step
- [x] pytest-bdd docs: read x Example, x Scenarios shortcut, x Step arguments, x Override fixtures via given steps, Backgrounds
- [x] grok `target_fixture`: when a `@given` step uses `target_fixture="name"`, the return value of that function becomes a Pytest fixture named `name`
    - see Claude.ai *"Gherkin name origin"*
    - **Fixture**: a value pytest hands a function, matched by parameter name
    - `target_fixture`: turns a step’s return value into a fixture for the rest of that scenario
    - **Scope**: one scenario; the next scenario starts with an empty table

.feature files
- [x] docs/template.feature
VS Code
- [x] Ctrl+Shift+X  # search "Cucumber", install the one by CucumberOpen
    - top result "Cucumber"
- [x] restart; open any .feature file  # colors appear
Sublime
- [x] Ctrl+Shift+P → "Package Control: Install Package" → "Cucumber"
- [x] open a .feature file → View → Syntax → Open all with current extension as → Cucumber → Gherkin

bdd templates
- [x] template.feature
- [x] docs/test_bdd_story_template.py

- [x] git commit -m "docs(plan): pytest_bdd templates"


---

# 11/13/2026 4:38p  -- PLAN -- healthz

WORKFLOW:
x want(feat), docs(plan)[, test(plan), test(WIP)], test(RED)[, feat(WIP)], feat(GREEN), chore(refactor), docs(cleanup), docs(learn), repeat

## Bring Forward the User Story:
"As a (client), I want to (reach the server), so that I can (ask for the temperature)"

## The Five Questions (from the user perspective except for #5)
Who → When → Then → Given
1. Who does it? (As a ...) [x] the client
2. What do they do (When ...) (# call it (act))?
    - [-] request GET /healthz
3. What do they see (Then ...) (# check it (assert))?
    - [-] (code) this http response
    - [-] (test) check status line and body only (for FastAPI swap later)
```
HTTP/1.1 200 OK            <- status line: version, code, reason phrase
Content-Type: text/plain
Content-Length: 2
                           <- blank line: headers are done
UP                         <- body
```
4. What must not happen (Then ...) (# check it (assert))?
    - [-] (test) the server stops answering after the first reply
5. What’s true beforehand (Given ...)
    (code): what GREEN must build; or (test): # set it up (arrange)
    - [-] (code) the port is wired
        - the code connects port, host, and handler, start_server() arguments
    - [-] (code) the server is listening
        - the port is turned on
    - [-] (test) nothing else is listening on PORT
    - [-] (code) /healthz routing exists
        - decision: eventually this will be a routing table
    - [-] (code) a function produces valid http response text from e.g. code/body inputs
        - `_build_reply()` exists but needs its own test(s)
    - [-] (test) main() is running
    - [-] (code) main() keeps running after it starts


- [c] Check each answer against the roadmap item? No. Put this in Refactor

## Write the promise -- one sentence for the whole scenario!?!?!?
Given → When → Then
- [-] "Given that the port is wired, the server is listening, nothing else is listening on PORT, /healthz routing exists, a function produces valid http response text from inputs, main() is running, and main() keeps running after it starts; When a user sends an http request `GET /healthz`, the server sends a valid http response with `200 OK` in the status line and `UP` in the body"

docstrings (promise details):
code name | condition \ more details
- [-] """ 200 | ???
          a client who requests the server gets a response """
- [-] git commit -m "docs(plan): server start and port assignment"

## Write the test name -- just one? really?

test names: `test_<interface>_<situation>_<what the client sees>`
- from: what's true beforehand
    - [~] test_http_port_is_wired / test_http_server_is_listening
    - [-] test_http_a_client_can_connect
    """port is wired and server is listening at 8000"
    - [-] test_route_temperature_returns_a_valid_reading
    """the temperature handler alone, with a planted reading -> 200 and that reading"""
    - [-] test_route_healthz_returns_200_UP
    """healthz handler alone, routing has to exist first"""
    - [-] test_service_a_valid_reading_exists
    """start main(), then check latest_temp fills, proves main() starts the loop
    reads memory instead of going through an interface, which is fine for wiring but
    isn't a client promise"""
- from: what do they do and what do they see
    - [-] test_request_get_healthz_returns_200_ok
    - [-] test_request_get_temperature_returns_200_and_a_valid_reading
- from: what must not happen
    - [-] test_service_remains_on_after_responses_sent
    """main() is still running after serving
    catches main() returning early, like forgetting to wait on the server"""
    - [-] test_service_remains_on_after_a_bad_request
    - [-] test_service_remains_on_after_a_sensor_reading_fails
    - [-] test_service_turns_on_and_stays_on_when_run_as_python_service_py


RED:
- [-] git commit -m "test(RED): "

GREEN:
- [-] git commit -m "feat(GREEN): "

REFACTOR:
- [-] DRY cleanup
- [-] opens
- [-] housekeeping / do now
- [-] check each answer against the roadmap item
- [-] git commit -m "chore(refactor):"
- [-] docs(cleanup)
- [-] docs(learn)
- [-] repeat ;)

no --> this is ridiculous. see Claude.ai reflective conversation: TDD and BDD health check. Conclusion: try TDD + BDD because so many of your items fromt he 5 questions map to BDD named concepts and there is even an existing package / framework for converting those items you just wrote and like into tests. You could just use docstrings and .md files, but the structure might be what you are looking for. Commit here and move forward with pytest-bdd and https://pytest-bdd.readthedocs.io/en/latest/.

Your next step: the 5 questions -> something real test stuff something something is called "Formulation" in that framework. Sounds good to me.

- [x] git commit -m "docs(plan): five questions for GET /healthz, adopt pytest-bdd" \
  -m "discovery: answered the five questions for one scenario (GET /healthz)" \
  -m "order: Who -> When -> Then (see, must not) -> Given; the Given is found last (Assert First)" \
  -m "Given split: (test) is what the test arranges, (code) is what GREEN must build" \
  -m "dropped: sorting answers against the roadmap; the user story sets scope, overlaps get combined in refactor" \
  -m "moving on to try pytest-bdd https://pytest-bdd.readthedocs.io/en/latest/" \
  -m "this maps your items you like to structured test and documentation categories" \
  -m "dropped: the one-sentence promise; Gherkin puts one condition per line" \
  -m "docs/template.feature: Gherkin template keyed to the five questions" \
  -m "next: formulation (.feature file), then automation (step definitions)"

---


11/12/2026 3:02p -- WANT

WORKFLOW:
x want(feat), x docs(plan)[, test(plan), test(WIP)], test(RED)[, feat(WIP)], feat(GREEN), chore(refactor), docs(cleanup), docs(learn), repeat

WANT:
README.md roadmap item
- [x] `main()`: start the sensor loop and the server on port 8000
user-story/why (in product terms): `As a ___, I want ___, so that ___`
- [x] "As a client, I want to reach the server, so that I can ask for the temperature"
- [x] "As a client, I want to ask for temperature, so I know if my pet is OK"
commit:
- [x] git commit -m "want(feat): start the service and reach it"

PLAN: healthz
"As a client, I want to reach the server, so that I can ask for the temperature"
docs(plan): the five questions, the promise, the test name
1. (`As a ____`) Who does it?
    - this is who you're gonna pretend to be in the test
    - [x] the client
2. (`When ____`) What do they do?
    - `# call it (act)`
    - [-] request GET /healthz
    - [-] request GET /temperature
3. (`Then ____`) What do they see?
    - `# check it (assert)`
    - test checks: proof that your setup worked
    - [-] the valid http responses:
```
HTTP/1.1 200 OK            <- status line: version, code, reason phrase
Content-Type: text/plain
Content-Length: 2
                           <- blank line: headers are done
UP                         <- body
```
```
HTTP/1.1 200 OK            <- status line: version, code, reason phrase
Content-Type: text/plain
Content-Length: <bytes in the reading>
                           <- blank line: headers are done
<a valid reading>          <- body
```
4. (`Given ____`) What’s true beforehand (the situation the client walks into)?
    - what *I* the builder either build in GREENm or `# set it up (arrange)` in a test
    - [-] the port is wired (code)
        (code connects port, host, and handler;
        you've chosen the start_server() arguments)
    - [-] the server is listening (the port is turned on) (code)
    - [-] /healthz and /temperature have routing (or, routing exists) (code)
    - [-] a valid temperature reading is ready for serving (code)
    - [-] something can produce valid http response text from inputs like code and body (code)
    - [-] main() is running (test)
5. What must not happen?
    - `# check it (assert)`
    - more checks
    - [-] no response
    - [-] the server, port, or temperature sensor loop stops


Check each answer against the roadmap item. ← missing?

test names: `test_<interface>_<situation>_<what the client sees>`
- from: what's true beforehand
    - [~] test_http_port_is_wired / test_http_server_is_listening
    - [-] test_http_a_client_can_connect
    """port is wired and server is listening at 8000"
    - [-] test_route_temperature_returns_a_valid_reading
    """the temperature handler alone, with a planted reading -> 200 and that reading"""
    - [-] test_route_healthz_returns_200_UP
    """healthz handler alone, routing has to exist first"""
    - [-] test_service_a_valid_reading_exists
    """start main(), then check latest_temp fills, proves main() starts the loop
    reads memory instead of going through an interface, which is fine for wiring but
    isn't a client promise"""
- from: what do they do and what do they see
    - [-] test_request_get_healthz_returns_200_ok
    - [-] test_request_get_temperature_returns_200_and_a_valid_reading
- from: what must not happen
    - [-] test_service_remains_on_after_responses_sent
    """main() is still running after serving
    catches main() returning early, like forgetting to wait on the server"""
    - [-] test_service_remains_on_after_a_bad_request
    - [-] test_service_remains_on_after_a_sensor_reading_fails
    - [-] test_service_turns_on_and_stays_on_when_run_as_python_service_py

docstrings (promise details):
code name | condition \ more details
- [-] """ 200 | ???
          a client who requests the server gets a response """
- [-] git commit -m "docs(plan): server start and port assignment"


RED:
- [-] git commit -m "test(RED): "

GREEN:
- [-] git commit -m "feat(GREEN): "

REFACTOR:
- [-] git commit -m "chore(refactor):"
- [-] docs(cleanup)
- [-] docs(learn)
- [-] repeat ;)


---

Claude wrote:

```python
# service.py -- the Service box

latest_reading = None   # step 3: the sensor arrow writes it, the 8000 arrow reads it


def read_sensor():
    """Step 2, arrow COM3 -> Service: ask the sensor once, return a number."""
    ...


def sensor_loop():
    """Step 4, on a clock: every few seconds, read_sensor() into latest_reading."""
    ...


def answer_temperature():
    """Step 2, arrow GET /temperature in on 8000 -> 18.3 back out."""
    ...
```

Step 3 is missing its variable. You added return types instead. That’s a good instinct, and it shows exactly why step 3 exists. listen_sensor keeps listening, so it never finishes, and a function that never finishes never returns. The reading can’t travel by return. It has to be written into a variable that get_and_send_http reads:

```python
latest_temp: float | None = None   # listen_sensor writes it, get_and_send_http reads it
```

(A small syntax note: a return annotation is just the type, -> float, with no name. Also, json isn’t a type. The answer is a number, so that one is -> float too.)

Step 4: yes, use async, and the while loop goes inside it. They aren’t alternatives. The loop is what repeats, and async is what lets it wait without freezing the program. On the NUC this is one Python program running on one thread:

- `time.sleep(2)` stops the whole program for 2 seconds, and Qs on 8000 sit waiting.
- `await asyncio.sleep(2)` stops only the loop, and Python answers Qs in the meantime.

```python
import asyncio

async def listen_sensor():
    while True:
        ...                       # read COM3, write latest_temp
        await asyncio.sleep(2)
```

`listen_sensor` has no return type now, because it never returns. That finishes the scaffold. Next you fill in `get_and_send_http` with a fake 18.3, the same first step as before.

---

11/6 2:25p

- [x] add a colon to the end of both def lines             # syntax error without it
- [x] listen_sensor: change -> float | None to -> None      # it never returns
- [x] listen_sensor: delete the return line                 # nothing after while True ever runs
- [x] get_and_send_http: delete the latest_temp parameter   # the sneaky one

---

11/7 12:46p

- [x] add at the top: import asyncio, import pytest, import service   # test_service.py
- [x] replace test 1 with the version below                          # test_service.py
- [x] replace test 2 with the skeleton below, fill in the 3 lines    # test_service.py
- [x] pytest                                                          # folder with both files


learn: asyncio

`asyncio.create_task()`
`asyncio.sleep()`
`asyncio.cancel()`

Underneath, it's one thread on one CPU core running a loop.
asyncio calls this the **event loop**. It keeps two lists in RAM:

- **ready:** paused functions that can run right now
- **timers:** paused functions waiting for a certain clock time

Each pass through the loop does four things:

1. Moves any timers whose time has come onto the ready list.
2. Asks the operating system whether any network connection has new bytes. This is how a Q arriving on port 8000 gets noticed. Whatever was waiting on those bytes moves onto ready.
3. Runs each ready function until it hits its next `await`. There it pauses and goes back to waiting.
4. Goes around again.

The key piece is `async def`. Calling an async function doesn't run it. `listen_sensor()` hands back a **coroutine**: the function, paused before its first line, with a saved spot for its local variables. Nothing happens until something puts it on the loop.

Here's what each call you've used does:

| You type | What happens |
|---|---|
| `asyncio.run(check())` | Builds an event loop and puts `check()` on it. Runs passes until `check()` finishes, then tears the loop down. |
| `asyncio.create_task(listen_sensor())` | Puts the coroutine on the ready list of a loop that's already running. It doesn't start yet, only at the next `await`. Outside async code there's no loop, which is why it errors there. |
| `await asyncio.sleep(0.1)` | Pauses this function, adds it to timers for 0.1 s from now, and frees the thread for whatever is ready. |
| `task.cancel()` | Flags the task. When it next wakes, it gets a `CancelledError` at its `await` instead of continuing, and stops. |

So test 1 plays out like this:

1. `asyncio.run` starts the loop with `check`.
2. `check` puts `listen_sensor` on ready, then sleeps, which frees the thread.
3. `listen_sensor` runs, writes 18.3, and pauses at its own sleep.
4. 0.1 s later, `check` wakes up, sees 18.3, and cancels `listen_sensor`.

so I could have written my own "while" loop, but asyncio does it for me, better

Yes. Inside asyncio there’s literally a while loop: `run_forever` calls `_run_once` over and over. What it does better than a hand-written one comes down to three things:

1. Pausing mid-function. A coroutine can stop at an await and pick up later with its local variables intact. A plain while loop can’t do that. You’d have to save each function’s state by hand.
2. Asking about many connections at once. One question to the operating system covers every open connection, instead of checking each one in turn.
3. Sleeping when nothing is ready. If no timer is due and no bytes have arrived, the thread actually sleeps until one of those happens. A hand-written loop tends to spin the CPU at 100% just checking.

Your `while True` in `listen_sensor` is still yours. It’s a small loop running inside the big one

---

- [x] parameterize -> parametrize          # pytest's spelling; it errors on the other one
- [x] assert result == test_temp           # = assigns, == compares
- [x] make the indentation all tabs        # the last 4 lines use spaces, the first 3 use tabs

---

```bash 
commit -m "first real tests" \
-m "green: listen_sensor stub writes a float to latest_temp model-level var" \
-m "green (by accident): get_and_send_http returns None" \
-m "RED:  -> next step: return latest_temp" \
-m "" \
-m "never trust a test you haven't seen fail"
-m "next step: make get_and_send_http pass"
```

---

hey wait, we didn't see the first test go red either ;)

- [x] take out the global line in service.py and you will!

```python
# global latest_temp  # use the module-level var, not a new local one
```

```bash
pytest
```

```python
 async def check():  # a loop
        task = asyncio.create_task(service.listen_sensor())
        await asyncio.sleep(0.1) # "soon" after it starts
>       assert isinstance(service.latest_temp, float)
E    assert False
E     +  where False = isinstance(None, float)
E     +    where None = service.latest_temp

test_service.py:28: AssertionError
=========================================================== short test summary info ===========================================================
FAILED test_service.py::test_listen_sensor_writes_a_float_to_latest_temp - assert False
========================================================= 1 failed, 1 passed in 0.42s ======
```

```bash
git add -A
git commit -m "test(RED): listen_sensor() writes a float"
```

- [x] comment back in
- [x] pytest
- [x] 2 passed

```bash
git add -A
git commit -m "test(GREEN): listen_sensor() writes a float" -m "listen_sensor() declares global latest_temp inside the function to grab the module-level var properly from the outside"
```

---

- [-] pytest test_service.py::test_get_and_send_http_returns_value_in_latest_temp
- [x] pytest -k http  # k=keywork=match any test with this text in the name

```python
=============================== FAILURES ======================
___________ test_get_and_send_http_returns_value_in_latest_temp[18.3] __________

test_temp = 18.3

    @pytest.mark.parametrize("test_temp", [18.3, None])
    def test_get_and_send_http_returns_value_in_latest_temp(test_temp):
        """ it returns whatever latest_temp holds. """

        # set it up
        service.latest_temp = test_temp  # 18.3, None

        # call it
        result = asyncio.run(service.get_and_send_http())

        # check it
>       assert result == test_temp  # = assigns, == compares
     ^^^^^^^^^^^^^^^^^^^^^^^^^^
E    assert None == 18.3

test_service.py:43: AssertionError
===================== short test summary info ====================
FAILED test_service.py::test_get_and_send_http_returns_value_in_latest_temp[18.3] - assert None == 18.3
================= 1 failed, 1 passed, 2 deselected in 0.24s =======
```

- [x] git commit -m "test(RED): "???"

> Make the stub able to fail. This is the standard trick. A stub that raises can’t accidentally match anything, so every case goes honestly red:

- [x] in get_and_send_http, replace ... with: raise NotImplementedError   # service.py
- [x] pytest -k http                                                      # expect 2 failed

I’d go with B. Then when you write return latest_temp, both cases go from red to green, and you can trust both of them.

```python
    async def get_and_send_http() -> float:
        """ Listen to port 8000 for http requests """
>       raise NotImplementedError
E    NotImplementedError

service.py:27: NotImplementedError
========== short test summary info =====================
FAILED test_service.py::test_get_and_send_http_returns_value_in_latest_temp[18.3] - NotImplementedError
FAILED test_service.py::test_get_and_send_http_returns_value_in_latest_temp[None] - NotImplementedError
========== 2 failed, 2 deselected in 0.39s =============
```

- [x] git commit -m "test(RED): get_and_send_http() returns latest_temp" -m "stub raises NotImplementedError so both cases fail"
- [x] return latest_temp in get_and_send_http()
- [x] pytest -k http
- [x] expect 2 passed

```python
====== 2 passed, 2 deselected in 0.11s ============
```

- [x] git commit -m "test(GREEN): get_send_http() returns latest_temp"

---

Refactor

This function just hands back a number -> 
- [x] function name -> answer_temperature()
Docstring should say what it actually does
- [x] docstring -> """Answer one GET /temperature with the latest reading"""
Test names change with a function name change
- [x] test_get_and_send_http_returns_value_in_latest_temp -> test_answer_temperature_returns_value_in_latest_temp

- [-] git commit -m "test(refactor): get_and_send_http() -> answer_temperature()" \
-m "The function doesn’t get or send any HTTP. Uvicorn does that part." \
-m "get_and_send_http() -> answer_temperature()" \
-m "docstring -> 'Answer one GET /temperature with the latest reading'" \
-m "test_get_and_send_http_returns_value_in_latest_temp -> test_answer_temperature_returns_value_in_latest_temp"

---

- [x] draft
so actually, you refactored get_and_send_http() -> 3 functions

f1:
f2:
f3:

plan: write your own http first, then refactor to FastAPI later

- [x] final
git commit -m "refactor: get_and_send_http() -> 3 functions" \
  -m "f1: answer_temperature() returns latest_temp (the old get_and_send_http body)" \
  -m "f2: get_and_send_http(reader, writer) reads the GET, writes the HTTP reply (stub)" \
  -m "f3: main() starts the sensor loop + server on 8000 (stub)" \
  -m "plan: write own http first, then refactor to FastAPI later"


---

- [x] git mv feedback.md devlog.md
- [x] general docs cleanup
- [x] git commit -m "docs: puzzle README + docs/ split" \
  -m "README: puzzle intro, stack, repo layout, tests, roadmap" \
  -m "docs/: design, interface-spec, scaffold-method, test-first-method" \
  -m "learning notes moved out of README"

---

your secrets ;)
- [x] git commit -m "chore: BIG SECRETS!! now hidden in plain sight"
- [x] git ls-files | grep calibration  # repo root
    - expect: calibration_constants.json must NOT be listed
    - actual [no output]

create and push the repo to github
- [x] gh repo create hi-t3c-mcp --public --source=. --push    # repo root
- [x] description
        "The most stable sensor ever built: every reading is a constant. Test-first Python asyncio service, headed for MCP."
- [x] topics
    python  asyncio  pytest  tdd  test-driven-development  rate-limiting  http-server  mcp  model-context-protocol  ai-agents  puzzle  railway

---

11/7 4:13p

Next on your roadmap is HTTP on port 8000, hand-written on asyncio. It’s the same loop you’ve done twice now:

- [x] Write handle_http’s promise in one sentence: what someone outside the function can see.
    - test_handle_http_gets_latest_temp()
        set it up (arrange)
            ask for the value
        run it (act)
            send the ask through the real function
            received = (service.handle_http(GET /temperature))
        check it (assert)
            assert received == 


Write the test and watch it go red. The stub already raises, so that part’s ready.
Make it green.
Commit RED and GREEN separately.

Step 1 is the only thing to do right now. The “someone outside” here is the client on the other end of port 8000, so the promise is your blue and black arrows: what the client sends, and what it gets back.

- [x] refactor get_and_send_http -> handle_http()
- [x] git commit -m "wip(RED): first draft of the http test, doesn't run yet"

---

Your promise is right: the reading, wrapped in HTTP. What doesn’t work is the call.

get_and_send_http doesn’t take a string, and it doesn’t return anything. The request arrives through reader and the reply leaves through writer, and those are the two ends of a real network connection. So the test can’t hand it "GET /temperature". The test has to be the client. It plays the Client Service box in your diagram: it opens a connection, sends the GET bytes, and reads the reply bytes.

```python
# open a connection
# sends the GET bytes
# read the reply bytes
```

- [x] happy path: red, green, refactor (fold in the handle_http rename); commit each
- [c] catalog the status codes in interface-spec.md; commit
- [c] one test per category, xfail if its behavior is a later roadmap step; commit each category

1. Group the categories by shared setup, not just by code. “Bad request bytes” (404, 400) can share one parametrized test, because only the bytes sent change. 503, 403, 429, and 410 each need their own setup, so each is its own category.
2. Tests for behavior you haven’t built yet should be marked, not left red. pytest has @pytest.mark.xfail(reason="rate limiter not built yet"), which means “expected to fail.” The suite stays green while the test sits there documenting the plan. When you reach that roadmap step, delete the mark and you’re at RED for real.


red: 
```python
>       assert reply.startswith(expected_status)
E    AssertionError: assert False
E     +  where False = <built-in method startswith of bytes object at 0x00007FF8
297393A8>(b'HTTP/1.1 200 OK')
E     +    where <built-in method startswith of bytes object at 0x00007FF8297393
A8> = b''.startswith

test_service.py:96: AssertionError
------------------------------ Captured log call ------------------------------
ERROR    asyncio:base_events.py:1879 Unhandled exception in client_connected_cb
transport: <_ProactorSocketTransport fd=556 read=<_OverlappedFuture finished res
ult=46>>
Traceback (most recent call last):
  File "C:\...\hi-t3c-mcp\service.py", line 35, in get_a
nd_send_http
    raise NotImplementedError
NotImplementedError
=========================== short test summary info ===========================
FAILED test_service.py::test_get_and_send_http_answers_get_temperature - Asserti
onError: assert False
======================= 1 failed, 4 deselected in 0.35s =
```

green:
your sevice.py needs to play the server now (the test is playing the client)
- [x] read https://docs.python.org/3/library/asyncio-stream.html. The “TCP echo server” example has almost exactly what you need.

Step    What happens    The call
1. Read the request, up to the blank line:
    `await reader.readuntil(b"\r\n\r\n")`
2. Get the number and turn it into body bytes
    `await answer_temperature()`; `str(...).encode()`
3. Build the reply: status line, headers, blank line, body
    - the mirror image of your build_request
4   Send it
    `writer.write(reply)`; `await writer.drain()`
5   Hang up
    `writer.close()`

- [x] git commit -m "wip(RED): get_and_send_http() draft, doesn't run"
- [!] git commit -m "test(RED): get_and_send_http() happy path"
    - you forgot this one

---

- [x] you did good except you need to wrap latest_temp in str() bc you .encode a string
but latest_temp is a float
- [x] pytest
    - expect: 5 green
    - actual [5 green] 
- [x] git commit -m "feat(GREEN): get_and_send_http() happy path" -m "answers GET /temperature with 200 OK + the reading"

---

11/8 2:00p

REFACTOR: get_and_send_http()

- [x] `_build_reply` docstring line 1: it was copied from `_build_request`
    ("the bytes a client sends")
      -> "the bytes the server sends back: status line, headers, blank line, body"
- [x] rename the local latest_temp in get_and_send_http to reading   
    (same name as the global reads confusingly)
- [x] answer_temperature docstring: drop TODO, "will call" -> "calls"
- [x] delete the stale comment on line 88
- [x] get_and_send_http -> handle_http (service.py, test name, handler var)
- [x] learning out of comments -> learning docs
- [!] git commit -m "refactor: get_and_send_http() -> handle_http()" \
  -m "test renamed: test_get_temperature_returns_200_with_the_reading" \
  -m "end_of_headers as bytes; local latest_temp -> reading" \
  -m "teaching comments moved out to stack-notes"
from our new stack-notes-git.md docs:
- [x] git commit --amend -m "chore(refactor): get_and_send_http() -> handle_http()" \
  -m "test renamed: test_get_temperature_returns_200_with_the_reading" \
  -m "end_of_headers as bytes; local latest_temp -> reading" \
  -m "teaching comments moved out to stack-notes"
- [x] git push --force    # only safe if nobody else has pulled it

---

WORKFLOW:
test(RED), feat(GREEN), chore(refactor), docs(cleanup), docs(plan)

---

DOCS: cleanup: 11/8 3:26p: PR/1 Claude.ai "Sensor data rate limiter service"

---

PLAN: http test suite: 11/8 4:01p

- [x] catalog the status codes in interface-spec.md; commit
    - [x] add a "Status codes" section to docs/interface-spec.md    # draft below
    - [c] decide: 503, or 200 with "None", before the first reading
    - [~] git commit -m "docs(plan): catalog the status codes"


```markdown
interface-spec.md:

## Status codes

| Code | Meaning here | Test category | Built in |
|---|---|---|---|
| `200 OK` | a reading exists; body is the reading | happy path | done |
| `503 Service Unavailable` | no reading yet | no reading | now |
| `404 Not Found` | path isn't `/temperature` (or a hint) | bad request | path parsing |
| `400 Bad Request` | the bytes aren't valid HTTP | bad request | path parsing |
| `403 Forbidden` | code missing or not on the list | access | access codes |
| `429 Too Many Requests` | over 5 per second for this code | rate | rate limiter |
| `410 Gone` | the readings are finished | end | end of message |

One test per category. The two bad-request codes share a parametrized test, since only the bytes sent change.
```

how did you come up with this list?
- [x] docs/http-error-model-method.md
- [x] add more codes to interface-spec.md now that we applied the method:
```markdown
405 Method Not Allowed  POST /temperature and the like, or fold it into 404
431 Request Header Fields Too Large no blank line within 64 KB
hang up, or 408 Request Timeout the client is too slow sending its request
```
Three decisions are still open in both files: 503 versus 200 with “None,” 405 versus 404, and hanging up versus 408.

The repo-layout trees in the README and design.md don’t list the new file yet. Add a line to each, or leave them for the next cleanup. A commit message that covers both files:

---

WORKFLOW:
test(plan), test(WIP), test(RED), feat(WIP), feat(GREEN), chore(refactor), docs(cleanup), docs(plan)

----

PLAN: http test suite (continued - remaining decisions): 11/8 4:47p

- [x] remaining
    - [!] decide: 503, or 200 with "None", before the first reading
        - [x] decision: 503 + Retry-After: 2
        - [x] learning: clients only retry when told when -> stack-notes-python.md
        - [x] decision: "not ready" is a status, not a value -> design.md #7
        - [!] new problem: clock-based readings repeat for fast clients
            - [x] decision/solution: when you implement access codes, make each allowed request gets the next reading for its code. That way nothing repeats and the end `410` is per code.
            - [c] captured in: design.md #8, README roadmap (access codes)
    - [!] still open: fold 405 and 501 into 404?
        - [x] decision: no -- these are different requests
        - [c] captured in interface-spec.md, http-error-model-method.md
    - [!] hang up vs 408
        - [x] decision: send 408 with a Connection: close header, then hang up
            (compatible with FastAPI too)
        - [c] captured in multiple docs

- [x] commit the catalog + method doc               # this step, docs only
    - [x] git commit -m "docs(plan): error model method + status codes catalog"

---

PLAN: http test suite (continued - test stubs, all xfail): 11/8 4:50p
next commit: test(plan): ...

- [x] write test stubs, one per category, all xfail       
- [x] pytest -k http
        - [x] http collects all the http tests (15, bc of the parametrize)
        - [x] 1 pass, 4 deselected, 10 xfailed
- [c] git commit -m "test(plan): all http test stubs, one per category, all xfail"


## Test names: 

Corrections:
- test_http_ on every one. They all test over a real connection, so pytest -k http runs exactly this group. Right now your happy-path test doesn’t contain “http,” so -k http misses it.
- Not answer_temperature. These tests never call that function. The subject is the HTTP request, and answer_temperature already has its own test.
- Situation first, code last. Each name reads like a bug report, and the codes line up at the end when you scan pytest’s output.
- 408 names the promise. “Is disconnected” is what the test checks. The 408 is the optional courtesy.
- 429 names the boundary. “Sixth request in one second” says exactly where the line is.
- 403 covers both cases. Missing and invalid codes both get it, so “without a valid code” fits

## Writing "promises" in the docstrings:

Applied to 403
Question    Answer
Who is outside? a client
What do they do?    asks for a reading
What’s true beforehand? they have no code, or a code that isn’t on the list
What do they see?   403 Forbidden
What must not happen?   they get a reading anyway

Now you try:
> slow client
@pytest.mark.xfail(reason="read timeout not built yet", strict=True)
def test_http_slow_client_is_disconnected():
    """408 Request Timeout | the client is too slow sending its request; reply carries `Connection: close`, then the server hangs up"""
    raise NotImplementedError("test not written yet")

Who is outside? a client
What do they do?    makes a connection but takes a long time before asking for a reading
What’s true beforehand? client just opened the connection
What do they see?   408 Request Timeout
What must not happen?   get a reading and/or stay connected 

test_http_slow_client_is_disconnected

A client who makes a connection but then doesn't send a request for x seconds gets 408 and the server hangs up

corrections:
Question    Yours   Refined
What do they do?
    - [~] takes a long time before asking 
    - [x] doesn’t finish sending its request
What’s true beforehand?
    - [~] client just opened the connection
    - [x] the connection is open; the read timeout is set
What do they see?
    - [~] 408
    - [x] the connection closes, with a 408 first
What must not happen?
    - [~] get a reading, stay connected
    - [x] stay connected (the main promise)

test name:

promise (docstring): a client that doesn't finish its request within the read timeout gets hung up on, with a 408 first



Try again:
> rate
@pytest.mark.xfail(reason="rate limiter not built yet", strict=True)
def test_http_sixth_request_in_one_second_returns_429():
    """429 Too Many Requests | over 5 per second for this code"""
    raise NotImplementedError("test not written yet")

Who is outside? a client
What do they do? ask for a 6th request within 1 second
What’s true beforehand? 5 requests within 1 second
What do they see? 429
What must not happen? get a reading

a client that sends a sixth request within a 1 second sliding window gets 429 until x

feedback: The promise has two edges. The 6th request inside the window gets 429, and a request after the window slides gets 200 again. The second edge is your “until x,” and it can be a second test too.

@pytest.mark.xfail(reason="rate limiter not built yet", strict=True)
def test_http_sixth_request_in_one_second_returns_429():
    """429 Too Many Requests | over 5 per second for this access code
    a sixth request from one access code within a 1-second sliding window gets 429 and no reading; Retry-After says when to try again"""
    raise NotImplementedError("test not written yet")

Try a 3rd time:
> end (last reading)
@pytest.mark.xfail(reason="end of readings not built yet", strict=True)
def test_http_after_last_reading_returns_410():
    """410 Gone | the readings are finished"""
    raise NotImplementedError("test not written yet")

Who is outside? a client
What do they do? asks for a reading after the last one available
What’s true beforehand? the last reading was sent
What do they see? 410 and the message that tells them it's the last one, because the design of the sensor might not indicate that it would ever stop in "reality". Should we hang up too?
What must not happen? keep sending readings

a client that sends a request after the last reading has been sent gets 410 Gone and a message to tell them that there are no more readings (and we hang up?)

++:
> end (last reading)
@pytest.mark.xfail(reason="end of readings not built yet", strict=True)
def test_http_after_last_reading_returns_410():
    """410 Gone | the readings are finished for this access code
    a request after this access code's last reading gets 410, a note that there are no more readings,
    and no reading; the sequence never starts over"""
    raise NotImplementedError("test not written yet")

- [x] git commit -m "test(plan): all http test stubs, one per category, all xfail"

---

old to new test names to remember what you learned:

- [x] happy path
    [x] test_get_temperature_returns_200_with_the_reading
    [c] test_http_get_temperature_returns_200_with_the_reading
- [c] no reading
    - [~] test_get_temperature_returns_503_with_no_reading_yet
    - [c] test_http_before_first_reading_returns_503
        - [c] 503 Service Unavailable | no reading yet; reply carries Retry-After: 2
- [c] bad request
    - [~] @pytest.mark.parametrize(input, [list of input])?
    - [~] test_get_temperature_returns_error_codes_for_bad_requests
    - [c] test_http_bad_request_returns_its_code
        - [c] `404 Not Found` | path isn't `/temperature` (or a hint)
        - [c] `405 Method Not Allowed` | path exists, method doesn't (`POST /temperature`); reply carries `Allow: GET`
        - [c] `400 Bad Request` | the bytes aren't valid HTTP
        - [c] `431 Request Header Fields Too Large` | no blank line within 64 KB `501 Not Implemented` | a method the server doesn't recognize at all (`FOO /temperature`)
- [c] slow client
    - [~] test_answer_temperature_returns_408_on_timeout
    - [c] test_http_slow_client_is_disconnected
        - [c] `408 Request Timeout` | the client is too slow sending its request; reply carries `Connection: close`, then the server hangs up
- [c] access
    - [~] test_answer_temperature_returns_403_on_missing_code
    - [c] test_http_without_valid_code_returns_403
        - [c] `403 Forbidden` | code missing or not on the list
- [c] rate
    - [~] test_answer_temperature_returns_429_rate_limited
    - [c] test_http_sixth_request_in_one_second_returns_429
        - [c] `429 Too Many Requests` | over 5 per second for this code
- [c] end
    - [~] test_answer_temperature_returns_410_on_end_of_readings
    - [c] test_http_after_last_reading_returns_410
        - [c] `410 Gone` | the readings are finished

- [x] learning docs update (PR #2)
- [x] git pull

---

claude.ai conversation started compacting -> move to a new one
hi-t3c-mcp 20261106: discovery

new chat:
hi-t3c-mcp 20261112: part deux
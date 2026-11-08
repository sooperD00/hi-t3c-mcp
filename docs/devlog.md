11/6/26 2:07p

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

- [ ] add a colon to the end of both def lines             # syntax error without it
- [ ] listen_sensor: change -> float | None to -> None      # it never returns
- [ ] listen_sensor: delete the return line                 # nothing after while True ever runs
- [ ] get_and_send_http: delete the latest_temp parameter   # the sneaky one

---

11/7 12:46p

- [ ] add at the top: import asyncio, import pytest, import service   # test_service.py
- [ ] replace test 1 with the version below                          # test_service.py
- [ ] replace test 2 with the skeleton below, fill in the 3 lines    # test_service.py
- [ ] pytest                                                          # folder with both files


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

- [ ] parameterize -> parametrize          # pytest's spelling; it errors on the other one
- [ ] assert result == test_temp           # = assigns, == compares
- [ ] make the indentation all tabs        # the last 4 lines use spaces, the first 3 use tabs

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

- [ ] git commit -m "test(RED): "???"

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

- [ ] final
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

- [ ] happy path: red, green, refactor (fold in the handle_http rename); commit each
- [ ] catalog the status codes in interface-spec.md; commit
- [ ] one test per category, xfail if its behavior is a later roadmap step; commit each category

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

---

- [x] you did good except you need to wrap latest_temp in str() bc you .encode a string
but latest_temp is a float
- [x] pytest
    - expect: 5 green
    - actual [5 green] 
- [x] git commit -m "feat(GREEN): get_and_send_http() happy path" -m "answers GET /temperature with 200 OK + the reading"

---

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
- [x] git commit -m "refactor: get_and_send_http() -> handle_http()" \
  -m "test renamed: test_get_temperature_returns_200_with_the_reading" \
  -m "end_of_headers as bytes; local latest_temp -> reading" \
  -m "teaching comments moved out to stack-notes"
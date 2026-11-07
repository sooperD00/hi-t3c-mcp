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
commit -m "test(RED): listen_sensor writes a float"
```
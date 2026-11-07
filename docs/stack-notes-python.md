# Python

## Writing a module-level variable from a function needs `global`

```python
latest_temp = None

async def listen_sensor():
    global latest_temp   # without this, the next line makes a new local variable
    latest_temp = 18.3
```

Reading it needs no declaration. Only writing does.

## `from module import name` makes a copy

`from service import latest_temp` grabs the value once, at import time, and never sees later writes. To see the current value, use `import service` and read `service.latest_temp`.

## A parameter hides a global with the same name

`def answer(latest_temp=None)` sees its own parameter, not the module-level `latest_temp`. In FastAPI it's worse: a parameter on an endpoint becomes something the client can set from the URL (`?latest_temp=99`).

## Tabs and spaces can't mix inside a block

Python raises `TabError` or `IndentationError: unindent does not match any outer indentation level`. In Sublime: View → Indentation → Convert Indentation to Tabs (or Spaces) fixes the whole file.

## Return annotations are just the type

`-> float`, not `-> temp: float`. `json` isn't a type; use what the function actually returns.

# asyncio

## What the event loop is

One thread runs a loop that keeps two lists: **ready** (paused functions that can run now) and **timers** (paused functions waiting for a clock time). Each pass moves due timers to ready, asks the OS which network connections have new bytes, runs each ready function until its next `await`, and goes around again. When nothing is ready, the thread sleeps.

## Calling an `async def` function doesn't run it

`listen_sensor()` returns a **coroutine**: the function paused before its first line. Something has to put it on the loop.

| Call | What happens |
|---|---|
| `asyncio.run(coro)` | builds a loop, runs `coro` until it finishes, tears the loop down |
| `asyncio.create_task(coro)` | puts `coro` on the running loop's ready list; it starts at the next `await`. Errors outside async code: there's no loop. |
| `await asyncio.sleep(s)` | pauses this function for `s` seconds and frees the thread |
| `time.sleep(s)` | freezes the whole thread, so nothing else runs |
| `task.cancel()` | the task gets a `CancelledError` at its next `await` and stops |

## You can't `await` a loop that runs forever

It never returns, so the `await` never finishes. Start it with `create_task` instead.

# pytest

## Finding and running tests

pytest runs files named `test_*.py` and the functions in them named `test_*`.

- `pytest file.py::test_name` runs one test.
- `pytest -k text` runs tests whose names contain `text` (`-k` = keyword). It takes `and`, `or`, and `not`.

## It's `parametrize`, not `parameterize`

```python
@pytest.mark.parametrize("test_temp", [18.3, None])
```

pytest errors on the other spellings.

## Testing async code without a plugin

```python
def test_something():
    async def check():
        task = asyncio.create_task(service.listen_sensor())
        await asyncio.sleep(0.1)
        assert isinstance(service.latest_temp, float)
        task.cancel()
    asyncio.run(check())
```

When lots of tests are async, the `pytest-asyncio` plugin lets the test itself be `async def`.

# Test first

A method for any project, written while building the Hi-T3C service.

## Before the first real test

Write a sanity test and run it:

```python
def test_sanity():
    assert 1 == 1
```

If it passes, the test runner found your file and ran it. From then on, any failure is about your code, not the setup.

## Writing a test

1. **Write down the promise each function makes, in one sentence.** Say it in terms of what someone outside the function can see, not what's inside it.
2. **Test the promise, not the stub.** "`latest_temp` is a float" stays true when the real sensor arrives. "`latest_temp == 18.3`" breaks the day it does.
3. **Every test has three parts:** set it up, call it, check it. (The usual name is *arrange, act, assert*.) A test that never calls the function is testing the language, not your code.

## Never trust a test you haven't seen fail

A test only proves something if it would fail when the code is wrong.

- **A stub should raise `NotImplementedError`, not `...`.** A `...` stub returns `None`, which can accidentally match an expected value and pass. A raising stub fails every case honestly.
- **If a test passes on its first run, break the code on purpose** and watch it go red, then undo the break. Pick a break you could actually make by mistake, like deleting a `global` line. (Tools that do this automatically are called *mutation testing*.)

## Red, green, refactor

1. **Red:** write the test and watch it fail for the reason you expect.
2. **Green:** make the smallest change that makes it pass.
3. **Refactor:** clean up names, comments, and layout. The tests stay green, which is how you know nothing broke.

Commit RED and GREEN separately, so the history shows each test failing before it passed.

## Reading a failure

- **A syntax error** stops the test runner before any test runs: `ERROR collecting ...` with a `SyntaxError`, `TabError`, or `IndentationError`.
- **A real red** says `FAILED`, and the lines starting with `E` show an `AssertionError`. Read from the bottom up. The middle of the traceback is only the path the error took on its way out.

## Worked example

Promises for the Hi-T3C service:

- `listen_sensor`: soon after it starts, `latest_temp` holds a number.
- `answer_temperature`: it returns whatever `latest_temp` holds.

```python
import asyncio
import pytest
import service


def test_listen_sensor_writes_a_float_to_latest_temp():
    """Soon after it starts, latest_temp holds a number."""
    async def check():  # the coroutine asyncio.run puts on the loop
        task = asyncio.create_task(service.listen_sensor())
        await asyncio.sleep(0.1)
        assert isinstance(service.latest_temp, float)
        task.cancel()
    asyncio.run(check())


@pytest.mark.parametrize("test_temp", [18.3, None])
def test_answer_temperature_returns_latest_temp(test_temp):
    """It returns whatever latest_temp holds."""
    service.latest_temp = test_temp                          # set it up
    result = asyncio.run(service.answer_temperature())      # call it
    assert result == test_temp                               # check it
```

The `None` case passed against a `...` stub before the function existed, only because the stub returned `None` anyway. Switching the stub to `raise NotImplementedError` made both cases red, so both greens meant something.

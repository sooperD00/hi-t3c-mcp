# Test first

A method for any project, written while building the Hi-T3C service. This is the inner loop. The outer loop, from a want to a failing scenario, is [want-to-done.md](want-to-done.md).

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

## Laying out test cases a person can review

- **Key each case on the situation** (the cause). The status code is the expected effect. Codes aren't unique per case: two different malformed requests both get 400, and missing and wrong access codes both get 403.
- **Put the code and its name side by side** every time (`"404", "Not Found"`) until the codes are second nature. Learn the first digit first: 2 means it worked, 4 means the client's fault, 5 means the server's fault.
- **The number is the identity; the name is a gloss.** Clients act on the number. The reason phrase is advisory, it's gone in HTTP/2 and 3, and names get renamed (RFC 9110 renamed 413 and 422).
- **Lay the cases out as an aligned table** with a header comment, so it reads like the spec table. Give odd values names (`NOT_HTTP`, `HUGE_HEADERS`) so each row stays one short line. Done this way, the comments become unnecessary.
- **Use one shared key** across the spec table, the test data, and the test output. That's *requirements traceability*: a reviewer matching on "404" lands on the right row every time.
- **No bare ambiguous words.** "Code" meant two things here, so it's `status_code` and `access_code`.

```python
BAD_REQUESTS = {
	# situation:            (code,  name,                              request)
	"unknown path":         ("404", "Not Found",                       _build_request("GET",  "/nope",        "localhost")),
	"POST to /temperature": ("405", "Method Not Allowed",              _build_request("POST", "/temperature", "localhost")),
	"not HTTP":             ("400", "Bad Request",                     NOT_HTTP),
	"headers over 64 KB":   ("431", "Request Header Fields Too Large", HUGE_HEADERS),
	"unknown method":       ("501", "Not Implemented",                 _build_request("FOO",  "/temperature", "localhost")),
}
```

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

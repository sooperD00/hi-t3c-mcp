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

# asyncio streams (TCP)

Docs: <https://docs.python.org/3/library/asyncio-stream.html>. The "TCP echo server using streams" example there is the minimal server shape.

## A server is `start_server` plus one handler call per connection

```python
async def handle(reader, writer):        # asyncio calls this once per client connection
    request = await reader.readuntil(b"\r\n\r\n")
    writer.write(b"...reply bytes...")
    await writer.drain()
    writer.close()

server = await asyncio.start_server(handle, "0.0.0.0", 8000)
await server.serve_forever()
```

`reader` is the bytes coming in from that one client. `writer` is where the reply bytes go back out.

| Call | What it does |
|---|---|
| `await reader.readuntil(sep)` | reads up to and including `sep`; `sep` must be bytes |
| `await reader.read()` | reads until the other side hangs up |
| `writer.write(data)` | puts bytes in an outgoing buffer in RAM; returns at once |
| `await writer.drain()` | waits until the OS has taken the buffered bytes (only really waits when the buffer is full) |
| `writer.close()` | hangs up; `await writer.wait_closed()` waits for that to finish |

## A client is `open_connection`: the same reader/writer pair from the other side

```python
reader, writer = await asyncio.open_connection("127.0.0.1", port)
```

## `readuntil` needs bytes, not str

```python
await reader.readuntil("\r\n\r\n")    # TypeError: argument should be integer or bytes-like object, not 'str'
await reader.readuntil(b"\r\n\r\n")   # works
```

## Port 0 means "any free port"

```python
server = await asyncio.start_server(handle, "127.0.0.1", 0)
port = server.sockets[0].getsockname()[1]   # the port the OS chose
```

Good for tests: they never collide with something already on 8000.

## A client that never finishes its request keeps the handler waiting

`readuntil` waits for the separator forever. In production, wrap reads in `asyncio.wait_for(..., timeout=...)`, or a slow or malicious client can hold connections open indefinitely.

# HTTP/1.1 by hand

## Read a request up to the blank line

You never know how many headers a client will send, but a blank line always marks the end of them. Every header line ends in `\r\n`, so the end of the last header plus the blank line is `\r\n\r\n`:

```python
end_of_headers = b"\r\n\r\n"
request = await reader.readuntil(end_of_headers)   # includes the \r\n\r\n
```

## The shapes

Request:

```
GET /temperature HTTP/1.1\r\n      <- method, path, version
Host: localhost:8000\r\n           <- headers, one per line
\r\n                               <- blank line: headers are done
```

Reply:

```
HTTP/1.1 200 OK\r\n                <- version, status code, reason
Content-Type: text/plain\r\n
Content-Length: 4\r\n              <- bytes of body that follow
\r\n                               <- blank line: headers are done
18.3                               <- body: exactly Content-Length bytes, no \r\n after
```

## `Content-Length` counts bytes, not characters

Compute it from the encoded body: `len(body.encode())`. `"18.3°C"` is 6 characters but 7 bytes.

## Why `Host` and `Content-Length` matter in 1.1

- `Host` is required, because one IP address can serve many websites.
- Connections stay open by default, so the client needs `Content-Length` (or the server hanging up) to know where the body ends.

## Clients only retry when told when

Browsers and plain `curl` don't retry on their own. Well-behaved programs and most agents retry when the reply includes `Retry-After: <seconds>`. Send it with `503` and `429`.

## A read timeout covers only the client sending its request

One connection, start to finish:

1. client connects
2. client sends the request, up to the blank line    <- the read timeout covers only this
3. server builds the reply and writes it
4. client reads the reply                            <- a write timeout would cover this
5. server hangs up

- It is not a limit between requests. If the server hangs up after every reply, there's no connection between requests to time.
- curl and agents send the whole request a few milliseconds after connecting, so they never get near it.
- Slow networks are fine: a 100-byte request takes about 15 ms even over a 56k modem.
- It catches clients that connect and then go quiet: stalled, malicious, or a person typing by hand.
- On timeout, send `408 Request Timeout` with `Connection: close`, then hang up.

## Typing HTTP by hand

`nc` (netcat) and `telnet` open a raw connection; whatever you type goes over the wire as-is:

    $ nc -C localhost 8000
    GET /temperature HTTP/1.1
    Host: localhost
    <Enter again: the blank line>

Plain `nc` sends only `\n` on Enter. `-C` makes it send `\r\n`, which HTTP requires; without it, a server waiting for `\r\n\r\n` never sees the end of the request, and its read timeout fires.

# str and bytes

## A network connection carries bytes; Python strings are characters

- `"text".encode()` → bytes (UTF-8 by default); `data.decode()` → str.
- `b"..."` writes bytes directly. It only accepts ASCII; for anything else, write a str and `.encode()` it.
- Plain ASCII characters are one byte each: `list("18.3".encode())` is `[49, 56, 46, 51]`.

## `float.encode()` doesn't exist

Turn numbers into text first: `str(18.3).encode()`.

# pytest

## When a server test gets an empty reply, read "Captured log call" first

The assertion only shows the symptom (`b''`). The handler's real exception (`AttributeError`, `TypeError`, `NotImplementedError`) is logged under "Captured log call."

## Testing a server: be the client

```python
server = await asyncio.start_server(handler, "127.0.0.1", 0)
port = server.sockets[0].getsockname()[1]
reader, writer = await asyncio.open_connection("127.0.0.1", port)
writer.write(request_bytes)
await writer.drain()
reply = await asyncio.wait_for(reader.read(), timeout=2)   # fail instead of hang
```

Assert on the promise (status line, body), not every header, so the test survives swapping in a framework.

## `xfail` for planned behavior

```python
@pytest.mark.xfail(reason="rate limiter not built yet")
```

Marks a test as expected to fail, so the suite stays green while the test documents the plan. Delete the mark when you build the behavior. `strict=True` turns an unexpected pass into a failure, which tells you when the mark is stale.

## Don't take expected values from the code under test

Give the test its own `CRLF` rather than importing the service's. If both use one definition, a mistake in it passes both.

# Naming

## A leading underscore means "internal to this file"

`_build_reply` signals a private helper. Nothing enforces it.

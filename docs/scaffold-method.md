# From a system diagram to a code scaffold

A method for any project: start from a box-and-arrow diagram of the real system, end with a file of empty, named stubs. Each step is a question you ask of the diagram.

## The steps

1. **Which boxes are code you write?**
   Cross out hardware, the operating system, and other people's programs. Whatever is left becomes your files.

2. **Every arrow that touches your box becomes a function.**
   An arrow in, an arrow out, or one arrow both ways: each is one function.

3. **Anything one arrow hands to another becomes a variable outside the functions.**
   If two functions never call each other, they can't pass a value by argument or `return`. The value has to wait in a spot both can reach.

4. **Anything that happens on a clock, instead of because an arrow fired, becomes a loop.**

5. **Write each one as an empty stub, with a comment naming its arrow.**
   That's the scaffold. Run it once to catch syntax errors. A pass prints nothing, since nothing calls the stubs yet.

6. **Something has to start it all.**
   One function runs at startup and starts the arrows. It doesn't carry data, so it doesn't sit on any arrow.

## Re-run the steps when a decision changes

Renaming a function, or picking a framework, can move a box. Run steps 1 and 2 again. For example, deciding that a framework handles the HTTP crosses out the "read the request bytes" part of an arrow and leaves a smaller function behind.

## From a sentence to a signature

To turn a one-sentence requirement into a function signature, take the sentence apart:

| Question about the sentence | Becomes |
|---|---|
| What's being asked? | the return type (a yes/no question returns `bool`) |
| What's different each time it's asked? | the parameters |
| What's the same every time? | set once, in `__init__` |
| What has to be remembered between asks? | state on `self`, which is why it's a class |

Name the function the way the caller would ask the question.

Example: "A request arrived at time `t`. Do we answer it?" becomes `RateLimiter(limit, per)` with `allow(t) -> bool`. If each client gets its own limit, the client changes from one ask to the next, so it becomes a parameter too: `allow(client, t)`.

## Worked example

The Hi-T3C service ([diagram](../design.PNG)):

1. Boxes: the USB sensor, COM port, and network port are hardware and the OS. The client is a phone browser. Only the Service box is left: `service.py`.
2. Arrows: COM3 in, and port 8000 in and out.
3. Shared: the sensor reading has to be waiting in RAM when a request arrives: `latest_temp`.
4. Clock: read the sensor every 2 seconds.
5. Scaffold:

```python
import asyncio

latest_temp: float | None = None  # listen_sensor writes it, answer_temperature reads it


# COM3 in
async def listen_sensor() -> None:
    """Read the sensor every 2 s and keep the latest reading."""
    global latest_temp  # writing a module-level variable needs this
    while True:
        latest_temp = 18.3  # STUB
        await asyncio.sleep(2)


# the number the reply carries
async def answer_temperature() -> float | None:
    """Return the latest reading."""
    raise NotImplementedError


# port 8000 in and out
async def handle_http(reader, writer) -> None:
    """Read the GET text, write the HTTP reply."""
    raise NotImplementedError


# starts both arrows
async def main() -> None:
    """Start the sensor loop and the server on 8000."""
    raise NotImplementedError
```

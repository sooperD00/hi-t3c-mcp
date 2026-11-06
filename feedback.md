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

2:25p

- [ ] add a colon to the end of both def lines             # syntax error without it
- [ ] listen_sensor: change -> float | None to -> None      # it never returns
- [ ] listen_sensor: delete the return line                 # nothing after while True ever runs
- [ ] get_and_send_http: delete the latest_temp parameter   # the sneaky one
# High-Temperature Tarantula Terrarium Checker: Hi-T3C Service

I want to check my tarantula's terrarium temperature while I'm at school so I can be confident she doesn't freeze to death. I set up a NUC with a USB temperature sensor to get and serve the data. I'm going to check it with my phone at school.


## Physical Requirements

- USB T-sensor
- NUC
- COM port
- Network port
- Phone with web access

## Software Requirements

- Python service on the NUC -> service.py

## System Diagram

```
      USB                          NUC
+-------------+        +--------------------------+
|             |        | Server                   |
|             |        |     +----------+         |
| T sensor    |--18.3--+---->| COM Port |         |
|             |        |     +----------+         |
| - Si sensor |        |          ^               |
|   chip      |        |          | COM3 (listen) |
|             |        |          |               |
| - Voltage   |        |     +----------+         |
|   -> number |        |     | Service  |  Python |
|   (18.3)    |        |     +----------+         |
|             |        |          |               |   HTTP/1.1 200 OK
+-------------+        |          | listen        |   Content-Type: text/plain
                       |          v               |   Content-Length: 4
                       |   +--------------+       |   18.3                        +---------+
                       |   | Network Port |-------+-----------------------------> | Client  |
                       |   |     8000     |<------+------------------------------ | Service |
                       |   +--------------+       |   GET /temperature HTTP/1.1   +---------+
                       |                          |   Host: 192.168.1.50:8000
                       +--------------------------+
```

## System -> Software Design


Methodology:

1. Identify code boxes

Which boxes are code you write? Cross out hardware, Windows, and other people’s programs. The USB sensor, COM port, and network port are hardware and Windows. The client is your phone’s browser, which someone else already wrote.

Only the Service box is left, so you get one file: service.py.

Scaffold after step 1:
```
hit3c/service.py
```

2. Identify functions

Every arrow that touches your box becomes a function. Service has two arrows: COM3 in, and port 8000 in and out. That makes two functions.

`service.py` after step 2:
```python

# COM3 in
def get_temperature():
	...

# port 8000 in and out
def get_and_send_http():
	...
```

3. Identify Variables

Anything one arrow hands to another becomes a variable outside the functions. The sensor’s reading has to be sitting in RAM, waiting, when a Q arrives.

`service.py` after step 3:
```python

# COM3 in
async def listen_sensor() -> temp: float
	...

# port 8000 in and out
async def get_and_send_http() -> msg: json
	...
```


4. Anything that happens on a clock, instead of because an arrow fired, becomes a loop. Reading the sensor every few seconds is on a clock.

Can we do async functions instead? I do know how to write a while loop but... let me know how to proceed.

5. Write each one as an empty stub, with a comment naming its arrow. That’s the scaffold.

Ok I think I did that. mmm Mine does not match yours.


## Fix Scaffold

```python
# service.py

import asyncio

""" module-level vars so latest T is waiting in RAM """
latest_temp: float | None = None 
	# the functions never call each other, so they can't pass a local var between them
	# listen_sensor writes it, get_and_send_http reads it
	# at "module-level" it lives ready in RAM

# COM3 in
async def listen_sensor() -> None:
	""" Listen to COM3 and cache the latest sensor reading """

	global latest_temp  # use the module-level var, not a new local one

	while True:
		### STUB ###
		latest_temp = 18.3
		############
		await asyncio.sleep(2)


# port 8000 in and out
async def get_and_send_http() -> float:
	""" Listen to port 8000 for http requests """
	...

```

## Copy corrected scaffold to .py and run

done

### Write your first tests

1. Write down the promise each function makes, in one sentence. Say it in terms of what someone outside the function can see, not what’s inside it.

- listen_sensor: soon after it starts, latest_temp holds a number.
- get_and_send_http: it returns whatever latest_temp holds.

2. Test the promise, not the stub. “latest_temp is a float” stays true when the real sensor arrives. “latest_temp == 18.3” breaks the day it does.

3. Let a test fail on purpose. get_and_send_http is still ..., which returns None, so its test fails right now. That failure tells you exactly what to write next.

You’ll need three Python facts that you just have to know:

- pytest finds files named test_*.py and runs the functions in them named test_*.
- A plain def test_... can run async code with asyncio.run(...).
- You can’t await a loop that runs forever. Instead, start it with asyncio.create_task(listen_sensor()), sleep a moment, check the variable, then call task.cancel().
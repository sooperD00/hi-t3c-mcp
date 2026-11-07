# service.py

import asyncio

""" module-level var so latest T is waiting in RAM 

	- the functions never call each other -> can't pass a local var
	- listen_sensor writes it, answer_temperature() reads it
"""
latest_temp: float | None = None 



# COM3 in
async def listen_sensor() -> None:
	""" Listen to COM3 and cache the latest sensor reading """

	global latest_temp  # module-level var for writing

	while True:
		latest_temp = 18.3   ## STUB
		await asyncio.sleep(2)  # seconds

async def answer_temperature() -> float | None:
	""" return the latest reading

		- TODO: get_and_send_http() will call this to answer the client's GET /temperature
		- `float | None`: latest_temp will be None before the first reading
		- no `global`: only writing needs it
	"""
	return latest_temp  # no `global` bc not writing

async def get_and_send_http(reader, writer) -> None:
	""" port 8000 in and out: read the GET text, write the HTTP reply """
	raise NotImplementedError

async def main() -> None:
	""" start it: sensor loop + server on 8000 """
	raise NotImplementedError


if __name__ == "__main__":
	print("")
	print("first run")
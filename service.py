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

	# global latest_temp  # use the module-level var, not a new local one

	while True:
		### STUB ###
		latest_temp = 18.3
		############
		await asyncio.sleep(2)  # seconds


# port 8000 in and out
async def get_and_send_http() -> float:
	""" Listen to port 8000 for http requests """
	...


if __name__ == "__main__":
	print("")
	print("first run")
# test_service.py

import asyncio
import pytest
import service  # service.py

# !from service import latest_temp! ## don't do this, you'l get only 1 instance

def test_foo():
	assert 1 == 1

def test_listen_sensor_writes_a_float_to_latest_temp(): 
	"""	soon after it starts, latest_temp holds a number. 

	asyncio steps:
		1. `asyncio.run` starts the loop with `check`.
		2. `check` puts `listen_sensor` on ready, then sleeps, which frees the thread.
		3. `listen_sensor` runs, writes 18.3, and pauses at its own sleep.
		4. 0.1 s later, `check` wakes up, sees 18.3, and cancels `listen_sensor`.

	[t-PLACEHOLDER]: only 1 test needs async right now, so use nested def -- no helper
	if lots of tests need async, use pytest-asyncio plugin rather than a helper
	"""

	async def check():  # the coroutine asyncio.run puts on the loop
		task = asyncio.create_task(service.listen_sensor())
		await asyncio.sleep(0.1) # "soon" after it starts
		assert isinstance(service.latest_temp, float)
		task.cancel()
	asyncio.run(check())  # run the loop

@pytest.mark.parametrize("test_temp", [18.3, None])
def test_answer_temperature_returns_value_in_latest_temp(test_temp):
	""" it returns whatever latest_temp holds. """
	
	# set it up
	service.latest_temp = test_temp  # 18.3, None

	# call it
	result = asyncio.run(service.answer_temperature())

	# check it
	assert result == test_temp  # = assigns, == compares
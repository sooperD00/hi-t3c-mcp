# test_service.py

import asyncio
import pytest
import service  # service.py

# !from service import latest_temp! ## don't do this, you'l get only 1 instance

### sanity test

def test_foo():
	assert 1 == 1


### listen_sensor()

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


### answer_temperature()

@pytest.mark.parametrize("test_temp", [18.3, None])
def test_answer_temperature_returns_value_in_latest_temp(test_temp):
	""" it returns whatever latest_temp holds. """
	
	# set it up
	service.latest_temp = test_temp  # 18.3, None

	# call it
	result = asyncio.run(service.answer_temperature())

	# check it
	assert result == test_temp  # = assigns, == compares


### get_and_send_http()

CRLF = "\r\n"  # every HTTP line ends with a carriage return + newline
HTTP_VERSION = "HTTP/1.1"   # which HTTP rules both sides follow

def _build_request(method: str, path: str, host: str) -> bytes:
	""" the bytes a client sends: request line, Host header, blank line """
	request_line = f"{method} {path} {HTTP_VERSION}"  # GET /temperature HTTP/1.1
	host_header = f"Host: {host}"                     # which server the client means
	blank_line = ""                                   # an empty line ends the headers
	text = request_line + CRLF + host_header + CRLF + blank_line + CRLF
	return text.encode()                        # sockets carry bytes, not str

def test_get_and_send_http_answers_get_temperature():
	""" a client that sends GET /temperature gets 200 OK with the latest reading """

	async def check():

		# vars
		test_temp = 18.3
		this_machine = "127.0.0.1"           # localhost: client and server on one computer
		any_free_port = 0                    # 0 = let the OS choose
		handler = service.get_and_send_http  # the server calls this once per connection
		request = _build_request("GET", "/temperature", this_machine)
		expected_status = f"{HTTP_VERSION} 200 OK".encode()
		end_of_headers = (CRLF + CRLF).encode()
		expected_body = str(test_temp).encode()  # 18.3 -> b"18.3"

		# set it up: a reading, and a server on a free port
		service.latest_temp = test_temp
		server = await asyncio.start_server(handler, this_machine, any_free_port)
		port = server.sockets[0].getsockname()[1]  # the port the OS chose

		# call it: be the client
		reader, writer = await asyncio.open_connection(this_machine, port)
		writer.write(request)
		await writer.drain()
		reply = await asyncio.wait_for(reader.read(), timeout=2)  # read until the server hangs up
		writer.close()
		server.close()

		# check it: the status line and the body, not every header
		assert reply.startswith(expected_status)
		assert reply.endswith(end_of_headers + expected_body)

	asyncio.run(check())
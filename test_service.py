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


### handle_http()

CRLF = "\r\n"  # every HTTP line ends with a carriage return + newline
HTTP_VERSION = "HTTP/1.1"   # which HTTP rules both sides follow

def _build_request(method: str, path: str, host: str) -> bytes:
	""" the bytes a client sends: request line, Host header, blank line """
	request_line = f"{method} {path} {HTTP_VERSION}"  # GET /temperature HTTP/1.1
	host_header = f"Host: {host}"                     # which server the client means
	blank_line = ""                                   # an empty line ends the headers
	text = request_line + CRLF + host_header + CRLF + blank_line + CRLF
	return text.encode()                        # sockets carry bytes, not str

# happy path
def test_http_get_temperature_returns_200_with_the_reading():
	"""200 OK | a reading exists; body is the reading
	a client that sends GET /temperature gets 200 OK with the latest reading as the whole body, then the server hangs up"""

	async def check():

		# vars
		test_temp = 18.3
		this_machine = "127.0.0.1"           # localhost: client and server on one computer
		any_free_port = 0                    # 0 = let the OS choose
		handler = service.handle_http  # the server calls this once per connection
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

# no reading
@pytest.mark.xfail(reason="503 reply not built yet", strict=True)
def test_http_before_first_reading_returns_503():
	"""503 Service Unavailable | no reading yet; reply carries Retry-After: 2
	a client asking before the first reading gets 503 with Retry-After set to the sensor period,
	never a 200 with a placeholder like 'None'"""
	raise NotImplementedError("test not written yet")

# bad requests
NOT_HTTP = ("not http at all" + CRLF + CRLF).encode()  # not valid HTTP
HUGE_HEADERS = (
	(f"GET /temperature {HTTP_VERSION}{CRLF}X-Filler: ").encode()
	+ b"a" * 70_000  # no blank line within 64 KB
)

BAD_REQUESTS = {
	# situation:            (code,  name,                              request)
	"unknown path":         ("404", "Not Found",                       _build_request("GET",  "/nope",        "localhost")),
	"POST to /temperature": ("405", "Method Not Allowed",              _build_request("POST", "/temperature", "localhost")),
	"not HTTP":             ("400", "Bad Request",                     NOT_HTTP),
	"headers over 64 KB":   ("431", "Request Header Fields Too Large", HUGE_HEADERS),
	"unknown method":       ("501", "Not Implemented",                 _build_request("FOO",  "/temperature", "localhost")),
}

@pytest.mark.xfail(reason="path parsing not built yet", strict=True)
@pytest.mark.parametrize("situation", BAD_REQUESTS,
	ids=lambda s: f"{BAD_REQUESTS[s][0]} {BAD_REQUESTS[s][1]} ({s})")
def test_http_bad_request_returns_its_status_code(situation):
	"""400, 404, 405, 431, 501 | bad request
	a client sending a request the server can't serve gets that situation's status code and name, and no reading;
	405 also carries Allow: GET, and the server keeps serving the next client"""
	status_code, name, request_bytes = BAD_REQUESTS[situation]
	raise NotImplementedError("test not written yet")

# slow client
@pytest.mark.xfail(reason="read timeout not built yet", strict=True)
def test_http_slow_client_is_disconnected():
	"""408 Request Timeout | client too slow sending its request; reply carries Connection: close, then the server hangs up
	a client that doesn't finish its request within the read timeout gets hung up on, with a 408 first"""
	raise NotImplementedError("test not written yet")

# access
@pytest.mark.xfail(reason="access codes not built yet", strict=True)
def test_http_reading_without_valid_access_code_returns_403():
	"""403 Forbidden | access code missing or not on the list
	a client asking for a reading without a valid access code gets 403 and no reading"""
	raise NotImplementedError("test not written yet")

# rate
@pytest.mark.xfail(reason="rate limiter not built yet", strict=True)
def test_http_sixth_request_in_one_second_returns_429():
	"""429 Too Many Requests | over 5 per second for this access code
	a sixth request from one access code within a 1-second sliding window gets 429 and no reading;
	Retry-After says when to try again, and rejected requests don't count toward the five"""
	raise NotImplementedError("test not written yet")

# end (last reading)
@pytest.mark.xfail(reason="end of readings not built yet", strict=True)
def test_http_after_last_reading_returns_410():
	"""410 Gone | the readings are finished for this access code
	a request after this access code's last reading gets 410, a note that there are no more readings,
	and no reading; the sequence never starts over"""
	raise NotImplementedError("test not written yet")
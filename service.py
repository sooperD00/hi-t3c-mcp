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


CRLF = "\r\n"  # every HTTP line ends with a carriage return + newline
HTTP_VERSION = "HTTP/1.1"   # which HTTP rules both sides follow

def _build_reply(code: str, reason: str, content_type: str, body: str) -> bytes:
	""" the bytes a client sends: request line, Host header, blank line 
	
	example: 
	b'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 4\r\n\r\n18.3'
	
	piece by piece:
		HTTP/1.1 200 OK\r\n          <- status line: version, code, reason
		Content-Type: text/plain\r\n <- what kind of body this is
		Content-Length: 4\r\n        <- how many bytes of body follow
		\r\n                         <- blank line: headers are done
		18.3                         <- body: exactly 4 bytes, no \r\n after it

	gotchas:
		No \r\n after the body. The body is exactly Content-Length bytes, and that’s why the test’s endswith(end_of_headers + expected_body) works.
		Content-Length is len(body) after .encode(), so compute it from the bytes, not the float.
	"""
	status_line = f"{HTTP_VERSION} {code} {reason}"  # _build_reply("200", "OK")  # "HTTP/1.1 200 OK\r\n"
	type_line = f"Content-Type: {content_type}"  # _build_reply("200", "OK", "text/plain")
	content_len_bytes = len(body.encode())  # calculate how many bytes in the body
	len_line = f"Content-Length: {content_len_bytes}"  # etc
	text = status_line + CRLF + type_line + CRLF + len_line + CRLF + CRLF + body
	return text.encode()                        # sockets carry bytes,

async def get_and_send_http(reader, writer) -> None:
	""" port 8000 in and out: read the GET text, write the HTTP reply 
	
		streams: https://docs.python.org/3/library/asyncio-stream.html 
			# "TCP echo server using streams"

		example request, e.g. from test_service.py: 
			b'GET /temperature HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n'
		e.g. from a real client, like `curl localhost:8000/temperature`:
			(more headers, still ending in a blank line):
			```
			GET /temperature HTTP/1.1\r\n
			Host: localhost:8000\r\n
			User-Agent: curl/8.9.1\r\n
			Accept: */*\r\n
			\r\n
			```
	"""

	# Read the request, up to the blank line
	# # You never know how many headers a client will send, 
	# # but the blank line always marks the end
	blank_line = b"\r\n\r\n"
	await reader.readuntil(blank_line)
	
	# Get the number and turn it into body bytes
	latest_temp = await answer_temperature()  # returns a float
	# latest_temp_bytes = str(...).encode()

	# Build the reply: status line, headers, blank line, body 
	# # the mirror image of your build_request
	code = "200"
	reason = "OK"
	content_type =  "text/plain"
	body = str(latest_temp)  # float -> str
	reply = _build_reply(code, reason, content_type, body)

	# Send it
	writer.write(reply)
	await writer.drain()

	# Hang up
	writer.close()



async def main() -> None:
	""" start it: sensor loop + server on 8000 """
	raise NotImplementedError


if __name__ == "__main__":
	print("")
	print("first run")
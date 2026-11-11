# Interface spec

What the code exposes. This file changes whenever a field, signature, or format changes. The reasons behind it live in [design.md](design.md).

## Module state

| Name | Type | Written by | Read by |
|---|---|---|---|
| `latest_temp` | `float \| None` | `listen_sensor()` | `answer_temperature()` |

`latest_temp` is `None` until the first reading.

## Functions

| Function | Diagram arrow | Signature | Status |
|---|---|---|---|
| `listen_sensor` | COM3 in | `async () -> None` | stub: writes 18.3 every 2 s |
| `answer_temperature` | the number the reply carries | `async () -> float \| None` | done: returns `latest_temp` |
| `handle_http` | port 8000 in and out | `async (reader, writer) -> None` | happy path: 200 + the reading |
| `_build_reply` | builds the port 8000 reply | `(code, reason, content_type, body: str) -> bytes` | done (private helper) |
| `main` | none: starts both arrows | `async () -> None` | stub: raises `NotImplementedError` |

## Config

| Setting | Value |
|---|---|
| Sensor read period | 2 s |
| Sensor port | `COM3` |
| HTTP port | 8000 |
| Rate limit (planned) | 5 requests per 1 s |
| Read timeout (planned) | 10 s  (slow enough for a phone connection) |

## HTTP

Request:

```
GET /temperature HTTP/1.1
Host: <server>:8000

```

Reply:

```
HTTP/1.1 200 OK
Content-Type: text/plain
Content-Length: 4

18.3
```

Over the rate limit (planned):

```
HTTP/1.1 429 Too Many Requests
Retry-After: 1

```

## Status codes

| Code | Meaning here | Test category | Built in |
|---|---|---|---|
| `200 OK` | a reading exists; body is the reading | happy path | done |
| `503 Service Unavailable` | no reading yet; reply carries `Retry-After: 2` | no reading | now |
| `404 Not Found` | path isn't `/temperature` (or a hint) | bad request | path parsing |
| `405 Method Not Allowed` | path exists, method doesn't (`POST /temperature`); reply carries `Allow: GET` | bad request | path parsing |
| `400 Bad Request` | the bytes aren't valid HTTP | bad request | path parsing |
| `431 Request Header Fields Too Large` | no blank line within 64 KB | bad request | path parsing |
| `501 Not Implemented` | a method the server doesn't recognize at all (`FOO /temperature`) | bad request | path parsing |
| `408 Request Timeout` | the client is too slow sending its request; reply carries `Connection: close`, then the server hangs up | slow client | read timeout |
| `403 Forbidden` | access code missing or not on the list | access | access codes |
| `429 Too Many Requests` | over 5 per second for this code | rate | rate limiter |
| `410 Gone` | the readings are finished | end | end of message |

One test per category. The two bad-request codes share a parametrized test, since only the bytes sent change.

The slow-client test checks the promise (that the server hangs up in time) and accepts either an empty reply or `408`.

Methodology: [http-error-model-method.md](http-error-model-method.md).

## Planned

- `GET /reading?code=<code>` replaces `/temperature` when access codes land; rate limited per code
- An MCP tool wrapping the same reading

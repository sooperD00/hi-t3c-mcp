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
| `handle_http` | port 8000 in and out | `async (reader, writer) -> None` | stub: raises `NotImplementedError` |
| `main` | none: starts both arrows | `async () -> None` | stub: raises `NotImplementedError` |

## Config

| Setting | Value |
|---|---|
| Sensor read period | 2 s |
| Sensor port | `COM3` |
| HTTP port | 8000 |
| Rate limit (planned) | 5 requests per 1 s |

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

## Planned

- `GET /reading?code=<code>`, rate limited per code
- An MCP tool wrapping the same reading

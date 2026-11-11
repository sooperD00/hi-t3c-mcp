# Deriving an HTTP error model

The **error model** (or response catalog) is the complete set of responses an HTTP service can give, with the condition behind each one. This method derives it from finite lists instead of a brainstorm, so you can tell when it's complete. It works for any HTTP service.

## The steps

### 1. Collect outcomes from four sources

Each source is a finite list you can walk item by item.

| Source | Walk this list | Ask of each item |
|---|---|---|
| Requirements | every rule with "must," "only," "at most," "until" | What happens when a request breaks this rule? |
| Protocol | what HTTP obliges any server to handle (RFC 9110; RFC 6585 for 429 and 431) | Can a client send us this? |
| Each call in the handler | the exceptions the docs list for every function you call | What does the client see when this raises? |
| Each dependency | everything the handler needs that could be missing or not ready | What happens when it's missing? |

A brainstorm (FMEA-style) still helps as a final pass, but it isn't the source.

### 2. Map each outcome to a code, and prune

HTTP defines what each status code means. Pick the one whose definition matches the outcome. Some outcomes get no reply at all, because the client is already gone.

Cross out outcomes your design can't reach. The catalog is relative to your design, not to the roughly 60 codes HTTP defines.

### 3. Arrange the outcomes as ordered gates

Walk one request through the service. Each place it can fail is a gate. Put the gates in the order the service checks them.

When several gates would fail, the first one wins, so the order is a design decision. Example: rate-limit by IP before checking an access code, or a bot can guess codes as fast as it likes.

The walk is also a check. If it finds a gate that no source produced, a source was missed.

### 4. Check completeness

- Every gate is a yes/no question, and both answers lead somewhere.
- List what can vary in a request (method, path, bytes, size, timing, credentials, rate, service state) and every value each one can take. Every value maps to an outcome.
- Watch every "anything else" value. If HTTP splits it further, split it too. (501 was first missed because "method: GET, or anything else" was too coarse.)

### 5. Write the outputs

- **The status-code table** in the interface spec: code, condition, test category.
- **One test per category**, where a category is a group of requests the service treats the same way (*equivalence partitioning*). Codes that share a setup and differ only in the bytes sent can share one parametrized test.
- **Tests at the edges** (*boundary values*), like the 5th versus 6th request in one second.
- **Tests for gates not built yet** get `@pytest.mark.xfail(reason=...)` until their step on the roadmap.
- **From the table to the tests:** each "Test category" becomes one test, and each "Built in" becomes that test's `xfail` reason. See "From the error model to a test" in [test-first-method.md](test-first-method.md).

### 6. Reality check

A service can only send codes that appear in its code. Search for every place a reply is built: that list is the true catalog today. Compare it with the table.

## Worked example: Hi-T3C

### 1. Collect

| Source | Item | Outcome |
|---|---|---|
| Requirements | serves only `/temperature` | unknown path |
| | an access code is required | missing or invalid code |
| | at most 5 requests per second | over the limit |
| | readings stop at the end | finished |
| Protocol | bytes must be valid HTTP | malformed request |
| | method must be one the resource supports | wrong method (`POST /temperature`) |
| | the request must arrive in reasonable time | client too slow |
| | method must be one the server recognizes | unrecognized method (`FOO /temperature`) |
| Each call | `reader.readuntil()` raises `IncompleteReadError` | client hung up early |
| | `reader.readuntil()` raises `LimitOverrunError` | headers over 64 KB |
| Dependencies | the sensor reading | no reading yet |
| | the readings config | config missing |

### 2. Map and prune

| Outcome | Code |
|---|---|
| a reading exists | `200 OK` |
| no reading yet | `503 Service Unavailable`, with `Retry-After: 2` |
| unknown path | `404 Not Found` |
| known method the path doesn't support | `405 Method Not Allowed`, with `Allow: GET` |
| method the server doesn't recognize    | `501 Not Implemented` |
| malformed request | `400 Bad Request` |
| headers over 64 KB | `431 Request Header Fields Too Large` |
| client too slow | `408 Request Timeout` with `Connection: close`, then hang up |
| client hung up early | no reply: nobody is there to receive it |
| missing or invalid code | `403 Forbidden` |
| over the limit | `429 Too Many Requests` |
| finished | `410 Gone` |
| config missing | fail at startup, not per request |

Pruned:

- `401`: needs an authentication-header scheme, which this service doesn't use
- `201`: nothing here creates anything
- `500`: a crash. FastAPI sends it; the hand-written server just drops the connection. Not tested on purpose.

### 3. Arrange

1. Did the whole request arrive, in time and under the size limit? (408; 431)
2. Is it valid HTTP? (400)
3. Is this client under its rate, by IP? (429)
4. Is it a path we serve, with a method it supports? (404; 405 or 501)
5. Is the access code valid? (403)
6. Are the readings still going? (410)
7. Is there a reading yet? (503)
8. All yes: 200

### 4. Check completeness

| What varies | Values | Outcomes |
|---|---|---|
| method | GET, another known method, unrecognized | continue, 405, 501 |
| path | `/temperature`, anything else | continue, 404 |
| bytes | valid HTTP, malformed | continue, 400 |
| size | normal, headers over 64 KB | continue, 431 |
| timing | in time, too slow, hung up | continue, 408, no reply |
| code | valid, invalid, missing | continue, 403, 403 |
| rate | under, over | continue, 429 |
| state | before first reading, running, finished | 503, 200, 410 |

### 5. Write the outputs

- **Status-code table:** [interface-spec.md](interface-spec.md#status-codes)
- **One test per category:**

  | Category | Codes | Setup |
  |---|---|---|
  | happy path | 200 | a reading exists |
  | no reading | 503 | `latest_temp = None` |
  | bad request | 400, 404, 405, 431, 501 | one parametrized test; only the bytes sent change |
  | slow client | 408 | send half a request, wait out the timeout |
  | access | 403 | missing or invalid code |
  | rate | 429 | over the limit in one second |
  | end | 410 | every reading already served |

- **Boundary tests:** the 5th request in a second (200) versus the 6th (429), and headers just under versus just over 64 KB.
- **When a code is a courtesy**: like `408`, test the promise underneath it (the server hangs up in time) and accept the courtesy as optional. The test then survives a framework swap.
- **Not built yet:** every category except the happy path starts as `xfail` until its roadmap step.

### 6. Reality check (today)

`handle_http` builds exactly one reply: `200`. Everything else in the table is planned.

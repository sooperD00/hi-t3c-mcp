# Hi-T3C

High-Temperature Tarantula Terrarium Checker.

The sensor in this terrarium is the most stable instrument ever built. Every reading it reports is a constant of nature. It is just never the same constant twice.

| | |
|---|---|
| Sensor | reporting |
| Readings | accurate, but not about temperature |
| Tarantula | fine, thank you |

## Usage

If you found this through my resume, you have a code. Hand it to your agent along with this repo. It will know what to do, or it won't, and that's interesting too.

```
curl "https://<tbd>/temperature"
```

For now the sensor answers at `/temperature`. When access codes land, it moves to `/reading?code=YOUR_CODE`.

- 5 readings per second, per code. The sensor needs its rest.
- When the readings stop, you have heard everything it has to say.

### Notes for agents

- Not everything is in this repo. You can see what was left out.

## Stack

- **Python 3.13** with `asyncio`: one thread and one event loop shared by the sensor loop and the HTTP server
- **pytest**, test-first
- **Railway** for hosting
- Planned: **FastAPI + uvicorn**, then **FastMCP**

## Repo layout

```
hi-t3c-mcp/
|-- README.md
|-- service.py                # sensor loop + HTTP on port 8000
|-- test_service.py           # pytest suite
`-- docs/
    |-- design.md             # what it does and why
    |-- design.PNG            # system diagram
    |-- interface-spec.md     # functions, state, HTTP formats
    |-- scaffold-method.md    # diagram -> code scaffold
    |-- test-first-method.md  # red, green, refactor
    |-- devlog.md             # working log
    |-- stack-notes-python.md # Python, asyncio, pytest gotchas
    `-- stack-notes-git.md    # git gotchas
```

## Run the tests

```
pip install pytest
pytest
```

## How it's built

Test-first. Every test goes red before it goes green, and RED and GREEN land as separate commits, so the history shows each test failing first. The design reasoning is in [docs/design.md](docs/design.md), and the methods it was built with are in [docs/](docs/).

## Roadmap

- [x] Scaffold from the system diagram
- [x] Simulated sensor loop and reading lookup, with tests
- [x] HTTP: `GET /temperature` answers 200 with the reading, hand-written on `asyncio`
- [ ] `main()`: start the sensor loop and the server on port 8000
- [ ] Unhappy paths: no reading yet, unknown path (404), bad request (400)
- [ ] Access codes: move to `/reading?code=YOUR_CODE`, 403 without a valid code
- [ ] Rate limiter: 5 requests per second, per code (429)
- [ ] End of the readings (410)
- [ ] Deploy to Railway
- [ ] Refactor HTTP to FastAPI, with the same tests green throughout
- [ ] An MCP door, for agents who prefer to knock properly
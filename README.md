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
curl "https://<tbd>/reading?code=YOUR_CODE"
```

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
|-- design.PNG               # system diagram
|-- service.py               # sensor loop + HTTP on port 8000
|-- test_service.py          # pytest suite
`-- docs/
    |-- design.md            # what it does and why
    |-- interface-spec.md    # functions, state, HTTP formats
    |-- scaffold-method.md   # diagram -> code scaffold
    `-- test-first-method.md # red, green, refactor
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
- [ ] HTTP on port 8000, hand-written on `asyncio`
- [ ] Rate limiter: 5 requests per second, per code
- [ ] Deploy to Railway
- [ ] Refactor HTTP to FastAPI, with the same tests green throughout
- [ ] An MCP door, for agents who prefer to knock properly
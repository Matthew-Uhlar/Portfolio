# Support Ticket API

A small Python API for tracking support requests, with SQLite storage and no third-party dependencies. I kept the domain focused so the interesting parts are easy to inspect: status rules, input validation, transactions, and HTTP tests.

## Run it

Requires Python 3.11 or newer. From this directory:

```sh
python server.py --db tickets.db --seed
python server.py --db tickets.db --port 8000
```

The seed command adds three fictional tickets each time it runs. Skip it for an empty database. The server binds to `127.0.0.1`; stop it with Ctrl+C. SQLite creates the database on the first run and checks its schema version on later runs.

```sh
curl http://127.0.0.1:8000/tickets
curl -X POST http://127.0.0.1:8000/tickets -H "Content-Type: application/json" -d '{"title":"Export button fails","description":"Clicking export leaves the page unchanged."}'
curl -X PATCH http://127.0.0.1:8000/tickets/1 -H "Content-Type: application/json" -d '{"status":"in_progress"}'
```

These examples use a POSIX shell. In PowerShell, use `Invoke-RestMethod`:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/tickets -Method Post -ContentType 'application/json' -Body '{"title":"Export button fails","description":"Clicking export leaves the page unchanged."}'
```

## API

| Method | Path | Behavior |
| --- | --- | --- |
| GET | `/health` | Process health; does not check the database |
| GET | `/tickets` | List newest first; accepts `status`, `q`, `limit`, `offset` |
| POST | `/tickets` | Create from required `title` and `description`; returns 201 |
| GET | `/tickets/{id}` | Ticket and its comments, oldest comment first |
| PATCH | `/tickets/{id}` | Update title, description, or status |
| DELETE | `/tickets/{id}` | Delete ticket and comments; returns empty 204 |
| POST | `/tickets/{id}/comments` | Add required `body`; returns 201 |
| GET | `/reports` | Total tickets and counts for every status |

List responses contain `items`, `total`, `limit`, and `offset`. Default page size is 20, maximum 100; offset is 0–100000. Search matches literal substrings in title or description, with SQLite's built-in lowercase behavior (primarily ASCII). `%` and `_` are ordinary search text. Search text is limited to 200 characters. Unknown or repeated query parameters on the list endpoint are rejected.

Titles allow 160 characters, descriptions 10000, and comments 4000. Required text cannot be blank. Bodies must be JSON objects, unknown fields are rejected, and request bodies are limited to 64 KiB. Times are UTC ISO 8601 strings. Errors use `{"error":"message"}` with 400 for invalid input, 404 for missing resources, 405 for unsupported methods on known routes, 409 for invalid transitions, and 503 for database operational failures. HTTP methods outside the implemented handlers use Python's default 501 response.

Allowed status changes:

| Current | Next |
| --- | --- |
| open | in_progress, closed |
| in_progress | open, resolved |
| resolved | open, closed |
| closed | open |

Setting the current status again is allowed. A rejected update changes nothing, including other fields sent with it.

## Design and tests

`tickets.py` owns the schema and business rules. `server.py` translates HTTP requests into store calls. SQL values use bound parameters. Status updates acquire a write transaction before reading the current ticket; list counts and rows share a read transaction. Each operation opens and closes its own connection, so request threads do not share one connection.

```sh
python -m unittest discover -v
```

Tests create temporary databases and start a real HTTP server on an automatically selected port. They cover persistence, rejected-update rollback, status transitions, comment deletion, filtering, pagination, reports, malformed input, and an HTTP lifecycle.

I chose the standard library to make the project easy to run and to make request handling visible. The tradeoff is that this is a local learning/demo API: it has no login, authorization, TLS, audit log, or rate limiting. Python's `http.server` is not a production web server. I would add authentication and a maintained web framework before deploying this for real users. Offset pagination and substring search are fine for a small demo; larger datasets would need different indexing and pagination choices.

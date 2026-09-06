"""Small localhost HTTP adapter for the ticket store."""

import argparse
import json
import re
import sqlite3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

from tickets import ConflictError, NotFoundError, Store, ValidationError


def make_server(store, port=8000):
    class Handler(BaseHTTPRequestHandler):
        def setup(self):
            super().setup()
            self.connection.settimeout(10)

        def reply(self, status, data=None, allow=None):
            body = json.dumps(data).encode() if data is not None else b""
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("X-Content-Type-Options", "nosniff")
            if allow:
                self.send_header("Allow", allow)
            self.end_headers()
            self.wfile.write(body)

        def read_body(self):
            if len(self.headers.get_all("Content-Length", [])) != 1:
                raise ValidationError("Exactly one Content-Length header is required")
            if self.headers.get("Transfer-Encoding"):
                raise ValidationError("Transfer-Encoding is not supported")
            if self.headers.get_content_type() != "application/json":
                raise ValidationError("Content-Type must be application/json")
            try:
                length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                raise ValidationError("Invalid Content-Length")
            if not 1 <= length <= 65536:
                raise ValidationError("Body must be 1..65536 bytes")
            try:
                return json.loads(self.rfile.read(length))
            except (ValueError, UnicodeDecodeError):
                raise ValidationError("Invalid JSON")

        def dispatch(self):
            try:
                url = urlsplit(self.path)
                method = self.command
                match = re.fullmatch(r"/tickets/([1-9][0-9]{0,17})(/comments)?", url.path)
                if url.path == "/health" and method == "GET":
                    return self.reply(200, {"status": "ok"})
                if url.path == "/reports" and method == "GET":
                    return self.reply(200, store.report())
                if url.path == "/tickets":
                    if method == "POST":
                        return self.reply(201, store.create(self.read_body()))
                    if method == "GET":
                        query = parse_qs(url.query, keep_blank_values=True, max_num_fields=10)
                        if set(query) - {"status", "q", "limit", "offset"} or any(len(v) != 1 for v in query.values()):
                            raise ValidationError("Unknown or repeated query parameter")
                        try:
                            limit = int(query.get("limit", ["20"])[0])
                            offset = int(query.get("offset", ["0"])[0])
                        except ValueError:
                            raise ValidationError("limit and offset must be integers")
                        return self.reply(200, store.list(query.get("status", [None])[0], query.get("q", [""])[0], limit, offset))
                elif match:
                    ticket_id = int(match[1])
                    if match[2]:
                        if method == "POST":
                            return self.reply(201, store.comment(ticket_id, self.read_body()))
                    elif method == "GET":
                        return self.reply(200, store.get(ticket_id))
                    elif method == "PATCH":
                        return self.reply(200, store.update(ticket_id, self.read_body()))
                    elif method == "DELETE":
                        store.delete(ticket_id)
                        return self.reply(204)
                elif url.path not in {"/health", "/reports"}:
                    return self.reply(404, {"error": "Route not found"})
                if url.path == "/tickets":
                    allow = "GET, POST"
                elif match:
                    allow = "POST" if match[2] else "GET, PATCH, DELETE"
                else:
                    allow = "GET"
                self.reply(405, {"error": "Method not allowed"}, allow=allow)
            except NotFoundError as exc:
                self.reply(404, {"error": str(exc)})
            except ConflictError as exc:
                self.reply(409, {"error": str(exc)})
            except (ValidationError, ValueError) as exc:
                self.reply(400, {"error": str(exc)})
            except sqlite3.OperationalError:
                self.reply(503, {"error": "Database temporarily unavailable"})

        do_GET = do_POST = do_PATCH = do_DELETE = do_PUT = do_OPTIONS = dispatch

    return ThreadingHTTPServer(("127.0.0.1", port), Handler)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default="tickets.db")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--seed", action="store_true", help="Add three fictional tickets and exit")
    args = parser.parse_args()
    store = Store(args.db)
    if args.seed:
        for title in ("Reset demo password", "Fix dashboard loading", "Add CSV export"):
            store.create({"title": title, "description": "Fictional ticket for the local demo."})
        print("Added three demo tickets.")
        return
    server = make_server(store, args.port)
    print(f"Ticket API: http://127.0.0.1:{server.server_port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()

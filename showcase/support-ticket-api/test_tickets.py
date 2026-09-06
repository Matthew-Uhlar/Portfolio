import http.client
import json
import tempfile
import threading
import unittest
from pathlib import Path

from server import make_server
from tickets import ConflictError, NotFoundError, Store, ValidationError


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "test.db"
        self.store = Store(self.path)

    def create(self, title="Printer broken"):
        return self.store.create({"title": title, "description": "Paper is stuck"})

    def test_persistence_and_migration_are_repeatable(self):
        ticket = self.create()
        self.assertEqual(Store(self.path).get(ticket["id"])["title"], "Printer broken")

    def test_lifecycle_and_invalid_transition_are_atomic(self):
        ticket = self.create()
        with self.assertRaises(ConflictError):
            self.store.update(ticket["id"], {"title": "changed", "status": "resolved"})
        self.assertEqual(self.store.get(ticket["id"])["title"], "Printer broken")
        for status in ("in_progress", "resolved", "closed", "open"):
            self.assertEqual(self.store.update(ticket["id"], {"status": status})["status"], status)

    def test_comments_and_delete_cascade(self):
        ticket = self.create()
        self.store.comment(ticket["id"], {"body": "Checking the paper tray"})
        self.assertEqual(len(self.store.get(ticket["id"])["comments"]), 1)
        self.store.delete(ticket["id"])
        with self.assertRaises(NotFoundError):
            self.store.get(ticket["id"])
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM comments").fetchone()[0], 0)

    def test_search_pagination_and_report(self):
        self.create("Printer A")
        second = self.create("Printer B")
        self.create("Network issue")
        self.store.update(second["id"], {"status": "in_progress"})
        page = self.store.list(q="PRINTER", limit=1, offset=1)
        self.assertEqual(page["total"], 2)
        self.assertEqual(page["items"][0]["title"], "Printer A")
        self.assertEqual(self.store.list(status="in_progress")["total"], 1)
        self.assertEqual(self.store.list(q="' OR 1=1 --")["total"], 0)
        self.assertEqual(self.store.report(), {"total": 3, "by_status": {"open": 2, "in_progress": 1, "resolved": 0, "closed": 0}})

    def test_validation(self):
        for data in (None, [], {}, {"title": " ", "description": "x"}, {"title": "x" * 161, "description": "x"}, {"title": "x", "description": "x", "id": 9}):
            with self.subTest(data=data), self.assertRaises(ValidationError):
                self.store.create(data)
        for options in ({"limit": 101}, {"offset": -1}, {"status": "invalid"}, {"q": "x" * 201}):
            with self.subTest(options=options), self.assertRaises(ValidationError):
                self.store.list(**options)


class HttpTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = Store(Path(self.temp.name) / "http.db")
        self.server = make_server(self.store, 0)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.temp.cleanup()

    def request(self, method, path, data=None, raw=None):
        connection = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=3)
        body = raw if raw is not None else json.dumps(data) if data is not None else None
        connection.request(method, path, body, {"Content-Type": "application/json"})
        response = connection.getresponse()
        payload = response.read()
        result = response.status, json.loads(payload) if payload else None
        connection.close()
        return result

    def test_http_lifecycle(self):
        code, ticket = self.request("POST", "/tickets", {"title": "Demo", "description": "Example"})
        self.assertEqual(code, 201)
        path = f"/tickets/{ticket['id']}"
        self.assertEqual(self.request("PATCH", path, {"status": "resolved"})[0], 409)
        self.assertEqual(self.request("PATCH", path, {"status": "in_progress"})[0], 200)
        self.assertEqual(self.request("POST", path + "/comments", {"body": "Started"})[0], 201)
        self.assertEqual(len(self.request("GET", path)[1]["comments"]), 1)
        self.assertEqual(self.request("GET", "/tickets?status=in_progress")[1]["total"], 1)
        self.assertEqual(self.request("GET", "/reports")[1]["total"], 1)
        self.assertEqual(self.request("DELETE", path), (204, None))
        self.assertEqual(self.request("GET", path)[0], 404)

    def test_http_errors(self):
        for path in ("/tickets?limit=abc", "/tickets?limit=0", "/tickets?limit=1&limit=2", "/tickets?surprise=yes"):
            self.assertEqual(self.request("GET", path)[0], 400)
        for raw in ("{", "null", "[]", "x" * 65537):
            self.assertEqual(self.request("POST", "/tickets", raw=raw)[0], 400)
        self.assertEqual(self.request("PUT", "/tickets")[0], 405)
        self.assertEqual(self.request("GET", "/unknown")[0], 404)
        self.assertEqual(self.request("GET", "/health"), (200, {"status": "ok"}))


if __name__ == "__main__":
    unittest.main()

"""SQLite ticket storage, with validation shared by the CLI and HTTP API."""

import sqlite3
from datetime import datetime, timezone


class ValidationError(ValueError):
    pass


class NotFoundError(LookupError):
    pass


class ConflictError(ValueError):
    pass


TRANSITIONS = {
    "open": {"in_progress", "closed"},
    "in_progress": {"open", "resolved"},
    "resolved": {"open", "closed"},
    "closed": {"open"},
}


def clean_text(value, field, maximum):
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise ValidationError(f"{field} must be non-empty text of at most {maximum} characters")
    return value.strip()


class Store:
    def __init__(self, path):
        self.path = str(path)
        with self.connect() as db:
            version = db.execute("PRAGMA user_version").fetchone()[0]
            if version > 1:
                raise RuntimeError("Database was created by a newer version")
            if version == 0:
                db.executescript("""
                    BEGIN IMMEDIATE;
                    CREATE TABLE tickets (
                        id INTEGER PRIMARY KEY,
                        title TEXT NOT NULL,
                        description TEXT NOT NULL,
                        status TEXT NOT NULL DEFAULT 'open'
                            CHECK(status IN ('open','in_progress','resolved','closed')),
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL
                    );
                    CREATE TABLE comments (
                        id INTEGER PRIMARY KEY,
                        ticket_id INTEGER NOT NULL REFERENCES tickets(id) ON DELETE CASCADE,
                        body TEXT NOT NULL,
                        created_at TEXT NOT NULL
                    );
                    CREATE INDEX tickets_status_id ON tickets(status, id);
                    CREATE INDEX comments_ticket ON comments(ticket_id, id);
                    PRAGMA user_version = 1;
                    COMMIT;
                """)

    def connect(self):
        db = sqlite3.connect(self.path, timeout=5)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys=ON")
        return db

    @staticmethod
    def now():
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def require(db, ticket_id):
        row = db.execute("SELECT * FROM tickets WHERE id=?", (ticket_id,)).fetchone()
        if row is None:
            raise NotFoundError("Ticket not found")
        return dict(row)

    def create(self, data):
        self.fields(data, {"title", "description"})
        title = clean_text(data.get("title"), "title", 160)
        description = clean_text(data.get("description"), "description", 10000)
        now = self.now()
        with self.connect() as db:
            cursor = db.execute("INSERT INTO tickets(title,description,created_at,updated_at) VALUES(?,?,?,?)", (title, description, now, now))
            return self.require(db, cursor.lastrowid)

    @staticmethod
    def fields(data, allowed):
        if not isinstance(data, dict) or set(data) - allowed:
            raise ValidationError("Expected a JSON object containing only supported fields")

    def get(self, ticket_id):
        with self.connect() as db:
            ticket = self.require(db, ticket_id)
            ticket["comments"] = [dict(row) for row in db.execute("SELECT * FROM comments WHERE ticket_id=? ORDER BY id", (ticket_id,))]
            return ticket

    def update(self, ticket_id, data):
        self.fields(data, {"title", "description", "status"})
        if not data:
            raise ValidationError("Provide at least one field")
        with self.connect() as db:
            # Lock before reading so two updates cannot validate against stale status.
            db.execute("BEGIN IMMEDIATE")
            ticket = self.require(db, ticket_id)
            for field, maximum in (("title", 160), ("description", 10000)):
                if field in data:
                    ticket[field] = clean_text(data[field], field, maximum)
            if "status" in data:
                status = data["status"]
                if not isinstance(status, str) or status not in TRANSITIONS:
                    raise ValidationError("Unknown status")
                if status != ticket["status"] and status not in TRANSITIONS[ticket["status"]]:
                    raise ConflictError(f"Cannot move from {ticket['status']} to {status}")
                ticket["status"] = status
            ticket["updated_at"] = self.now()
            db.execute("UPDATE tickets SET title=:title,description=:description,status=:status,updated_at=:updated_at WHERE id=:id", ticket)
            return ticket

    def delete(self, ticket_id):
        with self.connect() as db:
            result = db.execute("DELETE FROM tickets WHERE id=?", (ticket_id,))
            if not result.rowcount:
                raise NotFoundError("Ticket not found")

    def comment(self, ticket_id, data):
        self.fields(data, {"body"})
        body = clean_text(data.get("body"), "body", 4000)
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            self.require(db, ticket_id)
            now = self.now()
            cursor = db.execute("INSERT INTO comments(ticket_id,body,created_at) VALUES(?,?,?)", (ticket_id, body, now))
            db.execute("UPDATE tickets SET updated_at=? WHERE id=?", (now, ticket_id))
            return dict(db.execute("SELECT * FROM comments WHERE id=?", (cursor.lastrowid,)).fetchone())

    def list(self, status=None, q="", limit=20, offset=0):
        if status is not None and status not in TRANSITIONS:
            raise ValidationError("Unknown status")
        if not 1 <= limit <= 100 or not 0 <= offset <= 100000:
            raise ValidationError("limit must be 1..100 and offset must be 0..100000")
        if len(q) > 200:
            raise ValidationError("q must be at most 200 characters")
        conditions, args = [], []
        if status:
            conditions.append("status=?")
            args.append(status)
        if q:
            conditions.append("(instr(lower(title),lower(?))>0 OR instr(lower(description),lower(?))>0)")
            args.extend([q, q])
        where = " WHERE " + " AND ".join(conditions) if conditions else ""
        with self.connect() as db:
            db.execute("BEGIN")
            total = db.execute("SELECT COUNT(*) FROM tickets" + where, args).fetchone()[0]
            rows = db.execute("SELECT * FROM tickets" + where + " ORDER BY id DESC LIMIT ? OFFSET ?", args + [limit, offset])
            return {"items": [dict(row) for row in rows], "total": total, "limit": limit, "offset": offset}

    def report(self):
        with self.connect() as db:
            counts = {status: 0 for status in TRANSITIONS}
            for row in db.execute("SELECT status,COUNT(*) AS count FROM tickets GROUP BY status"):
                counts[row["status"]] = row["count"]
            return {"total": sum(counts.values()), "by_status": counts}

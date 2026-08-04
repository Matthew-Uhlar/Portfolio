from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from pathlib import Path
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

APP_DIR = Path(__file__).parent
DB_PATH = APP_DIR / "inventory.db"

app = Flask(__name__)
app.secret_key = "change-this-secret-key-before-production"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'manager', 'staff'))
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS inventory_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity >= 0),
            unit_type TEXT NOT NULL,
            minimum_stock INTEGER NOT NULL CHECK(minimum_stock >= 0),
            UNIQUE(name, category)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS supply_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL,
            requested_quantity INTEGER NOT NULL CHECK(requested_quantity > 0),
            requested_by TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(item_id) REFERENCES inventory_items(id)
        )
    """)

    admin_exists = cur.execute(
        "SELECT id FROM users WHERE username = ?",
        ("admin",)
    ).fetchone()

    if not admin_exists:
        cur.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            ("admin", generate_password_hash("admin123"), "admin")
        )

    item_count = cur.execute("SELECT COUNT(*) AS count FROM inventory_items").fetchone()["count"]
    if item_count == 0:
        sample_items = [
            ("Diapers", "Infant Supplies", 50, "packs", 20),
            ("Wipes", "Infant Supplies", 35, "boxes", 15),
            ("Paper Towels", "Cleaning", 12, "rolls", 10),
            ("Crayons", "Classroom Supplies", 8, "boxes", 5),
            ("Gloves", "Health Supplies", 25, "boxes", 10),
        ]
        cur.executemany("""
            INSERT INTO inventory_items (name, category, quantity, unit_type, minimum_stock)
            VALUES (?, ?, ?, ?, ?)
        """, sample_items)

    conn.commit()
    conn.close()


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user" not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped_view


def manager_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if session.get("role") not in ("admin", "manager"):
            flash("You do not have permission to access that page.", "danger")
            return redirect(url_for("dashboard"))
        return view(*args, **kwargs)
    return wrapped_view


@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session["user"] = user["username"]
            session["role"] = user["role"]
            flash("Login successful.", "success")
            return redirect(url_for("dashboard"))

        flash("Invalid username or password.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    conn = get_db()
    total_items = conn.execute("SELECT COUNT(*) AS count FROM inventory_items").fetchone()["count"]
    low_stock = conn.execute("""
        SELECT * FROM inventory_items
        WHERE quantity <= minimum_stock
        ORDER BY category, name
    """).fetchall()
    pending_requests = conn.execute("""
        SELECT sr.*, ii.name AS item_name
        FROM supply_requests sr
        JOIN inventory_items ii ON sr.item_id = ii.id
        WHERE sr.status = 'Pending'
        ORDER BY sr.created_at DESC
    """).fetchall()
    conn.close()

    return render_template(
        "dashboard.html",
        total_items=total_items,
        low_stock=low_stock,
        pending_requests=pending_requests
    )


@app.route("/inventory")
@login_required
def inventory():
    search = request.args.get("search", "").strip()
    conn = get_db()
    if search:
        items = conn.execute("""
            SELECT * FROM inventory_items
            WHERE name LIKE ? OR category LIKE ?
            ORDER BY category, name
        """, (f"%{search}%", f"%{search}%")).fetchall()
    else:
        items = conn.execute("""
            SELECT * FROM inventory_items
            ORDER BY category, name
        """).fetchall()
    conn.close()

    return render_template("inventory.html", items=items, search=search)


@app.route("/inventory/add", methods=["GET", "POST"])
@login_required
@manager_required
def add_item():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        unit_type = request.form.get("unit_type", "").strip()
        quantity = request.form.get("quantity", "0").strip()
        minimum_stock = request.form.get("minimum_stock", "0").strip()

        try:
            quantity = int(quantity)
            minimum_stock = int(minimum_stock)
            if quantity < 0 or minimum_stock < 0:
                raise ValueError
            if not name or not category or not unit_type:
                raise ValueError

            conn = get_db()
            conn.execute("""
                INSERT INTO inventory_items (name, category, quantity, unit_type, minimum_stock)
                VALUES (?, ?, ?, ?, ?)
            """, (name, category, quantity, unit_type, minimum_stock))
            conn.commit()
            conn.close()

            flash("Inventory item added successfully.", "success")
            return redirect(url_for("inventory"))

        except sqlite3.IntegrityError:
            flash("That item already exists in the selected category.", "danger")
        except ValueError:
            flash("Please enter valid item information. Quantities cannot be negative.", "danger")

    return render_template("item_form.html", item=None)


@app.route("/inventory/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
@manager_required
def edit_item(item_id):
    conn = get_db()
    item = conn.execute("SELECT * FROM inventory_items WHERE id = ?", (item_id,)).fetchone()

    if not item:
        conn.close()
        flash("Inventory item not found.", "danger")
        return redirect(url_for("inventory"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        unit_type = request.form.get("unit_type", "").strip()
        quantity = request.form.get("quantity", "0").strip()
        minimum_stock = request.form.get("minimum_stock", "0").strip()

        try:
            quantity = int(quantity)
            minimum_stock = int(minimum_stock)
            if quantity < 0 or minimum_stock < 0:
                raise ValueError
            if not name or not category or not unit_type:
                raise ValueError

            conn.execute("""
                UPDATE inventory_items
                SET name = ?, category = ?, quantity = ?, unit_type = ?, minimum_stock = ?
                WHERE id = ?
            """, (name, category, quantity, unit_type, minimum_stock, item_id))
            conn.commit()
            conn.close()

            flash("Inventory item updated successfully.", "success")
            return redirect(url_for("inventory"))

        except sqlite3.IntegrityError:
            flash("Another item with that name already exists in the selected category.", "danger")
        except ValueError:
            flash("Please enter valid item information. Quantities cannot be negative.", "danger")

    conn.close()
    return render_template("item_form.html", item=item)


@app.route("/requests", methods=["GET", "POST"])
@login_required
def requests_page():
    conn = get_db()

    if request.method == "POST":
        item_id = request.form.get("item_id")
        requested_quantity = request.form.get("requested_quantity", "0")
        notes = request.form.get("notes", "").strip()

        try:
            item_id = int(item_id)
            requested_quantity = int(requested_quantity)
            if requested_quantity <= 0:
                raise ValueError

            conn.execute("""
                INSERT INTO supply_requests (item_id, requested_quantity, requested_by, notes)
                VALUES (?, ?, ?, ?)
            """, (item_id, requested_quantity, session["user"], notes))
            conn.commit()
            flash("Supply request submitted successfully.", "success")

        except ValueError:
            flash("Please enter a valid request quantity.", "danger")

    items = conn.execute("SELECT * FROM inventory_items ORDER BY category, name").fetchall()
    requests = conn.execute("""
        SELECT sr.*, ii.name AS item_name
        FROM supply_requests sr
        JOIN inventory_items ii ON sr.item_id = ii.id
        ORDER BY sr.created_at DESC
    """).fetchall()
    conn.close()

    return render_template("requests.html", items=items, requests=requests)


@app.route("/requests/<int:request_id>/<status>")
@login_required
@manager_required
def update_request(request_id, status):
    if status not in ("Approved", "Denied", "Completed"):
        flash("Invalid request status.", "danger")
        return redirect(url_for("requests_page"))

    conn = get_db()
    conn.execute("UPDATE supply_requests SET status = ? WHERE id = ?", (status, request_id))
    conn.commit()
    conn.close()

    flash(f"Request marked as {status}.", "success")
    return redirect(url_for("requests_page"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)

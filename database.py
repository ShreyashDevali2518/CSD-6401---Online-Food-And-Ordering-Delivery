import sqlite3
from pathlib import Path
from threading import Lock


class DatabaseManager:
    """Singleton responsible for database configuration and access."""

    _instance = None
    _lock = Lock()

    def __new__(cls, database_path=None):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self, database_path=None):
        if self._initialized:
            return
        self.database_path = str(database_path or Path(__file__).with_name("restaurant.db"))
        self._initialized = True

    def connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def initialize(self):
        from werkzeug.security import generate_password_hash
        with self.connect() as con:
            con.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'customer'
                )
            """)
            con.execute("""
                CREATE TABLE IF NOT EXISTS menu_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    category TEXT NOT NULL,
                    price REAL NOT NULL CHECK(price > 0)
                )
            """)
            admin = con.execute("SELECT id FROM users WHERE email = ?", ("admin@goodbite.local",)).fetchone()
            if not admin:
                con.execute(
                    "INSERT INTO users(name,email,password_hash,role) VALUES(?,?,?,?)",
                    ("Restaurant Admin", "admin@goodbite.local",
                     generate_password_hash("Admin123!"), "admin")
                )
            count = con.execute("SELECT COUNT(*) FROM menu_items").fetchone()[0]
            if count == 0:
                from menu_factory import MenuItemFactory
                samples = [
                    ("main", "Classic Burger", "Grilled patty, lettuce and house sauce", 129),
                    ("main", "Margherita Pizza", "Mozzarella, tomato and basil", 249),
                    ("side", "Golden Fries", "Crispy seasoned potato fries", 89),
                    ("drink", "Cold Coffee", "Chilled creamy coffee", 99),
                ]
                for category, name, description, price in samples:
                    item = MenuItemFactory.create(category, name, description, price)
                    con.execute(
                        "INSERT INTO menu_items(name,description,category,price) VALUES(?,?,?,?)",
                        (item.name, item.description, item.category, item.price)
                    )

    def get_user_by_email(self, email):
        with self.connect() as con:
            row = con.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
            return dict(row) if row else None

    def get_user_by_id(self, user_id):
        with self.connect() as con:
            row = con.execute("SELECT id,name,email,role FROM users WHERE id = ?", (user_id,)).fetchone()
            return dict(row) if row else None

    def create_user(self, name, email, password_hash):
        with self.connect() as con:
            cursor = con.execute(
                "INSERT INTO users(name,email,password_hash,role) VALUES(?,?,?,'customer')",
                (name, email, password_hash)
            )
            return cursor.lastrowid

    def get_menu(self):
        with self.connect() as con:
            return [dict(row) for row in con.execute(
                "SELECT * FROM menu_items ORDER BY category,name"
            ).fetchall()]

    def insert_menu_item(self, item):
        with self.connect() as con:
            cursor = con.execute(
                "INSERT INTO menu_items(name,description,category,price) VALUES(?,?,?,?)",
                (item.name, item.description, item.category, item.price)
            )
            return cursor.lastrowid

    def delete_menu_item(self, item_id):
        with self.connect() as con:
            con.execute("DELETE FROM menu_items WHERE id = ?", (item_id,))


if __name__ == "__main__":
    DatabaseManager().initialize()
    print("Database initialized.")

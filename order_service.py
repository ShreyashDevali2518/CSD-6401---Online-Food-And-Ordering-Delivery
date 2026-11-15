import sqlite3
from pathlib import Path
from order import Order
from order_states import STATE_CLASSES


class OrderService:
    """Coordinates order storage and publishes lifecycle changes."""

    def __init__(self, notification_center, database_path=None):
        self.notification_center = notification_center
        self.database_path = str(database_path or Path(__file__).with_name("orders.db"))

    def connect(self):
        con = sqlite3.connect(self.database_path)
        con.row_factory = sqlite3.Row
        return con

    def initialize(self):
        with self.connect() as con:
            con.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer TEXT NOT NULL,
                    item TEXT NOT NULL,
                    address TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)

    def create_order(self, customer, item, address):
        customer, item, address = customer.strip(), item.strip(), address.strip()
        if not customer or not item or not address:
            raise ValueError("Please enter the customer name, food item and delivery address.")
        order = Order(id=0, customer=customer, item=item, address=address)
        with self.connect() as con:
            cursor = con.execute(
                "INSERT INTO orders(customer,item,address,status,created_at) VALUES(?,?,?,?,?)",
                (customer, item, address, order.status, order.created_at)
            )
            order.id = cursor.lastrowid
        self.notification_center.notify(order, "Your order has been placed.")
        return order

    def get_order(self, order_id):
        with self.connect() as con:
            row = con.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
        if not row:
            raise KeyError(f"Order #{order_id} was not found.")
        state_class = STATE_CLASSES.get(row["status"])
        if not state_class:
            raise ValueError("The saved order has an unknown status.")
        return Order(
            id=row["id"],
            customer=row["customer"],
            item=row["item"],
            address=row["address"],
            state=state_class(),
            created_at=row["created_at"],
        )

    def get_all_orders(self):
        with self.connect() as con:
            rows = con.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
        result = []
        for row in rows:
            result.append({
                "id": row["id"],
                "customer": row["customer"],
                "item": row["item"],
                "address": row["address"],
                "status": row["status"],
                "created_at": row["created_at"],
            })
        return result

    def _save_status(self, order):
        with self.connect() as con:
            con.execute("UPDATE orders SET status = ? WHERE id = ?", (order.status, order.id))

    def advance_order(self, order_id):
        order = self.get_order(order_id)
        previous = order.status
        order.advance()
        self._save_status(order)
        self.notification_center.notify(order, f"Order status changed from {previous} to {order.status}.")
        return order

    def cancel_order(self, order_id):
        order = self.get_order(order_id)
        previous = order.status
        order.cancel()
        self._save_status(order)
        self.notification_center.notify(order, f"Order status changed from {previous} to {order.status}.")
        return order

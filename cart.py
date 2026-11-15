class ShoppingCart:
    """Stores food and combo lines selected by the customer."""

    def __init__(self, items=None):
        self.items = [dict(item) for item in (items or [])]

    @classmethod
    def from_list(cls, items):
        return cls(items)

    def to_list(self):
        return [dict(item) for item in self.items]

    def add(self, item):
        self.items.append(dict(item))

    def remove(self, line_id):
        self.items = [item for item in self.items if item["line_id"] != line_id]

    def find(self, line_id):
        return next((item for item in self.items if item["line_id"] == line_id), None)

    def change_quantity(self, line_id, amount):
        item = self.find(line_id)
        if not item:
            return
        item["quantity"] += amount
        if item["quantity"] <= 0:
            self.remove(line_id)

    @property
    def total(self):
        return round(sum(item["price"] * item["quantity"] for item in self.items), 2)

    @property
    def count(self):
        return sum(item["quantity"] for item in self.items)

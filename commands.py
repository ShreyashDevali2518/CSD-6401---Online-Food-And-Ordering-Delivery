from abc import ABC, abstractmethod


class CartCommand(ABC):
    """Command interface for shopping-cart operations."""

    @abstractmethod
    def execute(self):
        raise NotImplementedError

    @abstractmethod
    def undo(self):
        raise NotImplementedError


class AddItemCommand(CartCommand):
    def __init__(self, cart, item):
        self.cart = cart
        self.item = dict(item)

    def execute(self):
        self.cart.add(self.item)

    def undo(self):
        self.cart.remove(self.item["line_id"])


class RemoveItemCommand(CartCommand):
    def __init__(self, cart, line_id):
        self.cart = cart
        self.line_id = line_id
        self.removed_item = None

    def execute(self):
        item = self.cart.find(self.line_id)
        self.removed_item = dict(item) if item else None
        self.cart.remove(self.line_id)

    def undo(self):
        if self.removed_item:
            self.cart.add(self.removed_item)


class ChangeQuantityCommand(CartCommand):
    def __init__(self, cart, line_id, amount):
        self.cart = cart
        self.line_id = line_id
        self.amount = amount

    def execute(self):
        self.cart.change_quantity(self.line_id, self.amount)

    def undo(self):
        self.cart.change_quantity(self.line_id, -self.amount)


class CartInvoker:
    """Invokes cart commands without needing to know their internal steps."""

    def execute(self, command):
        command.execute()
        return command

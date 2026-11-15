from abc import ABC, abstractmethod


class OrderState(ABC):
    """State interface: each state defines the permitted next operations."""

    name = "Unknown"

    @abstractmethod
    def advance(self, order):
        raise NotImplementedError

    def cancel(self, order):
        raise ValueError(f"An order in '{self.name}' status cannot be cancelled.")


class PlacedState(OrderState):
    name = "Placed"

    def advance(self, order):
        order.state = PreparingState()

    def cancel(self, order):
        order.state = CancelledState()


class PreparingState(OrderState):
    name = "Preparing"

    def advance(self, order):
        order.state = OutForDeliveryState()

    def cancel(self, order):
        order.state = CancelledState()


class OutForDeliveryState(OrderState):
    name = "Out for delivery"

    def advance(self, order):
        order.state = DeliveredState()


class DeliveredState(OrderState):
    name = "Delivered"

    def advance(self, order):
        raise ValueError("This order has already been delivered.")


class CancelledState(OrderState):
    name = "Cancelled"

    def advance(self, order):
        raise ValueError("A cancelled order cannot be advanced.")

    def cancel(self, order):
        raise ValueError("This order is already cancelled.")


STATE_CLASSES = {
    "Placed": PlacedState,
    "Preparing": PreparingState,
    "Out for delivery": OutForDeliveryState,
    "Delivered": DeliveredState,
    "Cancelled": CancelledState,
}

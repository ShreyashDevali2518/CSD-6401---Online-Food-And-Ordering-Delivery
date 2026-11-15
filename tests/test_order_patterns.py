import pytest
from order import Order
from order_states import PlacedState, PreparingState, OutForDeliveryState, DeliveredState, CancelledState
from observers import NotificationCenter, OrderObserver
from order_service import OrderService


class RecordingObserver(OrderObserver):
    def __init__(self):
        self.events = []

    def update(self, order, message):
        self.events.append((order.id, order.status, message))


def test_state_pattern_advances_order_lifecycle():
    order = Order(id=1, customer="Asha", item="Burger", address="Goa")
    assert order.status == "Placed"
    order.advance()
    assert order.status == "Preparing"
    order.advance()
    assert order.status == "Out for delivery"
    order.advance()
    assert order.status == "Delivered"


def test_delivered_order_cannot_advance():
    order = Order(id=1, customer="Asha", item="Burger", address="Goa", state=DeliveredState())
    with pytest.raises(ValueError):
        order.advance()


def test_cancel_only_allowed_before_delivery_stage():
    order = Order(id=1, customer="Asha", item="Burger", address="Goa")
    order.cancel()
    assert order.status == "Cancelled"
    with pytest.raises(ValueError):
        order.advance()


def test_observer_receives_notifications():
    center = NotificationCenter()
    observer = RecordingObserver()
    center.subscribe(observer)
    order = Order(id=8, customer="Ravi", item="Pizza", address="Pune")
    center.notify(order, "Order placed")
    assert observer.events == [(8, "Placed", "Order placed")]


def test_observer_can_unsubscribe():
    center = NotificationCenter()
    observer = RecordingObserver()
    center.subscribe(observer)
    center.unsubscribe(observer)
    center.notify(Order(id=2, customer="Mira", item="Fries", address="Goa"), "Update")
    assert observer.events == []


def test_order_service_persists_and_notifies(tmp_path):
    center = NotificationCenter()
    observer = RecordingObserver()
    center.subscribe(observer)
    service = OrderService(center, tmp_path / "test_orders.db")
    service.initialize()
    order = service.create_order("Nina", "Sandwich", "Panaji")
    assert order.status == "Placed"
    updated = service.advance_order(order.id)
    assert updated.status == "Preparing"
    assert service.get_order(order.id).status == "Preparing"
    assert len(observer.events) == 2


def test_order_creation_requires_all_fields(tmp_path):
    service = OrderService(NotificationCenter(), tmp_path / "validation.db")
    service.initialize()
    with pytest.raises(ValueError):
        service.create_order("", "Burger", "Address")

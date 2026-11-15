from abc import ABC, abstractmethod
from datetime import datetime


class OrderObserver(ABC):
    """Observer interface for receiving order status updates."""

    @abstractmethod
    def update(self, order, message):
        raise NotImplementedError


class NotificationCenter:
    """Subject that notifies all registered observers when an order changes."""

    def __init__(self):
        self._observers = []

    def subscribe(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def unsubscribe(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, order, message):
        for observer in list(self._observers):
            observer.update(order, message)


class EmailNotification(OrderObserver):
    """Coursework email-notification simulation; it does not send real email."""

    def update(self, order, message):
        print(
            f"[EMAIL SIMULATION] To: {order.customer} | "
            f"Order #{order.id}: {message}"
        )


class ConsoleNotification(OrderObserver):
    def update(self, order, message):
        print(
            f"[NOTIFICATION] Order #{order.id} for {order.customer}: "
            f"{message} ({datetime.now().strftime('%H:%M:%S')})"
        )

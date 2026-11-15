from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """Common interface for all discount calculations."""

    @abstractmethod
    def calculate(self, subtotal):
        raise NotImplementedError


class NoDiscount(DiscountStrategy):
    def calculate(self, subtotal):
        return 0.0


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage):
        if not 0 <= percentage <= 100:
            raise ValueError("Discount percentage must be between 0 and 100.")
        self.percentage = percentage

    def calculate(self, subtotal):
        return round(subtotal * self.percentage / 100, 2)


class FlatDiscount(DiscountStrategy):
    def __init__(self, amount):
        if amount < 0:
            raise ValueError("Flat discount cannot be negative.")
        self.amount = amount

    def calculate(self, subtotal):
        return round(min(subtotal, self.amount), 2)


DISCOUNT_OPTIONS = {
    "none": "No discount",
    "percentage": "10% discount",
    "flat": "₹50 off",
}


def get_discount_strategy(discount_type):
    strategies = {
        "none": NoDiscount(),
        "percentage": PercentageDiscount(10),
        "flat": FlatDiscount(50),
    }
    if discount_type not in strategies:
        raise ValueError("Please select a valid discount option.")
    return strategies[discount_type]

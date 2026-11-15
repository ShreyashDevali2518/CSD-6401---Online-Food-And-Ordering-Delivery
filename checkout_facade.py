from discounts import get_discount_strategy
from payment_adapters import get_payment_processor, PAYMENT_METHODS


class CheckoutFacade:
    """
    Facade provides one simple checkout operation.
    It coordinates input validation, discount calculation and payment.
    """

    def checkout(self, customer_name, amount, discount_type, payment_method):
        customer_name = (customer_name or "").strip()

        if not customer_name:
            raise ValueError("Please enter the customer's name.")

        try:
            amount = float(amount)
        except (TypeError, ValueError):
            raise ValueError("Please enter a valid order amount.")

        if amount <= 0:
            raise ValueError("Order amount must be greater than zero.")

        if discount_type not in ("none", "percentage", "flat"):
            raise ValueError("Please select a valid discount option.")

        if payment_method not in PAYMENT_METHODS:
            raise ValueError("Please select a valid payment method.")

        discount_strategy = get_discount_strategy(discount_type)
        discount_amount = discount_strategy.calculate(amount)
        final_amount = round(max(0, amount - discount_amount), 2)

        payment_processor = get_payment_processor(payment_method)
        receipt = payment_processor.pay(final_amount, customer_name)

        receipt.update({
            "subtotal": round(amount, 2),
            "discount": discount_amount,
            "final_total": final_amount,
        })
        return receipt

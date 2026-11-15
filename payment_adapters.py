from abc import ABC, abstractmethod
from datetime import datetime
from uuid import uuid4


class PaymentProcessor(ABC):
    """Target interface expected by the checkout application."""

    @abstractmethod
    def pay(self, amount, customer_name):
        raise NotImplementedError


# Simulated external gateways deliberately use different interfaces.
class CardGateway:
    def make_card_payment(self, amount_in_rupees, cardholder_name):
        return {
            "approved": True,
            "transaction_code": "CARD-" + uuid4().hex[:8].upper(),
            "charged": round(amount_in_rupees, 2),
            "holder": cardholder_name,
        }


class UpiGateway:
    def transfer_using_upi(self, details):
        return {
            "status": "SUCCESS",
            "upi_reference": "UPI-" + uuid4().hex[:8].upper(),
            "value": round(details["amount"], 2),
            "account": details["customer"],
        }


class WalletGateway:
    def withdraw_from_wallet(self, customer, amount_in_paise):
        return {
            "response_code": 200,
            "wallet_txn": "WALLET-" + uuid4().hex[:8].upper(),
            "debited": int(amount_in_paise),
            "wallet_user": customer,
        }


def make_receipt(success, method, customer, amount, reference):
    return {
        "success": success,
        "method": method,
        "customer": customer,
        "amount": round(amount, 2),
        "reference": reference,
        "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "message": "Payment successful (simulation)." if success else "Payment was declined.",
    }


class CardPaymentAdapter(PaymentProcessor):
    def __init__(self, gateway=None):
        self.gateway = gateway or CardGateway()

    def pay(self, amount, customer_name):
        response = self.gateway.make_card_payment(amount, customer_name)
        return make_receipt(
            response["approved"], "Card", response["holder"],
            response["charged"], response["transaction_code"]
        )


class UpiPaymentAdapter(PaymentProcessor):
    def __init__(self, gateway=None):
        self.gateway = gateway or UpiGateway()

    def pay(self, amount, customer_name):
        response = self.gateway.transfer_using_upi({
            "amount": amount, "customer": customer_name
        })
        return make_receipt(
            response["status"] == "SUCCESS", "UPI", response["account"],
            response["value"], response["upi_reference"]
        )


class WalletPaymentAdapter(PaymentProcessor):
    def __init__(self, gateway=None):
        self.gateway = gateway or WalletGateway()

    def pay(self, amount, customer_name):
        response = self.gateway.withdraw_from_wallet(customer_name, round(amount * 100))
        return make_receipt(
            response["response_code"] == 200, "Wallet", response["wallet_user"],
            response["debited"] / 100, response["wallet_txn"]
        )


PAYMENT_METHODS = {
    "card": "Credit / Debit Card",
    "upi": "UPI",
    "wallet": "Digital Wallet",
}


def get_payment_processor(method):
    adapters = {
        "card": CardPaymentAdapter,
        "upi": UpiPaymentAdapter,
        "wallet": WalletPaymentAdapter,
    }
    if method not in adapters:
        raise ValueError("Please select a valid payment method.")
    return adapters[method]()

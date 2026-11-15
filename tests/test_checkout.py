import pytest
from discounts import get_discount_strategy
from payment_adapters import get_payment_processor
from checkout_facade import CheckoutFacade


def test_percentage_discount():
    assert get_discount_strategy("percentage").calculate(200) == 20


def test_flat_discount_cannot_exceed_subtotal():
    assert get_discount_strategy("flat").calculate(30) == 30


def test_all_payment_adapters_use_common_result_shape():
    for method in ("card", "upi", "wallet"):
        result = get_payment_processor(method).pay(100, "Test Customer")
        assert result["success"] is True
        assert result["customer"] == "Test Customer"
        assert result["amount"] == 100
        assert result["reference"]


def test_facade_coordinates_discount_and_payment():
    receipt = CheckoutFacade().checkout("Asha", 200, "percentage", "upi")
    assert receipt["subtotal"] == 200
    assert receipt["discount"] == 20
    assert receipt["final_total"] == 180
    assert receipt["amount"] == 180
    assert receipt["method"] == "UPI"


@pytest.mark.parametrize("kwargs", [
    {"customer_name": "", "amount": 100, "discount_type": "none", "payment_method": "card"},
    {"customer_name": "Asha", "amount": 0, "discount_type": "none", "payment_method": "card"},
    {"customer_name": "Asha", "amount": 100, "discount_type": "none", "payment_method": "unknown"},
])
def test_facade_rejects_invalid_checkout(kwargs):
    with pytest.raises(ValueError):
        CheckoutFacade().checkout(**kwargs)

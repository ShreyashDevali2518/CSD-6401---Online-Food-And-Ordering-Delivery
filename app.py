from flask import Flask, render_template, request, redirect, url_for, session, flash
from checkout_facade import CheckoutFacade
from discounts import DISCOUNT_OPTIONS

app = Flask(__name__)
app.secret_key = "member-three-development-secret"
checkout_service = CheckoutFacade()


@app.get("/")
def index():
    receipt = session.get("receipt")
    return render_template(
        "index.html",
        discount_options=DISCOUNT_OPTIONS,
        receipt=receipt,
        form_data=session.pop("form_data", {}),
    )


@app.post("/checkout")
def checkout():
    customer_name = request.form.get("customer_name", "").strip()
    amount_text = request.form.get("amount", "").strip()
    discount_type = request.form.get("discount_type", "none")
    payment_method = request.form.get("payment_method", "").strip()

    session["form_data"] = {
        "customer_name": customer_name,
        "amount": amount_text,
        "discount_type": discount_type,
        "payment_method": payment_method,
    }

    try:
        amount = float(amount_text)
        receipt = checkout_service.checkout(
            customer_name=customer_name,
            amount=amount,
            discount_type=discount_type,
            payment_method=payment_method,
        )
    except (ValueError, TypeError) as error:
        flash(str(error), "error")
        return redirect(url_for("index"))

    session.pop("form_data", None)
    session["receipt"] = receipt
    session.modified = True
    flash("Checkout completed successfully.", "success")
    return redirect(url_for("index"))


@app.post("/receipt/clear")
def clear_receipt():
    session.pop("receipt", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=8000)

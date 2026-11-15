from flask import Flask, render_template, request, redirect, url_for, flash
from order_service import OrderService
from observers import NotificationCenter, EmailNotification, ConsoleNotification

app = Flask(__name__)
app.secret_key = "member-four-development-secret"

notification_center = NotificationCenter()
notification_center.subscribe(EmailNotification())
notification_center.subscribe(ConsoleNotification())
order_service = OrderService(notification_center)


@app.get("/")
def index():
    return render_template("index.html", orders=order_service.get_all_orders())


@app.post("/orders/create")
def create_order():
    customer = request.form.get("customer", "").strip()
    item = request.form.get("item", "").strip()
    address = request.form.get("address", "").strip()

    try:
        order = order_service.create_order(customer, item, address)
    except ValueError as error:
        flash(str(error), "error")
        return redirect(url_for("index"))

    flash(f"Order #{order.id} has been created.", "success")
    return redirect(url_for("index"))


@app.post("/orders/<int:order_id>/advance")
def advance_order(order_id):
    try:
        order = order_service.advance_order(order_id)
        flash(f"Order #{order.id} is now {order.status}.", "success")
    except (ValueError, KeyError) as error:
        flash(str(error), "error")
    return redirect(url_for("index"))


@app.post("/orders/<int:order_id>/cancel")
def cancel_order(order_id):
    try:
        order = order_service.cancel_order(order_id)
        flash(f"Order #{order.id} has been cancelled.", "success")
    except (ValueError, KeyError) as error:
        flash(str(error), "error")
    return redirect(url_for("index"))


if __name__ == "__main__":
    order_service.initialize()
    app.run(debug=True, port=5004)

from uuid import uuid4
from flask import Flask, render_template, request, redirect, url_for, session, flash

from catalog import FOOD_ITEMS
from cart import ShoppingCart
from commands import AddItemCommand, RemoveItemCommand, ChangeQuantityCommand, CartInvoker
from customization import build_customized_food, ADD_ONS
from meal_builder import MealComboBuilder

app = Flask(__name__)
app.secret_key = "member-two-development-secret"
invoker = CartInvoker()


def get_cart():
    return ShoppingCart.from_list(session.get("cart_items", []))


def save_cart(cart):
    session["cart_items"] = cart.to_list()
    session.modified = True


@app.get("/")
def index():
    cart = get_cart()
    return render_template(
        "index.html",
        foods=FOOD_ITEMS,
        addons=ADD_ONS,
        cart=cart.items,
        subtotal=cart.total,
    )


@app.post("/cart/add/<int:food_id>")
def add_food(food_id):
    food_data = next((item for item in FOOD_ITEMS if item["id"] == food_id), None)
    if not food_data:
        flash("That food item is not available.", "error")
        return redirect(url_for("index"))

    selected_addons = request.form.getlist("addons")
    customized_food = build_customized_food(food_data, selected_addons)

    cart = get_cart()
    cart_line = {
        "line_id": uuid4().hex,
        "name": customized_food.get_description(),
        "price": round(customized_food.get_cost(), 2),
        "quantity": 1,
        "kind": "food",
    }
    invoker.execute(AddItemCommand(cart, cart_line))
    save_cart(cart)
    flash(f'{cart_line["name"]} added to your cart.', "success")
    return redirect(url_for("index"))


@app.post("/cart/combo")
def add_combo():
    main_name = request.form.get("main_item", "").strip()
    side_name = request.form.get("side_item", "").strip()
    drink_name = request.form.get("drink_item", "").strip()

    main_item = next((x for x in FOOD_ITEMS if x["name"] == main_name), None)
    side_item = next((x for x in FOOD_ITEMS if x["name"] == side_name), None)
    drink_item = next((x for x in FOOD_ITEMS if x["name"] == drink_name), None)

    if not main_item or not side_item or not drink_item:
        flash("Choose one main, one side and one drink to build a combo.", "error")
        return redirect(url_for("index"))

    combo = (
        MealComboBuilder()
        .set_name("Your Meal Combo")
        .add_main(main_item)
        .add_side(side_item)
        .add_drink(drink_item)
        .build()
    )

    cart = get_cart()
    cart_line = {
        "line_id": uuid4().hex,
        "name": combo["name"] + ": " + ", ".join(combo["items"]),
        "price": combo["price"],
        "quantity": 1,
        "kind": "combo",
    }
    invoker.execute(AddItemCommand(cart, cart_line))
    save_cart(cart)
    flash("Your meal combo has been added.", "success")
    return redirect(url_for("index"))


@app.post("/cart/quantity/<line_id>/<int:delta>")
def change_quantity(line_id, delta):
    if delta not in (-1, 1):
        return redirect(url_for("index"))
    cart = get_cart()
    invoker.execute(ChangeQuantityCommand(cart, line_id, delta))
    save_cart(cart)
    return redirect(url_for("index"))


@app.post("/cart/remove/<line_id>")
def remove_item(line_id):
    cart = get_cart()
    invoker.execute(RemoveItemCommand(cart, line_id))
    save_cart(cart)
    flash("Item removed from your cart.", "success")
    return redirect(url_for("index"))


@app.post("/cart/clear")
def clear_cart():
    session["cart_items"] = []
    session.modified = True
    flash("Your cart is now empty.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5002)

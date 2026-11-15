from cart import ShoppingCart
from commands import AddItemCommand, RemoveItemCommand, ChangeQuantityCommand, CartInvoker
from customization import build_customized_food
from meal_builder import MealComboBuilder
import pytest


def test_command_add_remove_and_quantity():
    cart = ShoppingCart()
    invoker = CartInvoker()
    item = {"line_id": "a1", "name": "Burger", "price": 100, "quantity": 1}
    invoker.execute(AddItemCommand(cart, item))
    invoker.execute(ChangeQuantityCommand(cart, "a1", 1))
    assert cart.count == 2
    invoker.execute(RemoveItemCommand(cart, "a1"))
    assert cart.count == 0


def test_add_command_can_be_undone():
    cart = ShoppingCart()
    command = AddItemCommand(cart, {"line_id": "x", "name": "Fries", "price": 50, "quantity": 1})
    command.execute()
    command.undo()
    assert cart.items == []


def test_decorator_stacks_addons_and_costs():
    food = build_customized_food({"name": "Burger", "price": 100}, ["cheese", "patty"])
    assert food.get_description() == "Burger, Extra cheese, Extra patty"
    assert food.get_cost() == 165


def test_builder_creates_combo():
    combo = (
        MealComboBuilder()
        .set_name("Lunch Combo")
        .add_main({"name": "Burger", "price": 120, "category": "main"})
        .add_side({"name": "Fries", "price": 80, "category": "side"})
        .add_drink({"name": "Soda", "price": 50, "category": "drink"})
        .build()
    )
    assert combo["name"] == "Lunch Combo"
    assert combo["items"] == ["Burger", "Fries", "Soda"]
    assert combo["price"] == 250


def test_builder_rejects_wrong_category():
    builder = MealComboBuilder()
    with pytest.raises(ValueError):
        builder.add_side({"name": "Burger", "price": 100, "category": "main"})

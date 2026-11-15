from decorators import (
    BasicFood, ExtraCheese, ExtraPatty, ExtraToppings, Jalapenos, SpecialSauce
)

ADD_ONS = {
    "cheese": {"label": "Extra cheese", "price": 25},
    "patty": {"label": "Extra patty", "price": 40},
    "toppings": {"label": "Extra toppings", "price": 20},
    "jalapenos": {"label": "Jalapeños", "price": 15},
    "sauce": {"label": "Special sauce", "price": 10},
}

ADDON_DECORATORS = {
    "cheese": ExtraCheese,
    "patty": ExtraPatty,
    "toppings": ExtraToppings,
    "jalapenos": Jalapenos,
    "sauce": SpecialSauce,
}


def build_customized_food(food_data, selected_addons):
    """Wrap the basic food object with one decorator per selected add-on."""
    food = BasicFood(food_data["name"], food_data["price"])
    for addon_key in dict.fromkeys(selected_addons):
        decorator = ADDON_DECORATORS.get(addon_key)
        if decorator:
            food = decorator(food)
    return food

from dataclasses import dataclass


@dataclass
class MenuItem:
    name: str
    description: str
    category: str
    price: float


class MenuItemFactory:
    """Factory Method: creates menu items according to their category."""

    CATEGORIES = ("main", "side", "drink", "dessert")

    @staticmethod
    def create(category, name, description, price):
        if category not in MenuItemFactory.CATEGORIES:
            raise ValueError("Unsupported menu category.")
        if not name.strip() or not description.strip() or float(price) <= 0:
            raise ValueError("Menu item details are invalid.")
        return MenuItem(
            name=name.strip(),
            description=description.strip(),
            category=category,
            price=round(float(price), 2),
        )

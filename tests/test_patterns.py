import pytest
from database import DatabaseManager
from menu_factory import MenuItemFactory
from menu_proxy import MenuManagementProxy


def test_database_manager_is_singleton():
    first = DatabaseManager()
    second = DatabaseManager()
    assert first is second


def test_factory_creates_valid_menu_item():
    item = MenuItemFactory.create("drink", "Iced Tea", "Fresh lemon iced tea", 75)
    assert item.name == "Iced Tea"
    assert item.category == "drink"
    assert item.price == 75.0


def test_factory_rejects_invalid_category():
    with pytest.raises(ValueError):
        MenuItemFactory.create("unknown", "Test", "Test item", 50)


class FakeDatabase:
    def __init__(self):
        self.added = None
        self.deleted = None

    def insert_menu_item(self, item):
        self.added = item
        return 123

    def delete_menu_item(self, item_id):
        self.deleted = item_id


def test_proxy_allows_admin_to_add_menu_item():
    fake = FakeDatabase()
    proxy = MenuManagementProxy(fake)
    item = MenuItemFactory.create("side", "Salad", "Fresh salad", 80)
    assert proxy.add_item(item, {"role": "admin"}) == 123
    assert fake.added.name == "Salad"


def test_proxy_blocks_customer_from_changing_menu():
    proxy = MenuManagementProxy(FakeDatabase())
    item = MenuItemFactory.create("side", "Salad", "Fresh salad", 80)
    with pytest.raises(PermissionError):
        proxy.add_item(item, {"role": "customer"})

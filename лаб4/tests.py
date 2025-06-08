# tests.py
import unittest
from models import Dish, Menu, Client, Order
from patterns import KitchenNotifier, OrderDatabase, OrderFactory

class TestFoodOrderingSystem(unittest.TestCase):

    def setUp(self):
        # Очистимо singleton перед кожним тестом
        OrderDatabase._instance = None

    def test_create_dish(self):
        dish = Dish("Pizza", 150)
        self.assertEqual(dish.name, "Pizza")
        self.assertEqual(dish.price, 150)

    def test_add_dish_to_menu(self):
        menu = Menu()
        dish = Dish("Soup", 50)
        menu.add_dish(dish)
        self.assertTrue(menu.contains_dish(dish))
        self.assertIn(dish, menu.get_dishes())

    def test_create_client(self):
        client = Client("Anna")
        self.assertEqual(client.name, "Anna")

    def test_create_order(self):
        client = Client("Ivan")
        dish = Dish("Burger", 100)
        order = Order(client, [dish])
        self.assertEqual(order.client.name, "Ivan")
        self.assertEqual(order.dishes[0].name, "Burger")
        self.assertEqual(order.total_price(), 100)

    def test_create_order_no_client(self):
        with self.assertRaises(TypeError):
            Order(None, [Dish("Sushi", 200)])

    def test_factory_creates_order(self):
        factory = OrderFactory()
        client = Client("Petro")
        dish = Dish("Sushi", 200)
        order = factory.create_order(client, [dish])
        self.assertIsInstance(order, Order)
        self.assertEqual(order.dishes[0].name, "Sushi")

    def test_kitchen_notifier(self):
        client = Client("Oleh")
        order = Order(client, [Dish("Steak", 180)])
        notifier = KitchenNotifier()
        notifier.update(order)
        self.assertIn("New order for Oleh", notifier.notifications)

    def test_order_total_price_multiple_dishes(self):
        client = Client("Tania")
        dishes = [Dish("Pizza", 150), Dish("Soup", 50)]
        order = Order(client, dishes)
        self.assertEqual(order.total_price(), 200)

    def test_singleton_order_database(self):
        db1 = OrderDatabase()
        db2 = OrderDatabase()
        self.assertIs(db1, db2)

    def test_database_add_and_get_order(self):
        db = OrderDatabase()
        client = Client("Ira")
        order = Order(client, [Dish("Salad", 60)])
        db.add_order(order)
        self.assertIn(order, db.get_orders())

    def test_menu_dish_not_found(self):
        menu = Menu()
        dish = Dish("Lasagna", 180)
        self.assertFalse(menu.contains_dish(dish))  # Страва не додана

    def test_empty_order_price(self):
        client = Client("TestUser")
        order = Order(client, [])
        self.assertEqual(order.total_price(), 0)  # Ціна має бути 0

    def test_kitchen_notifier_multiple_orders(self):
        client1 = Client("A")
        client2 = Client("B")
        order1 = Order(client1, [Dish("Pizza", 150)])
        order2 = Order(client2, [Dish("Soup", 50)])
        notifier = KitchenNotifier()
        notifier.update(order1)
        notifier.update(order2)
        self.assertEqual(len(notifier.notifications), 2)

    def test_order_database_multiple_orders(self):
        db = OrderDatabase()
        db._orders.clear()
        client = Client("Multi")
        dish = Dish("Item", 100)
        for _ in range(3):
            db.add_order(Order(client, [dish]))
        self.assertEqual(len(db.get_orders()), 3)

    def test_order_dish_list_integrity(self):
        dish1 = Dish("A", 10)
        dish2 = Dish("B", 20)
        order = Order(Client("Check"), [dish1, dish2])
        self.assertEqual([d.name for d in order.dishes], ["A", "B"])

if __name__ == '__main__':
    unittest.main()

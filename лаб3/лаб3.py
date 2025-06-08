import unittest

# Клас для представлення продукту
class Product:
    def __init__(self, product_id, name, price):
        self.product_id = product_id
        self.name = name
        self.price = price

    def get_info(self):
        return f"Product({self.product_id}): {self.name} - ${self.price}"

    def __eq__(self, other):
        return isinstance(other, Product) and self.product_id == other.product_id

    def __hash__(self):
        return hash(self.product_id)

# Клас для представлення замовлення
class Order:
    def __init__(self, order_id, user):
        self.order_id = order_id
        self.user = user
        self.products = {}  # Використовуємо об'єкти Product як ключі, значення – кількість товару

    def add_product(self, product, quantity=1):
        if product in self.products:
            self.products[product] += quantity
        else:
            self.products[product] = quantity

    def remove_product(self, product, quantity=1):
        if product in self.products:
            if self.products[product] <= quantity:
                del self.products[product]
            else:
                self.products[product] -= quantity

    def calculate_total(self):
        total = sum(product.price * qty for product, qty in self.products.items())
        return total

# Клас для представлення користувача
class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.orders = []
        self.is_logged_in = False  # нове поле

    def register(self):
        return f"User {self.name} registered with email {self.email}"

    def login(self, email):
        if self.email == email:
            self.is_logged_in = True
            return f"User {self.name} logged in successfully"
        else:
            return "Login failed: incorrect email"

    def place_order(self, order):
        self.orders.append(order)

    def view_orders(self):
        return self.orders

class Admin:
    def __init__(self, admin_id, name, email):
        self.admin_id = admin_id
        self.name = name
        self.email = email

    def add_product(self, product_list, product):
        product_list.append(product)

    def remove_product(self, product_list, product):
        product_list.remove(product)

    def view_users(self, user_list):
        return user_list


# Модульні тести для перевірки роботи класів
class TestInternetStore(unittest.TestCase):
    def setUp(self):
        # Початкова ініціалізація для тестів
        self.user = User(1, "John Doe", "john@example.com")
        self.product1 = Product(101, "Laptop", 1500)
        self.product2 = Product(102, "Smartphone", 800)
        self.order = Order(201, self.user)

    def test_user_register(self):
        result = self.user.register()
        self.assertEqual(result, "User John Doe registered with email john@example.com")

    def test_place_order(self):
        self.user.place_order(self.order)
        self.assertIn(self.order, self.user.view_orders())

    def test_add_product_to_order(self):
        self.order.add_product(self.product1, 2)
        self.assertEqual(self.order.products[self.product1], 2)

    def test_add_product_multiple_times(self):
        self.order.add_product(self.product2, 1)
        self.order.add_product(self.product2, 2)
        self.assertEqual(self.order.products[self.product2], 3)

    def test_remove_product(self):
        self.order.add_product(self.product1, 3)
        self.order.remove_product(self.product1, 2)
        self.assertEqual(self.order.products[self.product1], 1)

    def test_remove_product_completely(self):
        self.order.add_product(self.product1, 1)
        self.order.remove_product(self.product1, 1)
        self.assertNotIn(self.product1, self.order.products)

    def test_calculate_total(self):
        self.order.add_product(self.product1, 1)
        self.order.add_product(self.product2, 2)
        expected_total = 1500 + 2 * 800
        self.assertEqual(self.order.calculate_total(), expected_total)

    def test_view_orders(self):
        self.user.place_order(self.order)
        orders = self.user.view_orders()
        self.assertIsInstance(orders, list)
        self.assertEqual(len(orders), 1)

    def test_get_info(self):
        info = self.product1.get_info()
        self.assertEqual(info, "Product(101): Laptop - $1500")

    def test_product_equality(self):
        product_same = Product(101, "Laptop", 1500)
        self.assertEqual(self.product1, product_same)
        product_different = Product(103, "Tablet", 400)
        self.assertNotEqual(self.product1, product_different)

    def test_login_success(self):
        result = self.user.login("john@example.com")
        self.assertTrue(self.user.is_logged_in)
        self.assertEqual(result, "User John Doe logged in successfully")

    def test_login_failure(self):
        result = self.user.login("wrong@example.com")
        self.assertFalse(self.user.is_logged_in)
        self.assertEqual(result, "Login failed: incorrect email")


if __name__ == '__main__':
    unittest.main()

class TestAdminActions(unittest.TestCase):
    def setUp(self):
        self.admin = Admin(1, "Admin", "admin@example.com")
        self.product1 = Product(201, "Monitor", 300.0)
        self.product2 = Product(202, "Mouse", 25.0)
        self.products = []
        self.users = [
            User(1, "John Doe", "john@example.com"),
            User(2, "Jane Smith", "jane@example.com")
        ]

    def test_add_product(self):
        self.admin.add_product(self.products, self.product1)
        self.assertIn(self.product1, self.products)

    def test_remove_product(self):
        self.products.append(self.product2)
        self.admin.remove_product(self.products, self.product2)
        self.assertNotIn(self.product2, self.products)

    def test_view_users(self):
        result = self.admin.view_users(self.users)
        self.assertEqual(result, self.users)
        self.assertEqual(len(result), 2)

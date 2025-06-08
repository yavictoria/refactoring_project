# patterns.py
from abc import ABC, abstractmethod
from models import Order

#Observer
class KitchenNotificationInterface(ABC):
    @abstractmethod
    def update(self, order: Order):
        pass

class KitchenNotifier(KitchenNotificationInterface):
    def __init__(self):
        self.notifications = []

    def update(self, order: Order):
        self.notifications.append(f"New order for {order.client.name}")

#Singleton
class OrderDatabase:
    _instance = None
    _orders = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OrderDatabase, cls).__new__(cls)
            cls._orders = []
        return cls._instance

    def add_order(self, order: Order):
        self._orders.append(order)

    def get_orders(self):
        return self._orders

#Factory
class OrderFactory:
    def create_order(self, client, dishes):
        return Order(client, dishes)

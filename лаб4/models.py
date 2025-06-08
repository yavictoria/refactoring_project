class Dish:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

class Menu:
    def __init__(self):
        self._dishes = []

    def add_dish(self, dish: Dish):
        self._dishes.append(dish)

    def contains_dish(self, dish: Dish) -> bool:
        return dish in self._dishes

    def get_dishes(self):
        return self._dishes

class Client:
    def __init__(self, name: str):
        self.name = name

class Order:
    def __init__(self, client: Client, dishes: list[Dish]):
        if client is None:
            raise TypeError("Client cannot be None")
        self.client = client
        self.dishes = dishes

    def total_price(self):
        return sum(dish.price for dish in self.dishes)
# functional.py
from models import Dish, Menu, Client
from patterns import KitchenNotifier, OrderDatabase, OrderFactory

def show_menu(menu):
    print("\n[MENU]")
    for idx, dish in enumerate(menu.get_dishes(), 1):
        print(f"{idx}. {dish.name} - {dish.price} грн")

def get_user_dishes(menu):
    selected_dishes = []
    show_menu(menu)
    print("\nВведіть номери страв через кому (наприклад: 1,2): ")
    input_str = input("Ваш вибір: ")

    try:
        indices = [int(i.strip()) - 1 for i in input_str.split(',')]
        for idx in indices:
            if 0 <= idx < len(menu.get_dishes()):
                selected_dishes.append(menu.get_dishes()[idx])
    except ValueError:
        print("Некоректне введення!")

    return selected_dishes

if __name__ == '__main__':
    menu = Menu()
    menu.add_dish(Dish("Pizza", 150))
    menu.add_dish(Dish("Soup", 50))
    menu.add_dish(Dish("Burger", 120))
    menu.add_dish(Dish("Sushi", 200))

    name = input("Введіть ваше ім'я: ")
    client = Client(name)

    dishes = get_user_dishes(menu)
    if not dishes:
        print("Замовлення не створено — не обрано жодної страви.")
    else:
        factory = OrderFactory()
        order = factory.create_order(client, dishes)

        notifier = KitchenNotifier()
        notifier.update(order)

        db = OrderDatabase()
        db.add_order(order)

        print("\n[Kitchen Notifications]")
        for note in notifier.notifications:
            print(note)

        print("\n[Orders in Database]")
        for o in db.get_orders():
            item_names = [d.name for d in o.dishes]
            print(f"Order by: {o.client.name}, Items: {item_names}")
            print(f"  Total: {o.total_price()} грн")

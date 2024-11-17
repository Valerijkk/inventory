import json
import os
from tabulate import tabulate

# Файл для сохранения данных инвентаря
INVENTORY_FILE = 'inventory.json'


def load_inventory():
    """Загружает инвентарь из файла, если он существует."""
    if os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, 'r', encoding='utf-8') as file:
            inventory = json.load(file)
        # Проверяем и рассчитываем 'total_cost' для каждого товара, если необходимо
        for item_id, details in inventory.items():
            if 'total_cost' not in details:
                try:
                    details['quantity'] = int(details['quantity'])
                    details['price'] = float(details['price'])
                    details['total_cost'] = details['quantity'] * details['price']
                except (ValueError, TypeError):
                    print(f"Ошибка данных для товара ID {item_id}. Проверьте количество и цену.")
                    details['total_cost'] = 0.0
        return inventory
    return {}


def save_inventory(inventory):
    """Сохраняет инвентарь в файл."""
    with open(INVENTORY_FILE, 'w', encoding='utf-8') as file:
        json.dump(inventory, file, ensure_ascii=False, indent=4)


def add_item(inventory):
    """Добавляет новый товар в инвентарь."""
    item_id = input("Введите ID товара: ").strip()
    if item_id in inventory:
        print("Товар с таким ID уже существует.")
        return
    name = input("Введите название товара: ").strip()
    quantity = input("Введите количество: ").strip()
    price = input("Введите цену за единицу: ").strip()
    if not quantity.isdigit() or not is_float(price):
        print("Некорректный ввод количества или цены.")
        return
    quantity = int(quantity)
    price = float(price)
    total_cost = quantity * price
    inventory[item_id] = {
        'name': name,
        'quantity': quantity,
        'price': price,
        'total_cost': total_cost
    }
    print("Товар успешно добавлен.")


def remove_item(inventory):
    """Удаляет товар из инвентаря."""
    item_id = input("Введите ID товара для удаления: ").strip()
    if item_id in inventory:
        del inventory[item_id]
        print("Товар успешно удален.")
    else:
        print("Товар с таким ID не найден.")


def update_item(inventory):
    """Обновляет информацию о товаре."""
    item_id = input("Введите ID товара для обновления: ").strip()
    if item_id not in inventory:
        print("Товар с таким ID не найден.")
        return
    print("Оставьте поле пустым, если не хотите изменять его.")
    name = input(f"Введите новое название (текущее: {inventory[item_id]['name']}): ").strip()
    quantity = input(f"Введите новое количество (текущее: {inventory[item_id]['quantity']}): ").strip()
    price = input(f"Введите новую цену (текущая: {inventory[item_id]['price']}): ").strip()

    if name:
        inventory[item_id]['name'] = name
    if quantity:
        if quantity.isdigit():
            inventory[item_id]['quantity'] = int(quantity)
        else:
            print("Некорректный ввод количества. Изменение пропущено.")
    if price:
        if is_float(price):
            inventory[item_id]['price'] = float(price)
        else:
            print("Некорректный ввод цены. Изменение пропущено.")

    # Перерасчет суммарной стоимости
    try:
        inventory[item_id]['total_cost'] = inventory[item_id]['quantity'] * inventory[item_id]['price']
    except KeyError:
        inventory[item_id]['total_cost'] = 0.0
        print("Не удалось рассчитать суммарную стоимость. Проверьте количество и цену.")

    print("Информация о товаре обновлена.")


def view_inventory(inventory):
    """Отображает все товары в инвентаре."""
    if not inventory:
        print("Инвентарь пуст.")
        return
    headers = ["ID", "Название", "Количество", "Цена (руб.)", "Суммарная стоимость (руб.)"]
    table = []
    for item_id, details in inventory.items():
        table.append([
            item_id,
            details['name'],
            details['quantity'],
            f"{details['price']:.2f}",
            f"{details['total_cost']:.2f}"
        ])
    print(tabulate(table, headers, tablefmt="grid", stralign="center", numalign="center"))


def search_item(inventory):
    """Ищет товар по названию или ID."""
    query = input("Введите ID или название товара для поиска: ").strip().lower()
    results = {}
    for item_id, details in inventory.items():
        if query in item_id.lower() or query in details['name'].lower():
            results[item_id] = details
    if results:
        headers = ["ID", "Название", "Количество", "Цена (руб.)", "Суммарная стоимость (руб.)"]
        table = []
        for item_id, details in results.items():
            table.append([
                item_id,
                details['name'],
                details['quantity'],
                f"{details['price']:.2f}",
                f"{details['total_cost']:.2f}"
            ])
        print(f"Найдено {len(results)} товар(ов):")
        print(tabulate(table, headers, tablefmt="grid", stralign="center", numalign="center"))
    else:
        print("Товары не найдены.")


def is_float(value):
    """Проверяет, является ли строка числом с плавающей точкой."""
    try:
        float(value)
        return True
    except ValueError:
        return False


def main():
    inventory = load_inventory()
    while True:
        print("\n=== Инвентаризация Товаров ===")
        print("1. Добавить товар")
        print("2. Удалить товар")
        print("3. Обновить информацию о товаре")
        print("4. Просмотреть инвентарь")
        print("5. Поиск товара")
        print("6. Выйти")
        choice = input("Выберите действие (1-6): ").strip()

        if choice == '1':
            add_item(inventory)
            save_inventory(inventory)
        elif choice == '2':
            remove_item(inventory)
            save_inventory(inventory)
        elif choice == '3':
            update_item(inventory)
            save_inventory(inventory)
        elif choice == '4':
            view_inventory(inventory)
        elif choice == '5':
            search_item(inventory)
        elif choice == '6':
            print("Выход из программы. До свидания!")
            break
        else:
            print("Некорректный выбор. Пожалуйста, попробуйте снова.")


if __name__ == "__main__":
    main()

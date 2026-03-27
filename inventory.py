from exceptions import NegativeNumberException
import service
import handle_files


def get_int(msg: str):
    """
    Read a positive integer from user input.

    Args:
        msg (str): Input message.

    Returns:
        int: Valid integer greater than 0.
    """
    value = None
    while value is None:
        try:
            num = int(input(msg))
            if num <= 0:
                raise NegativeNumberException("Value must be > 0")
            value = num
        except Exception as e:
            print(e)
    return value


def get_float(msg: str):
    """
    Read a positive float from user input.

    Args:
        msg (str): Input message.

    Returns:
        float: Valid number greater than 0.
    """
    value = None
    while value is None:
        try:
            num = float(input(msg))
            if num <= 0:
                raise NegativeNumberException("Value must be > 0")
            value = num
        except Exception as e:
            print(e)
    return value


def get_str(msg: str):
    """
    Read a non-empty string from user input.

    Args:
        msg (str): Input message.

    Returns:
        str: Non-empty text.
    """
    value = None
    while value is None:
        text = input(msg).strip()
        if text:
            value = text
        else:
            print("Value cannot be empty")
    return value


def ask_yes_no(msg: str):
    """
    Ask a yes/no question.

    Args:
        msg (str): Prompt message.

    Returns:
        bool: True for 'y', False for 'n'.
    """
    option = None
    while option not in ("y", "n"):
        option = input(msg).lower()
    return option == "y"


def handle_create(products: list[dict]):
    """
    Handle product creation flow.

    Args:
        products (list[dict]): Product list.
    """
    name = get_str("Name: ")
    price = get_float("Price: ")
    quantity = get_int("Quantity: ")
    service.add_product(products, name, price, quantity)
    print("Product added.")


def handle_update(products: list[dict]):
    """
    Handle product update flow.

    Args:
        products (list[dict]): Product list.
    """
    id = get_int("Enter product id: ")

    updates = {}
    if ask_yes_no("Change name? (y/n): "):
        updates["name"] = get_str("New name: ")
    if ask_yes_no("Change price? (y/n): "):
        updates["price"] = get_float("New price: ")
    if ask_yes_no("Change quantity? (y/n): "):
        updates["quantity"] = get_int("New quantity: ")

    if not updates:
        print("No changes.")
        return

    if service.update_product(products, id, updates):
        print("Updated successfully")
    else:
        print("Product not found")


def handle_delete(products: list[dict]):
    """
    Handle product deletion flow.

    Args:
        products (list[dict]): Product list.
    """
    id = get_int("Enter product id: ")
    if service.delete_product(products, id):
        print("Deleted")
    else:
        print("Not found")


def handle_search(products: list[dict]):
    """
    Handle product search flow.

    Args:
        products (list[dict]): Product list.
    """
    id = get_int("Enter product id: ")
    product = service.search_product_by_id(products, id)
    if product:
        service.print_product(product)
    else:
        print("Not found")


def handle_save(products: list[dict]):
    """
    Handle saving inventory to CSV.

    Args:
        products (list[dict]): Product list.
    """
    path = get_str("Enter file path: ")
    header = ask_yes_no("Include header? (y/n): ")
    handle_files.save_csv(products, path, header)


def handle_load(products: list[dict]):
    """
    Handle loading inventory from CSV.

    Args:
        products (list[dict]): Product list.
    """
    path = get_str("Enter file path: ")
    new_data = handle_files.load_csv(path)

    if not new_data:
        return

    overwrite = ask_yes_no("Overwrite inventory? (y/n): ")

    if overwrite:
        products.clear()
        products.extend(new_data)
        print("Inventory replaced.")
    else:
        for new in new_data:
            existing = next((p for p in products if p["id"] == new["id"]), None)

            if existing:
                existing["quantity"] += new["quantity"]
                existing["price"] = new["price"]
                existing["total_line"] = existing["price"] * existing["quantity"]
            else:
                products.append(new)

        print("Inventory merged.")


def show_menu():
    """
    Display the main menu.
    """
    print("\nMENU")
    print("1. Add")
    print("2. Show")
    print("3. Stats")
    print("4. Search")
    print("5. Update")
    print("6. Delete")
    print("7. Save CSV")
    print("8. Load CSV")
    print("9. Exit")


def main():
    """
    Run the main application loop.
    """
    products = []
    running = True

    while running:
        show_menu()

        try:
            option = int(input("Option: "))
        except:
            print("Invalid input")
            continue

        match option:
            case 1:
                handle_create(products)
            case 2:
                service.show_inventory(products)
            case 3:
                print("\n".join(service.statics(products)))
            case 4:
                handle_search(products)
            case 5:
                handle_update(products)
            case 6:
                handle_delete(products)
            case 7:
                handle_save(products)
            case 8:
                handle_load(products)
            case 9:
                print("Bye!")
                running = False
            case _:
                print("Invalid option")


if __name__ == "__main__":
    main()

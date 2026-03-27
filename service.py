def add_product(inventory: list[dict], name: str, price: float, quantity: int):
    """
    Add a new product to the inventory.

    Args:
        inventory (list[dict]): Product list.
        name (str): Product name.
        price (float): Product price.
        quantity (int): Product quantity.
    """
    last_id = inventory[-1]["id"] if inventory else 0
    inventory.append(
        {
            "id": last_id + 1,
            "name": name,
            "price": price,
            "quantity": quantity,
            "total_line": price * quantity,
        }
    )


def show_inventory(inventory: list[dict]):
    """
    Display all products in the inventory.

    Args:
        inventory (list[dict]): Product list.
    """
    if not inventory:
        print("Empty inventory")
        return

    for item in inventory:
        print_product(item)


def print_product(item: dict):
    """
    Print a single product in a formatted way.

    Args:
        item (dict): Product data.
    """
    print(" | ".join(f"{k}: {v}" for k, v in item.items()))


def search_product_by_id(inventory, id):
    return next((p for p in inventory if p["id"] == id), None)


def update_product(inventory: list[dict], id: int, updates: dict):
    """
    Update product fields by ID.

    Args:
        inventory (list[dict]): Product list.
        id (int): Product ID.
        updates (dict): Fields to update.

    Returns:
        bool: True if updated, False if not found.
    """
    product = search_product_by_id(inventory, id)
    if not product:
        return False

    product.update({k: v for k, v in updates.items() if v is not None})
    product["total_line"] = product["price"] * product["quantity"]
    return True


def delete_product(inventory: list[dict], id: int):
    """
    Remove a product by ID.

    Args:
        inventory (list[dict]): Product list.
        id (int): Product ID.

    Returns:
        bool: True if deleted, False if not found.
    """
    for i, p in enumerate(inventory):
        if p["id"] == id:
            inventory.pop(i)
            return True
    return False


def statics(inventory):
    """
    Calculate inventory statistics.

    Args:
        inventory (list[dict]): Product list.

    Returns:
        tuple: Summary of inventory statistics or empty message.
    """
    if not inventory:
        return ("Empty inventory",)

    total_units = sum(p["quantity"] for p in inventory)
    total_value = sum(p["total_line"] for p in inventory)

    most_expensive = max(inventory, key=lambda p: p["price"])
    most_stock = max(inventory, key=lambda p: p["quantity"])

    return (
        f"Total units: {total_units}",
        f"Total value: {total_value}",
        f"Most expensive: {most_expensive['name']} (${most_expensive['price']})",
        f"Most stock: {most_stock['name']} ({most_stock['quantity']})",
    )

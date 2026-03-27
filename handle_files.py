import csv
from exceptions import NegativeNumberException as Nne


def save_csv(inventory: list[dict], path: str, include_header=True):
    """
    Save inventory data to a CSV file.

    Args:
        inventory (list[dict]): List of products.
        path (str): Output file path.
        include_header (bool): Whether to write the header.

    Returns:
        None
    """
    if not inventory:
        print("Empty inventory")
        return

    try:
        with open(path, "w", newline="") as file:
            fields = ["id", "name", "price", "quantity", "total_line"]
            writer = csv.DictWriter(file, fieldnames=fields)

            if include_header:
                writer.writeheader()

            writer.writerows(inventory)

        print(f"Saved in: {path}")

    except Exception as e:
        print(f"Error saving file: {e}")


def load_csv(path: str):
    """
    Load inventory data from a CSV file.

    Args:
        path (str): File path.

    Returns:
        list[dict] | None: Valid products list, empty list if header is invalid,
        or None if file is not found or an error occurs.
    """
    inventory = []
    errors = 0

    try:
        with open(path) as file:
            reader = csv.DictReader(file)

            expected = ["id", "name", "price", "quantity", "total_line"]
            if reader.fieldnames != expected:
                print("Invalid header")
                return []

            for row in reader:
                try:
                    price = float(row["price"])
                    quantity = int(row["quantity"])

                    if price <= 0 or quantity <= 0:
                        raise Nne("Price and quantity most be greater than zero")

                    inventory.append(
                        {
                            "id": int(row["id"]),
                            "name": row["name"],
                            "price": price,
                            "quantity": quantity,
                            "total_line": price * quantity,
                        }
                    )

                except:
                    errors += 1

        print(f"Loaded: {len(inventory)} | Invalid rows: {errors}")
        return inventory

    except FileNotFoundError:
        print("File not found")
    except Exception as e:
        print(f"Error: {e}")

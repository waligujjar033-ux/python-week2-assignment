# T2 - Fixed Legacy Stock Room Script


class InsufficientStockError(Exception):
    """Raised when requested quantity exceeds available stock."""
    pass


def add_stock(stock, name, qty, log=None):
    """Add quantity to stock and return the restocked item log."""

    if log is None:
        log = []

    stock[name] = stock.get(name, 0) + qty
    log.append(name)

    return log


def remove_empty(stock):
    """Remove zero-quantity items and return their names."""

    removed = []

    for name in list(stock):
        if stock[name] == 0:
            del stock[name]
            removed.append(name)

    return removed


def sell(stock, prices, name, qty):
    """Sell an item and return its total sale amount."""

    if name not in stock:
        raise KeyError(f"'{name}' is not in stock.")

    if qty <= 0:
        raise ValueError("quantity must be greater than zero.")

    if stock[name] < qty:
        raise InsufficientStockError(
            f"only {stock[name]} {name} in stock."
        )

    stock[name] -= qty

    return prices[name] * qty


def stock_value(stock, prices):
    """Calculate and return the total stock value."""

    total = 0

    for name, qty in stock.items():
        total += prices[name] * qty

    return total


def main():
    """Run the stock room program with input validation."""

    stock = {
        "pen": 40,
        "notebook": 0,
        "bag": 5,
        "marker": 0
    }

    prices = {
        "pen": 20,
        "notebook": 150,
        "bag": 1200,
        "marker": 80
    }

    sold_count = 0

    # BUG-1: Mutable default argument fixed
    print("Restocked:", add_stock(stock, "pen", 10))
    print("Restocked:", add_stock(stock, "bag", 2))

    # BUG-2: Safe dictionary deletion
    removed = remove_empty(stock)

    print("Removed:", ", ".join(removed))

    # BUG-3 and BUG-6: Safe user input
    while True:

        name = input("Item to sell: ").strip().lower()

        try:
            if name not in stock:
                raise KeyError(f"'{name}' is not in stock.")

            while True:

                qty_input = input("Quantity: ")

                try:
                    qty = int(qty_input)
                    if qty <= 0:
                     print("Error: quantity must be greater than zero.")
                     continue

                    # BUG-6: Custom exception handled here
                    sale_amount = sell(stock, prices, name, qty)

                except ValueError:
                    print("Error: quantity must be a whole number.")

                except InsufficientStockError as error:
                    print("Error:", error)

                else:
                    # BUG-4: Counter updated in main
                    sold_count += 1

                    print(f"Sale: Rs {sale_amount:,}")

                    print("Items sold:", sold_count)

                    # BUG-5: Function returns stock value
                    print(f"Stock value: Rs {stock_value(stock, prices):,}")

                    return

        except KeyError as error:
            print("Error:", error.args[0])


if __name__ == "__main__":
    main()
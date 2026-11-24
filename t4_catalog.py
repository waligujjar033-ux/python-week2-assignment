from functools import reduce



# T4 - PRODUCT CATALOG FILTER



# 1. PRODUCT DATA


products = [
    {"name": "Redmi Note 13", "category": "Phones", "price": 62000, "rating": 4.4, "stock": 12},
    {"name": "Galaxy A15", "category": "Phones", "price": 48500, "rating": 4.1, "stock": 0},
    {"name": "ThinkPad E14", "category": "Laptops", "price": 185000, "rating": 4.6, "stock": 4},
    {"name": "HP 15s", "category": "Laptops", "price": 142000, "rating": 4.0, "stock": 7},
    {"name": "Sony WH-CH520", "category": "Headphones", "price": 14500, "rating": 4.5, "stock": 20},
    {"name": "JBL Tune 510", "category": "Headphones", "price": 11000, "rating": 4.2, "stock": 0},
    {"name": "Anker Soundcore 3", "category": "Speakers", "price": 13500, "rating": 4.7, "stock": 9},
    {"name": "Desk Lamp", "category": "Lighting", "price": 3200, "rating": 4.3, "stock": 30},
    {"name": "LED Strip 5m", "category": "Lighting", "price": 1800, "rating": 3.8, "stock": 45},
    {"name": "Office Chair", "category": "Furniture", "price": 28500, "rating": 4.5, "stock": 6},
    {"name": "Standing Desk", "category": "Furniture", "price": 74000, "rating": 4.8, "stock": 2},
    {"name": "USB-C Cable", "category": "Accessories", "price": 650, "rating": 2.9, "stock": 120}
]



# 2. CATEGORY TREE - NESTED DICTIONARY


category_tree = {
    "Electronics": {
        "Phones": {},
        "Laptops": {},
        "Audio": {
            "Headphones": {},
            "Speakers": {}
        },
        "Accessories": {}
    },
    "Home": {
        "Lighting": {},
        "Furniture": {}
    }
}



# PART A - SEVEN ONE-LINERS


def part_a():
    """Display the results of seven product catalog tasks."""
    print("\n========== PART A ==========")

    # TASK 1
    # In-stock products under Rs 5000

    task1 = [
        p["name"]
        for p in products
        if p["stock"] > 0 and p["price"] < 5000
    ]

    print("\nTask 1 - In-stock products under Rs 5000:")
    print(task1)


    # TASK 2
    # Products rating >= 4.5 with 10% discount

    task2 = {
        p["name"]: round(p["price"] * 0.90, 2)
        for p in products
        if p["rating"] >= 4.5
    }

    print("\nTask 2 - 10% Discount:")
    print(task2)


    # TASK 3
    # All categories having products

    task3 = {
        p["category"]
        for p in products
    }

    print("\nTask 3 - All Categories:")
    print(task3)

    print("Total Categories:", len(task3))


    # TASK 4
    # Top 3 products by rating
    # Cheaper product first if ratings are equal

    task4 = sorted(
        products,
        key=lambda p: (-p["rating"], p["price"])
    )[:3]

    print("\nTask 4 - Top 3 Products:")

    for p in task4:
        print(p["name"], "-", p["rating"])


    # TASK 5
    # Total stock value

    task5 = reduce(
        lambda total, p: total + p["price"] * p["stock"],
        products,
        0
    )

    print("\nTask 5 - Total Stock Value:")
    print(f"Rs {task5:,}")


    # TASK 6
    # Any product out of stock?
    # Are all ratings >= 3?

    task6_any = any(
        p["stock"] == 0
        for p in products
    )

    task6_all = all(
        p["rating"] >= 3
        for p in products
    )

    print("\nTask 6 - Any and All:")
    print("Any out of stock:", task6_any)
    print("All ratings >= 3:", task6_all)


    # TASK 7
    # Product count per category

    task7 = {
        category: sum(
            p["category"] == category
            for p in products
        )
        for category in task3
    }

    print("\nTask 7 - Product Count Per Category:")

    for category, count in sorted(task7.items()):
        print(category, ":", count)



# PART B - FILTER FUNCTIONS



# 3. RECURSIVE SUBCATEGORIES FUNCTION

def subcategories(tree, name):
    """Find a category and its subcategories recursively."""
    def search(branch):
        """Search the category tree for the requested category."""
        for category, children in branch.items():

            if category == name:
                return collect(category, children)

            result = search(children)

            if result is not None:
                return result

        return None


    def collect(category, children):
        """Collect a category and its subcategories."""
        result = [category]

        for child, grandchildren in children.items():
            result.extend(
                collect(child, grandchildren)
            )

        return result


    result = search(tree)

    if result is None:
        raise ValueError(
            f"'{name}' is not a category."
        )

    return result



# 4. FILTER PRODUCTS FUNCTION


def filter_products(
    products,
    *,
    category=None,
    max_price=None,
    min_rating=None,
    in_stock=False,
    sort_by="price"
):
    """Filter and sort products using the specified criteria."""
    # Validate sorting option

    if sort_by not in ["price", "rating", "name"]:
        raise ValueError(
            "sort_by must be price, rating or name."
        )

    # Create a new list
    filtered = list(products)


    # CATEGORY FILTER

    if category is not None:

        valid_categories = subcategories(
            category_tree,
            category
        )

        filtered = [
            p for p in filtered
            if p["category"] in valid_categories
        ]


    # MAXIMUM PRICE FILTER

    if max_price is not None:

        filtered = [
            p for p in filtered
            if p["price"] <= max_price
        ]


    # MINIMUM RATING FILTER

    if min_rating is not None:

        filtered = [
            p for p in filtered
            if p["rating"] >= min_rating
        ]


    # IN-STOCK FILTER

    if in_stock:

        filtered = [
            p for p in filtered
            if p["stock"] > 0
        ]


    # SORTING

    if sort_by == "price":

        filtered = sorted(
            filtered,
            key=lambda p: p["price"]
        )

    elif sort_by == "rating":

        filtered = sorted(
            filtered,
            key=lambda p: -p["rating"]
        )

    elif sort_by == "name":

        filtered = sorted(
            filtered,
            key=lambda p: p["name"].lower()
        )

    return filtered


# ------------------------------------------
# 5. DISPLAY PRODUCTS
# ------------------------------------------

def display_products(items):
    """Display matching products in a formatted table."""
    print()

    print(
        f"{'#':<3} "
        f"{'Name':<20} "
        f"{'Category':<15} "
        f"{'Price (Rs)':>12} "
        f"{'Rating':>8} "
        f"{'Stock':>7}"
    )

    print("-" * 75)

    for index, p in enumerate(items, start=1):

        print(
            f"{index:<3} "
            f"{p['name']:<20} "
            f"{p['category']:<15} "
            f"{p['price']:>12,} "
            f"{p['rating']:>8.1f} "
            f"{p['stock']:>7}"
        )

    print(f"\n{len(items)} of {len(products)} products match.")



# 6. INPUT HELPERS

def ask_optional_number(prompt):
    """Ask the user for an optional non-negative number."""
    while True:

        value = input(prompt).strip()

        if value == "":
            return None

        try:
            number = float(value)

            if not (float("-inf") < number < float("inf")):
                raise ValueError

            if number < 0:
                print("Please enter a positive number.")
                continue

            return number

        except ValueError:
            print("Invalid number! Try again.")


def ask_yes_no(prompt):
    """Ask the user for a yes or no response."""
    while True:

        answer = input(prompt).strip().lower()

        if answer in ["y", "yes"]:
            return True

        if answer in ["n", "no", ""]:
            return False

        print("Please enter y or n.")


def ask_sort():
    """Ask the user to select a valid sorting option."""
    while True:

        sort_by = input(
            "Sort by (price/rating/name): "
        ).strip().lower()

        if sort_by == "":
            return "price"

        if sort_by in ["price", "rating", "name"]:
            return sort_by

        print(
            "Invalid sort! Choose price, rating or name."
        )


# ------------------------------------------
# 7. MAIN FILTER MENU
# ------------------------------------------

def main():
    """Run the product catalog filtering program."""
    # Print Part A answers first
    part_a()

    print("\n========== PART B ==========")

    while True:

        print("\n--- Product Filter ---")

        category = input(
            "Category (Enter = all): "
        ).strip()

        if category == "":
            category = None

        try:

            # Validate category
            if category is not None:
                subcategories(
                    category_tree,
                    category
                )

            max_price = ask_optional_number(
                "Max price (Enter = any): "
            )

            min_rating = ask_optional_number(
                "Min rating (Enter = any): "
            )

            in_stock = ask_yes_no(
                "In stock only? (y/n): "
            )

            sort_by = ask_sort()

            # Apply filters

            results = filter_products(
                products,
                category=category,
                max_price=max_price,
                min_rating=min_rating,
                in_stock=in_stock,
                sort_by=sort_by
            )

            # Display results

            display_products(results)

        except ValueError as error:

            print("Error:", error)

        print()

        again = ask_yes_no(
            "Filter again? (y/n): "
        )

        if not again:

            print("\nThank you for using Product Catalog!")
            break


# 8. PROGRAM ENTRY POINT

if __name__ == "__main__":
    main()
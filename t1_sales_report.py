from collections import Counter, defaultdict


# January sales data
january_data = """
Ali,Lahore,keyboard,2,3500
Sara,Karachi,mouse,1,1200
Hassan,Lahore,monitor,1,32000
Ayesha,Islamabad,keyboard,1,3500
Ali,Lahore,mouse,3,1200
Usman,Karachi,headset,2,4500
"""

# February sales data
february_data = """
Sara,Karachi,monitor,1,32000
Ali,Lahore,headset,1,4500
Bilal,Islamabad,mouse,2,1200
Ayesha,Islamabad,webcam,1,6000
Sara,Karachi,keyboard,2,3500
Zara,Lahore,mouse,1,1200
"""


# Convert sales text into dictionaries
def parse_sales(data):
    """Convert CSV-style sales text into  list of dictionaries."""

    sales = []

    for line in data.strip().splitlines():

        customer, city, product, quantity, price = line.strip().split(",")

        sale = {
            "customer": customer.strip(),
            "city": city.strip(),
            "product": product.strip(),
            "quantity": int(quantity),
            "price": int(price)
        }

        sales.append(sale)

    return sales


# Calculate revenue by product
def calculate_revenue(sales):
    """Calculate total revenue for each product."""

    revenue = defaultdict(int)

    for sale in sales:
        revenue[sale["product"]] += sale["quantity"] * sale["price"]

    return dict(revenue)


# Find top 3 products by quantity
def top_products(sales):
    """Return the three products with the highest units sold."""

    counter = Counter()

    for sale in sales:
        counter[sale["product"]] += sale["quantity"]

    return counter.most_common(3)


# Group customers by city
def customers_by_city(sales):
    """Group unique customers by city."""

    cities = defaultdict(set)

    for sale in sales:
        cities[sale["city"]].add(sale["customer"])

    return dict(cities)


# Customer and product sets
def calculate_sets(january, february):
    """Calculate customer and product differences between months."""

    january_customers = {sale["customer"] for sale in january}
    february_customers = {sale["customer"] for sale in february}

    january_products = {sale["product"] for sale in january}
    february_products = {sale["product"] for sale in february}

    return {
        "both": january_customers & february_customers,
        "january_only": january_customers - february_customers,
        "february_new": february_customers - january_customers,
        "new_products": february_products - january_products
    }


# Find top spending customer
def top_customer(sales):
    """Find the customer who spent the most money."""

    spending = defaultdict(int)

    for sale in sales:
        spending[sale["customer"]] += sale["quantity"] * sale["price"]

    return max(spending.items(), key=lambda item: item[1])


# Create inverted product index
def product_buyers(sales):
    """Map each product to the set of customers who bought it."""

    index = defaultdict(set)

    for sale in sales:
        index[sale["product"]].add(sale["customer"])

    return dict(index)


# Main report
def main():
    """Generate and print the complete sales report."""

    january = parse_sales(january_data)
    february = parse_sales(february_data)

    all_sales = january + february

    # Revenue by product
    print("Revenue by product")

    revenue = calculate_revenue(all_sales)

    sorted_revenue = sorted(
        revenue.items(),
        key=lambda item: item[1],
        reverse=True
    )

    for product, amount in sorted_revenue:
        print(f"  {product:<10} Rs {amount:>7,}")

    print(f"  {'TOTAL':<10} Rs {sum(revenue.values()):>7,}")

    # Top 3 products
    print("\nTop 3 products by units")

    for number, (product, quantity) in enumerate(top_products(all_sales), 1):
        print(f"  {number}. {product} ({quantity})")

    # Customers by city
    print("\nCustomers by city")

    cities = customers_by_city(all_sales)

    for city in sorted(cities):
        names = ", ".join(sorted(cities[city]))
        print(f"  {city}: {names}")

    # Customer sets
    print("\nCustomer sets")

    sets = calculate_sets(january, february)

    print("  Both months:", ", ".join(sorted(sets["both"])))
    print("  January only:", ", ".join(sorted(sets["january_only"])))
    print("  New in February:", ", ".join(sorted(sets["february_new"])))
    print("  Products new in February:", ", ".join(sorted(sets["new_products"])))

    # Top customer
    customer, amount = top_customer(all_sales)

    print(f"\nTop customer: {customer} (Rs {amount:,})")

    # Inverted index
    buyers = product_buyers(all_sales)

    mouse_buyers = ", ".join(sorted(buyers.get("mouse", set())))

    print(f"Buyers of mouse: {mouse_buyers}")


if __name__ == "__main__":
    main() 
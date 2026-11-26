import csv
import json
from pathlib import Path
from datetime import datetime, date
from decimal import Decimal, InvalidOperation


# ==============================
# FILE PATHS
# ==============================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

CSV_FILE = DATA_DIR / "expenses.csv"

JSON_FILE = DATA_DIR / "expenses.json"

ERROR_FILE = BASE_DIR / "errors.log"

FIELDS = ["date", "category", "amount", "note"]


# ==============================
# ERROR LOGGING
# ==============================

def log_error(line_number, reason):
    """Record invalid expense rows in the error log."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = f"{timestamp} | line {line_number} | {reason}\n"

    try:
        with ERROR_FILE.open("a", encoding="utf-8") as file:
            file.write(message)

    except FileNotFoundError:
        return "Error: log file location not found."

    except PermissionError:
        return "Error: permission denied while writing errors.log."

    return ""

# ==============================
# VALIDATE EXPENSE
# ==============================

def validate_expense(row):
    """Validate an expense row and return the cleaned expense."""
    if None in row or any(row.get(field) is None for field in FIELDS):
        raise ValueError("missing column")

    expense_date = row["date"].strip()

    category = row["category"].strip()

    amount_text = row["amount"].strip()

    note = row["note"].strip()

    try:
        date.fromisoformat(expense_date)

        if len(expense_date) != 10:
            raise ValueError

    except ValueError:
        raise ValueError(f"invalid date '{expense_date}'")

    if not category:
        raise ValueError("category cannot be empty")

    try:
        amount = Decimal(amount_text)

    except InvalidOperation:
        raise ValueError(f"invalid amount '{amount_text}'")

    if not amount.is_finite():
        raise ValueError(f"invalid amount '{amount_text}'")

    if amount <= 0:
        raise ValueError("amount must be greater than zero")

    return {
        "date": expense_date,
        "category": category,
        "amount": amount,
        "note": note
    }


# ==============================
# LOAD CSV
# ==============================

def load_expenses():
    """Load valid expenses from CSV and log invalid rows."""
    expenses = []

    bad_rows = 0
    log_messages = []

    try:

        with CSV_FILE.open(
            "r",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            reader = csv.DictReader(file)

            for line_number, row in enumerate(reader, start=2):

                try:

                    expense = validate_expense(row)

                    expenses.append(expense)

                except (ValueError, TypeError) as error:

                    bad_rows += 1

                    log_message = log_error(line_number, str(error))

                    if log_message:
                        log_messages.append(log_message)
        message = (
            f"Loaded {len(expenses)} expenses from "
            f"data/expenses.csv "
            f"({bad_rows} bad rows skipped, see errors.log)"
        )

    except FileNotFoundError:
        message = "expenses.csv not found. Starting with empty list."

    except PermissionError:
        message = "Permission denied while reading expenses.csv."

    return expenses, message, log_messages

# ==============================
# SAVE CSV
# ==============================

def save_expenses(expenses):
    """Save expenses to the CSV file and return the save status."""
    try:

        DATA_DIR.mkdir(parents=True, exist_ok=True)

        with CSV_FILE.open(
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(file, fieldnames=FIELDS)

            writer.writeheader()

            for expense in expenses:

                writer.writerow({
                    "date": expense["date"],
                    "category": expense["category"],
                    "amount": f"{expense['amount']:.2f}",
                    "note": expense["note"]
                })

        return True, ""

    except FileNotFoundError:
        return False, "Error: CSV file path not found."

    except PermissionError:
        return False, "Error: permission denied while saving CSV."


# ==============================
# ADD EXPENSE
# ==============================

def collect_expense():
    """Collect and validate expense details."""
    print("\n===== Add Expense =====")

    while True:

        expense_date = input(
            "Date (YYYY-MM-DD, Enter = today): "
        ).strip()

        if not expense_date:
            expense_date = date.today().isoformat()

        try:
            date.fromisoformat(expense_date)

            if len(expense_date) != 10:
                raise ValueError

            break

        except ValueError:
            print("Error: invalid date. Use YYYY-MM-DD.")

    while True:

        category = input("Category: ").strip()

        if category:
            break

        print("Error: category cannot be empty.")

    while True:

        amount_text = input("Amount (Rs): ").strip()

        try:

            amount = Decimal(amount_text)

            if not amount.is_finite() or amount <= 0:
                print("Error: amount must be greater than zero.")
                continue

            break

        except InvalidOperation:

            print("Error: enter a valid amount.")

    note = input("Note: ").strip()

    expense = {
        "date": expense_date,
        "category": category,
        "amount": amount,
        "note": note
    }

    return expense


def add_expense(expenses, expense):
    """Add and save a validated expense."""

    expenses.append(expense)

    success, message = save_expenses(expenses)

    if success:
        return True, ""

    expenses.pop()
    return False, message

# ==============================
# LIST EXPENSES
# ==============================

def list_expenses(expenses):
    """Display all expenses in a formatted table."""
    print("\n===== All Expenses =====")

    if not expenses:
        print("No expenses found.")
        return

    print(
        f"{'Date':<13}"
        f"{'Category':<15}"
        f"{'Amount':>12}  "
        f"Note"
    )

    print("-" * 65)

    for expense in expenses:

        print(
            f"{expense['date']:<13}"
            f"{expense['category']:<15}"
            f"{expense['amount']:>12,.2f}  "
            f"{expense['note']}"
        )


# ==============================
# MONTHLY TOTALS
# ==============================

def calculate_monthly_totals(expenses):
    """Calculate and return total expenses for each month."""
    totals = {}

    for expense in expenses:

        month = expense["date"][:7]

        totals[month] = (
            totals.get(month, Decimal("0.00"))
            + expense["amount"]
        )

    return dict(sorted(totals.items()))

def calculate_overall_total(totals):
    """Calculate the overall expense total."""
    return sum(totals.values(), Decimal("0.00"))


def show_monthly_totals(expenses):
    """Display monthly expense totals and the overall total."""
    totals = calculate_monthly_totals(expenses)

    print(f"{'Month':<10} {'Total'}")

    overall_total = calculate_overall_total(totals)

    for month, amount in totals.items():

        print(f"{month:<10} Rs {amount:>9,.2f}")

    print(f"{'TOTAL':<10} Rs {overall_total:>9,.2f}")

# ==============================
# CATEGORY TOTALS
# ==============================

def calculate_category_totals(expenses):
    """Calculate category totals and overall expenses."""
    totals = {}

    for expense in expenses:

        category = expense["category"]

        totals[category] = (
            totals.get(category, Decimal("0.00"))
            + expense["amount"]
        )

    overall_total = sum(
        totals.values(),
        Decimal("0.00")
    )

    sorted_categories = sorted(
        totals.items(),
        key=lambda item: item[1],
        reverse=True
    )
    results = []

    for category, amount in sorted_categories:
        if overall_total > 0:
            percentage = (amount / overall_total) * Decimal("100")
        else:
            percentage = Decimal("0")

        results.append((category, amount, percentage))

    return results

def show_category_totals(expenses):
    """Display category totals and percentage shares."""

    results = calculate_category_totals(expenses)

    print(
        f"{'Category':<10}"
        f"{'Total':<13}"
        f"{'Share':>6}"
    )

    for category, amount, percentage in results:
        print(
            f"{category:<10}"
            f"Rs {amount:>9,.2f} "
            f"{percentage:>5.1f}%"
        )


# ==============================
# EXPORT JSON
# ==============================

def export_json(expenses):
    """Export expenses and monthly totals to a JSON file."""
    monthly_totals = calculate_monthly_totals(expenses)

    json_expenses = []

    for expense in expenses:

        json_expenses.append({
            "date": expense["date"],
            "category": expense["category"],
            "amount": f"{expense['amount']:.2f}",
            "note": expense["note"]
        })

    json_monthly_totals = {}

    for month, amount in monthly_totals.items():

        json_monthly_totals[month] = f"{amount:.2f}"

    data = {
        "expenses": json_expenses,
        "monthly_totals": json_monthly_totals
    }

    try:

        DATA_DIR.mkdir(parents=True, exist_ok=True)

        with JSON_FILE.open(
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

        return (
            f"Exported {len(expenses)} expenses "
            f"to data/expenses.json"
        )

    except FileNotFoundError:
        return "Error: JSON file path not found."

    except PermissionError:
        return "Error: permission denied while exporting JSON."


# ==============================
# MAIN MENU
# ==============================

def main():
    """Run the expense logger menu and handle user choices."""
    expenses, message, log_messages = load_expenses()

    for log_message in log_messages:
        print(log_message)

    print(message)
    while True:

        print("\n===== Expense Logger =====")

        print("1. Add 2. List 3. Monthly totals 4. By category 5. Export JSON 6. Exit")

        choice = input("\nChoose: ").strip()

        if choice == "1":
            expense = collect_expense()

            success, message = add_expense(expenses, expense)

            if success:
                print(
                    f"Saved: {expense['date']} "
                    f"{expense['category']} Rs {expense['amount']:,.2f}"
                )
            else:
                print(message)
                print("Expense was not saved.")

        elif choice == "2":

            list_expenses(expenses)

        elif choice == "3":

            show_monthly_totals(expenses)

        elif choice == "4":

            show_category_totals(expenses)

        elif choice == "5":
            message = export_json(expenses)
            print(message)

        elif choice == "6":

            print("Expense Logger closed.")
            break

        else:

            print("Invalid choice! Select 1 to 6.")


# ==============================
# RUN PROGRAM
# ==============================

if __name__ == "__main__":
    main()
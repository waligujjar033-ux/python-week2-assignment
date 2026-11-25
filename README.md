# Python Week 2 Developer Assignment

Required Python Version: 3.12+
Tested on Python: 3.14.5
## Topics
- Dictionaries and Sets
- Functions
- Comprehensions and Lambda
- Modules and Packages
- File Handling
- Error Handling
- Command-Line Applications

## Tasks
T1 - Sales Report
T2 - Bug Fix
T3 - Converter
T4 - Product Catalog
T5 - CLI
T6 - Expense Logger
T7 - To-Do Application

## How to Run Each Ticket

```bash
python t1_sales_report.py
python t2_bugfix.py
python t3_converter.py
python t3_converter.py --test
python t4_catalog.py
python t5_cli.py --help
python t6_expenses.py
python -m todo
```


## Task 2 - Bug Log

### BUG-1: Mutable Default Argument
Cause: The same default list was reused between function calls.
Fix: Replaced the default list with None.

### BUG-2: Dictionary RuntimeError
Cause: Dictionary items were deleted during iteration.
Fix: Used list(stock) to safely remove empty items.

### BUG-3: Quantity TypeError
Cause: input() returned a string instead of an integer.
Fix: Converted quantity using int().

### BUG-4: UnboundLocalError
Cause: sold_count was modified inside a function.
Fix: Updated sold_count inside main() without global.

### BUG-5: Missing Return
Cause: stock_value() calculated the total but returned None.
Fix: Added return total.

### BUG-6: Invalid Input Handling
Cause: Unknown items, invalid quantities and insufficient stock caused errors.
Fix: Added specific exception handling and InsufficientStockError.

## T5 — Utilities Package and CLI

### Description
A Python utilities package with a command-line interface using argparse.

### Features
- Secure password generation
- Slug generation
- Email validation
- Word counting
- Age calculation in days
- Days until a future date
- Error handling

### Package Structure
```text
utils/
├── __init__.py
├── strings.py
├── dates.py
└── security.py
```

### Create Virtual Environment
```bash
python -m venv .venv
```

### Activate on Windows PowerShell
```powershell
.\.venv\Scripts\Activate.ps1
```

### Activate on Windows CMD
```cmd
.venv\Scripts\activate.bat
```

### Activate on macOS/Linux
```bash
source .venv/bin/activate
```

### Install Requirements
```bash
python -m pip install -r requirements.txt
```

### Run Commands
```bash
python t5_cli.py --help
python t5_cli.py password --length 16
python t5_cli.py password --length 16 --no-symbols
python t5_cli.py slug "Hello, World! Python 3.12"
python t5_cli.py email ali.r@mail.com
python t5_cli.py age 2005-08-14
python t5_cli.py until 2027-01-01
```

### Error Handling
Invalid inputs display an error message and exit with code 1.
Successful commands exit with code 0.

### Dependencies
Python 3.12 or later.
rich==15.0.0 is required for the T7 To-Do Application.

## What I Found Hardest

- **T3 – Unit Converter:** Handling multiple values, unit conversions, and input validation.
- **T6 – Expense Logger:** Handling invalid CSV rows, calculating totals, and exporting data to JSON.
- **T7 – To-Do Application:** Managing unique task IDs, handling corrupted JSON files, and separating logic across different modules.

These tasks helped me improve my understanding of functions, file handling, error handling, and modular programming.
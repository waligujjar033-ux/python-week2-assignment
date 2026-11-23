import sys


# T3 - UNIT CONVERTER BUILT FROM FUNCTIONS



# 1. CONVERSION FACTORS

LENGTH = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1,
    "km": 1000,
    "inch": 0.0254,
    "ft": 0.3048,
    "mile": 1609.344
}

WEIGHT = {
    "g": 0.001,
    "kg": 1,
    "oz": 0.028349523125,
    "lb": 0.45359237
}

TEMPERATURE = ["C", "F", "K"]


# 2. REUSABLE INPUT HELPERS


def ask_choice(prompt, options):

    while True:

        choice = input(prompt).strip()

        if choice in options:
            return choice

        print("Invalid choice! Try again.")


def ask_number(prompt):

    while True:

        try:
            number = float(input(prompt))
            if not (float("-inf") < number < float("inf")):
                raise ValueError
            return number

        except ValueError:
            print("Invalid number! Please try again.")


# 3. LENGTH AND WEIGHT CONVERSION


def convert_factor(value, from_unit, to_unit, factors):

    base_value = value * factors[from_unit]

    result = base_value / factors[to_unit]

    return result



# 4. TEMPERATURE FUNCTIONS


def to_kelvin(value, unit):

    if unit == "C":
        result = value + 273.15

    elif unit == "F":
        result = (value - 32) * 5 / 9 + 273.15

    elif unit == "K":
        result = value

    else:
        raise ValueError("Unknown temperature unit.")

    if result < -1e-9:
        raise ValueError(
            "temperature cannot be below absolute zero."
        )

    return max(0, result)


def from_kelvin(value, unit):

    if unit == "C":
        return value - 273.15

    elif unit == "F":
        return (value - 273.15) * 9 / 5 + 32

    elif unit == "K":
        return value

    else:
        raise ValueError("Unknown temperature unit.")


def convert_temperature(value, from_unit, to_unit):

    kelvin = to_kelvin(value, from_unit)

    return from_kelvin(kelvin, to_unit)


# 5. MAIN CONVERT FUNCTION


def convert(value, from_unit, to_unit, *, precision=2):

    if not isinstance(precision, int) or precision < 0:
        raise ValueError("Precision must be a non-negative integer.")

    if isinstance(value, bool):
        raise ValueError("Value must be a number.")

    try:
        value = float(value)
    except (TypeError, ValueError):
        raise ValueError("Value must be a number.")

    if not (float("-inf") < value < float("inf")):
        raise ValueError("Value must be finite.")

    if from_unit in LENGTH and to_unit in LENGTH:

        result = convert_factor(
            value,
            from_unit,
            to_unit,
            LENGTH
        )

    elif from_unit in WEIGHT and to_unit in WEIGHT:

        result = convert_factor(
            value,
            from_unit,
            to_unit,
            WEIGHT
        )

    elif from_unit in TEMPERATURE and to_unit in TEMPERATURE:

        result = convert_temperature(
            value,
            from_unit,
            to_unit
        )

    else:

        all_units = set(LENGTH) | set(WEIGHT) | set(TEMPERATURE)

        if from_unit not in all_units:
            raise ValueError(
                f"'{from_unit}' is not a valid unit."
            )

        if to_unit not in all_units:
            raise ValueError(
                f"'{to_unit}' is not a valid unit."
            )

        raise ValueError(
            "Cannot convert between different categories."
        )

    if not (float("-inf") < result < float("inf")):
        raise ValueError("Conversion result is not finite.")

    return round(result, precision)



# 6. MULTIPLE VALUES CONVERSION


def convert_many(values, from_unit, to_unit):

    results = []

    for value in values:

        result = convert(
            value,
            from_unit,
            to_unit
        )

        results.append(result)

    return results



# 7. VALUE INPUT HELPER


def ask_values(prompt):

    while True:

        raw = input(prompt).strip()

        parts = raw.split(",")

        if not raw:
            print("Please enter at least one number.")
            continue

        if len(parts) == 1:
            return [ask_number_from_text(parts[0])]

        try:

            values = []

            for part in parts:
                number = float(part.strip())

                if not (float("-inf") < number < float("inf")):
                    raise ValueError

                values.append(number)

            return values

        except ValueError:
            print("Invalid values! Enter numbers separated by commas.")


def ask_number_from_text(text):

    while True:

        try:
            number = float(text.strip())

            if not (float("-inf") < number < float("inf")):
                raise ValueError

            return number

        except ValueError:
            print("Invalid number! Try again.")
            return ask_number("Value: ")



# 8. DISPLAY FUNCTION


def display_results(values, results, from_unit, to_unit):

    for value, result in zip(values, results):

        print(
            f"{value:g} {from_unit} = "
            f"{result:.2f} {to_unit}"
        )


# 9. UNIT INPUT HELPER


def ask_unit(prompt, options, category):

    while True:

        unit = input(prompt).strip()

        if category == "temperature":
            unit = unit.upper()
        else:
            unit = unit.lower()

        if unit in options:
            return unit

        print(
            f"Error: '{unit}' is not a {category} unit."
        )



# 10. MAIN MENU


def main():

    while True:

        print("\n===== Unit Converter =====")

        print("1. Length")
        print("2. Weight")
        print("3. Temperature")
        print("4. Exit")

        choice = ask_choice(
            "Choose: ",
            ["1", "2", "3", "4"]
        )

        if choice == "4":

            print("Thank you for using Unit Converter!")
            break

        if choice == "1":

            units = LENGTH
            category = "length"

            print("Units: mm, cm, m, km, inch, ft, mile")

        elif choice == "2":

            units = WEIGHT
            category = "weight"

            print("Units: g, kg, oz, lb")

        else:

            units = TEMPERATURE
            category = "temperature"

            print("Units: C, F, K")

        from_unit = ask_unit(
            "From: ",
            units,
            category
        )

        to_unit = ask_unit(
            "To: ",
            units,
            category
        )

        values = ask_values("Value: ")

        try:

            results = convert_many(
                values,
                from_unit,
                to_unit
            )

            display_results(
                values,
                results,
                from_unit,
                to_unit
            )

        except ValueError as error:

            print("Error:", error)



# 11. AUTOMATIC TESTS


def run_tests():

    # Test 1: Length
    assert convert(1000, "mm", "m") == 1

    # Test 2: Length
    assert convert(100, "cm", "m") == 1

    # Test 3: Length
    assert convert(1, "km", "m") == 1000

    # Test 4: Inch to cm
    assert convert(1, "inch", "cm") == 2.54

    # Test 5: Weight
    assert convert(1000, "g", "kg") == 1

    # Test 6: Weight
    assert convert(1, "kg", "g") == 1000

    # Test 7: Celsius to Fahrenheit
    assert convert(0, "C", "F") == 32

    # Test 8: Fahrenheit to Celsius
    assert convert(32, "F", "C") == 0

    # Test 9: Celsius to Kelvin
    assert convert(0, "C", "K") == 273.15

    # Test 10: Multiple values
    assert convert_many(
        [1, 5, 10],
        "inch",
        "cm"
    ) == [2.54, 12.7, 25.4]

    # Test 11: Invalid category
    try:
        convert(10, "km", "kg")
        assert False, "Expected ValueError"
    except ValueError:
        pass

    # Test 12: Below absolute zero
    try:
        convert(-5, "K", "C")
        assert False, "Expected ValueError"
    except ValueError:
        pass

    # Test 13: Unknown unit
    try:
        convert(10, "stone", "kg")
        assert False, "Expected ValueError"
    except ValueError:
        pass

    # Test 14: Precision
    assert convert(
        1,
        "mile",
        "km",
        precision=3
    ) == 1.609

    print("All tests passed.")



# 12. PROGRAM ENTRY POINT


if __name__ == "__main__":

    if "--test" in sys.argv:
        run_tests()

    else:
        main()
from datetime import date


def parse_date(date_text):

    if not isinstance(date_text, str):
        raise ValueError("Date must be a string.")

    try:
        return date.fromisoformat(date_text)

    except ValueError:
        raise ValueError(
            "Invalid date. Use YYYY-MM-DD format."
        )


def age_in_days(birth_date):

    birth = parse_date(birth_date)

    today = date.today()

    if birth > today:
        raise ValueError(
            "Birth date cannot be in the future."
        )

    return (today - birth).days


def days_until(target_date):

    target = parse_date(target_date)

    today = date.today()

    if target < today:
        raise ValueError(
            f"{target_date} is in the past."
        )

    return (target - today).days


# Demo
if __name__ == "__main__":

    print("Age:", age_in_days("2005-08-14"), "days")

    print("Days until:", days_until("2027-01-01"))
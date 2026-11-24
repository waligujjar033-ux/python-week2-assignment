import secrets
import string


def make_password(length=12, *, symbols=True):
    """Generate a random password with optional symbols."""
    if isinstance(length, bool) or not isinstance(length, int):
        raise ValueError(
            "Length must be an integer."
        )

    if length < 8 or length > 64:
        raise ValueError(
            "length must be between 8 and 64."
        )

    if not isinstance(symbols, bool):
        raise ValueError(
            "symbols must be True or False."
        )

    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special = "!@#$%^&*?"

    password = [
        secrets.choice(lowercase),
        secrets.choice(uppercase),
        secrets.choice(digits)
    ]

    all_characters = lowercase + uppercase + digits

    if symbols:

        password.append(
            secrets.choice(special)
        )

        all_characters += special

    while len(password) < length:

        password.append(
            secrets.choice(all_characters)
        )

    # Securely shuffle the password
    secrets.SystemRandom().shuffle(password)

    return "".join(password)


# Demo
if __name__ == "__main__":

    print("Password:", make_password())

    print(
        "Without symbols:",
        make_password(16, symbols=False)
    )
import argparse
import sys

from utils import (
    slugify,
    is_valid_email,
    word_count,
    age_in_days,
    days_until,
    make_password
)


def main():
    """Run the command-line utilities and handle user commands."""
    parser = argparse.ArgumentParser(
        description="T5 Utilities Command Line Tool"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    # ----------------------------------
    # PASSWORD COMMAND
    # ----------------------------------

    password_parser = subparsers.add_parser(
        "password",
        help="Generate a secure password"
    )

    password_parser.add_argument(
        "--length",
        type=int,
        default=12,
        help="Password length (8-64)"
    )

    password_parser.add_argument(
        "--no-symbols",
        action="store_true",
        help="Generate password without symbols"
    )

    # ----------------------------------
    # SLUG COMMAND
    # ----------------------------------

    slug_parser = subparsers.add_parser(
        "slug",
        help="Convert text into a slug"
    )

    slug_parser.add_argument(
        "text",
        help="Text to convert"
    )

    # ----------------------------------
    # EMAIL COMMAND
    # ----------------------------------

    email_parser = subparsers.add_parser(
        "email",
        help="Validate an email address"
    )

    email_parser.add_argument(
        "email",
        help="Email address"
    )

    # ----------------------------------
    # AGE COMMAND
    # ----------------------------------

    age_parser = subparsers.add_parser(
        "age",
        help="Calculate age in days"
    )

    age_parser.add_argument(
        "birth_date",
        help="Birth date YYYY-MM-DD"
    )

    # ----------------------------------
    # UNTIL COMMAND
    # ----------------------------------

    until_parser = subparsers.add_parser(
        "until",
        help="Calculate days until a date"
    )

    until_parser.add_argument(
        "target_date",
        help="Target date YYYY-MM-DD"
    )

    # ----------------------------------
    # PARSE ARGUMENTS
    # ----------------------------------

    args = parser.parse_args()

    try:

        if args.command == "password":

            result = make_password(
                args.length,
                symbols=not args.no_symbols
            )

            print(result)

        elif args.command == "slug":

            result = slugify(args.text)

            print(result)

        elif args.command == "email":

            result = is_valid_email(args.email)

            if result:
                print(
                    f"{args.email} is valid."
                )

            else:
                print(
                    f"{args.email} is not valid."
                )

        elif args.command == "age":

            result = age_in_days(
                args.birth_date
            )

            print(f"{result:,} days")

        elif args.command == "until":

            result = days_until(
                args.target_date
            )

            print(
                f"{result:,} days until "
                f"{args.target_date}"
            )

    except (ValueError, TypeError) as error:

        print(f"Error: {error}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
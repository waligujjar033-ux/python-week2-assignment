import re
import unicodedata


def slugify(text):
    """Convert text into a URL-friendly slug."""
    if not isinstance(text, str):
        raise ValueError("Text must be a string.")

    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")

    text = text.lower()

    text = re.sub(r"[^a-z0-9]+", "-", text)

    return text.strip("-")


def is_valid_email(text):
    """Check whether the given email address is valid."""
    if not isinstance(text, str):
        raise ValueError("Email must be a string.")
    if ".." in text:
        return False
    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    return re.fullmatch(pattern, text) is not None


def word_count(text):
    """Count the words in the given text."""
    if not isinstance(text, str):
        raise ValueError("Text must be a string.")

    return len(text.split())


# Demo
if __name__ == "__main__":

    print(slugify("Hello, World! Python 3.12"))

    print(is_valid_email("ali.r@mail.com"))

    print(word_count("I am learning Python"))
"""
String utilities module demonstrating relative imports.

This module provides string manipulation functions and shows how
relative imports work within a package structure.
"""

# Relative import from parent package
from ..config import DEFAULT_SEPARATOR


def format_result(text):
    """Format a result string with decorative borders."""
    border = "=" * len(str(text))
    return f"\n{border}\n{text}\n{border}"


def capitalize_words(text, separator=None):
    """Capitalize each word in a string."""
    if separator is None:
        separator = DEFAULT_SEPARATOR

    words = text.split(separator)
    capitalized = [word.capitalize() for word in words]
    return separator.join(capitalized)


def reverse_string(text):
    """Reverse a string and format the result."""
    reversed_text = text[::-1]
    return format_result(f"'{text}' reversed is '{reversed_text}'")


def join_with_formatting(*args, separator=None):
    """Join multiple arguments with a separator and format."""
    if separator is None:
        separator = DEFAULT_SEPARATOR

    joined = separator.join(str(arg) for arg in args)
    return format_result(f"Joined: {joined}")


def count_characters(text):
    """Count characters in text and return formatted result."""
    # Using relative import to access helper from same package
    from . import AVAILABLE_MODULES

    char_count = len(text)
    word_count = len(text.split())

    result = f"Text: '{text}'\nCharacters: {char_count}\nWords: {word_count}"
    result += f"\nProcessed by: {AVAILABLE_MODULES}"

    return format_result(result)


def create_banner(text, width=50, char="*"):
    """Create a banner around text."""
    if len(text) > width - 4:
        width = len(text) + 4

    border = char * width
    padding = (width - len(text) - 2) // 2
    content_line = char + " " * padding + text + " " * padding + char

    # Adjust if odd width
    if len(content_line) < width:
        content_line += " "

    banner = f"{border}\n{content_line}\n{border}"
    return banner


# Module constants
STRING_MODULE_NAME = "string_utils"
SUPPORTED_OPERATIONS = [
    "capitalize_words",
    "reverse_string",
    "join_with_formatting",
    "count_characters",
    "create_banner",
]

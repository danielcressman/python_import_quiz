"""
Helper utilities for mypackage.
"""

import datetime


def format_output(value, style="default"):
    """
    Format a value for output.

    Args:
        value: The value to format
        style: Formatting style ("default", "fancy", "timestamp")

    Returns:
        Formatted string
    """
    if style == "default":
        return str(value)
    elif style == "fancy":
        return f"✨ {value} ✨"
    elif style == "timestamp":
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"[{timestamp}] {value}"
    else:
        raise ValueError(f"Unknown style: {style}")


def validate_input(value, expected_type):
    """
    Validate that a value is of the expected type.

    Args:
        value: Value to validate
        expected_type: Expected type

    Returns:
        True if valid, raises TypeError if not
    """
    if not isinstance(value, expected_type):
        raise TypeError(
            f"Expected {expected_type.__name__}, got {type(value).__name__}"
        )
    return True


def join_strings(*args, separator=" "):
    """Join multiple strings with a separator."""
    return separator.join(str(arg) for arg in args)

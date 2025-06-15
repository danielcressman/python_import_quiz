"""
Configuration module for myproject.

This module contains configuration constants and settings that are used
throughout the project via relative imports.
"""

# Mathematical constants
PI_CONSTANT = 3.14159265359
E_CONSTANT = 2.71828182846
GOLDEN_RATIO = 1.61803398875

# Default settings
DEFAULT_PRECISION = 4
DEFAULT_SEPARATOR = " "
DEFAULT_ENCODING = "utf-8"

# Application settings
APP_NAME = "MyProject Relative Imports Demo"
APP_VERSION = "1.0.0"
DEBUG_MODE = False

# Format settings
DEFAULT_WIDTH = 50
DEFAULT_BANNER_CHAR = "*"
DEFAULT_BORDER_CHAR = "="

# Validation settings
MAX_STRING_LENGTH = 1000
MAX_NUMBER_VALUE = 1e6
MIN_NUMBER_VALUE = -1e6

# Error messages
ERROR_MESSAGES = {
    "division_by_zero": "Cannot divide by zero",
    "invalid_input": "Invalid input provided",
    "out_of_range": "Value is out of acceptable range",
    "string_too_long": f"String exceeds maximum length of {MAX_STRING_LENGTH}",
}

# Module metadata
CONFIG_MODULE_NAME = "config"
LAST_UPDATED = "2024-01-01"


def get_config_info():
    """Return configuration information."""
    return {
        "app_name": APP_NAME,
        "version": APP_VERSION,
        "precision": DEFAULT_PRECISION,
        "debug": DEBUG_MODE,
        "constants": {
            "pi": PI_CONSTANT,
            "e": E_CONSTANT,
            "golden_ratio": GOLDEN_RATIO,
        },
    }


def validate_number(value):
    """Validate that a number is within acceptable range."""
    if not isinstance(value, (int, float)):
        raise TypeError("Value must be a number")

    if value < MIN_NUMBER_VALUE or value > MAX_NUMBER_VALUE:
        raise ValueError(ERROR_MESSAGES["out_of_range"])

    return True


def validate_string(text):
    """Validate that a string is within acceptable length."""
    if not isinstance(text, str):
        raise TypeError("Value must be a string")

    if len(text) > MAX_STRING_LENGTH:
        raise ValueError(ERROR_MESSAGES["string_too_long"])

    return True

"""
Module Alpha for demonstrating star import conflicts.

This module defines several functions and variables that will
conflict with those in module_beta when both are imported with *.
"""


def process():
    """Process function from module alpha."""
    return "Processing from ALPHA module"


def calculate(x, y):
    """Calculate function from module alpha."""
    return f"ALPHA calculation: {x} + {y} = {x + y}"


def transform(data):
    """Transform function from module alpha."""
    return f"ALPHA transform: {data.upper()}"


class Helper:
    """Helper class from module alpha."""

    def __init__(self):
        self.source = "alpha"

    def help(self):
        return f"Help from {self.source} module"


# Variables that will conflict
CONSTANT = "ALPHA_CONSTANT"
VERSION = "1.0.0-alpha"
CONFIG = {"source": "alpha", "priority": 1}

# Private variables (shouldn't be imported with *)
_private_value = "This is private to alpha"

# List of what should be imported with *
__all__ = [
    "process",
    "calculate",
    "transform",
    "Helper",
    "CONSTANT",
    "VERSION",
    "CONFIG",
]


def get_module_info():
    """Get information about this module."""
    return {
        "name": "module_alpha",
        "functions": ["process", "calculate", "transform"],
        "classes": ["Helper"],
        "constants": ["CONSTANT", "VERSION", "CONFIG"],
    }

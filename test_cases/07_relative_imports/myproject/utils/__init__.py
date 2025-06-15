"""
Utils subpackage for myproject.

This subpackage contains utility modules that demonstrate
relative imports within a nested package structure.
"""

from .math_utils import add, multiply, power
from .string_utils import capitalize_words, reverse_string

__all__ = ["add", "multiply", "power", "capitalize_words", "reverse_string"]

# Subpackage metadata
UTILS_VERSION = "1.0.0"
AVAILABLE_MODULES = ["math_utils", "string_utils"]

"""
Math utilities module demonstrating relative imports.

This module shows how to use relative imports to access other modules
within the same package structure.
"""

# Relative import from sibling module
# Relative import from parent package
from ..config import DEFAULT_PRECISION
from .string_utils import format_result


def add(a, b):
    """Add two numbers and format the result."""
    result = a + b
    return format_result(f"{a} + {b} = {result}")


def multiply(a, b):
    """Multiply two numbers and format the result."""
    result = a * b
    return format_result(f"{a} × {b} = {result}")


def power(base, exponent):
    """Calculate base raised to the power of exponent."""
    result = base**exponent
    return format_result(f"{base}^{exponent} = {result}")


def divide(a, b, precision=None):
    """Divide a by b with optional precision control."""
    if b == 0:
        raise ValueError("Cannot divide by zero")

    if precision is None:
        precision = DEFAULT_PRECISION

    result = round(a / b, precision)
    return format_result(f"{a} ÷ {b} = {result}")


def calculate_circle_area(radius):
    """Calculate the area of a circle using relative imports."""
    # Using relative import to access constants from parent
    from .. import PI_CONSTANT

    area = PI_CONSTANT * power(radius, 2)
    return format_result(f"Circle area (r={radius}): {area}")


# Module constants
MATH_MODULE_NAME = "math_utils"
SUPPORTED_OPERATIONS = ["add", "multiply", "power", "divide"]

"""
Core functionality for mypackage.
"""

# Package constant
CONSTANT = 42


def calculate(x, y, operation="add"):
    """
    Perform basic calculations.

    Args:
        x: First number
        y: Second number
        operation: Operation to perform ("add", "subtract", "multiply", "divide")

    Returns:
        Result of the calculation
    """
    if operation == "add":
        return x + y
    elif operation == "subtract":
        return x - y
    elif operation == "multiply":
        return x * y
    elif operation == "divide":
        if y == 0:
            raise ValueError("Cannot divide by zero")
        return x / y
    else:
        raise ValueError(f"Unknown operation: {operation}")


def _private_function():
    """This is a private function that shouldn't be imported."""
    return "This should not be accessible from outside"

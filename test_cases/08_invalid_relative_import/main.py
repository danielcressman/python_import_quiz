#!/usr/bin/env python3
"""
Test script that demonstrates invalid relative import usage.

This script attempts to use relative imports incorrectly, which should
result in an ImportError or ValueError. Relative imports can only be used
within packages, not in scripts run directly.
"""

# This relative import is invalid because this script is being run directly
# as the main module, not as part of a package
from ..nonexistent import some_function

# This is also invalid - trying to import from a sibling that doesn't exist
from .sibling_module import another_function


def main():
    print("This should never print because the imports will fail")

    # These function calls would fail even if imports worked
    result1 = some_function()
    result2 = another_function()

    print(f"Results: {result1}, {result2}")


if __name__ == "__main__":
    main()

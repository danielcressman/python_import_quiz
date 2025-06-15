#!/usr/bin/env python3
"""
Test script for the mypackage example.

This demonstrates various ways to import from a Python package
with an __init__.py file.
"""

# Import the entire package
import mypackage

# Import everything that's in __all__
from mypackage import *

# Import specific functions from the package
from mypackage import CONSTANT, calculate, format_output


def main():
    print("Testing package imports...")
    print("=" * 40)

    # Test package info
    print("1. Package information:")
    print(mypackage.package_info())
    print()

    # Test imported constant
    print("2. Using imported constant:")
    print(f"CONSTANT = {CONSTANT}")
    print()

    # Test imported functions
    print("3. Using imported functions:")
    result = calculate(10, 5, "multiply")
    print(f"10 * 5 = {result}")

    formatted = format_output(result, "fancy")
    print(f"Formatted: {formatted}")
    print()

    # Test accessing through package namespace
    print("4. Using package namespace:")
    division_result = mypackage.calculate(20, 4, "divide")
    print(f"20 / 4 = {division_result}")

    timestamp_output = mypackage.format_output("Package test complete", "timestamp")
    print(timestamp_output)
    print()

    # Test version info
    print("5. Package metadata:")
    print(f"Version: {mypackage.__version__}")
    print(f"Author: {mypackage.__author__}")

    print("\nAll package imports successful!")


if __name__ == "__main__":
    main()

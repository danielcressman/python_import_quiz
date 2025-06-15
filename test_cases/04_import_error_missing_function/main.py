#!/usr/bin/env python3
"""
Test script that attempts to import a function that doesn't exist in the module.

This should result in an ImportError because the 'divide' function
is not defined in math_utils.py.
"""

# This import will fail because 'divide' function doesn't exist in math_utils
from math_utils import add, divide, multiply, subtract


def main():
    print("Testing math operations...")

    # These would work if the import succeeded
    print(f"5 + 3 = {add(5, 3)}")
    print(f"10 - 4 = {subtract(10, 4)}")
    print(f"6 * 7 = {multiply(6, 7)}")

    # This would fail even if import succeeded since divide doesn't exist
    print(f"20 / 4 = {divide(20, 4)}")


if __name__ == "__main__":
    main()

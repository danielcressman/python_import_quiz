#!/usr/bin/env python3
"""
Test script for relative imports demonstration.

This script tests relative imports within a Python package structure.
It demonstrates how modules can import from each other using relative
import syntax (. and ..).
"""

# Import the main package
import myproject

# Import specific functions
from myproject.core import main_function, run_comprehensive_demo

# Import specific modules from the package
from myproject.utils import math_utils, string_utils


def main():
    print("Testing relative imports...")
    print("=" * 50)

    # Test basic package import
    print("1. Package Information:")
    print(f"Package: {myproject.PACKAGE_NAME}")
    print(f"Version: {myproject.__version__}")
    print(f"Debug mode: {myproject.DEBUG}")
    print()

    # Test main function from core module
    print("2. Running main function from core:")
    try:
        result = main_function()
        print(f"Main function result: {result}")
    except Exception as e:
        print(f"Error in main function: {e}")
    print()

    # Test direct module access
    print("3. Direct module access:")
    try:
        # Test math utilities
        math_result = math_utils.multiply(6, 7)
        print(f"Math result: {math_result}")

        # Test string utilities
        string_result = string_utils.reverse_string("imports")
        print(f"String result: {string_result}")

        # Test another string function
        banner = string_utils.create_banner("RELATIVE IMPORTS", width=40)
        print(f"Banner:\n{banner}")
    except Exception as e:
        print(f"Error in direct module access: {e}")
    print()

    # Test accessing through package namespace
    print("4. Package namespace access:")
    try:
        # Access through package
        pkg_math = myproject.math_utils.add(15, 25)
        print(f"Package math result: {pkg_math}")

        pkg_string = myproject.string_utils.capitalize_words("python package imports")
        print(f"Package string result: {pkg_string}")
    except Exception as e:
        print(f"Error in package namespace access: {e}")
    print()

    # Test comprehensive demo
    print("5. Comprehensive demonstration:")
    try:
        demo_result = run_comprehensive_demo()
        print(f"\nDemo result: {demo_result}")
    except Exception as e:
        print(f"Error in comprehensive demo: {e}")

    print("\nRelative imports test complete!")


if __name__ == "__main__":
    main()

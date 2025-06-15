#!/usr/bin/env python3
"""
Test script that attempts to import a module with syntax errors.

This script tries to import broken_module.py which contains various
syntax errors. This should result in a SyntaxError when Python
tries to parse the module.
"""

# This import will fail because broken_module.py has syntax errors
import broken_module


def main():
    print("This should never print because the import will fail due to syntax errors")

    # These function calls would fail even if the import worked
    result = broken_module.valid_function()
    print(f"Result: {result}")

    # Try to use the broken functions
    broken_result = broken_module.broken_function()
    print(f"Broken result: {broken_result}")

    # Try to instantiate the broken class
    obj = broken_module.BrokenClass()
    print(f"Object: {obj}")


if __name__ == "__main__":
    main()

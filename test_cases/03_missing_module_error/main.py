#!/usr/bin/env python3
"""
Test script that attempts to import a module that doesn't exist.

This should result in a ModuleNotFoundError.
"""

# This import will fail because 'nonexistent_module' doesn't exist
import nonexistent_module


def main():
    print("This should never print because the import will fail")
    result = nonexistent_module.some_function()
    print(f"Result: {result}")


if __name__ == "__main__":
    main()

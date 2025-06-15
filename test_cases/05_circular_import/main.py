#!/usr/bin/env python3
"""
Test script that demonstrates circular import issues.

This script imports modules that have circular dependencies,
which can cause ImportError or AttributeError depending on
when the imports are executed.
"""

# Import both modules - this will trigger the circular import
import module_a
import module_b


def main():
    print("Testing circular imports...")
    print("=" * 40)

    try:
        print("1. Calling function from module A:")
        result_a = module_a.function_a()
        print(f"Result: {result_a}")
    except Exception as e:
        print(f"Error calling function_a: {e}")

    try:
        print("\n2. Calling function from module B:")
        result_b = module_b.function_b()
        print(f"Result: {result_b}")
    except Exception as e:
        print(f"Error calling function_b: {e}")

    try:
        print("\n3. Starting chain from module A:")
        chain_a = module_a.start_chain()
        print(f"Chain result: {chain_a}")
    except Exception as e:
        print(f"Error in chain from A: {e}")

    try:
        print("\n4. Starting chain from module B:")
        chain_b = module_b.start_from_b()
        print(f"Chain result: {chain_b}")
    except Exception as e:
        print(f"Error in chain from B: {e}")

    print("\nCircular import test complete!")


if __name__ == "__main__":
    main()

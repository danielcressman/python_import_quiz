#!/usr/bin/env python3
"""
Test script that demonstrates AttributeError scenarios.

This script imports a module and then tries to access attributes
(functions, variables, classes) that don't exist, which should
result in AttributeError exceptions.
"""

import data_module


def main():
    print("Testing attribute access...")
    print("=" * 40)

    # Test accessing existing attributes first (these should work)
    print("1. Testing existing attributes:")
    try:
        result = data_module.process_data("test data")
        print(f"✓ process_data: {result}")

        processor = data_module.DataProcessor("TestProcessor")
        print(f"✓ DataProcessor created: {processor.name}")

        print(f"✓ MODULE_VERSION: {data_module.MODULE_VERSION}")
    except Exception as e:
        print(f"Unexpected error with existing attributes: {e}")

    print()

    # Test accessing non-existent function (should cause AttributeError)
    print("2. Testing non-existent function:")
    try:
        # This function doesn't exist in data_module
        missing_result = data_module.missing_function("test")
        print(f"This shouldn't print: {missing_result}")
    except AttributeError as e:
        print(f"✓ AttributeError caught: {e}")
    except Exception as e:
        print(f"Unexpected error type: {e}")

    print()

    # Test accessing non-existent constant (should cause AttributeError)
    print("3. Testing non-existent constant:")
    try:
        # This constant doesn't exist in data_module
        missing_const = data_module.MISSING_CONSTANT
        print(f"This shouldn't print: {missing_const}")
    except AttributeError as e:
        print(f"✓ AttributeError caught: {e}")
    except Exception as e:
        print(f"Unexpected error type: {e}")

    print()

    # Test accessing non-existent class (should cause AttributeError)
    print("4. Testing non-existent class:")
    try:
        # This class doesn't exist in data_module
        missing_class = data_module.MissingClass()
        print(f"This shouldn't print: {missing_class}")
    except AttributeError as e:
        print(f"✓ AttributeError caught: {e}")
    except Exception as e:
        print(f"Unexpected error type: {e}")

    print()

    # Test accessing non-existent method on existing class
    print("5. Testing non-existent method on existing class:")
    try:
        processor = data_module.DataProcessor()
        # This method doesn't exist on DataProcessor
        result = processor.missing_method("test")
        print(f"This shouldn't print: {result}")
    except AttributeError as e:
        print(f"✓ AttributeError caught: {e}")
    except Exception as e:
        print(f"Unexpected error type: {e}")

    print()

    # Test accessing non-existent attribute on class instance
    print("6. Testing non-existent attribute on class instance:")
    try:
        processor = data_module.DataProcessor()
        # This attribute doesn't exist on DataProcessor instances
        missing_attr = processor.missing_attribute
        print(f"This shouldn't print: {missing_attr}")
    except AttributeError as e:
        print(f"✓ AttributeError caught: {e}")
    except Exception as e:
        print(f"Unexpected error type: {e}")

    print("\nAttribute error test complete!")
    print("If you see this message, the AttributeErrors were handled properly.")


if __name__ == "__main__":
    main()

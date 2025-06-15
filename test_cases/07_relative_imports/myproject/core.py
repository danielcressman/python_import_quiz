"""
Core module for myproject demonstrating relative imports.

This module serves as the main entry point and demonstrates how to use
relative imports to access other modules within the same package.
"""

# Relative imports from sibling modules
from .config import (
    APP_NAME,
    APP_VERSION,
    get_config_info,
    validate_number,
    validate_string,
)
from .utils import math_utils, string_utils

# Relative imports of specific functions
from .utils.math_utils import add
from .utils.string_utils import capitalize_words, create_banner, reverse_string


def main_function():
    """Main function that demonstrates relative imports in action."""
    print(create_banner(f"{APP_NAME} v{APP_VERSION}", char="="))
    print("\nDemonstrating relative imports...")

    # Use functions imported relatively
    math_result = add(10, 5)
    print(f"\nMath operation: {math_result}")

    string_result = capitalize_words("hello world from relative imports")
    print(f"String operation: {string_result}")

    reverse_result = reverse_string("relative")
    print(f"Reverse operation: {reverse_result}")

    # Use module-level access
    power_result = math_utils.power(2, 8)
    print(f"Power operation: {power_result}")

    banner_result = string_utils.create_banner("SUCCESS!", width=30)
    print(f"\nBanner:\n{banner_result}")

    return "Core function execution completed successfully"


def demonstrate_validation():
    """Demonstrate validation functions from config module."""
    print("\nDemonstrating validation...")

    try:
        # Test number validation
        validate_number(42)
        print("✓ Number validation passed")

        # Test string validation
        validate_string("This is a valid string")
        print("✓ String validation passed")

        # Test invalid number
        validate_number("not a number")

    except (TypeError, ValueError) as e:
        print(f"✓ Validation caught error as expected: {e}")


def show_config():
    """Display configuration information using relative imports."""
    print("\nConfiguration Information:")
    config_info = get_config_info()

    for key, value in config_info.items():
        if isinstance(value, dict):
            print(f"{key.title()}:")
            for sub_key, sub_value in value.items():
                print(f"  {sub_key}: {sub_value}")
        else:
            print(f"{key.title()}: {value}")


def run_comprehensive_demo():
    """Run a comprehensive demonstration of all relative import features."""
    print("=" * 60)
    print("COMPREHENSIVE RELATIVE IMPORTS DEMONSTRATION")
    print("=" * 60)

    # Main functionality
    result = main_function()
    print(f"\nMain result: {result}")

    # Validation demo
    demonstrate_validation()

    # Configuration display
    show_config()

    # Advanced math operations
    print("\nAdvanced Math Operations:")
    try:
        circle_area = math_utils.calculate_circle_area(5)
        print(f"Circle area: {circle_area}")

        division_result = math_utils.divide(100, 7, precision=3)
        print(f"Division: {division_result}")

    except Exception as e:
        print(f"Math operation error: {e}")

    # Advanced string operations
    print("\nAdvanced String Operations:")
    char_count = string_utils.count_characters("Relative imports are powerful!")
    print(char_count)

    join_result = string_utils.join_with_formatting(
        "Python", "Relative", "Imports", separator=" -> "
    )
    print(join_result)

    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)

    return "All relative import demonstrations completed successfully"


# Module constants accessible through relative imports
CORE_MODULE_NAME = "core"
FEATURES = [
    "relative_imports",
    "package_structure",
    "cross_module_access",
    "validation",
    "configuration",
]


def get_module_info():
    """Return information about this core module."""
    return {
        "name": CORE_MODULE_NAME,
        "features": FEATURES,
        "imports": {
            "config_functions": [
                "get_config_info",
                "validate_number",
                "validate_string",
            ],
            "math_functions": ["add", "multiply", "power"],
            "string_functions": ["capitalize_words", "create_banner", "reverse_string"],
            "modules": ["math_utils", "string_utils"],
        },
    }


# Package constants that can be imported by other modules
PI_CONSTANT = 3.14159  # Re-exported from config for convenience
DEFAULT_MESSAGE = "Hello from core module!"

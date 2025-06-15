#!/usr/bin/env python3
"""
Test script that demonstrates star import conflicts.

This script imports from two modules using star imports (*), where both
modules define functions and variables with the same names. This creates
namespace conflicts where the second import overwrites the first.
"""

# Import everything from module_alpha first
from module_alpha import *

# Import everything from module_beta second (this will overwrite conflicting names)
from module_beta import *


def main():
    print("Testing star import conflicts...")
    print("=" * 50)

    print("Note: module_alpha was imported first, then module_beta")
    print("The second import (beta) should overwrite conflicting names.\n")

    # Test conflicting functions
    print("1. Testing conflicting functions:")
    print("   Calling process():")
    result = process()
    print(f"   Result: {result}")
    print("   (Should be from BETA module)")

    print("\n   Calling calculate(10, 5):")
    calc_result = calculate(10, 5)
    print(f"   Result: {calc_result}")
    print("   (Should be BETA's multiplication, not ALPHA's addition)")

    print("\n   Calling transform('Hello World'):")
    transform_result = transform("Hello World")
    print(f"   Result: {transform_result}")
    print("   (Should be BETA's lowercase, not ALPHA's uppercase)")

    # Test conflicting variables
    print("\n2. Testing conflicting variables:")
    print(f"   CONSTANT = {CONSTANT}")
    print("   (Should be 'BETA_CONSTANT')")

    print(f"   VERSION = {VERSION}")
    print("   (Should be '2.0.0-beta')")

    print(f"   CONFIG = {CONFIG}")
    print("   (Should be beta's config with priority 2)")

    # Test conflicting classes
    print("\n3. Testing conflicting classes:")
    helper = Helper()
    help_result = helper.help()
    print(f"   Helper().help() = {help_result}")
    print("   (Should be from beta module)")

    # Test functions unique to beta (should work)
    print("\n4. Testing functions unique to beta:")
    try:
        analyze_result = analyze("test data")
        print(f"   analyze('test data') = {analyze_result}")
        print("   (This function only exists in beta)")
    except NameError as e:
        print(f"   Error: {e}")

    # Test classes unique to beta (should work)
    print("\n5. Testing classes unique to beta:")
    try:
        analyzer = Analyzer()
        analysis = analyzer.analyze("sample text")
        print(f"   Analyzer().analyze('sample text') = {analysis}")
        print("   (This class only exists in beta)")
    except NameError as e:
        print(f"   Error: {e}")

    # Test variables unique to beta (should work)
    print("\n6. Testing variables unique to beta:")
    try:
        print(f"   BETA_SPECIFIC = {BETA_SPECIFIC}")
        print(f"   SETTINGS = {SETTINGS}")
        print("   (These variables only exist in beta)")
    except NameError as e:
        print(f"   Error: {e}")

    # Demonstrate the problem: alpha functions are no longer accessible
    print("\n7. Demonstrating the problem:")
    print("   Can we still access alpha's specific behavior?")

    # Try to access alpha's get_module_info (should fail if not in __all__)
    try:
        alpha_info = get_module_info()
        print(f"   get_module_info() result: {alpha_info}")
        print("   (This shows which module's version is accessible)")
    except NameError as e:
        print(f"   Error accessing get_module_info: {e}")

    # Show the namespace pollution
    print("\n8. Current namespace contents:")
    current_globals = {
        name: value
        for name, value in globals().items()
        if not name.startswith("_") and name not in ["main"]
    }

    print("   Available names from star imports:")
    for name in sorted(current_globals.keys()):
        if name not in [
            "__annotations__",
            "__builtins__",
            "__cached__",
            "__doc__",
            "__file__",
            "__loader__",
            "__name__",
            "__package__",
            "__spec__",
        ]:
            print(f"     {name}")

    print("\nStar import conflicts demonstration complete!")
    print("\nKey takeaway: The second star import overwrote conflicting names.")
    print("This is why star imports are generally discouraged in production code.")


if __name__ == "__main__":
    main()

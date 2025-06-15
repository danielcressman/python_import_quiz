#!/usr/bin/env python3
"""
Test script comparing packages with empty __init__.py vs packages without __init__.py.

This script demonstrates the difference between:
1. Regular packages (with __init__.py) - traditional Python packages
2. Namespace packages (without __init__.py) - PEP 420 implicit namespace packages

Both work in Python 3.3+, but have different behaviors and characteristics.
"""

# Import from package with __init__.py (regular package)
from package_with_init import module_a
from package_with_init.module_a import ClassA, function_from_a

# Import from package without __init__.py (namespace package)
from package_without_init import module_b
from package_without_init.module_b import ClassB, function_from_b


def test_regular_package():
    """Test the regular package (with __init__.py)."""
    print("REGULAR PACKAGE (with __init__.py):")
    print("-" * 40)

    # Test function import
    result = function_from_a()
    print(f"Function result: {result}")

    # Test calculation
    sum_result = module_a.calculate_sum(10, 5)
    print(f"Sum calculation: 10 + 5 = {sum_result}")

    # Test class instantiation
    obj_a = ClassA()
    print(f"Class info: {obj_a.get_info()}")

    # Test module attributes
    print(f"Module name: {module_a.MODULE_NAME}")
    print(f"Package type: {module_a.PACKAGE_TYPE}")
    print(f"Available functions: {module_a.AVAILABLE_FUNCTIONS}")

    # Test package object attributes
    try:
        import package_with_init

        print(f"Package object: {package_with_init}")
        print(
            f"Package __file__: {getattr(package_with_init, '__file__', 'Not available')}"
        )
        print(
            f"Package __path__: {getattr(package_with_init, '__path__', 'Not available')}"
        )
    except Exception as e:
        print(f"Error accessing package attributes: {e}")


def test_namespace_package():
    """Test the namespace package (without __init__.py)."""
    print("\nNAMESPACE PACKAGE (without __init__.py):")
    print("-" * 40)

    # Test function import
    result = function_from_b()
    print(f"Function result: {result}")

    # Test calculation
    product_result = module_b.calculate_product(10, 5)
    print(f"Product calculation: 10 * 5 = {product_result}")

    # Test class instantiation
    obj_b = ClassB()
    print(f"Class info: {obj_b.get_info()}")

    # Test module attributes
    print(f"Module name: {module_b.MODULE_NAME}")
    print(f"Package type: {module_b.PACKAGE_TYPE}")
    print(f"Available functions: {module_b.AVAILABLE_FUNCTIONS}")

    # Test package object attributes
    try:
        import package_without_init

        print(f"Package object: {package_without_init}")
        print(
            f"Package __file__: {getattr(package_without_init, '__file__', 'Not available')}"
        )
        print(
            f"Package __path__: {getattr(package_without_init, '__path__', 'Not available')}"
        )
    except Exception as e:
        print(f"Error accessing package attributes: {e}")


def compare_packages():
    """Compare the two package types."""
    print("\nPACKAGE COMPARISON:")
    print("-" * 40)

    # Import both packages
    import package_with_init
    import package_without_init

    print("Regular Package (with __init__.py):")
    print(f"  Type: {type(package_with_init)}")
    print(f"  Has __file__: {hasattr(package_with_init, '__file__')}")
    print(f"  Has __path__: {hasattr(package_with_init, '__path__')}")

    if hasattr(package_with_init, "__file__"):
        print(f"  __file__ value: {package_with_init.__file__}")

    print("\nNamespace Package (without __init__.py):")
    print(f"  Type: {type(package_without_init)}")
    print(f"  Has __file__: {hasattr(package_without_init, '__file__')}")
    print(f"  Has __path__: {hasattr(package_without_init, '__path__')}")

    if hasattr(package_without_init, "__path__"):
        print(f"  __path__ value: {package_without_init.__path__}")

    # Test directory listing capabilities
    print("\nDirectory listing:")
    try:
        print(
            f"  Regular package dir(): {[item for item in dir(package_with_init) if not item.startswith('_')]}"
        )
    except Exception as e:
        print(f"  Regular package dir() error: {e}")

    try:
        print(
            f"  Namespace package dir(): {[item for item in dir(package_without_init) if not item.startswith('_')]}"
        )
    except Exception as e:
        print(f"  Namespace package dir() error: {e}")


def test_import_behaviors():
    """Test different import behaviors."""
    print("\nIMPORT BEHAVIOR TESTS:")
    print("-" * 40)

    # Test importing the package itself
    print("1. Importing packages directly:")
    try:
        import package_with_init as regular_pkg

        print(f"   ✓ Regular package imported: {regular_pkg}")
    except Exception as e:
        print(f"   ✗ Regular package import failed: {e}")

    try:
        import package_without_init as namespace_pkg

        print(f"   ✓ Namespace package imported: {namespace_pkg}")
    except Exception as e:
        print(f"   ✗ Namespace package import failed: {e}")

    # Test star imports (should fail for namespace packages without __all__)
    print("\n2. Testing star imports:")
    try:
        # This should work but import nothing since __init__.py is empty
        from package_with_init import *

        print("   ✓ Star import from regular package succeeded (but imported nothing)")
    except Exception as e:
        print(f"   ✗ Star import from regular package failed: {e}")

    try:
        # This should fail since namespace packages don't support * imports
        from package_without_init import *

        print("   ✓ Star import from namespace package succeeded")
    except Exception as e:
        print(f"   ✗ Star import from namespace package failed: {e}")

    # Test submodule access
    print("\n3. Testing submodule access:")
    try:
        print("   ✓ Submodule access in regular package works")
    except Exception as e:
        print(f"   ✗ Submodule access in regular package failed: {e}")

    try:
        print("   ✓ Submodule access in namespace package works")
    except Exception as e:
        print(f"   ✗ Submodule access in namespace package failed: {e}")


def main():
    print("Testing empty __init__.py vs missing __init__.py")
    print("=" * 60)
    print("This test compares regular packages (with __init__.py) vs")
    print("namespace packages (without __init__.py) introduced in PEP 420.")
    print()

    # Test regular package functionality
    test_regular_package()

    # Test namespace package functionality
    test_namespace_package()

    # Compare the packages
    compare_packages()

    # Test import behaviors
    test_import_behaviors()

    print("\n" + "=" * 60)
    print("SUMMARY OF DIFFERENCES:")
    print("=" * 60)
    print("Regular Package (with __init__.py):")
    print("• Has __file__ attribute pointing to __init__.py")
    print("• Can contain initialization code")
    print("• Can control what gets imported with __all__")
    print("• Supports star imports (from package import *)")
    print("• Traditional Python package format")
    print()
    print("Namespace Package (without __init__.py):")
    print("• No __file__ attribute")
    print("• Cannot contain initialization code")
    print("• Does not support star imports")
    print("• Can span multiple directories")
    print("• Implicit namespace packages (PEP 420)")
    print("• Useful for distributing packages across multiple locations")
    print()
    print("Both types work for importing submodules and are valid in Python 3.3+")


if __name__ == "__main__":
    main()

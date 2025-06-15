#!/usr/bin/env python3
"""
Test script for namespace package imports.

This demonstrates importing from a namespace package (a package
without __init__.py). In Python 3.3+, this creates an implicit
namespace package.
"""

# Import from the namespace package
from namespace_pkg import tools
from namespace_pkg.tools import Toolbox, hammer, screwdriver


def main():
    print("Testing namespace package imports...")
    print("=" * 40)

    # Test direct function imports
    print("1. Using directly imported functions:")
    print(hammer())
    print(screwdriver())
    print()

    # Test module-level access
    print("2. Using module-level access:")
    print(tools.wrench())
    print(f"Tool count: {tools.TOOL_COUNT}")
    print(f"Info: {tools.NAMESPACE_INFO}")
    print()

    # Test class import and usage
    print("3. Using imported class:")
    toolbox = Toolbox()
    print(toolbox.list_tools())
    print(toolbox.add_tool("Hammer"))
    print(toolbox.add_tool("Screwdriver"))
    print(toolbox.add_tool("Wrench"))
    print(toolbox.list_tools())
    print()

    # Test accessing through full module path
    print("4. Accessing through full module path:")
    new_toolbox = tools.Toolbox()
    print(new_toolbox.add_tool("Drill"))
    print(new_toolbox.list_tools())

    print("\nNamespace package import test complete!")


if __name__ == "__main__":
    main()

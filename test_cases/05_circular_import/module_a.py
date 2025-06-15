def function_a():
    """Function in module A that depends on module B."""
    # Import module B from within the function to demonstrate circular import
    from module_b import function_b

    print("Function A is calling function B")
    return function_b() + " -> A"


def helper_a():
    """Helper function in module A."""
    return "Helper from A"


# This import at module level creates a circular dependency
# module_a imports module_b, and module_b imports module_a
import module_b


def start_chain():
    """Start the circular import chain."""
    print("Starting from module A")
    return module_b.function_b()

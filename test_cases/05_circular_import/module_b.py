def function_b():
    """Function in module B that depends on module A."""
    # Import module A from within the function to demonstrate circular import
    from module_a import function_a

    print("Function B is calling function A")
    return function_a() + " -> B"


def helper_b():
    """Helper function in module B."""
    return "Helper from B"


# This import at module level creates a circular dependency
# module_b imports module_a, and module_a imports module_b
import module_a


def start_from_b():
    """Start the circular import chain from module B."""
    print("Starting from module B")
    return module_a.function_a()

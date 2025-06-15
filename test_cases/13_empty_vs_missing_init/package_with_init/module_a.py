def function_from_a():
    """Function from module A in package with __init__.py."""
    return "Hello from module A (regular package)"


def calculate_sum(a, b):
    """Calculate sum of two numbers."""
    return a + b


class ClassA:
    """Class from module A."""

    def __init__(self):
        self.name = "ClassA"
        self.package_type = "regular"

    def get_info(self):
        return f"{self.name} from {self.package_type} package"


# Module constants
MODULE_NAME = "module_a"
PACKAGE_TYPE = "regular"
AVAILABLE_FUNCTIONS = ["function_from_a", "calculate_sum"]

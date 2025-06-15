def function_from_b():
    """Function from module B in namespace package (no __init__.py)."""
    return "Hello from module B (namespace package)"


def calculate_product(a, b):
    """Calculate product of two numbers."""
    return a * b


class ClassB:
    """Class from module B."""

    def __init__(self):
        self.name = "ClassB"
        self.package_type = "namespace"

    def get_info(self):
        return f"{self.name} from {self.package_type} package"


# Module constants
MODULE_NAME = "module_b"
PACKAGE_TYPE = "namespace"
AVAILABLE_FUNCTIONS = ["function_from_b", "calculate_product"]

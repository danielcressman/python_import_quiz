def process_data(data):
    """Process some data and return results."""
    return f"Processed: {data}"


def validate_input(value):
    """Validate input value."""
    if value is None:
        raise ValueError("Value cannot be None")
    return True


class DataProcessor:
    """A simple data processor class."""

    def __init__(self, name="DefaultProcessor"):
        self.name = name
        self.processed_count = 0

    def process(self, item):
        """Process an individual item."""
        self.processed_count += 1
        return f"{self.name} processed: {item}"

    def get_stats(self):
        """Get processing statistics."""
        return {"name": self.name, "processed_count": self.processed_count}


# Module constants
MODULE_VERSION = "1.0.0"
SUPPORTED_FORMATS = ["json", "csv", "xml"]

# Note: deliberately NOT defining these attributes that will be accessed:
# - missing_function (function that doesn't exist)
# - MISSING_CONSTANT (constant that doesn't exist)
# - MissingClass (class that doesn't exist)

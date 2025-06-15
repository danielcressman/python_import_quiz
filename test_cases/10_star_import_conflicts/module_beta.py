"""
Module Beta for demonstrating star import conflicts.

This module defines several functions and variables with the same names
as those in module_alpha, creating conflicts when both are imported with *.
"""


def process():
    """Process function from module beta."""
    return "Processing from BETA module"


def calculate(x, y):
    """Calculate function from module beta."""
    return f"BETA calculation: {x} * {y} = {x * y}"


def transform(data):
    """Transform function from module beta."""
    return f"BETA transform: {data.lower()}"


def analyze(data):
    """Analyze function unique to module beta."""
    return f"BETA analysis: {len(data)} characters"


class Helper:
    """Helper class from module beta."""

    def __init__(self):
        self.source = "beta"

    def help(self):
        return f"Help from {self.source} module"


class Analyzer:
    """Analyzer class unique to module beta."""

    def __init__(self):
        self.results = []

    def analyze(self, item):
        result = f"Analyzed: {item}"
        self.results.append(result)
        return result


# Variables that will conflict
CONSTANT = "BETA_CONSTANT"
VERSION = "2.0.0-beta"
CONFIG = {"source": "beta", "priority": 2}

# Additional variables unique to beta
BETA_SPECIFIC = "Only in beta module"
SETTINGS = {"mode": "beta", "debug": True}

# Private variables (shouldn't be imported with *)
_private_value = "This is private to beta"

# List of what should be imported with *
__all__ = [
    "process",
    "calculate",
    "transform",
    "analyze",
    "Helper",
    "Analyzer",
    "CONSTANT",
    "VERSION",
    "CONFIG",
    "BETA_SPECIFIC",
    "SETTINGS",
]


def get_module_info():
    """Get information about this module."""
    return {
        "name": "module_beta",
        "functions": ["process", "calculate", "transform", "analyze"],
        "classes": ["Helper", "Analyzer"],
        "constants": ["CONSTANT", "VERSION", "CONFIG", "BETA_SPECIFIC", "SETTINGS"],
    }

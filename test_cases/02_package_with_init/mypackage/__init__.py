"""
My Package - A simple Python package example.

This package demonstrates how __init__.py works to make a directory
into a Python package and control what gets imported.
"""

from .core import CONSTANT, calculate
from .helpers import format_output

# Package-level variables
__version__ = "1.0.0"
__author__ = "Quiz Creator"

# What gets imported when someone does "from mypackage import *"
__all__ = ["calculate", "format_output", "CONSTANT", "package_info"]


def package_info():
    """Return information about this package."""
    return f"Package: mypackage v{__version__} by {__author__}"

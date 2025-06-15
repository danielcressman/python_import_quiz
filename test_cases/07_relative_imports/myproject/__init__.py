"""
Main package for relative imports demonstration.

This package shows how relative imports work within a package structure.
"""

from .core import main_function
from .utils import math_utils, string_utils

__version__ = "1.0.0"
__all__ = ["main_function", "string_utils", "math_utils"]

# Package-level configuration
DEBUG = False
PACKAGE_NAME = "myproject"

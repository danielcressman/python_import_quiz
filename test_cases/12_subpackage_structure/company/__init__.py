"""
Company package - A demonstration of complex subpackage structure.

This package simulates a company's organizational structure with
different departments as subpackages, showing how to organize
and import from nested package hierarchies.
"""

from .finance import accounting, budgeting
from .hr import employee_management, payroll
from .it import security, systems

# Company-wide constants
COMPANY_NAME = "TechCorp Industries"
FOUNDED_YEAR = 2010
HEADQUARTERS = "San Francisco, CA"

# Package version
__version__ = "2.0.0"
__author__ = "Company IT Department"

# What gets imported with "from company import *"
__all__ = [
    "employee_management",
    "payroll",
    "accounting",
    "budgeting",
    "systems",
    "security",
    "get_company_info",
    "list_departments",
]


def get_company_info():
    """Get basic company information."""
    return {
        "name": COMPANY_NAME,
        "founded": FOUNDED_YEAR,
        "headquarters": HEADQUARTERS,
        "version": __version__,
        "departments": ["HR", "Finance", "IT"],
    }


def list_departments():
    """List all available departments."""
    departments = {
        "HR": {
            "modules": ["employee_management", "payroll"],
            "description": "Human Resources department",
        },
        "Finance": {
            "modules": ["accounting", "budgeting"],
            "description": "Financial operations department",
        },
        "IT": {
            "modules": ["systems", "security"],
            "description": "Information Technology department",
        },
    }
    return departments


# Company-wide utility function
def generate_employee_id(department_code, employee_number):
    """Generate a standardized employee ID."""
    return f"{COMPANY_NAME[:4].upper()}-{department_code}-{employee_number:04d}"


# Cross-department constants
STANDARD_WORK_HOURS = 40
VACATION_DAYS_PER_YEAR = 20
SICK_DAYS_PER_YEAR = 10

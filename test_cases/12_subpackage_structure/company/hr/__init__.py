"""
HR (Human Resources) subpackage for the company package.

This subpackage contains modules related to human resources management,
including employee management and payroll operations.
"""

from .employee_management import Employee, EmployeeManager, hire_employee
from .payroll import PayrollProcessor, calculate_salary, process_benefits

# HR department constants
DEPARTMENT_NAME = "Human Resources"
DEPARTMENT_CODE = "HR"
HR_EMAIL = "hr@techcorp.com"
HR_PHONE = "(555) 123-4567"

# HR policies
MIN_SALARY = 30000
MAX_SALARY = 200000
PROBATION_PERIOD_DAYS = 90
ANNUAL_REVIEW_MONTH = "January"

# What gets imported with "from company.hr import *"
__all__ = [
    "Employee",
    "EmployeeManager",
    "hire_employee",
    "PayrollProcessor",
    "calculate_salary",
    "process_benefits",
    "get_hr_info",
    "validate_employee_data",
]


def get_hr_info():
    """Get HR department information."""
    return {
        "department": DEPARTMENT_NAME,
        "code": DEPARTMENT_CODE,
        "contact": {"email": HR_EMAIL, "phone": HR_PHONE},
        "policies": {
            "min_salary": MIN_SALARY,
            "max_salary": MAX_SALARY,
            "probation_days": PROBATION_PERIOD_DAYS,
            "review_month": ANNUAL_REVIEW_MONTH,
        },
    }


def validate_employee_data(employee_data):
    """Validate employee data according to HR policies."""
    errors = []

    # Check required fields
    required_fields = ["name", "position", "salary", "start_date"]
    for field in required_fields:
        if field not in employee_data:
            errors.append(f"Missing required field: {field}")

    # Validate salary range
    if "salary" in employee_data:
        salary = employee_data["salary"]
        if salary < MIN_SALARY or salary > MAX_SALARY:
            errors.append(
                f"Salary {salary} is outside acceptable range ({MIN_SALARY}-{MAX_SALARY})"
            )

    return errors if errors else None


# HR department metadata
HR_VERSION = "1.2.0"
SUPPORTED_OPERATIONS = [
    "employee_management",
    "payroll_processing",
    "benefits_administration",
    "performance_reviews",
]

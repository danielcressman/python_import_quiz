"""
Employee management module for the HR department.

This module provides functionality for managing employees including
creating employee records, tracking employment data, and performing
basic employee operations.
"""

import datetime
from typing import Dict, List, Optional


class Employee:
    """Represents an individual employee."""

    def __init__(
        self,
        name: str,
        position: str,
        salary: float,
        start_date: str,
        employee_id: Optional[str] = None,
        department: str = "HR",
    ):
        self.name = name
        self.position = position
        self.salary = salary
        self.start_date = start_date
        self.employee_id = employee_id or self._generate_temp_id()
        self.department = department
        self.status = "Active"
        self.performance_ratings = []
        self.benefits = {}

    def _generate_temp_id(self):
        """Generate a temporary employee ID."""
        return f"TEMP-{hash(self.name) % 10000:04d}"

    def get_years_of_service(self):
        """Calculate years of service."""
        start = datetime.datetime.strptime(self.start_date, "%Y-%m-%d")
        today = datetime.datetime.now()
        return (today - start).days / 365.25

    def add_performance_rating(self, rating: float, review_date: str, notes: str = ""):
        """Add a performance rating."""
        if not 1.0 <= rating <= 5.0:
            raise ValueError("Rating must be between 1.0 and 5.0")

        self.performance_ratings.append(
            {"rating": rating, "date": review_date, "notes": notes}
        )

    def get_average_rating(self):
        """Get average performance rating."""
        if not self.performance_ratings:
            return None
        ratings = [r["rating"] for r in self.performance_ratings]
        return sum(ratings) / len(ratings)

    def update_salary(self, new_salary: float, effective_date: str):
        """Update employee salary."""
        if new_salary <= 0:
            raise ValueError("Salary must be positive")

        old_salary = self.salary
        self.salary = new_salary
        return f"Salary updated from ${old_salary:,.2f} to ${new_salary:,.2f} effective {effective_date}"

    def terminate_employment(self, termination_date: str, reason: str = ""):
        """Terminate employee."""
        self.status = "Terminated"
        self.termination_date = termination_date
        self.termination_reason = reason
        return f"Employee {self.name} terminated on {termination_date}"

    def __str__(self):
        return f"Employee({self.name}, {self.position}, ${self.salary:,.2f})"

    def __repr__(self):
        return (
            f"Employee(name='{self.name}', position='{self.position}', "
            f"salary={self.salary}, employee_id='{self.employee_id}')"
        )


class EmployeeManager:
    """Manages a collection of employees."""

    def __init__(self):
        self.employees: Dict[str, Employee] = {}
        self.next_employee_number = 1

    def add_employee(self, employee: Employee) -> str:
        """Add an employee to the system."""
        if not employee.employee_id or employee.employee_id.startswith("TEMP-"):
            # Generate proper employee ID
            from .. import generate_employee_id

            employee.employee_id = generate_employee_id("HR", self.next_employee_number)
            self.next_employee_number += 1

        if employee.employee_id in self.employees:
            raise ValueError(f"Employee ID {employee.employee_id} already exists")

        self.employees[employee.employee_id] = employee
        return employee.employee_id

    def get_employee(self, employee_id: str) -> Optional[Employee]:
        """Get an employee by ID."""
        return self.employees.get(employee_id)

    def get_employee_by_name(self, name: str) -> Optional[Employee]:
        """Get an employee by name."""
        for employee in self.employees.values():
            if employee.name.lower() == name.lower():
                return employee
        return None

    def remove_employee(self, employee_id: str) -> bool:
        """Remove an employee from the system."""
        if employee_id in self.employees:
            del self.employees[employee_id]
            return True
        return False

    def list_employees(self, status: str = "Active") -> List[Employee]:
        """List employees by status."""
        return [emp for emp in self.employees.values() if emp.status == status]

    def get_employees_by_department(self, department: str) -> List[Employee]:
        """Get employees in a specific department."""
        return [
            emp
            for emp in self.employees.values()
            if emp.department.lower() == department.lower()
        ]

    def get_salary_statistics(self) -> Dict:
        """Get salary statistics for all active employees."""
        active_employees = self.list_employees("Active")
        if not active_employees:
            return {"count": 0, "total": 0, "average": 0, "min": 0, "max": 0}

        salaries = [emp.salary for emp in active_employees]
        return {
            "count": len(salaries),
            "total": sum(salaries),
            "average": sum(salaries) / len(salaries),
            "min": min(salaries),
            "max": max(salaries),
        }

    def employees_due_for_review(self, review_month: str = "January") -> List[Employee]:
        """Get employees due for performance review."""
        # Simplified: return employees with no ratings or ratings older than 1 year
        due_for_review = []
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=365)

        for employee in self.list_employees("Active"):
            if not employee.performance_ratings:
                due_for_review.append(employee)
            else:
                last_review = max(
                    datetime.datetime.strptime(r["date"], "%Y-%m-%d")
                    for r in employee.performance_ratings
                )
                if last_review < cutoff_date:
                    due_for_review.append(employee)

        return due_for_review

    def __len__(self):
        return len(self.employees)

    def __contains__(self, employee_id):
        return employee_id in self.employees


# Module-level functions
def hire_employee(
    name: str,
    position: str,
    salary: float,
    start_date: str,
    department: str = "HR",
    manager: Optional[EmployeeManager] = None,
) -> Employee:
    """Hire a new employee and optionally add to a manager."""
    # Validate input
    if salary <= 0:
        raise ValueError("Salary must be positive")

    try:
        datetime.datetime.strptime(start_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Start date must be in YYYY-MM-DD format")

    # Create employee
    employee = Employee(name, position, salary, start_date, department=department)

    # Add to manager if provided
    if manager:
        employee_id = manager.add_employee(employee)
        employee.employee_id = employee_id

    return employee


def create_employee_report(employees: List[Employee]) -> str:
    """Create a formatted report of employees."""
    if not employees:
        return "No employees to report"

    report_lines = [
        "Employee Report",
        "=" * 50,
        f"Total Employees: {len(employees)}",
        "",
        "Employee Details:",
        "-" * 30,
    ]

    for emp in sorted(employees, key=lambda x: x.name):
        years_service = emp.get_years_of_service()
        avg_rating = emp.get_average_rating()
        rating_str = f"{avg_rating:.1f}" if avg_rating else "No ratings"

        report_lines.append(
            f"• {emp.name} ({emp.employee_id})"
            f"\n  Position: {emp.position}"
            f"\n  Salary: ${emp.salary:,.2f}"
            f"\n  Years of Service: {years_service:.1f}"
            f"\n  Average Rating: {rating_str}"
            f"\n  Status: {emp.status}"
            f"\n"
        )

    return "\n".join(report_lines)


# Module constants
MODULE_NAME = "employee_management"
SUPPORTED_EMPLOYEE_STATUSES = ["Active", "Terminated", "On Leave", "Suspended"]
MAX_EMPLOYEES_PER_MANAGER = 50

# Default employee benefits
DEFAULT_BENEFITS = {
    "health_insurance": True,
    "dental_insurance": True,
    "vision_insurance": False,
    "retirement_401k": True,
    "life_insurance": True,
}

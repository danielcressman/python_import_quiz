"""
Payroll module for the HR department.

This module provides functionality for processing payroll, calculating
salaries, managing benefits, and handling payroll-related operations.
"""

import datetime
from typing import Dict, List

# Import from parent package for company-wide constants
from .. import STANDARD_WORK_HOURS


class PayrollProcessor:
    """Handles payroll processing operations."""

    def __init__(self):
        self.pay_periods = []
        self.tax_rates = {
            "federal": 0.22,
            "state": 0.08,
            "social_security": 0.062,
            "medicare": 0.0145,
        }
        self.benefit_deductions = {
            "health_insurance": 250.00,
            "dental_insurance": 50.00,
            "vision_insurance": 25.00,
            "retirement_401k": 0.06,  # 6% of salary
            "life_insurance": 20.00,
        }

    def calculate_gross_pay(self, salary: float, pay_period: str = "biweekly") -> float:
        """Calculate gross pay for a pay period."""
        if pay_period == "weekly":
            return salary / 52
        elif pay_period == "biweekly":
            return salary / 26
        elif pay_period == "monthly":
            return salary / 12
        elif pay_period == "annual":
            return salary
        else:
            raise ValueError(f"Unsupported pay period: {pay_period}")

    def calculate_taxes(self, gross_pay: float) -> Dict[str, float]:
        """Calculate tax deductions."""
        taxes = {}
        for tax_type, rate in self.tax_rates.items():
            taxes[tax_type] = gross_pay * rate
        return taxes

    def calculate_benefit_deductions(
        self, gross_pay: float, benefits: Dict[str, bool]
    ) -> Dict[str, float]:
        """Calculate benefit deductions based on enrolled benefits."""
        deductions = {}
        for benefit, enrolled in benefits.items():
            if enrolled and benefit in self.benefit_deductions:
                deduction_amount = self.benefit_deductions[benefit]
                if benefit == "retirement_401k":
                    # 401k is percentage of gross pay
                    deductions[benefit] = gross_pay * deduction_amount
                else:
                    # Fixed amount deductions
                    deductions[benefit] = deduction_amount
        return deductions

    def process_payroll(
        self,
        employee_id: str,
        gross_pay: float,
        benefits: Dict[str, bool],
        overtime_hours: float = 0,
        overtime_rate: float = 1.5,
    ) -> Dict:
        """Process complete payroll for an employee."""
        # Calculate overtime pay
        overtime_pay = 0
        if overtime_hours > 0:
            hourly_rate = gross_pay / (STANDARD_WORK_HOURS * 2)  # biweekly
            overtime_pay = overtime_hours * hourly_rate * overtime_rate

        total_gross = gross_pay + overtime_pay

        # Calculate deductions
        taxes = self.calculate_taxes(total_gross)
        benefit_deductions = self.calculate_benefit_deductions(total_gross, benefits)

        # Calculate totals
        total_taxes = sum(taxes.values())
        total_benefits = sum(benefit_deductions.values())
        total_deductions = total_taxes + total_benefits
        net_pay = total_gross - total_deductions

        return {
            "employee_id": employee_id,
            "pay_period": datetime.datetime.now().strftime("%Y-%m-%d"),
            "gross_pay": {
                "regular": gross_pay,
                "overtime": overtime_pay,
                "total": total_gross,
            },
            "deductions": {
                "taxes": taxes,
                "benefits": benefit_deductions,
                "total_taxes": total_taxes,
                "total_benefits": total_benefits,
                "total_deductions": total_deductions,
            },
            "net_pay": net_pay,
        }

    def generate_paystub(self, payroll_data: Dict) -> str:
        """Generate a formatted paystub."""
        lines = [
            "=" * 50,
            "PAYSTUB",
            "=" * 50,
            f"Employee ID: {payroll_data['employee_id']}",
            f"Pay Period: {payroll_data['pay_period']}",
            "",
            "EARNINGS:",
            "-" * 20,
            f"Regular Pay:      ${payroll_data['gross_pay']['regular']:>10.2f}",
            f"Overtime Pay:     ${payroll_data['gross_pay']['overtime']:>10.2f}",
            f"Gross Total:      ${payroll_data['gross_pay']['total']:>10.2f}",
            "",
            "DEDUCTIONS:",
            "-" * 20,
        ]

        # Add tax deductions
        for tax_type, amount in payroll_data["deductions"]["taxes"].items():
            tax_name = tax_type.replace("_", " ").title()
            lines.append(f"{tax_name:<15}: ${amount:>10.2f}")

        lines.append("")

        # Add benefit deductions
        for benefit, amount in payroll_data["deductions"]["benefits"].items():
            benefit_name = benefit.replace("_", " ").title()
            lines.append(f"{benefit_name:<15}: ${amount:>10.2f}")

        lines.extend(
            [
                "",
                f"Total Deductions: ${payroll_data['deductions']['total_deductions']:>10.2f}",
                "=" * 50,
                f"NET PAY:          ${payroll_data['net_pay']:>10.2f}",
                "=" * 50,
            ]
        )

        return "\n".join(lines)


# Module-level functions
def calculate_salary(
    hourly_rate: float, hours_per_week: float = STANDARD_WORK_HOURS
) -> float:
    """Calculate annual salary from hourly rate."""
    if hourly_rate <= 0:
        raise ValueError("Hourly rate must be positive")
    if hours_per_week <= 0 or hours_per_week > 80:
        raise ValueError("Hours per week must be between 1 and 80")

    return hourly_rate * hours_per_week * 52


def calculate_hourly_rate(
    annual_salary: float, hours_per_week: float = STANDARD_WORK_HOURS
) -> float:
    """Calculate hourly rate from annual salary."""
    if annual_salary <= 0:
        raise ValueError("Annual salary must be positive")
    if hours_per_week <= 0:
        raise ValueError("Hours per week must be positive")

    return annual_salary / (hours_per_week * 52)


def process_benefits(employee_benefits: Dict[str, bool]) -> Dict:
    """Process and validate employee benefits."""
    valid_benefits = [
        "health_insurance",
        "dental_insurance",
        "vision_insurance",
        "retirement_401k",
        "life_insurance",
    ]

    processed_benefits = {}
    invalid_benefits = []

    for benefit, enrolled in employee_benefits.items():
        if benefit in valid_benefits:
            processed_benefits[benefit] = enrolled
        else:
            invalid_benefits.append(benefit)

    # Add default benefits if not specified
    for benefit in valid_benefits:
        if benefit not in processed_benefits:
            processed_benefits[benefit] = False

    result = {"benefits": processed_benefits}
    if invalid_benefits:
        result["warnings"] = f"Invalid benefits ignored: {invalid_benefits}"

    return result


def calculate_pto_accrual(
    years_of_service: float, accrual_rate: float = 3.08
) -> Dict[str, float]:
    """Calculate PTO (Paid Time Off) accrual."""
    # Base accrual rate (hours per pay period)
    base_rate = accrual_rate

    # Increase rate based on years of service
    if years_of_service >= 10:
        multiplier = 1.5
    elif years_of_service >= 5:
        multiplier = 1.25
    elif years_of_service >= 2:
        multiplier = 1.1
    else:
        multiplier = 1.0

    adjusted_rate = base_rate * multiplier
    annual_accrual = adjusted_rate * 26  # 26 pay periods per year
    max_accrual = 240  # Maximum 240 hours (6 weeks)

    return {
        "hours_per_pay_period": adjusted_rate,
        "annual_accrual_hours": min(annual_accrual, max_accrual),
        "years_of_service": years_of_service,
        "multiplier": multiplier,
    }


def validate_payroll_data(payroll_data: Dict) -> List[str]:
    """Validate payroll data for completeness and accuracy."""
    errors = []

    # Required fields
    if "employee_id" not in payroll_data:
        errors.append("Missing employee_id")

    if "gross_pay" not in payroll_data:
        errors.append("Missing gross_pay")
    elif payroll_data.get("gross_pay", 0) <= 0:
        errors.append("Gross pay must be positive")

    # Validate net pay calculation
    if "net_pay" in payroll_data and "gross_pay" in payroll_data:
        gross = payroll_data["gross_pay"]
        net = payroll_data["net_pay"]
        deductions = payroll_data.get("deductions", {}).get("total_deductions", 0)

        if abs((gross - deductions) - net) > 0.01:  # Allow for rounding
            errors.append(
                "Net pay calculation doesn't match gross pay minus deductions"
            )

    return errors


# Payroll reporting functions
def generate_payroll_summary(payroll_records: List[Dict]) -> Dict:
    """Generate a summary of payroll records."""
    if not payroll_records:
        return {"error": "No payroll records provided"}

    total_gross = sum(
        record.get("gross_pay", {}).get("total", 0) for record in payroll_records
    )
    total_net = sum(record.get("net_pay", 0) for record in payroll_records)
    total_taxes = sum(
        record.get("deductions", {}).get("total_taxes", 0) for record in payroll_records
    )
    total_benefits = sum(
        record.get("deductions", {}).get("total_benefits", 0)
        for record in payroll_records
    )

    return {
        "period": datetime.datetime.now().strftime("%Y-%m"),
        "employee_count": len(payroll_records),
        "totals": {
            "gross_pay": total_gross,
            "net_pay": total_net,
            "taxes": total_taxes,
            "benefits": total_benefits,
            "total_deductions": total_taxes + total_benefits,
        },
        "averages": {
            "gross_pay": total_gross / len(payroll_records),
            "net_pay": total_net / len(payroll_records),
        },
    }


# Module constants
MODULE_NAME = "payroll"
SUPPORTED_PAY_PERIODS = ["weekly", "biweekly", "monthly", "annual"]
DEFAULT_TAX_YEAR = datetime.datetime.now().year
MINIMUM_WAGE = 15.00  # Federal minimum wage

# Payroll processing constants
MAX_OVERTIME_HOURS_PER_WEEK = 20
STANDARD_OVERTIME_RATE = 1.5
DOUBLE_TIME_RATE = 2.0

"""
Finance subpackage for the company package.

This subpackage contains modules related to financial operations,
including accounting and budgeting functionality.
"""

from .accounting import AccountManager, Transaction, generate_financial_report
from .budgeting import Budget, BudgetManager, create_budget_plan

# Finance department constants
DEPARTMENT_NAME = "Finance"
DEPARTMENT_CODE = "FIN"
FINANCE_EMAIL = "finance@techcorp.com"
FINANCE_PHONE = "(555) 234-5678"

# Financial constants
FISCAL_YEAR_START = "January"
CURRENCY = "USD"
DEFAULT_BUDGET_CYCLE = "annual"
TAX_RATE = 0.21  # Corporate tax rate

# Account types
ACCOUNT_TYPES = ["assets", "liabilities", "equity", "revenue", "expenses"]

# What gets imported with "from company.finance import *"
__all__ = [
    "AccountManager",
    "Transaction",
    "generate_financial_report",
    "Budget",
    "BudgetManager",
    "create_budget_plan",
    "get_finance_info",
    "validate_transaction",
]


def get_finance_info():
    """Get Finance department information."""
    return {
        "department": DEPARTMENT_NAME,
        "code": DEPARTMENT_CODE,
        "contact": {"email": FINANCE_EMAIL, "phone": FINANCE_PHONE},
        "settings": {
            "fiscal_year_start": FISCAL_YEAR_START,
            "currency": CURRENCY,
            "tax_rate": TAX_RATE,
            "budget_cycle": DEFAULT_BUDGET_CYCLE,
        },
        "account_types": ACCOUNT_TYPES,
    }


def validate_transaction(transaction_data):
    """Validate transaction data according to finance policies."""
    errors = []

    # Check required fields
    required_fields = ["amount", "account", "description", "date"]
    for field in required_fields:
        if field not in transaction_data:
            errors.append(f"Missing required field: {field}")

    # Validate amount
    if "amount" in transaction_data:
        amount = transaction_data["amount"]
        if not isinstance(amount, (int, float)) or amount == 0:
            errors.append("Amount must be a non-zero number")

    # Validate account type
    if "account" in transaction_data:
        account = transaction_data["account"]
        if account not in ACCOUNT_TYPES:
            errors.append(f"Invalid account type. Must be one of: {ACCOUNT_TYPES}")

    return errors if errors else None


# Finance department metadata
FINANCE_VERSION = "2.1.0"
SUPPORTED_OPERATIONS = [
    "accounting",
    "budgeting",
    "financial_reporting",
    "expense_tracking",
    "revenue_management",
]

# Compliance and audit settings
AUDIT_TRAIL_ENABLED = True
FINANCIAL_CONTROLS = {
    "dual_approval_threshold": 10000,
    "expense_limit_per_department": 50000,
    "quarterly_review_required": True,
}

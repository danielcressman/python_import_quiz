"""
Accounting module for the Finance department.

This module provides functionality for managing financial accounts,
processing transactions, and generating financial reports.
"""

import datetime
from typing import Dict, List, Optional, Union


class Transaction:
    """Represents a financial transaction."""

    def __init__(
        self,
        amount: float,
        account: str,
        description: str,
        date: str,
        transaction_type: str = "expense",
        reference_id: Optional[str] = None,
    ):
        self.amount = amount
        self.account = account
        self.description = description
        self.date = date
        self.transaction_type = transaction_type
        self.reference_id = reference_id or self._generate_reference_id()
        self.created_at = datetime.datetime.now().isoformat()
        self.status = "pending"

    def _generate_reference_id(self) -> str:
        """Generate a unique reference ID for the transaction."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        return f"TXN-{timestamp}-{hash(self.description) % 1000:03d}"

    def approve(self) -> str:
        """Approve the transaction."""
        self.status = "approved"
        return f"Transaction {self.reference_id} approved"

    def reject(self, reason: str = "") -> str:
        """Reject the transaction."""
        self.status = "rejected"
        self.rejection_reason = reason
        return f"Transaction {self.reference_id} rejected: {reason}"

    def is_debit(self) -> bool:
        """Check if transaction is a debit (increases expenses/assets)."""
        return self.transaction_type in ["expense", "asset_increase"]

    def is_credit(self) -> bool:
        """Check if transaction is a credit (increases revenue/liabilities)."""
        return self.transaction_type in ["revenue", "liability_increase"]

    def __str__(self):
        return f"Transaction({self.amount}, {self.account}, {self.description})"

    def __repr__(self):
        return (
            f"Transaction(amount={self.amount}, account='{self.account}', "
            f"description='{self.description}', date='{self.date}')"
        )


class Account:
    """Represents a financial account."""

    def __init__(self, name: str, account_type: str, initial_balance: float = 0.0):
        self.name = name
        self.account_type = account_type
        self.balance = initial_balance
        self.transactions: List[Transaction] = []
        self.created_date = datetime.datetime.now().strftime("%Y-%m-%d")

    def add_transaction(self, transaction: Transaction) -> None:
        """Add a transaction to this account."""
        self.transactions.append(transaction)

        # Update balance based on account type and transaction type
        if self.account_type in ["assets", "expenses"]:
            # Debit increases assets and expenses
            if transaction.is_debit():
                self.balance += transaction.amount
            else:
                self.balance -= transaction.amount
        else:
            # Credit increases liabilities, equity, and revenue
            if transaction.is_credit():
                self.balance += transaction.amount
            else:
                self.balance -= transaction.amount

    def get_balance(self) -> float:
        """Get current account balance."""
        return self.balance

    def get_transaction_history(self) -> List[Transaction]:
        """Get all transactions for this account."""
        return sorted(self.transactions, key=lambda t: t.date, reverse=True)

    def get_transactions_by_date_range(
        self, start_date: str, end_date: str
    ) -> List[Transaction]:
        """Get transactions within a date range."""
        return [t for t in self.transactions if start_date <= t.date <= end_date]

    def __str__(self):
        return f"Account({self.name}, {self.account_type}, ${self.balance:.2f})"


class AccountManager:
    """Manages financial accounts and transactions."""

    def __init__(self):
        self.accounts: Dict[str, Account] = {}
        self.transaction_log: List[Transaction] = []

    def create_account(
        self, name: str, account_type: str, initial_balance: float = 0.0
    ) -> Account:
        """Create a new financial account."""
        if name in self.accounts:
            raise ValueError(f"Account '{name}' already exists")

        valid_types = ["assets", "liabilities", "equity", "revenue", "expenses"]
        if account_type not in valid_types:
            raise ValueError(f"Invalid account type. Must be one of: {valid_types}")

        account = Account(name, account_type, initial_balance)
        self.accounts[name] = account
        return account

    def get_account(self, name: str) -> Optional[Account]:
        """Get an account by name."""
        return self.accounts.get(name)

    def list_accounts(self, account_type: Optional[str] = None) -> List[Account]:
        """List all accounts, optionally filtered by type."""
        if account_type:
            return [
                acc
                for acc in self.accounts.values()
                if acc.account_type == account_type
            ]
        return list(self.accounts.values())

    def record_transaction(self, transaction: Transaction) -> str:
        """Record a transaction and update the appropriate account."""
        # Validate account exists
        if transaction.account not in self.accounts:
            raise ValueError(f"Account '{transaction.account}' does not exist")

        # Add to account
        account = self.accounts[transaction.account]
        account.add_transaction(transaction)

        # Add to transaction log
        self.transaction_log.append(transaction)

        return f"Transaction recorded: {transaction.reference_id}"

    def transfer_funds(
        self, from_account: str, to_account: str, amount: float, description: str
    ) -> List[str]:
        """Transfer funds between accounts."""
        if from_account not in self.accounts:
            raise ValueError(f"Source account '{from_account}' does not exist")
        if to_account not in self.accounts:
            raise ValueError(f"Destination account '{to_account}' does not exist")
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")

        date = datetime.datetime.now().strftime("%Y-%m-%d")

        # Create debit transaction (decrease source account)
        debit_txn = Transaction(
            amount=amount,
            account=from_account,
            description=f"Transfer to {to_account}: {description}",
            date=date,
            transaction_type="expense",
        )

        # Create credit transaction (increase destination account)
        credit_txn = Transaction(
            amount=amount,
            account=to_account,
            description=f"Transfer from {from_account}: {description}",
            date=date,
            transaction_type="revenue",
        )

        # Record both transactions
        results = []
        results.append(self.record_transaction(debit_txn))
        results.append(self.record_transaction(credit_txn))

        return results

    def get_trial_balance(self) -> Dict[str, float]:
        """Generate trial balance showing all account balances."""
        trial_balance = {}
        for account_name, account in self.accounts.items():
            trial_balance[account_name] = account.get_balance()
        return trial_balance

    def get_balance_sheet(self) -> Dict[str, Dict[str, float]]:
        """Generate a basic balance sheet."""
        balance_sheet = {"assets": {}, "liabilities": {}, "equity": {}}

        for account in self.accounts.values():
            if account.account_type in balance_sheet:
                balance_sheet[account.account_type][account.name] = account.balance

        # Calculate totals
        balance_sheet["totals"] = {
            "total_assets": sum(balance_sheet["assets"].values()),
            "total_liabilities": sum(balance_sheet["liabilities"].values()),
            "total_equity": sum(balance_sheet["equity"].values()),
        }

        return balance_sheet

    def get_income_statement(
        self, start_date: str, end_date: str
    ) -> Dict[str, Union[Dict, float]]:
        """Generate income statement for a date range."""
        revenue_total = 0
        expense_total = 0
        revenue_details = {}
        expense_details = {}

        for account in self.accounts.values():
            transactions = account.get_transactions_by_date_range(start_date, end_date)

            if account.account_type == "revenue":
                account_revenue = sum(t.amount for t in transactions if t.is_credit())
                if account_revenue > 0:
                    revenue_details[account.name] = account_revenue
                    revenue_total += account_revenue

            elif account.account_type == "expenses":
                account_expenses = sum(t.amount for t in transactions if t.is_debit())
                if account_expenses > 0:
                    expense_details[account.name] = account_expenses
                    expense_total += account_expenses

        net_income = revenue_total - expense_total

        return {
            "period": f"{start_date} to {end_date}",
            "revenue": revenue_details,
            "expenses": expense_details,
            "totals": {
                "total_revenue": revenue_total,
                "total_expenses": expense_total,
                "net_income": net_income,
            },
        }


# Module-level functions
def generate_financial_report(
    account_manager: AccountManager, report_type: str = "summary"
) -> str:
    """Generate a formatted financial report."""
    if report_type == "summary":
        return _generate_summary_report(account_manager)
    elif report_type == "balance_sheet":
        return _generate_balance_sheet_report(account_manager)
    elif report_type == "trial_balance":
        return _generate_trial_balance_report(account_manager)
    else:
        raise ValueError(f"Unsupported report type: {report_type}")


def _generate_summary_report(account_manager: AccountManager) -> str:
    """Generate a summary financial report."""
    lines = [
        "FINANCIAL SUMMARY REPORT",
        "=" * 50,
        f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "ACCOUNT OVERVIEW:",
        "-" * 30,
    ]

    for account_type in ["assets", "liabilities", "equity", "revenue", "expenses"]:
        accounts = account_manager.list_accounts(account_type)
        if accounts:
            lines.append(f"\n{account_type.upper()}:")
            total = 0
            for account in accounts:
                lines.append(f"  {account.name:<25} ${account.balance:>12,.2f}")
                total += account.balance
            lines.append(f"  {'TOTAL ' + account_type.upper():<25} ${total:>12,.2f}")

    lines.extend(
        [
            "",
            f"Total Transactions: {len(account_manager.transaction_log)}",
            f"Total Accounts: {len(account_manager.accounts)}",
            "=" * 50,
        ]
    )

    return "\n".join(lines)


def _generate_balance_sheet_report(account_manager: AccountManager) -> str:
    """Generate a balance sheet report."""
    balance_sheet = account_manager.get_balance_sheet()

    lines = [
        "BALANCE SHEET",
        "=" * 50,
        f"As of: {datetime.datetime.now().strftime('%Y-%m-%d')}",
        "",
        "ASSETS:",
        "-" * 20,
    ]

    for asset, amount in balance_sheet["assets"].items():
        lines.append(f"{asset:<30} ${amount:>12,.2f}")

    lines.extend(
        [
            f"{'TOTAL ASSETS':<30} ${balance_sheet['totals']['total_assets']:>12,.2f}",
            "",
            "LIABILITIES:",
            "-" * 20,
        ]
    )

    for liability, amount in balance_sheet["liabilities"].items():
        lines.append(f"{liability:<30} ${amount:>12,.2f}")

    lines.extend(
        [
            f"{'TOTAL LIABILITIES':<30} ${balance_sheet['totals']['total_liabilities']:>12,.2f}",
            "",
            "EQUITY:",
            "-" * 20,
        ]
    )

    for equity, amount in balance_sheet["equity"].items():
        lines.append(f"{equity:<30} ${amount:>12,.2f}")

    lines.extend(
        [
            f"{'TOTAL EQUITY':<30} ${balance_sheet['totals']['total_equity']:>12,.2f}",
            "=" * 50,
            f"{'TOTAL LIAB. + EQUITY':<30} ${balance_sheet['totals']['total_liabilities'] + balance_sheet['totals']['total_equity']:>12,.2f}",
        ]
    )

    return "\n".join(lines)


def _generate_trial_balance_report(account_manager: AccountManager) -> str:
    """Generate a trial balance report."""
    trial_balance = account_manager.get_trial_balance()

    lines = [
        "TRIAL BALANCE",
        "=" * 50,
        f"As of: {datetime.datetime.now().strftime('%Y-%m-%d')}",
        "",
        f"{'ACCOUNT NAME':<30} {'DEBIT':<15} {'CREDIT':<15}",
        "-" * 60,
    ]

    total_debits = 0
    total_credits = 0

    for account_name, balance in trial_balance.items():
        account = account_manager.get_account(account_name)
        if account.account_type in ["assets", "expenses"]:
            # Normal debit balance accounts
            if balance >= 0:
                lines.append(f"{account_name:<30} ${balance:<14,.2f}")
                total_debits += balance
            else:
                lines.append(f"{account_name:<30} {'':15} ${abs(balance):<14,.2f}")
                total_credits += abs(balance)
        else:
            # Normal credit balance accounts
            if balance >= 0:
                lines.append(f"{account_name:<30} {'':15} ${balance:<14,.2f}")
                total_credits += balance
            else:
                lines.append(f"{account_name:<30} ${abs(balance):<14,.2f}")
                total_debits += abs(balance)

    lines.extend(
        [
            "-" * 60,
            f"{'TOTALS:':<30} ${total_debits:<14,.2f} ${total_credits:<14,.2f}",
            "",
            f"Difference: ${abs(total_debits - total_credits):.2f}",
            "=" * 50,
        ]
    )

    return "\n".join(lines)


# Module constants
MODULE_NAME = "accounting"
SUPPORTED_ACCOUNT_TYPES = ["assets", "liabilities", "equity", "revenue", "expenses"]
TRANSACTION_STATUSES = ["pending", "approved", "rejected"]

# Default chart of accounts
DEFAULT_ACCOUNTS = {
    "Cash": "assets",
    "Accounts Receivable": "assets",
    "Equipment": "assets",
    "Accounts Payable": "liabilities",
    "Notes Payable": "liabilities",
    "Owner's Equity": "equity",
    "Service Revenue": "revenue",
    "Office Expenses": "expenses",
    "Utilities Expense": "expenses",
}

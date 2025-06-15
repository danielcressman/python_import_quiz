"""
Budgeting module for the Finance department.

This module provides functionality for creating and managing budgets,
tracking budget performance, and generating budget reports.
"""

import datetime
from typing import Dict, List, Optional


class Budget:
    """Represents a financial budget."""

    def __init__(
        self,
        name: str,
        period: str,
        start_date: str,
        end_date: str,
        total_amount: float,
    ):
        self.name = name
        self.period = period  # monthly, quarterly, annual
        self.start_date = start_date
        self.end_date = end_date
        self.total_amount = total_amount
        self.categories: Dict[str, float] = {}
        self.actual_spending: Dict[str, float] = {}
        self.created_date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.status = "draft"

    def add_category(self, category: str, amount: float) -> str:
        """Add a budget category with allocated amount."""
        if amount <= 0:
            raise ValueError("Budget amount must be positive")

        self.categories[category] = amount
        self.actual_spending[category] = 0.0
        return f"Added category '{category}' with budget ${amount:,.2f}"

    def update_category(self, category: str, new_amount: float) -> str:
        """Update the budget amount for a category."""
        if category not in self.categories:
            raise ValueError(f"Category '{category}' does not exist")
        if new_amount <= 0:
            raise ValueError("Budget amount must be positive")

        old_amount = self.categories[category]
        self.categories[category] = new_amount
        return (
            f"Updated '{category}' budget from ${old_amount:,.2f} to ${new_amount:,.2f}"
        )

    def record_expense(
        self, category: str, amount: float, description: str = ""
    ) -> str:
        """Record an actual expense against a budget category."""
        if category not in self.categories:
            raise ValueError(f"Category '{category}' does not exist in budget")
        if amount <= 0:
            raise ValueError("Expense amount must be positive")

        self.actual_spending[category] += amount
        return f"Recorded ${amount:,.2f} expense for '{category}': {description}"

    def get_category_status(self, category: str) -> Dict:
        """Get status information for a specific category."""
        if category not in self.categories:
            raise ValueError(f"Category '{category}' does not exist")

        budgeted = self.categories[category]
        spent = self.actual_spending[category]
        remaining = budgeted - spent
        percent_used = (spent / budgeted) * 100 if budgeted > 0 else 0

        return {
            "category": category,
            "budgeted": budgeted,
            "spent": spent,
            "remaining": remaining,
            "percent_used": percent_used,
            "over_budget": spent > budgeted,
        }

    def get_budget_summary(self) -> Dict:
        """Get overall budget summary."""
        total_budgeted = sum(self.categories.values())
        total_spent = sum(self.actual_spending.values())
        total_remaining = total_budgeted - total_spent
        percent_used = (total_spent / total_budgeted) * 100 if total_budgeted > 0 else 0

        over_budget_categories = [
            cat
            for cat in self.categories
            if self.actual_spending[cat] > self.categories[cat]
        ]

        return {
            "name": self.name,
            "period": self.period,
            "date_range": f"{self.start_date} to {self.end_date}",
            "totals": {
                "budgeted": total_budgeted,
                "spent": total_spent,
                "remaining": total_remaining,
                "percent_used": percent_used,
            },
            "categories_count": len(self.categories),
            "over_budget_categories": over_budget_categories,
            "status": self.status,
        }

    def approve(self) -> str:
        """Approve the budget."""
        self.status = "approved"
        return f"Budget '{self.name}' approved"

    def freeze(self) -> str:
        """Freeze the budget (no more changes allowed)."""
        self.status = "frozen"
        return f"Budget '{self.name}' frozen"

    def __str__(self):
        return f"Budget({self.name}, {self.period}, ${self.total_amount:,.2f})"


class BudgetManager:
    """Manages multiple budgets and budget operations."""

    def __init__(self):
        self.budgets: Dict[str, Budget] = {}
        self.budget_templates: Dict[str, Dict] = {}

    def create_budget(
        self,
        name: str,
        period: str,
        start_date: str,
        end_date: str,
        total_amount: float,
    ) -> Budget:
        """Create a new budget."""
        if name in self.budgets:
            raise ValueError(f"Budget '{name}' already exists")

        valid_periods = ["monthly", "quarterly", "annual"]
        if period not in valid_periods:
            raise ValueError(f"Invalid period. Must be one of: {valid_periods}")

        budget = Budget(name, period, start_date, end_date, total_amount)
        self.budgets[name] = budget
        return budget

    def get_budget(self, name: str) -> Optional[Budget]:
        """Get a budget by name."""
        return self.budgets.get(name)

    def list_budgets(self, status: Optional[str] = None) -> List[Budget]:
        """List budgets, optionally filtered by status."""
        if status:
            return [b for b in self.budgets.values() if b.status == status]
        return list(self.budgets.values())

    def delete_budget(self, name: str) -> bool:
        """Delete a budget."""
        if name in self.budgets:
            del self.budgets[name]
            return True
        return False

    def copy_budget(self, source_name: str, new_name: str, new_dates: Dict) -> Budget:
        """Copy an existing budget with new dates."""
        if source_name not in self.budgets:
            raise ValueError(f"Source budget '{source_name}' does not exist")
        if new_name in self.budgets:
            raise ValueError(f"Budget '{new_name}' already exists")

        source_budget = self.budgets[source_name]
        new_budget = Budget(
            new_name,
            source_budget.period,
            new_dates["start_date"],
            new_dates["end_date"],
            source_budget.total_amount,
        )

        # Copy categories
        for category, amount in source_budget.categories.items():
            new_budget.add_category(category, amount)

        self.budgets[new_name] = new_budget
        return new_budget

    def compare_budgets(self, budget1_name: str, budget2_name: str) -> Dict:
        """Compare two budgets."""
        if budget1_name not in self.budgets:
            raise ValueError(f"Budget '{budget1_name}' does not exist")
        if budget2_name not in self.budgets:
            raise ValueError(f"Budget '{budget2_name}' does not exist")

        budget1 = self.budgets[budget1_name]
        budget2 = self.budgets[budget2_name]

        comparison = {
            "budget1": budget1.get_budget_summary(),
            "budget2": budget2.get_budget_summary(),
            "differences": {},
        }

        # Compare categories
        all_categories = set(budget1.categories.keys()) | set(budget2.categories.keys())
        for category in all_categories:
            amount1 = budget1.categories.get(category, 0)
            amount2 = budget2.categories.get(category, 0)
            difference = amount2 - amount1

            comparison["differences"][category] = {
                "budget1_amount": amount1,
                "budget2_amount": amount2,
                "difference": difference,
                "percent_change": (difference / amount1 * 100)
                if amount1 != 0
                else float("inf"),
            }

        return comparison

    def create_template(self, name: str, categories: Dict[str, float]) -> str:
        """Create a budget template."""
        self.budget_templates[name] = categories
        return f"Created budget template '{name}' with {len(categories)} categories"

    def create_budget_from_template(
        self,
        template_name: str,
        budget_name: str,
        period: str,
        start_date: str,
        end_date: str,
        total_amount: float,
    ) -> Budget:
        """Create a new budget from a template."""
        if template_name not in self.budget_templates:
            raise ValueError(f"Template '{template_name}' does not exist")

        budget = self.create_budget(
            budget_name, period, start_date, end_date, total_amount
        )

        # Add categories from template
        template = self.budget_templates[template_name]
        for category, amount in template.items():
            budget.add_category(category, amount)

        return budget

    def get_consolidated_report(self) -> Dict:
        """Get a consolidated report of all budgets."""
        if not self.budgets:
            return {"error": "No budgets found"}

        total_budgeted = 0
        total_spent = 0
        budget_summaries = []

        for budget in self.budgets.values():
            summary = budget.get_budget_summary()
            budget_summaries.append(summary)
            total_budgeted += summary["totals"]["budgeted"]
            total_spent += summary["totals"]["spent"]

        return {
            "consolidated_totals": {
                "total_budgeted": total_budgeted,
                "total_spent": total_spent,
                "total_remaining": total_budgeted - total_spent,
                "overall_percent_used": (total_spent / total_budgeted * 100)
                if total_budgeted > 0
                else 0,
            },
            "budget_count": len(self.budgets),
            "individual_budgets": budget_summaries,
            "generated_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }


# Module-level functions
def create_budget_plan(
    name: str,
    total_amount: float,
    categories: Dict[str, float],
    period: str = "annual",
    start_date: Optional[str] = None,
) -> Budget:
    """Create a complete budget plan with categories."""
    if start_date is None:
        start_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Calculate end date based on period
    start_dt = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    if period == "monthly":
        end_dt = start_dt + datetime.timedelta(days=30)
    elif period == "quarterly":
        end_dt = start_dt + datetime.timedelta(days=90)
    else:  # annual
        end_dt = start_dt + datetime.timedelta(days=365)

    end_date = end_dt.strftime("%Y-%m-%d")

    # Create budget
    budget = Budget(name, period, start_date, end_date, total_amount)

    # Add categories
    for category, amount in categories.items():
        budget.add_category(category, amount)

    return budget


def analyze_budget_performance(budget: Budget) -> Dict:
    """Analyze budget performance and provide insights."""
    summary = budget.get_budget_summary()
    categories_analysis = []

    for category in budget.categories:
        status = budget.get_category_status(category)

        # Determine performance level
        if status["percent_used"] <= 50:
            performance = "under_utilized"
        elif status["percent_used"] <= 90:
            performance = "on_track"
        elif status["percent_used"] <= 100:
            performance = "near_limit"
        else:
            performance = "over_budget"

        categories_analysis.append(
            {
                "category": category,
                "performance": performance,
                "status": status,
            }
        )

    # Overall performance assessment
    overall_percent = summary["totals"]["percent_used"]
    if overall_percent <= 75:
        overall_performance = "conservative"
    elif overall_percent <= 95:
        overall_performance = "balanced"
    elif overall_percent <= 100:
        overall_performance = "aggressive"
    else:
        overall_performance = "over_budget"

    return {
        "budget_name": budget.name,
        "overall_performance": overall_performance,
        "categories_analysis": categories_analysis,
        "recommendations": _generate_budget_recommendations(
            budget, categories_analysis
        ),
        "analysis_date": datetime.datetime.now().strftime("%Y-%m-%d"),
    }


def _generate_budget_recommendations(
    budget: Budget, categories_analysis: List[Dict]
) -> List[str]:
    """Generate budget recommendations based on analysis."""
    recommendations = []

    # Check for over-budget categories
    over_budget = [c for c in categories_analysis if c["performance"] == "over_budget"]
    if over_budget:
        recommendations.append(
            f"Review spending in {len(over_budget)} over-budget categories: "
            f"{', '.join([c['category'] for c in over_budget])}"
        )

    # Check for under-utilized categories
    under_utilized = [
        c for c in categories_analysis if c["performance"] == "under_utilized"
    ]
    if (
        len(under_utilized) > len(budget.categories) * 0.3
    ):  # More than 30% under-utilized
        recommendations.append(
            "Consider reallocating funds from under-utilized categories to areas with higher demand"
        )

    # Overall budget health
    summary = budget.get_budget_summary()
    if summary["totals"]["percent_used"] > 90:
        recommendations.append(
            "Budget utilization is high - monitor remaining spending carefully"
        )
    elif summary["totals"]["percent_used"] < 50:
        recommendations.append(
            "Budget utilization is low - consider if allocations match actual needs"
        )

    if not recommendations:
        recommendations.append("Budget performance is within acceptable parameters")

    return recommendations


def generate_budget_forecast(budget: Budget, months_ahead: int = 3) -> Dict:
    """Generate budget forecast based on current spending patterns."""
    if not budget.actual_spending:
        return {"error": "No spending data available for forecasting"}

    # Calculate average monthly spending rate
    days_elapsed = (
        datetime.datetime.now()
        - datetime.datetime.strptime(budget.start_date, "%Y-%m-%d")
    ).days

    if days_elapsed <= 0:
        return {"error": "Budget has not started yet"}

    monthly_rates = {}
    for category, spent in budget.actual_spending.items():
        monthly_rates[category] = (spent / days_elapsed) * 30  # Convert to monthly rate

    # Project future spending
    forecast = {}
    for category, monthly_rate in monthly_rates.items():
        projected_spending = monthly_rate * months_ahead
        budget_remaining = (
            budget.categories[category] - budget.actual_spending[category]
        )

        forecast[category] = {
            "current_monthly_rate": monthly_rate,
            "projected_spending": projected_spending,
            "budget_remaining": budget_remaining,
            "will_exceed_budget": projected_spending > budget_remaining,
            "months_until_exhausted": budget_remaining / monthly_rate
            if monthly_rate > 0
            else float("inf"),
        }

    return {
        "budget_name": budget.name,
        "forecast_period_months": months_ahead,
        "forecast_date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "categories_forecast": forecast,
    }


# Module constants
MODULE_NAME = "budgeting"
SUPPORTED_PERIODS = ["monthly", "quarterly", "annual"]
BUDGET_STATUSES = ["draft", "approved", "frozen", "archived"]

# Default budget templates
DEFAULT_TEMPLATES = {
    "department_budget": {
        "Personnel": 60000,
        "Equipment": 15000,
        "Supplies": 5000,
        "Travel": 3000,
        "Training": 2000,
    },
    "project_budget": {
        "Development": 50000,
        "Testing": 15000,
        "Documentation": 5000,
        "Deployment": 10000,
        "Contingency": 5000,
    },
    "marketing_budget": {
        "Advertising": 25000,
        "Events": 15000,
        "Content Creation": 8000,
        "Tools & Software": 3000,
        "Research": 4000,
    },
}

# Budget analysis thresholds
PERFORMANCE_THRESHOLDS = {
    "under_utilized": 50,
    "on_track": 90,
    "near_limit": 100,
}

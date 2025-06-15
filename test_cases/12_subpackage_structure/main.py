#!/usr/bin/env python3
"""
Test script for complex subpackage structure demonstration.

This script tests importing from a complex package hierarchy with multiple
nested subpackages (company.hr, company.finance, company.it) and demonstrates
how Python handles imports across deep package structures.
"""

# Import the main company package
import company

# Import specific subpackages
from company import finance, hr, it

# Import specific modules from subpackages
from company.finance import accounting, budgeting

# Import specific classes and functions
from company.finance.accounting import AccountManager, Transaction
from company.hr import payroll
from company.hr.employee_management import Employee, EmployeeManager
from company.it import security, systems
from company.it.security import SecurityManager


def main():
    print("Testing complex subpackage structure...")
    print("=" * 60)

    # Test main package information
    print("1. Main Company Package:")
    company_info = company.get_company_info()
    print(f"   Company: {company_info['name']}")
    print(f"   Founded: {company_info['founded']}")
    print(f"   Version: {company_info['version']}")
    print(f"   Departments: {', '.join(company_info['departments'])}")
    print()

    # Test HR department
    print("2. HR Department Operations:")
    print("-" * 30)

    # Create employee manager
    emp_manager = EmployeeManager()

    # Create employees
    try:
        emp1 = Employee("Alice Johnson", "Software Engineer", 75000, "2024-01-15")
        emp2 = Employee("Bob Smith", "HR Manager", 85000, "2023-06-01")

        # Add employees to manager
        emp1_id = emp_manager.add_employee(emp1)
        emp2_id = emp_manager.add_employee(emp2)

        print(f"   Created employee: {emp1.name} (ID: {emp1_id})")
        print(f"   Created employee: {emp2.name} (ID: {emp2_id})")

        # Test payroll processing
        processor = payroll.PayrollProcessor()

        # Process payroll for Alice
        alice_benefits = {
            "health_insurance": True,
            "dental_insurance": True,
            "vision_insurance": False,
            "retirement_401k": True,
            "life_insurance": True,
        }

        alice_payroll = processor.process_payroll(
            emp1_id,
            processor.calculate_gross_pay(75000, "biweekly"),
            alice_benefits,
            overtime_hours=5,
        )

        print(f"   Processed payroll for {emp1.name}")
        print(f"   Gross Pay: ${alice_payroll['gross_pay']['total']:.2f}")
        print(f"   Net Pay: ${alice_payroll['net_pay']:.2f}")

    except Exception as e:
        print(f"   HR Operations Error: {e}")

    print()

    # Test Finance department
    print("3. Finance Department Operations:")
    print("-" * 30)

    try:
        # Create account manager
        account_mgr = AccountManager()

        # Create accounts
        cash_account = account_mgr.create_account("Cash", "assets", 10000)
        revenue_account = account_mgr.create_account("Service Revenue", "revenue")
        expense_account = account_mgr.create_account("Office Expenses", "expenses")

        print("   Created accounts: Cash, Service Revenue, Office Expenses")

        # Record some transactions
        transaction1 = Transaction(
            5000, "Service Revenue", "Client payment", "2024-01-15", "revenue"
        )
        transaction2 = Transaction(
            500, "Office Expenses", "Office supplies", "2024-01-16", "expense"
        )

        account_mgr.record_transaction(transaction1)
        account_mgr.record_transaction(transaction2)

        print(
            f"   Recorded transactions: Revenue ${transaction1.amount}, Expense ${transaction2.amount}"
        )

        # Generate financial report
        summary_report = accounting.generate_financial_report(account_mgr, "summary")
        print("   Generated financial summary report")

        # Test budgeting
        budget_mgr = budgeting.BudgetManager()

        # Create a budget
        dept_budget = budget_mgr.create_budget(
            "IT Department 2024", "annual", "2024-01-01", "2024-12-31", 100000
        )

        # Add budget categories
        dept_budget.add_category("Personnel", 60000)
        dept_budget.add_category("Equipment", 25000)
        dept_budget.add_category("Training", 10000)
        dept_budget.add_category("Supplies", 5000)

        print(
            f"   Created budget: {dept_budget.name} with ${dept_budget.total_amount:,.2f}"
        )

        # Record some expenses
        dept_budget.record_expense("Personnel", 15000, "Q1 salaries")
        dept_budget.record_expense("Equipment", 5000, "New laptops")

        budget_summary = dept_budget.get_budget_summary()
        print(f"   Budget utilization: {budget_summary['totals']['percent_used']:.1f}%")

    except Exception as e:
        print(f"   Finance Operations Error: {e}")

    print()

    # Test IT department
    print("4. IT Department Operations:")
    print("-" * 30)

    try:
        # Create security manager
        sec_manager = SecurityManager()

        # Create users
        admin_user = sec_manager.create_user("admin", "SecureP@ssw0rd123!", "admin")
        regular_user = sec_manager.create_user("jdoe", "MyP@ssw0rd456!", "user")

        print(f"   Created users: {admin_user['username']} ({admin_user['role']})")
        print(f"                  {regular_user['username']} ({regular_user['role']})")

        # Test authentication
        auth_result = sec_manager.authenticate_user("admin", "SecureP@ssw0rd123!")
        if auth_result["success"]:
            print("   Authentication successful for admin user")
            print(f"   Session ID: {auth_result['session_id'][:16]}...")

        # Test permissions
        has_permission = security.check_permissions(
            "admin", "system_config", sec_manager
        )
        print(f"   Admin has system_config permission: {has_permission}")

        # Test system monitoring
        web_server = systems.SystemMonitor("web-server-01")
        db_server = systems.SystemMonitor("database-01")

        web_health = web_server.check_system_health()
        db_health = db_server.check_system_health()

        print("   System monitoring:")
        print(
            f"     Web Server: {web_health['status']} (CPU: {web_health['metrics']['cpu_usage']:.1f}%)"
        )
        print(
            f"     Database: {db_health['status']} (Memory: {db_health['metrics']['memory_usage']:.1f}%)"
        )

        # Test network management
        network_mgr = systems.NetworkManager()

        # Add firewall rule
        firewall_rule = {
            "action": "allow",
            "protocol": "tcp",
            "port": 8080,
            "source": "192.168.1.0/24",
        }

        rule_result = network_mgr.add_firewall_rule(firewall_rule)
        print(f"   Network: {rule_result}")

        network_status = network_mgr.get_network_status()
        print(
            f"   Network Status: {network_status['status']} ({len(network_status['active_interfaces'])} active interfaces)"
        )

    except Exception as e:
        print(f"   IT Operations Error: {e}")

    print()

    # Test cross-department integration
    print("5. Cross-Department Integration:")
    print("-" * 30)

    try:
        # Generate company-wide employee ID
        emp_id = company.generate_employee_id("IT", 1001)
        print(f"   Generated employee ID: {emp_id}")

        # Test department information
        departments = company.list_departments()
        for dept_name, dept_info in departments.items():
            print(f"   {dept_name}: {dept_info['description']}")
            print(f"     Modules: {', '.join(dept_info['modules'])}")

        # Test accessing nested functionality
        hr_info = hr.get_hr_info()
        finance_info = finance.get_finance_info()
        it_info = it.get_it_info()

        print("   Department contacts:")
        print(f"     HR: {hr_info['contact']['email']}")
        print(f"     Finance: {finance_info['contact']['email']}")
        print(f"     IT: {it_info['contact']['email']}")

    except Exception as e:
        print(f"   Integration Error: {e}")

    print()

    # Test package metadata and structure
    print("6. Package Structure Verification:")
    print("-" * 30)

    print(f"   Company package version: {company.__version__}")
    print(f"   Available in company.*: {', '.join(company.__all__)}")

    # Test that all imports worked correctly
    imported_modules = [
        "company",
        "company.hr",
        "company.finance",
        "company.it",
        "company.hr.employee_management",
        "company.hr.payroll",
        "company.finance.accounting",
        "company.finance.budgeting",
        "company.it.security",
        "company.it.systems",
    ]

    print(f"   Successfully imported {len(imported_modules)} modules:")
    for module in imported_modules:
        print(f"     ✓ {module}")

    print("\n" + "=" * 60)
    print("SUBPACKAGE STRUCTURE TEST COMPLETE")
    print("=" * 60)
    print("\nKey demonstrations:")
    print("• Complex nested package hierarchy (3 levels deep)")
    print("• Cross-package imports and dependencies")
    print("• Relative imports within subpackages")
    print("• Package-level __init__.py files controlling exports")
    print("• Module-level functions and classes")
    print("• Cross-departmental data sharing")
    print("• Proper package metadata and versioning")

    print("\nThis test case shows how Python handles:")
    print("• Nested package structures")
    print("• Import resolution across package boundaries")
    print("• Package initialization and __all__ exports")
    print("• Relative vs absolute imports")
    print("• Complex dependency chains")


if __name__ == "__main__":
    main()

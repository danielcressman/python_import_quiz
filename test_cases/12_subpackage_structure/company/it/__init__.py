"""
IT (Information Technology) subpackage for the company package.

This subpackage contains modules related to information technology operations,
including systems management and security functionality.
"""

from .security import SecurityManager, audit_system, check_permissions
from .systems import NetworkManager, SystemMonitor, deploy_application

# IT department constants
DEPARTMENT_NAME = "Information Technology"
DEPARTMENT_CODE = "IT"
IT_EMAIL = "it@techcorp.com"
IT_PHONE = "(555) 345-6789"

# IT policies and settings
SECURITY_LEVEL = "high"
BACKUP_FREQUENCY = "daily"
MONITORING_ENABLED = True
AUDIT_LOGGING = True

# System requirements
MIN_PASSWORD_LENGTH = 12
SESSION_TIMEOUT_MINUTES = 30
MAX_LOGIN_ATTEMPTS = 3
FIREWALL_ENABLED = True

# What gets imported with "from company.it import *"
__all__ = [
    "SecurityManager",
    "audit_system",
    "check_permissions",
    "SystemMonitor",
    "NetworkManager",
    "deploy_application",
    "get_it_info",
    "validate_security_settings",
]


def get_it_info():
    """Get IT department information."""
    return {
        "department": DEPARTMENT_NAME,
        "code": DEPARTMENT_CODE,
        "contact": {"email": IT_EMAIL, "phone": IT_PHONE},
        "security": {
            "level": SECURITY_LEVEL,
            "min_password_length": MIN_PASSWORD_LENGTH,
            "session_timeout": SESSION_TIMEOUT_MINUTES,
            "max_login_attempts": MAX_LOGIN_ATTEMPTS,
        },
        "operations": {
            "backup_frequency": BACKUP_FREQUENCY,
            "monitoring_enabled": MONITORING_ENABLED,
            "audit_logging": AUDIT_LOGGING,
            "firewall_enabled": FIREWALL_ENABLED,
        },
    }


def validate_security_settings(settings):
    """Validate security settings according to IT policies."""
    errors = []

    # Check password requirements
    if "password_length" in settings:
        if settings["password_length"] < MIN_PASSWORD_LENGTH:
            errors.append(
                f"Password length must be at least {MIN_PASSWORD_LENGTH} characters"
            )

    # Check session timeout
    if "session_timeout" in settings:
        if settings["session_timeout"] > SESSION_TIMEOUT_MINUTES:
            errors.append(
                f"Session timeout cannot exceed {SESSION_TIMEOUT_MINUTES} minutes"
            )

    # Check security level
    if "security_level" in settings:
        valid_levels = ["low", "medium", "high", "maximum"]
        if settings["security_level"] not in valid_levels:
            errors.append(f"Security level must be one of: {valid_levels}")

    return errors if errors else None


# IT department metadata
IT_VERSION = "3.0.0"
SUPPORTED_OPERATIONS = [
    "system_monitoring",
    "security_management",
    "network_administration",
    "application_deployment",
    "backup_management",
    "user_access_control",
]

# Compliance and security standards
COMPLIANCE_STANDARDS = ["SOX", "GDPR", "ISO27001", "NIST"]
SECURITY_PROTOCOLS = {
    "encryption": "AES-256",
    "authentication": "multi_factor",
    "network_security": "zero_trust",
    "access_control": "role_based",
}

"""
Security module for the IT department.

This module provides functionality for security management, user authentication,
access control, and security auditing operations.
"""

import datetime
import hashlib
import random
from typing import Dict, List, Optional


class SecurityManager:
    """Manages security operations and policies."""

    def __init__(self):
        self.users = {}
        self.permissions = {}
        self.audit_log = []
        self.security_policies = {
            "min_password_length": 12,
            "password_complexity": True,
            "session_timeout": 30,
            "max_login_attempts": 3,
            "two_factor_required": True,
        }
        self.active_sessions = {}
        self.failed_login_attempts = {}

    def create_user(self, username: str, password: str, role: str = "user") -> Dict:
        """Create a new user account."""
        if username in self.users:
            raise ValueError(f"User '{username}' already exists")

        # Validate password
        validation_result = self.validate_password(password)
        if not validation_result["valid"]:
            raise ValueError(
                f"Password validation failed: {validation_result['errors']}"
            )

        # Hash password
        password_hash = self._hash_password(password)

        user_data = {
            "username": username,
            "password_hash": password_hash,
            "role": role,
            "created_date": datetime.datetime.now().isoformat(),
            "last_login": None,
            "is_active": True,
            "two_factor_enabled": False,
            "permissions": self._get_default_permissions(role),
        }

        self.users[username] = user_data
        self._log_security_event("user_created", username, {"role": role})

        return {
            "username": username,
            "role": role,
            "created": user_data["created_date"],
            "permissions": user_data["permissions"],
        }

    def authenticate_user(self, username: str, password: str) -> Dict:
        """Authenticate a user login attempt."""
        if username not in self.users:
            self._log_security_event(
                "login_failed", username, {"reason": "user_not_found"}
            )
            return {"success": False, "reason": "Invalid credentials"}

        user = self.users[username]

        # Check if account is active
        if not user["is_active"]:
            self._log_security_event(
                "login_failed", username, {"reason": "account_disabled"}
            )
            return {"success": False, "reason": "Account disabled"}

        # Check failed login attempts
        if self._is_account_locked(username):
            self._log_security_event(
                "login_failed", username, {"reason": "account_locked"}
            )
            return {
                "success": False,
                "reason": "Account locked due to too many failed attempts",
            }

        # Verify password
        if not self._verify_password(password, user["password_hash"]):
            self._record_failed_login(username)
            self._log_security_event(
                "login_failed", username, {"reason": "invalid_password"}
            )
            return {"success": False, "reason": "Invalid credentials"}

        # Check if 2FA is required
        if (
            self.security_policies["two_factor_required"]
            and not user["two_factor_enabled"]
        ):
            return {
                "success": False,
                "reason": "Two-factor authentication required",
                "requires_2fa_setup": True,
            }

        # Successful login
        session_id = self._create_session(username)
        user["last_login"] = datetime.datetime.now().isoformat()
        self._clear_failed_login_attempts(username)
        self._log_security_event("login_success", username, {"session_id": session_id})

        return {
            "success": True,
            "session_id": session_id,
            "user": {
                "username": username,
                "role": user["role"],
                "permissions": user["permissions"],
            },
        }

    def validate_password(self, password: str) -> Dict:
        """Validate password against security policies."""
        errors = []

        # Check minimum length
        if len(password) < self.security_policies["min_password_length"]:
            errors.append(
                f"Password must be at least {self.security_policies['min_password_length']} characters"
            )

        # Check complexity if required
        if self.security_policies["password_complexity"]:
            has_upper = any(c.isupper() for c in password)
            has_lower = any(c.islower() for c in password)
            has_digit = any(c.isdigit() for c in password)
            has_special = any(c in "!@#$%^&*()_+-=[]{}|;':\",./<>?" for c in password)

            if not has_upper:
                errors.append("Password must contain at least one uppercase letter")
            if not has_lower:
                errors.append("Password must contain at least one lowercase letter")
            if not has_digit:
                errors.append("Password must contain at least one digit")
            if not has_special:
                errors.append("Password must contain at least one special character")

        return {"valid": len(errors) == 0, "errors": errors}

    def change_password(
        self, username: str, old_password: str, new_password: str
    ) -> Dict:
        """Change a user's password."""
        if username not in self.users:
            raise ValueError("User not found")

        user = self.users[username]

        # Verify old password
        if not self._verify_password(old_password, user["password_hash"]):
            self._log_security_event(
                "password_change_failed", username, {"reason": "invalid_old_password"}
            )
            return {"success": False, "reason": "Invalid current password"}

        # Validate new password
        validation_result = self.validate_password(new_password)
        if not validation_result["valid"]:
            return {
                "success": False,
                "reason": "New password validation failed",
                "errors": validation_result["errors"],
            }

        # Update password
        user["password_hash"] = self._hash_password(new_password)
        self._log_security_event("password_changed", username)

        return {"success": True, "message": "Password changed successfully"}

    def create_session(self, username: str) -> str:
        """Create a new user session."""
        return self._create_session(username)

    def validate_session(self, session_id: str) -> Dict:
        """Validate a user session."""
        if session_id not in self.active_sessions:
            return {"valid": False, "reason": "Session not found"}

        session = self.active_sessions[session_id]

        # Check if session has expired
        session_start = datetime.datetime.fromisoformat(session["created"])
        session_age = (datetime.datetime.now() - session_start).total_seconds() / 60

        if session_age > self.security_policies["session_timeout"]:
            del self.active_sessions[session_id]
            self._log_security_event(
                "session_expired", session["username"], {"session_id": session_id}
            )
            return {"valid": False, "reason": "Session expired"}

        # Update last activity
        session["last_activity"] = datetime.datetime.now().isoformat()

        return {
            "valid": True,
            "username": session["username"],
            "role": self.users[session["username"]]["role"],
        }

    def logout_user(self, session_id: str) -> bool:
        """Log out a user by ending their session."""
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            username = session["username"]
            del self.active_sessions[session_id]
            self._log_security_event("logout", username, {"session_id": session_id})
            return True
        return False

    def grant_permission(self, username: str, permission: str) -> str:
        """Grant a permission to a user."""
        if username not in self.users:
            raise ValueError("User not found")

        user = self.users[username]
        if permission not in user["permissions"]:
            user["permissions"].append(permission)
            self._log_security_event(
                "permission_granted", username, {"permission": permission}
            )
            return f"Permission '{permission}' granted to user '{username}'"

        return f"User '{username}' already has permission '{permission}'"

    def revoke_permission(self, username: str, permission: str) -> str:
        """Revoke a permission from a user."""
        if username not in self.users:
            raise ValueError("User not found")

        user = self.users[username]
        if permission in user["permissions"]:
            user["permissions"].remove(permission)
            self._log_security_event(
                "permission_revoked", username, {"permission": permission}
            )
            return f"Permission '{permission}' revoked from user '{username}'"

        return f"User '{username}' does not have permission '{permission}'"

    def get_audit_log(
        self, username: Optional[str] = None, limit: int = 100
    ) -> List[Dict]:
        """Get security audit log entries."""
        if username:
            filtered_log = [
                entry for entry in self.audit_log if entry["username"] == username
            ]
        else:
            filtered_log = self.audit_log

        return filtered_log[-limit:]

    def _hash_password(self, password: str) -> str:
        """Hash a password using SHA-256."""
        salt = "techcorp_salt_2024"  # In production, use a random salt per password
        return hashlib.sha256((password + salt).encode()).hexdigest()

    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify a password against its hash."""
        return self._hash_password(password) == password_hash

    def _create_session(self, username: str) -> str:
        """Create a new session for a user."""
        session_id = hashlib.md5(
            f"{username}{datetime.datetime.now().isoformat()}{random.randint(1000, 9999)}".encode()
        ).hexdigest()

        self.active_sessions[session_id] = {
            "username": username,
            "created": datetime.datetime.now().isoformat(),
            "last_activity": datetime.datetime.now().isoformat(),
        }

        return session_id

    def _get_default_permissions(self, role: str) -> List[str]:
        """Get default permissions for a role."""
        role_permissions = {
            "admin": ["read", "write", "delete", "user_management", "system_config"],
            "manager": ["read", "write", "user_management"],
            "user": ["read"],
            "guest": [],
        }
        return role_permissions.get(role, ["read"])

    def _is_account_locked(self, username: str) -> bool:
        """Check if an account is locked due to failed login attempts."""
        if username not in self.failed_login_attempts:
            return False

        attempts = self.failed_login_attempts[username]
        return attempts["count"] >= self.security_policies["max_login_attempts"]

    def _record_failed_login(self, username: str):
        """Record a failed login attempt."""
        if username not in self.failed_login_attempts:
            self.failed_login_attempts[username] = {"count": 0, "last_attempt": None}

        self.failed_login_attempts[username]["count"] += 1
        self.failed_login_attempts[username]["last_attempt"] = (
            datetime.datetime.now().isoformat()
        )

    def _clear_failed_login_attempts(self, username: str):
        """Clear failed login attempts for a user."""
        if username in self.failed_login_attempts:
            del self.failed_login_attempts[username]

    def _log_security_event(
        self, event_type: str, username: str, details: Optional[Dict] = None
    ):
        """Log a security event to the audit log."""
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "event_type": event_type,
            "username": username,
            "details": details or {},
        }
        self.audit_log.append(log_entry)

        # Keep only recent log entries (last 1000)
        if len(self.audit_log) > 1000:
            self.audit_log = self.audit_log[-1000:]


# Module-level functions
def check_permissions(
    username: str, required_permission: str, security_manager: SecurityManager
) -> bool:
    """Check if a user has a specific permission."""
    if username not in security_manager.users:
        return False

    user = security_manager.users[username]
    return required_permission in user["permissions"]


def audit_system(security_manager: SecurityManager) -> Dict:
    """Perform a security audit of the system."""
    audit_results = {
        "audit_date": datetime.datetime.now().isoformat(),
        "total_users": len(security_manager.users),
        "active_users": sum(
            1 for user in security_manager.users.values() if user["is_active"]
        ),
        "active_sessions": len(security_manager.active_sessions),
        "failed_login_attempts": len(security_manager.failed_login_attempts),
        "recent_security_events": len(security_manager.audit_log),
        "security_issues": [],
    }

    # Check for security issues
    issues = []

    # Check for users without 2FA
    users_without_2fa = [
        username
        for username, user in security_manager.users.items()
        if not user["two_factor_enabled"] and user["role"] in ["admin", "manager"]
    ]
    if users_without_2fa:
        issues.append(
            f"Admin/Manager users without 2FA: {', '.join(users_without_2fa)}"
        )

    # Check for old sessions
    old_sessions = []
    for session_id, session in security_manager.active_sessions.items():
        session_age = (
            datetime.datetime.now()
            - datetime.datetime.fromisoformat(session["created"])
        ).total_seconds() / 3600
        if session_age > 24:  # Sessions older than 24 hours
            old_sessions.append(session_id)

    if old_sessions:
        issues.append(f"Sessions older than 24 hours: {len(old_sessions)}")

    # Check password policy compliance
    weak_passwords = []
    for username, user in security_manager.users.items():
        # This is a simplified check - in reality, you wouldn't re-validate stored hashes
        if len(user["password_hash"]) < 64:  # SHA-256 should be 64 characters
            weak_passwords.append(username)

    audit_results["security_issues"] = issues

    return audit_results


def generate_security_report(security_manager: SecurityManager) -> str:
    """Generate a comprehensive security report."""
    audit_results = audit_system(security_manager)

    lines = [
        "SECURITY AUDIT REPORT",
        "=" * 50,
        f"Generated: {audit_results['audit_date']}",
        "",
        "USER STATISTICS:",
        "-" * 20,
        f"Total Users: {audit_results['total_users']}",
        f"Active Users: {audit_results['active_users']}",
        f"Active Sessions: {audit_results['active_sessions']}",
        f"Failed Login Attempts: {audit_results['failed_login_attempts']}",
        "",
        "SECURITY POLICIES:",
        "-" * 20,
    ]

    for policy, value in security_manager.security_policies.items():
        lines.append(f"{policy.replace('_', ' ').title()}: {value}")

    lines.extend(
        [
            "",
            "SECURITY ISSUES:",
            "-" * 20,
        ]
    )

    if audit_results["security_issues"]:
        for issue in audit_results["security_issues"]:
            lines.append(f"⚠️  {issue}")
    else:
        lines.append("✅ No security issues detected")

    lines.extend(
        [
            "",
            "RECENT ACTIVITY:",
            "-" * 20,
        ]
    )

    recent_events = security_manager.get_audit_log(limit=10)
    for event in recent_events[-5:]:  # Show last 5 events
        lines.append(
            f"{event['timestamp'][:19]} - {event['event_type']} - {event['username']}"
        )

    lines.append("=" * 50)

    return "\n".join(lines)


def encrypt_data(data: str, key: str = "default_key") -> str:
    """Simple encryption function (for demonstration - use proper encryption in production)."""
    # This is a very basic XOR cipher for demonstration
    # In production, use proper encryption libraries like cryptography
    encrypted = ""
    for i, char in enumerate(data):
        key_char = key[i % len(key)]
        encrypted += chr(ord(char) ^ ord(key_char))

    # Convert to hex for safe storage
    return encrypted.encode("latin1").hex()


def decrypt_data(encrypted_hex: str, key: str = "default_key") -> str:
    """Simple decryption function (for demonstration - use proper encryption in production)."""
    try:
        # Convert from hex
        encrypted = bytes.fromhex(encrypted_hex).decode("latin1")

        # XOR decrypt
        decrypted = ""
        for i, char in enumerate(encrypted):
            key_char = key[i % len(key)]
            decrypted += chr(ord(char) ^ ord(key_char))

        return decrypted
    except Exception:
        return "Decryption failed"


def validate_ip_address(ip_address: str) -> bool:
    """Validate an IP address format."""
    parts = ip_address.split(".")
    if len(parts) != 4:
        return False

    try:
        for part in parts:
            num = int(part)
            if not 0 <= num <= 255:
                return False
        return True
    except ValueError:
        return False


# Module constants
MODULE_NAME = "security"
SUPPORTED_ROLES = ["admin", "manager", "user", "guest"]
DEFAULT_PERMISSIONS = ["read", "write", "delete", "user_management", "system_config"]

# Security configuration
SECURITY_LEVELS = ["low", "medium", "high", "maximum"]
ENCRYPTION_ALGORITHMS = ["AES-256", "RSA-2048", "ChaCha20"]

# Compliance standards
COMPLIANCE_FRAMEWORKS = {
    "SOX": "Sarbanes-Oxley Act",
    "GDPR": "General Data Protection Regulation",
    "HIPAA": "Health Insurance Portability and Accountability Act",
    "ISO27001": "Information Security Management",
    "NIST": "National Institute of Standards and Technology",
}

# Default security policies
DEFAULT_SECURITY_POLICIES = {
    "min_password_length": 12,
    "password_complexity": True,
    "session_timeout": 30,
    "max_login_attempts": 3,
    "two_factor_required": True,
    "audit_logging": True,
    "encryption_required": True,
}

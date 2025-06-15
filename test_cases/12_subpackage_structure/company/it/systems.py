"""
Systems module for the IT department.

This module provides functionality for system monitoring, network management,
and application deployment operations.
"""

import datetime
import random
from typing import Dict, List


class SystemMonitor:
    """Monitors system health and performance."""

    def __init__(self, system_name: str):
        self.system_name = system_name
        self.status = "online"
        self.last_check = datetime.datetime.now()
        self.metrics = {
            "cpu_usage": 0.0,
            "memory_usage": 0.0,
            "disk_usage": 0.0,
            "network_latency": 0.0,
        }
        self.alerts = []
        self.uptime_start = datetime.datetime.now()

    def check_system_health(self) -> Dict:
        """Perform a system health check."""
        self.last_check = datetime.datetime.now()

        # Simulate system metrics (in real world, these would be actual readings)
        self.metrics["cpu_usage"] = random.uniform(10, 90)
        self.metrics["memory_usage"] = random.uniform(20, 85)
        self.metrics["disk_usage"] = random.uniform(30, 95)
        self.metrics["network_latency"] = random.uniform(1, 100)

        # Check for alerts
        self._check_thresholds()

        return {
            "system": self.system_name,
            "status": self.status,
            "timestamp": self.last_check.isoformat(),
            "metrics": self.metrics.copy(),
            "uptime_hours": self.get_uptime_hours(),
            "alerts": len(self.alerts),
        }

    def _check_thresholds(self):
        """Check metrics against alert thresholds."""
        thresholds = {
            "cpu_usage": 80,
            "memory_usage": 85,
            "disk_usage": 90,
            "network_latency": 50,
        }

        for metric, value in self.metrics.items():
            if value > thresholds[metric]:
                alert = {
                    "timestamp": datetime.datetime.now().isoformat(),
                    "metric": metric,
                    "value": value,
                    "threshold": thresholds[metric],
                    "severity": "high"
                    if value > thresholds[metric] * 1.1
                    else "medium",
                }
                self.alerts.append(alert)

        # Keep only recent alerts (last 24 hours)
        cutoff = datetime.datetime.now() - datetime.timedelta(hours=24)
        self.alerts = [
            alert
            for alert in self.alerts
            if datetime.datetime.fromisoformat(alert["timestamp"]) > cutoff
        ]

    def get_uptime_hours(self) -> float:
        """Get system uptime in hours."""
        uptime = datetime.datetime.now() - self.uptime_start
        return uptime.total_seconds() / 3600

    def restart_system(self) -> str:
        """Restart the system."""
        self.uptime_start = datetime.datetime.now()
        self.status = "restarting"
        self.alerts.clear()

        # Simulate restart time
        import time

        time.sleep(0.1)  # Brief pause to simulate restart

        self.status = "online"
        return f"System {self.system_name} restarted successfully"

    def get_alert_summary(self) -> Dict:
        """Get summary of current alerts."""
        if not self.alerts:
            return {"status": "no_alerts", "count": 0}

        high_alerts = [a for a in self.alerts if a["severity"] == "high"]
        medium_alerts = [a for a in self.alerts if a["severity"] == "medium"]

        return {
            "status": "has_alerts",
            "count": len(self.alerts),
            "high_severity": len(high_alerts),
            "medium_severity": len(medium_alerts),
            "latest_alert": self.alerts[-1] if self.alerts else None,
        }


class NetworkManager:
    """Manages network configurations and connections."""

    def __init__(self):
        self.connections = {}
        self.firewall_rules = []
        self.network_interfaces = {
            "eth0": {"status": "up", "ip": "192.168.1.100", "speed": "1Gbps"},
            "eth1": {"status": "down", "ip": None, "speed": "1Gbps"},
            "wlan0": {"status": "up", "ip": "192.168.1.101", "speed": "300Mbps"},
        }

    def add_firewall_rule(self, rule: Dict) -> str:
        """Add a firewall rule."""
        required_fields = ["action", "protocol", "port", "source"]
        for field in required_fields:
            if field not in rule:
                raise ValueError(f"Missing required field: {field}")

        rule["id"] = len(self.firewall_rules) + 1
        rule["created"] = datetime.datetime.now().isoformat()
        self.firewall_rules.append(rule)

        return f"Firewall rule {rule['id']} added: {rule['action']} {rule['protocol']} port {rule['port']}"

    def remove_firewall_rule(self, rule_id: int) -> str:
        """Remove a firewall rule by ID."""
        for i, rule in enumerate(self.firewall_rules):
            if rule["id"] == rule_id:
                removed_rule = self.firewall_rules.pop(i)
                return f"Removed firewall rule {rule_id}: {removed_rule['action']} {removed_rule['protocol']}"

        raise ValueError(f"Firewall rule {rule_id} not found")

    def list_firewall_rules(self) -> List[Dict]:
        """List all firewall rules."""
        return self.firewall_rules.copy()

    def configure_interface(self, interface: str, config: Dict) -> str:
        """Configure a network interface."""
        if interface not in self.network_interfaces:
            raise ValueError(f"Interface {interface} not found")

        old_config = self.network_interfaces[interface].copy()
        self.network_interfaces[interface].update(config)

        return f"Interface {interface} configured: {old_config} -> {self.network_interfaces[interface]}"

    def get_network_status(self) -> Dict:
        """Get overall network status."""
        active_interfaces = [
            name
            for name, config in self.network_interfaces.items()
            if config["status"] == "up"
        ]

        return {
            "interfaces": self.network_interfaces.copy(),
            "active_interfaces": active_interfaces,
            "firewall_rules_count": len(self.firewall_rules),
            "connections_count": len(self.connections),
            "status": "healthy" if active_interfaces else "degraded",
        }

    def ping_host(self, hostname: str) -> Dict:
        """Simulate pinging a host."""
        # Simulate ping results
        success = random.choice([True, True, True, False])  # 75% success rate
        latency = random.uniform(1, 50) if success else None

        return {
            "hostname": hostname,
            "success": success,
            "latency_ms": latency,
            "timestamp": datetime.datetime.now().isoformat(),
        }

    def trace_route(self, destination: str) -> List[Dict]:
        """Simulate trace route to destination."""
        hops = []
        hop_count = random.randint(3, 8)

        for i in range(1, hop_count + 1):
            hops.append(
                {
                    "hop": i,
                    "ip": f"192.168.{i}.{random.randint(1, 254)}",
                    "latency_ms": random.uniform(1, 20) * i,
                    "hostname": f"router-{i}.example.com" if i % 2 == 0 else None,
                }
            )

        return hops


# Module-level functions
def deploy_application(app_name: str, version: str, target_servers: List[str]) -> Dict:
    """Deploy an application to target servers."""
    if not app_name or not version:
        raise ValueError("Application name and version are required")

    if not target_servers:
        raise ValueError("At least one target server is required")

    deployment_results = {}

    for server in target_servers:
        # Simulate deployment (in real world, this would involve actual deployment steps)
        success = random.choice([True, True, True, False])  # 75% success rate

        deployment_results[server] = {
            "success": success,
            "status": "deployed" if success else "failed",
            "timestamp": datetime.datetime.now().isoformat(),
            "error": None if success else f"Connection timeout to {server}",
        }

    overall_success = all(result["success"] for result in deployment_results.values())

    return {
        "application": app_name,
        "version": version,
        "target_servers": target_servers,
        "overall_success": overall_success,
        "results": deployment_results,
        "deployment_id": f"DEPLOY-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
    }


def check_service_status(service_name: str) -> Dict:
    """Check the status of a system service."""
    # Simulate service status check
    statuses = ["running", "stopped", "starting", "stopping", "error"]
    status = random.choice(statuses)

    uptime = None
    if status == "running":
        uptime = random.randint(1, 168)  # 1 to 168 hours

    return {
        "service": service_name,
        "status": status,
        "uptime_hours": uptime,
        "pid": random.randint(1000, 9999) if status == "running" else None,
        "memory_usage_mb": random.randint(10, 500) if status == "running" else 0,
        "timestamp": datetime.datetime.now().isoformat(),
    }


def backup_system(
    source_path: str, destination_path: str, compression: bool = True
) -> Dict:
    """Perform a system backup."""
    if not source_path or not destination_path:
        raise ValueError("Source and destination paths are required")

    # Simulate backup process
    file_count = random.randint(100, 10000)
    size_mb = random.randint(500, 50000)
    duration_minutes = random.randint(5, 120)

    success = random.choice([True, True, True, False])  # 75% success rate

    backup_info = {
        "source": source_path,
        "destination": destination_path,
        "compression_enabled": compression,
        "success": success,
        "files_backed_up": file_count if success else random.randint(0, file_count),
        "size_mb": size_mb if success else random.randint(0, size_mb),
        "duration_minutes": duration_minutes,
        "timestamp": datetime.datetime.now().isoformat(),
        "backup_id": f"BACKUP-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
    }

    if not success:
        backup_info["error"] = random.choice(
            [
                "Insufficient disk space",
                "Permission denied",
                "Network connection lost",
                "Source files locked",
            ]
        )

    return backup_info


def monitor_disk_usage(path: str = "/") -> Dict:
    """Monitor disk usage for a given path."""
    # Simulate disk usage monitoring
    total_gb = random.randint(100, 2000)
    used_gb = random.randint(20, int(total_gb * 0.9))
    free_gb = total_gb - used_gb
    usage_percent = (used_gb / total_gb) * 100

    # Determine status based on usage
    if usage_percent < 70:
        status = "healthy"
    elif usage_percent < 85:
        status = "warning"
    else:
        status = "critical"

    return {
        "path": path,
        "total_gb": total_gb,
        "used_gb": used_gb,
        "free_gb": free_gb,
        "usage_percent": round(usage_percent, 2),
        "status": status,
        "timestamp": datetime.datetime.now().isoformat(),
    }


def generate_system_report(systems: List[SystemMonitor]) -> str:
    """Generate a comprehensive system report."""
    if not systems:
        return "No systems to report on"

    lines = [
        "SYSTEM MONITORING REPORT",
        "=" * 50,
        f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Systems Monitored: {len(systems)}",
        "",
    ]

    for system in systems:
        health = system.check_system_health()
        alert_summary = system.get_alert_summary()

        lines.extend(
            [
                f"System: {system.system_name}",
                f"Status: {health['status']}",
                f"Uptime: {health['uptime_hours']:.1f} hours",
                "Metrics:",
                f"  CPU Usage: {health['metrics']['cpu_usage']:.1f}%",
                f"  Memory Usage: {health['metrics']['memory_usage']:.1f}%",
                f"  Disk Usage: {health['metrics']['disk_usage']:.1f}%",
                f"  Network Latency: {health['metrics']['network_latency']:.1f}ms",
                f"Alerts: {alert_summary['count']} ({alert_summary['high_severity']} high, {alert_summary['medium_severity']} medium)",
                "-" * 30,
            ]
        )

    return "\n".join(lines)


# Module constants
MODULE_NAME = "systems"
SUPPORTED_SERVICES = ["apache2", "nginx", "mysql", "postgresql", "redis", "docker"]
DEFAULT_BACKUP_LOCATION = "/backups"
MONITORING_INTERVAL_SECONDS = 300  # 5 minutes

# System thresholds
ALERT_THRESHOLDS = {
    "cpu_usage": 80,
    "memory_usage": 85,
    "disk_usage": 90,
    "network_latency": 50,
}

# Network configuration defaults
DEFAULT_FIREWALL_RULES = [
    {"action": "allow", "protocol": "tcp", "port": 22, "source": "any"},
    {"action": "allow", "protocol": "tcp", "port": 80, "source": "any"},
    {"action": "allow", "protocol": "tcp", "port": 443, "source": "any"},
    {"action": "deny", "protocol": "any", "port": "any", "source": "any"},
]

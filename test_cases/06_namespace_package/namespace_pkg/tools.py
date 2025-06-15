"""
Tools module in a namespace package.

This module exists in a directory without __init__.py,
making it part of a namespace package.
"""


def hammer():
    """A hammer tool."""
    return "🔨 Hammer: Good for nails!"


def screwdriver():
    """A screwdriver tool."""
    return "🪛 Screwdriver: Perfect for screws!"


def wrench():
    """A wrench tool."""
    return "🔧 Wrench: Grips and turns bolts!"


class Toolbox:
    """A toolbox to hold tools."""

    def __init__(self):
        self.tools = []

    def add_tool(self, tool_name):
        """Add a tool to the toolbox."""
        self.tools.append(tool_name)
        return f"Added {tool_name} to toolbox"

    def list_tools(self):
        """List all tools in the toolbox."""
        if not self.tools:
            return "Toolbox is empty"
        return f"Tools in toolbox: {', '.join(self.tools)}"


# Module-level variable
TOOL_COUNT = 3
NAMESPACE_INFO = "This module is in a namespace package (no __init__.py)"

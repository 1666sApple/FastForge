"""
System validation functionality
"""

import subprocess
from core.base import BaseSetup


class SystemValidator(BaseSetup):
    """Handles system prerequisites validation."""

    def check_node_npm(self):
        """Check if Node.js and npm are installed."""
        try:
            node_result = self.run_command(
                ['node', '--version'], capture_output=True)
            npm_result = self.run_command(
                ['npm', '--version'], capture_output=True)

            if node_result and npm_result:
                print(f"✅ Node.js: {node_result.stdout.strip()}")
                print(f"✅ npm: {npm_result.stdout.strip()}")
                return True
            else:
                print("❌ Node.js or npm not found")
                return False
        except FileNotFoundError:
            print("❌ Node.js or npm not found")
            return False

    def check_prerequisites(self):
        """Check all system prerequisites."""
        if not self.check_node_npm():
            print("\n❌ Please install Node.js and npm first:")
            print("   https://nodejs.org/")
            return False
        return True

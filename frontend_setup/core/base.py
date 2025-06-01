"""
Base setup functionality shared across all components
"""

import subprocess
from pathlib import Path


class BaseSetup:
    """Base class for all setup operations."""

    def __init__(self):
        """Initialize base setup."""
        self.current_dir = Path.cwd()

    def run_command(self, command, cwd=None, shell=False, capture_output=False):
        """Run a command and handle output."""
        try:
            if not capture_output:
                print(f"🔧 Running: {' '.join(command) if isinstance(command, list) else command}")

            result = subprocess.run(
                command,
                cwd=cwd or self.current_dir,
                shell=shell,
                text=True,
                capture_output=capture_output
            )

            if result.returncode == 0:
                if not capture_output:
                    print("✅ Command completed successfully")
                return result if capture_output else True
            else:
                if not capture_output:
                    print(f"❌ Command failed with exit code {result.returncode}")
                return False

        except Exception as e:
            print(f"❌ Error running command: {e}")
            return False

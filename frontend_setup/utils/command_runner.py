"""
Command execution utilities
"""

import subprocess
import sys
from pathlib import Path


class CommandRunner:
    """Handles command execution with various options."""

    def __init__(self):
        """Initialize command runner."""
        pass

    def run_command(self, command, cwd=None, shell=False, capture_output=False, timeout=None):
        """
        Run a command with comprehensive options.

        Args:
            command: Command to run (list or string)
            cwd: Working directory
            shell: Use shell execution
            capture_output: Capture stdout/stderr
            timeout: Command timeout in seconds

        Returns:
            CompletedProcess if capture_output=True, bool otherwise
        """
        try:
            if not capture_output:
                print(
                    f"🔧 Running: {' '.join(command) if isinstance(command, list) else command}")

            result = subprocess.run(
                command,
                cwd=cwd,
                shell=shell,
                text=True,
                capture_output=capture_output,
                timeout=timeout
            )

            if result.returncode == 0:
                if not capture_output:
                    print("✅ Command completed successfully")
                return result if capture_output else True
            else:
                if not capture_output:
                    print(
                        f"❌ Command failed with exit code {result.returncode}")
                    if result.stderr:
                        print(f"Error: {result.stderr}")
                return result if capture_output else False

        except subprocess.TimeoutExpired:
            print(f"❌ Command timed out after {timeout} seconds")
            return False
        except FileNotFoundError:
            print(
                f"❌ Command not found: {command[0] if isinstance(command, list) else command}")
            return False
        except Exception as e:
            print(f"❌ Error running command: {e}")
            return False

    def run_interactive_command(self, command, cwd=None):
        """
        Run a command interactively (showing output in real-time).

        Args:
            command: Command to run
            cwd: Working directory

        Returns:
            bool: Success status
        """
        try:
            print(
                f"🔧 Running: {' '.join(command) if isinstance(command, list) else command}")

            process = subprocess.Popen(
                command,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )

            # Print output in real-time
            for line in iter(process.stdout.readline, ''):
                print(line.rstrip())

            process.wait()

            if process.returncode == 0:
                print("✅ Command completed successfully")
                return True
            else:
                print(f"❌ Command failed with exit code {process.returncode}")
                return False

        except Exception as e:
            print(f"❌ Error running interactive command: {e}")
            return False

    def check_command_exists(self, command):
        """
        Check if a command exists in the system.

        Args:
            command: Command name to check

        Returns:
            bool: True if command exists
        """
        try:
            result = subprocess.run(
                ['which', command] if sys.platform != 'win32' else [
                    'where', command],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except Exception:
            return False

    def get_command_version(self, command, version_flag='--version'):
        """
        Get version of a command.

        Args:
            command: Command name
            version_flag: Flag to get version (default: --version)

        Returns:
            str: Version string or None if failed
        """
        try:
            result = subprocess.run(
                [command, version_flag],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except Exception:
            return None

    def run_npm_command(self, npm_command, cwd=None, interactive=False):
        """
        Run npm command with proper error handling.

        Args:
            npm_command: npm command parts (e.g., ['install', 'react'])
            cwd: Working directory
            interactive: Whether to run interactively

        Returns:
            bool: Success status
        """
        command = ['npm'] + npm_command

        if interactive:
            return self.run_interactive_command(command, cwd)
        else:
            return self.run_command(command, cwd)

    def run_npx_command(self, npx_command, cwd=None, interactive=False):
        """
        Run npx command with proper error handling.

        Args:
            npx_command: npx command parts
            cwd: Working directory
            interactive: Whether to run interactively

        Returns:
            bool: Success status
        """
        command = ['npx'] + npx_command

        if interactive:
            return self.run_interactive_command(command, cwd)
        else:
            return self.run_command(command, cwd)

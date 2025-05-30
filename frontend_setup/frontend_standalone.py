#!/usr/bin/env python3
"""
Standalone script to run React Setup CLI
"""
from frontend import FrontendSetupCLI


def main():
    """Main function to run the CLI."""
    cli = FrontendSetupCLI()
    cli.run_interactive_setup()


if __name__ == "__main__":
    main()

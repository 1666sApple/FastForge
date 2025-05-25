"""
User interface functionality for CLI interactions
"""

import re


class UserInterface:
    """Handles user interface interactions."""

    def __init__(self):
        """Initialize user interface handler."""
        pass

    def get_framework_choice(self):
        """Get framework choice from user."""
        print("📋 Choose a React framework:")
        print("1. Create React App (CRA)")
        print("2. Next.js")
        print("3. Vite React")

        while True:
            choice = input("\nEnter your choice (1-3): ").strip()
            if choice in ['1', '2', '3']:
                return choice
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

    def get_language_choice(self):
        """Get language choice (JavaScript or TypeScript)."""
        print("\n📋 Choose language:")
        print("1. JavaScript")
        print("2. TypeScript")

        while True:
            choice = input("\nEnter your choice (1-2): ").strip()
            if choice == '1':
                return False  # JavaScript
            elif choice == '2':
                return True   # TypeScript
            print("❌ Invalid choice. Please enter 1 or 2.")

    def get_app_name(self):
        """Get application name from user."""
        while True:
            app_name = input("\n📝 Enter your app name: ").strip()

            if not app_name:
                print("❌ App name cannot be empty.")
                continue

            # Check if app name is valid (no spaces, special chars, etc.)
            if not re.match(r'^[a-zA-Z0-9_-]+$', app_name):
                print(
                    "❌ App name can only contain letters, numbers, hyphens, and underscores.")
                continue

            return app_name

    def get_setup_options(self, framework_choice):
        """Get additional setup options from user."""
        print("\n🔧 Additional setup options:")

        setup_options = {}

        # Ask for project structure
        structure_choice = input(
            "Create additional project structure? (y/n): ").strip().lower()
        setup_options['structure'] = structure_choice in ['y', 'yes']

        # Ask for common packages
        packages_choice = input(
            "Install common React packages? (y/n): ").strip().lower()
        setup_options['packages'] = packages_choice in ['y', 'yes']

        # Ask for Tailwind CSS (skip for Next.js as it has built-in option)
        if framework_choice != '2':  # Not Next.js
            tailwind_choice = input(
                "Setup Tailwind CSS? (y/n): ").strip().lower()
            setup_options['tailwind'] = tailwind_choice in ['y', 'yes']
        else:
            # For Next.js, ask if they want Tailwind during creation
            tailwind_choice = input(
                "Include Tailwind CSS in Next.js setup? (y/n): ").strip().lower()
            setup_options['tailwind'] = tailwind_choice in ['y', 'yes']

        return setup_options

    def ask_start_server(self):
        """Ask if user wants to start development server."""
        choice = input(
            "\n🚀 Start development server now? (y/n): ").strip().lower()
        return choice in ['y', 'yes']

    def show_welcome_message(self):
        """Show welcome message."""
        print("=" * 50)
        print("    🚀 React Setup CLI")
        print("    Set up React projects with modern configurations")
        print("=" * 50)

    def show_completion_message(self, project_name):
        """Show project completion message."""
        print("\n" + "=" * 50)
        print(f"    ✅ Project '{project_name}' created successfully!")
        print("    Happy coding! 🎉")
        print("=" * 50)

    def get_user_confirmation(self, message):
        """Get yes/no confirmation from user."""
        while True:
            choice = input(f"{message} (y/n): ").strip().lower()
            if choice in ['y', 'yes']:
                return True
            elif choice in ['n', 'no']:
                return False
            print("❌ Please enter 'y' for yes or 'n' for no.")

    def display_error(self, message):
        """Display error message."""
        print(f"\n❌ Error: {message}")

    def display_success(self, message):
        """Display success message."""
        print(f"\n✅ {message}")

    def display_info(self, message):
        """Display info message."""
        print(f"\nℹ️  {message}")

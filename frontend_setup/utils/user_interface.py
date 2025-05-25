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
            if not choice:
                print("❌ Please enter a choice. You cannot leave this field empty.")
                continue
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
            if not choice:
                print("❌ Please enter a choice. You cannot leave this field empty.")
                continue
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
                print("❌ App name cannot be empty. Please enter a valid app name.")
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
            "Create additional project structure? [Y/n]: ").strip().lower()
        if not structure_choice:  # Default to yes if empty
            setup_options['structure'] = True
        else:
            setup_options['structure'] = structure_choice in ['y', 'yes']

        # Ask for common packages
        packages_choice = input(
            "Install common React packages? [Y/n]: ").strip().lower()
        if not packages_choice:  # Default to yes if empty
            setup_options['packages'] = True
        else:
            setup_options['packages'] = packages_choice in ['y', 'yes']

        # Ask for Tailwind CSS (skip for Next.js as it has built-in option)
        if framework_choice != '2':  # Not Next.js
            tailwind_choice = input(
                "Setup Tailwind CSS? [Y/n]: ").strip().lower()
            if not tailwind_choice:  # Default to yes if empty
                setup_options['tailwind'] = True
            else:
                setup_options['tailwind'] = tailwind_choice in ['y', 'yes']
        else:
            # For Next.js, ask if they want Tailwind during creation
            tailwind_choice = input(
                "Include Tailwind CSS in Next.js setup? [Y/n]: ").strip().lower()
            if not tailwind_choice:  # Default to yes if empty
                setup_options['tailwind'] = True
            else:
                setup_options['tailwind'] = tailwind_choice in ['y', 'yes']

        return setup_options

    def ask_start_server(self):
        """Ask if user wants to start development server."""
        choice = input(
            "\n🚀 Start development server now? [Y/n]: ").strip().lower()
        if not choice:  # Default to yes if empty
            return True
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

    def get_user_confirmation(self, message, default=True):
        """Get yes/no confirmation from user with default option."""
        default_text = "[Y/n]" if default else "[y/N]"
        while True:
            choice = input(f"{message} {default_text}: ").strip().lower()
            if not choice:  # Empty input, use default
                return default
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

    def show_configuration_summary(self, framework_choice, use_typescript, app_name, setup_options):
        """Show configuration summary and allow user to confirm or edit."""
        framework_names = {
            '1': 'Create React App (CRA)',
            '2': 'Next.js',
            '3': 'Vite React'
        }

        print("\n" + "=" * 60)
        print("    📋 CONFIGURATION SUMMARY")
        print("=" * 60)
        print(f"App Name:           {app_name}")
        print(f"Framework:          {framework_names[framework_choice]}")
        print(
            f"Language:           {'TypeScript' if use_typescript else 'JavaScript'}")
        print(
            f"Project Structure:  {'Yes' if setup_options.get('structure', False) else 'No'}")
        print(
            f"Common Packages:    {'Yes' if setup_options.get('packages', False) else 'No'}")
        print(
            f"Tailwind CSS:       {'Yes' if setup_options.get('tailwind', False) else 'No'}")
        print("=" * 60)

        while True:
            print("\nOptions:")
            print("1. Proceed with these settings")
            print("2. Edit app name")
            print("3. Change framework")
            print("4. Change language")
            print("5. Modify setup options")
            print("6. Start over")

            choice = input("\nWhat would you like to do? (1-6): ").strip()

            if not choice:
                print("❌ Please enter a choice. You cannot leave this field empty.")
                continue

            if choice == '1':
                return 'proceed', None, None, None, None
            elif choice == '2':
                return 'edit_name', None, None, None, None
            elif choice == '3':
                return 'edit_framework', None, None, None, None
            elif choice == '4':
                return 'edit_language', None, None, None, None
            elif choice == '5':
                return 'edit_options', None, None, None, None
            elif choice == '6':
                return 'restart', None, None, None, None
            else:
                print("❌ Invalid choice. Please enter a number between 1-6.")

    def get_complete_configuration(self):
        """Get complete configuration from user with confirmation loop."""
        while True:
            # Get all configuration
            framework_choice = self.get_framework_choice()
            use_typescript = self.get_language_choice()
            app_name = self.get_app_name()
            setup_options = self.get_setup_options(framework_choice)

            # Show summary and get user action
            action, _, _, _, _ = self.show_configuration_summary(
                framework_choice, use_typescript, app_name, setup_options)

            if action == 'proceed':
                return framework_choice, use_typescript, app_name, setup_options
            elif action == 'edit_name':
                app_name = self.get_app_name()
                # Show updated summary
                action, _, _, _, _ = self.show_configuration_summary(
                    framework_choice, use_typescript, app_name, setup_options)
                if action == 'proceed':
                    return framework_choice, use_typescript, app_name, setup_options
            elif action == 'edit_framework':
                framework_choice = self.get_framework_choice()
                setup_options = self.get_setup_options(
                    framework_choice)  # Re-get options for new framework
                # Show updated summary
                action, _, _, _, _ = self.show_configuration_summary(
                    framework_choice, use_typescript, app_name, setup_options)
                if action == 'proceed':
                    return framework_choice, use_typescript, app_name, setup_options
            elif action == 'edit_language':
                use_typescript = self.get_language_choice()
                # Show updated summary
                action, _, _, _, _ = self.show_configuration_summary(
                    framework_choice, use_typescript, app_name, setup_options)
                if action == 'proceed':
                    return framework_choice, use_typescript, app_name, setup_options
            elif action == 'edit_options':
                setup_options = self.get_setup_options(framework_choice)
                # Show updated summary
                action, _, _, _, _ = self.show_configuration_summary(
                    framework_choice, use_typescript, app_name, setup_options)
                if action == 'proceed':
                    return framework_choice, use_typescript, app_name, setup_options
            elif action == 'restart':
                continue  # Start the whole loop over

    def show_command_preview(self, command, description=""):
        """Show the command that will be executed and ask for confirmation."""
        print("\n" + "=" * 60)
        print("    🔧 COMMAND PREVIEW")
        print("=" * 60)
        if description:
            print(f"Description: {description}")
        print(f"Command:     {command}")
        print("=" * 60)

        return self.get_user_confirmation(
            "\nProceed with command execution?", default=True)

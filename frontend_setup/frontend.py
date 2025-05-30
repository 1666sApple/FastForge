"""
Main React Setup CLI - Parent Component
This serves as the orchestrator for all React project setup operations.
"""

from pathlib import Path
from core.base import BaseSetup
from core.validator import SystemValidator
from frameworks.create_react_app import CreateReactAppSetup
from frameworks.nextjs import NextJSSetup
from frameworks.vite import ViteSetup
from setup.package_manager import PackageManager
from setup.project_structure import ProjectStructureManager
from setup.styling import StylingSetup
from utils.user_interface import UserInterface


class FrontendSetupCLI(BaseSetup):
    """Main React Setup CLI orchestrator."""

    def __init__(self):
        """Initialize React setup CLI."""
        super().__init__()
        self.validator = SystemValidator()
        self.ui = UserInterface()
        self.package_manager = PackageManager()
        self.structure_manager = ProjectStructureManager()
        self.styling_setup = StylingSetup()

        # Framework handlers
        self.frameworks = {
            '1': CreateReactAppSetup(),
            '2': NextJSSetup(),
            '3': ViteSetup()
        }

    def setup_react_project(self, app_name, framework_choice, use_typescript, setup_options=None):
        """Set up a React project with the chosen configuration."""
        if not self.validator.check_prerequisites():
            return None

        app_path = self.current_dir / app_name
        framework_handler = self.frameworks.get(framework_choice)

        if not framework_handler:
            print(f"❌ Invalid framework choice: {framework_choice}")
            return None

        # Create the project
        success = framework_handler.create_project(
            app_name, use_typescript, setup_options)

        if success and setup_options:
            self._apply_additional_setup(
                app_path, setup_options, use_typescript, framework_choice)

        if success:
            framework_handler.show_project_info(app_path, use_typescript)
            return app_path

        return None

    def _apply_additional_setup(self, app_path, setup_options, use_typescript, framework_choice):
        """Apply additional setup options."""
        if setup_options.get('structure', False):
            self.structure_manager.create_project_structure(app_path)

        if setup_options.get('packages', False):
            self.package_manager.install_common_packages(app_path)
            self.package_manager.install_dev_packages(app_path, use_typescript)

        # Setup styling if requested
        if setup_options.get('tailwind', False):
            # Skip Tailwind setup for Next.js if already configured
            if not (framework_choice == '2' and setup_options.get('tailwind', False)):
                self.styling_setup.setup_tailwind(app_path)

    def run_interactive_setup(self):
        """Run the interactive setup process."""
        print("=== React Setup CLI ===")
        print("Set up React projects with modern configurations\n")

        if not self.validator.check_prerequisites():
            return None

        # Get user choices
        framework_choice = self.ui.get_framework_choice()
        use_typescript = self.ui.get_language_choice()
        app_name = self.ui.get_app_name()
        setup_options = self.ui.get_setup_options(framework_choice)

        # Create the project
        project_path = self.setup_react_project(
            app_name, framework_choice, use_typescript, setup_options)

        if project_path:
            start_server = self.ui.ask_start_server()
            if start_server:
                self.start_dev_server(project_path)

        return project_path

    def start_dev_server(self, project_path):
        """Start the development server."""
        print(f"\n🚀 Starting development server...")
        package_json = project_path / 'package.json'

        if package_json.exists():
            print("Starting development server... (Press Ctrl+C to stop)")
            return self.run_command(['npm', 'start'], cwd=project_path)
        else:
            print("❌ No package.json found in project directory")
            return False


def main():
    """Main function for React setup CLI."""
    cli = FrontendSetupCLI()
    cli.run_interactive_setup()


if __name__ == "__main__":
    main()

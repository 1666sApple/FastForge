"""
React Setup CLI
Provides command line interface for common React project setup tasks.
"""

import os
import subprocess
import sys
from pathlib import Path


class ReactSetupCLI:
    """Class to handle React project setup via CLI commands."""

    def __init__(self):
        """Initialize React setup CLI."""
        self.current_dir = Path.cwd()

    def check_node_npm(self):
        """Check if Node.js and npm are installed."""
        try:
            node_result = subprocess.run(
                ['node', '--version'], capture_output=True, text=True)
            npm_result = subprocess.run(
                ['npm', '--version'], capture_output=True, text=True)

            if node_result.returncode == 0 and npm_result.returncode == 0:
                print(f"✅ Node.js: {node_result.stdout.strip()}")
                print(f"✅ npm: {npm_result.stdout.strip()}")
                return True
            else:
                print("❌ Node.js or npm not found")
                return False
        except FileNotFoundError:
            print("❌ Node.js or npm not found")
            return False

    def run_command(self, command, cwd=None, shell=False):
        """Run a command and handle output."""
        try:
            print(
                f"🔧 Running: {' '.join(command) if isinstance(command, list) else command}")

            result = subprocess.run(
                command,
                cwd=cwd or self.current_dir,
                shell=shell,
                text=True,
                capture_output=False
            )

            if result.returncode == 0:
                print("✅ Command completed successfully")
                return True
            else:
                print(f"❌ Command failed with exit code {result.returncode}")
                return False

        except Exception as e:
            print(f"❌ Error running command: {e}")
            return False

    def create_react_app(self, app_name, use_typescript=False, template=None):
        """Create a new React app using create-react-app."""
        if not self.check_node_npm():
            return False

        print(f"\n🚀 Creating React app: {app_name}")

        command = ['npx', 'create-react-app', app_name]

        if use_typescript:
            command.extend(['--template', 'typescript'])
        elif template:
            command.extend(['--template', template])

        return self.run_command(command)

    def create_next_app(self, app_name, use_typescript=False, tailwind=False, eslint=True):
        """Create a new Next.js app."""
        if not self.check_node_npm():
            return False

        print(f"\n🚀 Creating Next.js app: {app_name}")

        command = ['npx', 'create-next-app@latest', app_name]

        if use_typescript:
            command.append('--typescript')
        else:
            command.append('--javascript')

        if tailwind:
            command.append('--tailwind')

        if eslint:
            command.append('--eslint')
        else:
            command.append('--no-eslint')

        command.extend(['--app', '--src-dir', '--import-alias', '@/*'])

        return self.run_command(command)

    def create_vite_react_app(self, app_name, use_typescript=False):
        """Create a new React app using Vite."""
        if not self.check_node_npm():
            return False

        print(f"\n🚀 Creating Vite React app: {app_name}")

        template = 'react-ts' if use_typescript else 'react'
        command = ['npm', 'create', 'vite@latest',
                   app_name, '--', '--template', template]

        if self.run_command(command):
            print(f"\n📦 Installing dependencies for {app_name}...")
            app_path = self.current_dir / app_name
            return self.run_command(['npm', 'install'], cwd=app_path)

        return False

    def install_common_packages(self, project_path, packages=None):
        """Install common React packages."""
        if not packages:
            packages = [
                'axios',           # HTTP client
                'react-router-dom',  # Routing
                'styled-components',  # CSS-in-JS
                '@mui/material',   # Material-UI
                '@emotion/react',  # Required for MUI
                '@emotion/styled',  # Required for MUI
                'framer-motion',   # Animations
                'react-query',     # Data fetching
                'zustand',         # State management
                'react-hook-form',  # Form handling
                'yup',             # Form validation
            ]

        print(f"\n📦 Installing common packages...")
        for package in packages:
            print(f"  - {package}")

        command = ['npm', 'install'] + packages
        return self.run_command(command, cwd=project_path)

    def install_dev_packages(self, project_path, use_typescript=False):
        """Install common development packages."""
        dev_packages = [
            'prettier',
            'eslint-config-prettier',
            'eslint-plugin-prettier',
            '@testing-library/react',
            '@testing-library/jest-dom',
            '@testing-library/user-event',
        ]

        if use_typescript:
            dev_packages.extend([
                '@types/react',
                '@types/react-dom',
                '@types/node',
            ])

        print(f"\n📦 Installing development packages...")
        for package in dev_packages:
            print(f"  - {package}")

        command = ['npm', 'install', '--save-dev'] + dev_packages
        return self.run_command(command, cwd=project_path)

    def setup_tailwind(self, project_path):
        """Set up Tailwind CSS in a React project."""
        print(f"\n🎨 Setting up Tailwind CSS...")

        # Install Tailwind
        if not self.run_command(['npm', 'install', '-D', 'tailwindcss', 'postcss', 'autoprefixer'], cwd=project_path):
            return False

        # Initialize Tailwind config
        if not self.run_command(['npx', 'tailwindcss', 'init', '-p'], cwd=project_path):
            return False

        # Create tailwind config content
        tailwind_config = '''/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}'''

        config_path = project_path / 'tailwind.config.js'
        with open(config_path, 'w') as f:
            f.write(tailwind_config)

        # Create/update CSS file
        css_content = '''@tailwind base;
@tailwind components;
@tailwind utilities;'''

        css_path = project_path / 'src' / 'index.css'
        with open(css_path, 'w') as f:
            f.write(css_content)

        print("✅ Tailwind CSS setup completed")
        return True

    def create_project_structure(self, project_path):
        """Create additional folder structure for React project."""
        directories = [
            'src/components/common',
            'src/components/ui',
            'src/pages',
            'src/hooks',
            'src/utils',
            'src/services',
            'src/context',
            'src/assets/images',
            'src/assets/icons',
            'src/styles',
            'public/images',
        ]

        print(f"\n📁 Creating project structure...")

        for directory in directories:
            dir_path = project_path / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"Created: {directory}")

        # Create index files for components
        component_dirs = ['src/components/common', 'src/components/ui']
        for comp_dir in component_dirs:
            index_path = project_path / comp_dir / 'index.js'
            with open(index_path, 'w') as f:
                f.write('// Export components from this directory\n')

        return True

    def start_dev_server(self, project_path):
        """Start the development server."""
        print(f"\n🚀 Starting development server...")

        # Check for package.json to determine project type
        package_json = project_path / 'package.json'
        if package_json.exists():
            print("Starting development server... (Press Ctrl+C to stop)")
            return self.run_command(['npm', 'start'], cwd=project_path)
        else:
            print("❌ No package.json found in project directory")
            return False

    def show_project_info(self, project_path, project_type, use_typescript=False):
        """Show information about the created project."""
        lang_str = "TypeScript" if use_typescript else "JavaScript"
        print(f"\n🎉 {project_type} ({lang_str}) project created successfully!")
        print(f"📁 Location: {project_path}")
        print(f"\n📋 Next steps:")
        print(f"1. cd {project_path.name}")

        if project_type == "Next.js":
            print(f"2. npm run dev (to start development server)")
            print(f"3. Open http://localhost:3000 in your browser")
        else:
            print(f"2. npm start (to start development server)")
            print(f"3. Open http://localhost:3000 in your browser")

        print(f"\n📚 Available commands:")
        if project_type == "Next.js":
            print(f"  npm run dev    - Start Next.js development server")
            print(f"  npm run build  - Build for production")
            print(f"  npm start      - Start production server")
        else:
            print(f"  npm start      - Start development server")
            print(f"  npm run build  - Build for production")
            print(f"  npm test       - Run tests")

    def get_framework_choice(self):
        """Get user's framework choice."""
        print("\n🛠️ Choose React framework:")
        print("1. Create React App (CRA)")
        print("2. Next.js")
        print("3. Vite")

        while True:
            choice = input("\nEnter your choice (1-3): ").strip()
            if choice in ['1', '2', '3']:
                return choice
            print("Invalid choice. Please enter 1-3.")

    def get_language_choice(self):
        """Get user's language choice."""
        print("\n💻 Choose language:")
        print("1. JavaScript")
        print("2. TypeScript")

        while True:
            choice = input("\nEnter your choice (1-2): ").strip()
            if choice in ['1', '2']:
                return choice == '2'  # Return True for TypeScript
            print("Invalid choice. Please enter 1 or 2.")

    def setup_react_project(self, app_name, framework_choice, use_typescript, setup_options=None):
        """Set up a React project with the chosen configuration."""
        app_path = self.current_dir / app_name
        success = False
        project_type = ""

        if framework_choice == '1':
            # Create React App
            success = self.create_react_app(app_name, use_typescript)
            project_type = "Create React App"
        elif framework_choice == '2':
            # Next.js App
            tailwind = setup_options.get(
                'tailwind', False) if setup_options else False
            success = self.create_next_app(app_name, use_typescript, tailwind)
            project_type = "Next.js"
        elif framework_choice == '3':
            # Vite React App
            success = self.create_vite_react_app(app_name, use_typescript)
            project_type = "Vite React"

        if success and setup_options:
            # Additional setup options
            if setup_options.get('structure', False):
                self.create_project_structure(app_path)

            if setup_options.get('packages', False):
                self.install_common_packages(app_path)
                self.install_dev_packages(app_path, use_typescript)

            # Setup Tailwind if requested and not Next.js with Tailwind
            if setup_options.get('tailwind', False) and not (framework_choice == '2' and setup_options.get('tailwind', False)):
                self.setup_tailwind(app_path)

        if success:
            self.show_project_info(app_path, project_type, use_typescript)
            return app_path

        return None


def main():
    """Main function for React setup CLI."""
    cli = ReactSetupCLI()

    print("=== React Setup CLI ===")
    print("Set up React projects with modern configurations")
    print()

    # Check prerequisites
    if not cli.check_node_npm():
        print("\n❌ Please install Node.js and npm first:")
        print("   https://nodejs.org/")
        return

    # Get framework choice
    framework_choice = cli.get_framework_choice()

    # Get language choice
    use_typescript = cli.get_language_choice()

    # Get app name
    app_name = input("\nEnter app name: ").strip()
    if not app_name:
        print("App name cannot be empty.")
        return

    # Sanitize app name
    app_name = "".join(c for c in app_name if c.isalnum() or c in "-_").lower()

    # Get additional setup options
    setup_options = {}

    if framework_choice == '2':  # Next.js
        setup_options['tailwind'] = input(
            "Use Tailwind CSS? (y/N): ").strip().lower() in ['y', 'yes']
    else:
        setup_options['tailwind'] = input(
            "Setup Tailwind CSS? (y/N): ").strip().lower() in ['y', 'yes']

    setup_options['structure'] = input(
        "Create additional project structure? (y/N): ").strip().lower() in ['y', 'yes']
    setup_options['packages'] = input(
        "Install common packages? (y/N): ").strip().lower() in ['y', 'yes']

    # Create the project
    project_path = cli.setup_react_project(
        app_name, framework_choice, use_typescript, setup_options)

    if project_path:
        start_server = input(
            "\nStart development server now? (y/N): ").strip().lower() in ['y', 'yes']
        if start_server:
            cli.start_dev_server(project_path)


if __name__ == "__main__":
    main()

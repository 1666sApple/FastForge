"""
Next.js specific setup functionality - Fixed version
"""

import os
import subprocess
from pathlib import Path
from core.base import BaseSetup


class NextJSSetup(BaseSetup):
    """Handles Next.js project creation."""

    def create_project(self, app_name, use_typescript=False, setup_options=None):
        """Create a new Next.js app."""
        print(f"\n🚀 Creating Next.js app: {app_name}")

        command = ['npx', 'create-next-app@latest', app_name]

        if use_typescript:
            command.append('--typescript')
        else:
            command.append('--javascript')

        if setup_options and setup_options.get('tailwind', False):
            command.append('--tailwind')

        # Default Next.js options
        command.extend([
            '--eslint',
            '--app',
            '--src-dir',
            '--import-alias', '@/*'
        ])

        return self.run_command(command)

    def install_compatible_packages(self, project_path, use_typescript=False):
        """Install React 19 compatible packages."""

        original_dir = os.getcwd()

        try:
            # Ensure we're in the project directory
            print(f"📂 Changing to project directory: {project_path}")
            os.chdir(project_path)
            print(f"📂 Current directory: {os.getcwd()}")

            print("📦 Installing compatible packages...")

            # Core packages compatible with React 19
            core_packages = [
                'axios',
                'react-router-dom@latest',
                '@tanstack/react-query@latest',  # Updated from react-query
                'zustand',
                'react-hook-form',
                '@hookform/resolvers',  # For yup integration
                'yup',
                'framer-motion@latest'
            ]

            # UI packages that might need legacy peer deps
            ui_packages = [
                '@mui/material@latest',
                '@emotion/react@latest',
                '@emotion/styled@latest',
                '@mui/icons-material@latest'
            ]

            # Install core packages first
            print("  - Installing core packages...")
            print(f"    Packages: {', '.join(core_packages)}")
            core_cmd = ['npm', 'install'] + core_packages

            result = subprocess.run(
                core_cmd, capture_output=True, text=True, cwd=os.getcwd())
            if result.returncode != 0:
                print(f"❌ Core packages failed, trying with --legacy-peer-deps...")
                core_cmd_legacy = ['npm', 'install',
                                   '--legacy-peer-deps'] + core_packages
                result = subprocess.run(
                    core_cmd_legacy, capture_output=True, text=True, cwd=os.getcwd())
                if result.returncode != 0:
                    print(
                        f"❌ Failed to install core packages: {result.stderr}")
                    return False

            print("✅ Core packages installed successfully!")

            # Install UI packages with legacy peer deps flag for MUI compatibility
            print("  - Installing UI packages...")
            print(f"    Packages: {', '.join(ui_packages)}")
            ui_cmd = ['npm', 'install', '--legacy-peer-deps'] + ui_packages

            result = subprocess.run(
                ui_cmd, capture_output=True, text=True, cwd=os.getcwd())
            if result.returncode != 0:
                print(f"❌ Failed to install UI packages: {result.stderr}")
                return False

            print("✅ UI packages installed successfully!")

            # Development packages
            dev_packages = [
                'prettier',
                'eslint-config-prettier',
                'eslint-plugin-prettier',
                '@testing-library/react@latest',
                '@testing-library/jest-dom@latest',
                '@testing-library/user-event@latest'
            ]

            if use_typescript:
                dev_packages.extend([
                    '@types/react@latest',
                    '@types/react-dom@latest',
                    '@types/node@latest'
                ])

            print("  - Installing development packages...")
            print(f"    Packages: {', '.join(dev_packages)}")
            dev_cmd = ['npm', 'install', '--save-dev'] + dev_packages

            result = subprocess.run(
                dev_cmd, capture_output=True, text=True, cwd=os.getcwd())
            if result.returncode != 0:
                print(f"❌ Failed to install dev packages: {result.stderr}")
                return False

            print("✅ All packages installed successfully!")
            return True

        except Exception as e:
            print(f"❌ Error installing packages: {e}")
            return False
        finally:
            os.chdir(original_dir)

    def start_dev_server(self, project_path):
        """Start the Next.js development server."""

        print(f"\n🚀 Starting development server...")
        print("Starting development server... (Press Ctrl+C to stop)")

        original_dir = os.getcwd()
        try:
            # Ensure we're in the correct directory
            print(f"📂 Changing to project directory: {project_path}")
            os.chdir(project_path)
            print(f"📂 Current directory: {os.getcwd()}")

            # Use 'npm run dev' for development server
            print("🔧 Running: npm run dev")
            result = subprocess.run(['npm', 'run', 'dev'], cwd=os.getcwd())
            return result.returncode == 0

        except Exception as e:
            print(f"❌ Error starting dev server: {e}")
            return False
        finally:
            os.chdir(original_dir)

    def build_project(self, project_path):
        """Build the Next.js project for production."""

        print(f"\n🔨 Building project for production...")

        original_dir = os.getcwd()
        try:
            print(f"📂 Changing to project directory: {project_path}")
            os.chdir(project_path)
            print(f"📂 Current directory: {os.getcwd()}")

            print("🔧 Running: npm run build")
            result = subprocess.run(['npm', 'run', 'build'], cwd=os.getcwd())
            return result.returncode == 0

        except Exception as e:
            print(f"❌ Error building project: {e}")
            return False
        finally:
            os.chdir(original_dir)

    def start_production_server(self, project_path):
        """Start the Next.js production server (requires build first)."""

        print(f"\n🚀 Starting production server...")

        original_dir = os.getcwd()
        try:
            print(f"📂 Changing to project directory: {project_path}")
            os.chdir(project_path)
            print(f"📂 Current directory: {os.getcwd()}")

            # First check if build exists
            if not os.path.exists('.next'):
                print("❌ No production build found. Building first...")
                print("🔧 Running: npm run build")
                build_result = subprocess.run(
                    ['npm', 'run', 'build'], cwd=os.getcwd())
                if build_result.returncode != 0:
                    print("❌ Build failed!")
                    return False
                print("✅ Build completed successfully!")

            print("🔧 Running: npm start")
            result = subprocess.run(['npm', 'start'], cwd=os.getcwd())
            return result.returncode == 0

        except Exception as e:
            print(f"❌ Error starting production server: {e}")
            return False
        finally:
            os.chdir(original_dir)

    def create_project_structure(self, project_path):
        """Create additional project structure."""

        directories = [
            'src/components/common',
            'src/components/ui',
            'src/hooks',
            'src/utils',
            'src/services',
            'src/context',
            'src/assets/images',
            'src/assets/icons',
            'src/styles/globals',
            'public/images',
            'public/icons',
            'docs'
        ]

        print("📁 Creating additional project structure...")
        for directory in directories:
            dir_path = os.path.join(project_path, directory)
            try:
                os.makedirs(dir_path, exist_ok=True)
                print(f"Created: {directory}")
            except Exception as e:
                print(f"❌ Failed to create {directory}: {e}")

    def create_config_files(self, project_path, use_typescript=False):
        """Create additional configuration files."""

        # Prettier config
        prettier_config = {
            "semi": True,
            "trailingComma": "es5",
            "singleQuote": True,
            "printWidth": 80,
            "tabWidth": 2
        }

        # VS Code settings
        vscode_settings = {
            "editor.formatOnSave": True,
            "editor.defaultFormatter": "esbenp.prettier-vscode",
            "editor.codeActionsOnSave": {
                "source.fixAll.eslint": True
            }
        }

        try:
            import json

            # Create .prettierrc
            with open(os.path.join(project_path, '.prettierrc'), 'w') as f:
                json.dump(prettier_config, f, indent=2)

            # Create .vscode directory and settings
            vscode_dir = os.path.join(project_path, '.vscode')
            os.makedirs(vscode_dir, exist_ok=True)

            with open(os.path.join(vscode_dir, 'settings.json'), 'w') as f:
                json.dump(vscode_settings, f, indent=2)

            print("✅ Configuration files created")

        except Exception as e:
            print(f"❌ Failed to create config files: {e}")

    def show_project_info(self, project_path, use_typescript=False):
        """Show information about the created Next.js project."""
        lang_str = "TypeScript" if use_typescript else "JavaScript"
        print(f"\n🎉 Next.js ({lang_str}) project created successfully!")
        print(f"📁 Location: {project_path}")
        print(f"\n📋 Next steps:")
        print(f"1. cd {project_path.name}")
        print(f"2. npm run dev (to start development server)")
        print(f"3. Open http://localhost:3000 in your browser")
        print(f"\n📚 Available commands:")
        print(f"  npm run dev    - Start Next.js development server")
        print(f"  npm run build  - Build for production")
        print(f"  npm start      - Start production server (requires build first)")
        print(f"  npm run lint   - Run ESLint")

        print(f"\n🔧 Installed packages:")
        print(f"  • @tanstack/react-query (updated from react-query)")
        print(f"  • Material-UI with React 19 compatibility")
        print(f"  • Framer Motion for animations")
        print(f"  • React Hook Form with Yup validation")
        print(f"  • Zustand for state management")
        print(f"  • Axios for HTTP requests")

        print(f"\n💡 Tips:")
        print(f"  • Use --legacy-peer-deps if you encounter peer dependency issues")
        print(f"  • @tanstack/react-query replaces the old react-query package")
        print(f"  • All packages are compatible with React 19")

    def setup_complete_project(self, app_name, use_typescript=False, setup_options=None):
        """Complete project setup with all configurations."""

        # Create the Next.js project
        if not self.create_project(app_name, use_typescript, setup_options):
            return False

        project_path = Path.cwd() / app_name

        # Create additional structure
        self.create_project_structure(project_path)

        # Install compatible packages - this is where the main fix is needed
        print(f"\n📦 Installing packages in: {project_path}")
        if not self.install_compatible_packages(project_path, use_typescript):
            print("⚠️  Package installation had issues, but project structure is ready")
            print("💡 You can manually install packages by running:")
            print(f"   cd {app_name}")
            print(
                "   npm install --legacy-peer-deps @tanstack/react-query axios zustand react-hook-form")

        # Create config files
        self.create_config_files(project_path, use_typescript)

        # Show project info
        self.show_project_info(project_path, use_typescript)

        return True

    def fix_failed_installation(self, project_path):
        """Fix failed package installation by installing compatible versions."""

        original_dir = os.getcwd()

        try:
            print(f"🔧 Fixing package installation in: {project_path}")
            os.chdir(project_path)

            # Remove node_modules and package-lock.json to start fresh
            print("🧹 Cleaning up previous installation...")
            if os.path.exists('node_modules'):
                import shutil
                shutil.rmtree('node_modules')
            if os.path.exists('package-lock.json'):
                os.remove('package-lock.json')

            # Install the fixed packages
            # Assume TypeScript
            return self.install_compatible_packages('.', True)

        except Exception as e:
            print(f"❌ Error fixing installation: {e}")
            return False
        finally:
            os.chdir(original_dir)

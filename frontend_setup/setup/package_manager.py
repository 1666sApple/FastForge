"""
Package installation and management functionality
"""

from core.base import BaseSetup


class PackageManager(BaseSetup):
    """Handles package installation and management."""

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

    def install_packages(self, project_path, packages, dev=False):
        """Install custom packages."""
        if not packages:
            return True

        flag = '--save-dev' if dev else '--save'
        command = ['npm', 'install', flag] + packages
        return self.run_command(command, cwd=project_path)

"""
Styling setup functionality (Tailwind CSS, etc.)
"""

from core.base import BaseSetup
from utils.file_operations import FileOperations


class StylingSetup(BaseSetup):
    """Handles styling setup for React projects."""

    def __init__(self):
        super().__init__()
        self.file_ops = FileOperations()

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

        # Create/update CSS file
        css_content = '''@tailwind base;
@tailwind components;
@tailwind utilities;'''

        config_path = project_path / 'tailwind.config.js'
        css_path = project_path / 'src' / 'index.css'

        if (self.file_ops.write_file(config_path, tailwind_config) and
                self.file_ops.write_file(css_path, css_content)):
            print("✅ Tailwind CSS setup completed")
            return True

        return False

    def setup_styled_components(self, project_path):
        """Set up styled-components."""
        print(f"\n💅 Setting up styled-components...")
        return self.run_command(['npm', 'install', 'styled-components'], cwd=project_path)

    def setup_emotion(self, project_path):
        """Set up Emotion CSS-in-JS."""
        print(f"\n😊 Setting up Emotion...")
        packages = ['@emotion/react', '@emotion/styled']
        return self.run_command(['npm', 'install'] + packages, cwd=project_path)

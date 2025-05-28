"""
Vite specific setup functionality
"""

from core.base import BaseSetup


class ViteSetup(BaseSetup):
    """Handles Vite React project creation."""

    def create_project(self, app_name, use_typescript=False, setup_options=None):
        """Create a new React app using Vite."""
        print(f"\n🚀 Creating Vite React app: {app_name}")

        template = 'react-ts' if use_typescript else 'react'
        command = ['npm', 'create', 'vite@latest',
                   app_name, '--', '--template', template]

        if self.run_command(command):
            print(f"\n📦 Installing dependencies for {app_name}...")
            app_path = self.current_dir / app_name
            return self.run_command(['npm', 'install'], cwd=app_path)

        return False

    def show_project_info(self, project_path, use_typescript=False):
        """Show information about the created Vite React project."""
        lang_str = "TypeScript" if use_typescript else "JavaScript"
        print(f"\n🎉 Vite React ({lang_str}) project created successfully!")
        print(f"📁 Location: {project_path}")
        print(f"\n📋 Next steps:")
        print(f"1. cd {project_path.name}")
        print(f"2. npm run dev (to start development server)")
        print(f"3. Open http://localhost:5173 in your browser")
        print(f"\n📚 Available commands:")
        print(f"  npm run dev    - Start development server")
        print(f"  npm run build  - Build for production")
        print(f"  npm run preview - Preview production build")

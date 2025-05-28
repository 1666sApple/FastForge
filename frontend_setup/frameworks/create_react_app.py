"""
Create React App specific setup functionality
"""

from core.base import BaseSetup


class CreateReactAppSetup(BaseSetup):
    """Handles Create React App project creation."""

    def create_project(self, app_name, use_typescript=False, setup_options=None):
        """Create a new React app using create-react-app."""
        print(f"\n🚀 Creating React app: {app_name}")

        command = ['npx', 'create-react-app', app_name]

        if use_typescript:
            command.extend(['--template', 'typescript'])
        elif setup_options and setup_options.get('template'):
            command.extend(['--template', setup_options['template']])

        return self.run_command(command)

    def show_project_info(self, project_path, use_typescript=False):
        """Show information about the created Create React App project."""
        lang_str = "TypeScript" if use_typescript else "JavaScript"
        print(
            f"\n🎉 Create React App ({lang_str}) project created successfully!")
        print(f"📁 Location: {project_path}")
        print(f"\n📋 Next steps:")
        print(f"1. cd {project_path.name}")
        print(f"2. npm start (to start development server)")
        print(f"3. Open http://localhost:3000 in your browser")
        print(f"\n📚 Available commands:")
        print(f"  npm start      - Start development server")
        print(f"  npm run build  - Build for production")
        print(f"  npm test       - Run tests")

"""
Project structure creation functionality
"""

from core.base import BaseSetup


class ProjectStructureManager(BaseSetup):
    """Handles project directory structure creation."""

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
        self._create_component_index_files(project_path)
        return True

    def _create_component_index_files(self, project_path):
        """Create index files for component directories."""
        component_dirs = ['src/components/common', 'src/components/ui']
        for comp_dir in component_dirs:
            index_path = project_path / comp_dir / 'index.js'
            with open(index_path, 'w') as f:
                f.write('// Export components from this directory\n')

    def create_custom_structure(self, project_path, directories):
        """Create custom directory structure."""
        print(f"\n📁 Creating custom project structure...")

        for directory in directories:
            dir_path = project_path / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"Created: {directory}")

        return True

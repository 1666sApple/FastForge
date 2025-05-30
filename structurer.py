"""
GenAI Project Builder CLI
Creates complete full-stack GenAI projects with Python backend and React frontend.
"""

import os
import sys
from pathlib import Path
import subprocess

# Import the builder modules
from python_builder import PythonProjectBuilder
from react_setup import ReactSetupCLI


class GenAIProjectCLI:
    """Main CLI class for creating GenAI projects."""

    def __init__(self):
        """Initialize the GenAI project CLI."""
        self.current_dir = Path.cwd()
        self.python_builder = None
        self.react_cli = ReactSetupCLI()

    def sanitize_name(self, name):
        """Sanitize project name to be valid for both Python and React."""
        return "".join(c for c in name if c.isalnum() or c in "-_").lower()

    def create_full_stack_project(self, project_name, base_path="."):
        """Create a full-stack GenAI project with Python backend and React frontend."""
        print("Creating full-stack GenAI project...")
        print(f"Project name: {project_name}")
        print(f"Base path: {base_path}")

        base_path = Path(base_path).resolve()
        project_root = base_path / project_name

        # Create main project directory
        project_root.mkdir(parents=True, exist_ok=True)
        print(f"Created main project directory: {project_root}")

        # Create backend
        backend_path = project_root / "backend"
        print("\nCreating Python backend...")

        # Initialize python builder with correct paths
        original_cwd = os.getcwd()
        os.chdir(project_root)

        try:
            self.python_builder = PythonProjectBuilder("backend", ".")
            self.python_builder.create_directory_structure()
            self.python_builder.create_python_files()
            self.python_builder.create_config_files()
            self.python_builder.create_gitkeep_files()
            print("Backend created successfully")
        except Exception as e:
            print(f"Error creating backend: {e}")
            os.chdir(original_cwd)
            return False

        # Get React configuration from user
        print("\n" + "="*50)
        print("Frontend Configuration")
        print("="*50)

        # Choose React framework
        framework_choice = self.get_react_framework_choice()

        # Choose language
        use_typescript = self.get_language_choice()

        # Get additional options
        setup_options = self.get_react_setup_options(framework_choice)

        # Create frontend
        frontend_name = "frontend"
        print(f"\nCreating React frontend...")

        try:
            success = self.setup_react_frontend(
                frontend_name, framework_choice, use_typescript, setup_options)

            if not success:
                print("Failed to create frontend")
                os.chdir(original_cwd)
                return False

        except Exception as e:
            print(f"Error creating frontend: {e}")
            os.chdir(original_cwd)
            return False
        finally:
            os.chdir(original_cwd)

        # Create additional project files
        self.create_project_files(project_root, project_name)

        return True

    def create_backend_only(self, project_name, base_path="."):
        """Create only Python backend."""
        print("Creating Python GenAI backend...")

        self.python_builder = PythonProjectBuilder(project_name, base_path)

        try:
            self.python_builder.build_project()
            return True
        except Exception as e:
            print(f"Error creating backend: {e}")
            return False

    def get_react_framework_choice(self):
        """Get user's React framework choice."""
        print("\n🛠️ Choose React framework:")
        print("1. Create React App (CRA) - Traditional React setup")
        print("2. Next.js - Full-stack React framework")
        print("3. Vite - Fast build tool for React")

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

    def get_react_setup_options(self, framework_choice):
        """Get additional React setup options from user."""
        setup_options = {}

        # Tailwind CSS option
        if framework_choice == '2':  # Next.js
            setup_options['tailwind'] = input(
                "\n🎨 Use Tailwind CSS? (y/N): ").strip().lower() in ['y', 'yes']
        else:
            setup_options['tailwind'] = input(
                "\n🎨 Setup Tailwind CSS? (y/N): ").strip().lower() in ['y', 'yes']

        # Additional project structure
        setup_options['structure'] = input(
            "📁 Create additional project structure (recommended)? (Y/n): ").strip().lower() not in ['n', 'no']

        # Common packages
        setup_options['packages'] = input(
            "📦 Install common packages (axios, react-router-dom, etc.)? (Y/n): ").strip().lower() not in ['n', 'no']

        return setup_options

    def setup_react_frontend(self, frontend_name, framework_choice, use_typescript, setup_options):
        """Set up React frontend with chosen configuration."""
        success = False
        frontend_path = Path.cwd() / frontend_name

        print(f"\n🚀 Creating React frontend...")

        if framework_choice == '1':
            # Create React App
            template = 'typescript' if use_typescript else None
            success = self.react_cli.create_react_app(
                frontend_name, use_typescript, template)
            print("Created with Create React App")

        elif framework_choice == '2':
            # Next.js App
            tailwind = setup_options.get('tailwind', False)
            success = self.react_cli.create_next_app(
                frontend_name, use_typescript, tailwind)
            print("Created with Next.js")

        elif framework_choice == '3':
            # Vite React App
            success = self.react_cli.create_vite_react_app(
                frontend_name, use_typescript)
            print("Created with Vite")

        if success and frontend_path.exists():
            print(f"✅ Frontend created at: {frontend_path}")

            # Apply additional setup options
            if setup_options.get('structure', False):
                print("📁 Creating additional project structure...")
                self.react_cli.create_project_structure(frontend_path)

            if setup_options.get('packages', False):
                print("📦 Installing common packages...")
                self.react_cli.install_common_packages(frontend_path)
                self.react_cli.install_dev_packages(
                    frontend_path, use_typescript)

            # Setup Tailwind if requested and not already set up by Next.js
            if setup_options.get('tailwind', False) and framework_choice != '2':
                print("🎨 Setting up Tailwind CSS...")
                self.react_cli.setup_tailwind(frontend_path)
            elif framework_choice == '2' and setup_options.get('tailwind', False):
                print("🎨 Tailwind CSS already configured with Next.js")

            return True

        return success

    def create_frontend_only(self, project_name, base_path=".", interactive=True):
        """Create only React frontend with interactive options."""
        print(f"Creating React frontend...")

        base_path_obj = Path(base_path).resolve()
        original_cwd = os.getcwd()
        os.chdir(base_path_obj)

        try:
            if interactive:
                # Get configuration from user
                print("\n" + "="*50)
                print("Frontend Configuration")
                print("="*50)

                framework_choice = self.get_react_framework_choice()
                use_typescript = self.get_language_choice()
                setup_options = self.get_react_setup_options(framework_choice)
            else:
                # Default configuration
                framework_choice = '3'  # Vite
                use_typescript = True
                setup_options = {
                    'tailwind': True,
                    'structure': True,
                    'packages': True
                }

            success = self.setup_react_frontend(
                project_name, framework_choice, use_typescript, setup_options)

            return success

        except Exception as e:
            print(f"Error creating frontend: {e}")
            return False
        finally:
            os.chdir(original_cwd)

    def create_project_files(self, project_root, project_name):
        """Create additional project files for full-stack setup."""

        # Main README
        readme_content = f"""# {project_name}

A full-stack GenAI project with Python backend and React frontend.

## Project Structure

```
{project_name}/
├── backend/          # Python GenAI backend
│   ├── src/         # Source code
│   ├── data/        # Data files
│   ├── models/      # ML models
│   ├── tests/       # Tests
│   └── scripts/     # Utility scripts
├── frontend/        # React frontend
│   ├── src/         # Source code
│   ├── public/      # Static files
│   └── package.json # Dependencies
├── docs/           # Documentation
└── docker-compose.yml # Docker setup
```

## Quick Start

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install -r requirements.txt
python main.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Docker Setup
```bash
docker-compose up --build
```

## Development

### Backend
- Main API: `backend/src/api/endpoints.py`
- Models: `backend/src/models/`
- Data processing: `backend/src/data/`
- Configuration: `backend/src/config/settings.py`

### Frontend
- Components: `frontend/src/components/`
- Pages: `frontend/src/pages/`
- Services: `frontend/src/services/`
- Utilities: `frontend/src/utils/`

## API Endpoints

- GET `/` - Welcome message
- GET `/health` - Health check
- POST `/api/v1/predict` - ML predictions
- GET `/api/v1/models` - List available models

## Tech Stack

### Backend
- Python 3.8+
- FastAPI
- Pydantic
- scikit-learn / PyTorch / TensorFlow
- SQLAlchemy (optional)

### Frontend
- React 18+
- TypeScript
- Vite
- Tailwind CSS
- Axios
- React Router

## License

MIT License
"""

        readme_path = project_root / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)

        # Docker compose for full stack
        docker_compose_content = f"""version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - PROJECT_NAME={project_name} Backend
      - API_HOST=0.0.0.0
      - API_PORT=8000
    volumes:
      - ./backend/data:/app/data
      - ./backend/models:/app/models
      - ./backend/logs:/app/logs
    networks:
      - genai-network

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8000
    depends_on:
      - backend
    networks:
      - genai-network

networks:
  genai-network:
    driver: bridge
"""

        docker_compose_path = project_root / "docker-compose.yml"
        with open(docker_compose_path, 'w', encoding='utf-8') as f:
            f.write(docker_compose_content)

        # Frontend Dockerfile
        frontend_dockerfile = """FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
"""

        frontend_docker_path = project_root / "frontend" / "Dockerfile"
        with open(frontend_docker_path, 'w', encoding='utf-8') as f:
            f.write(frontend_dockerfile)

        # Create docs directory
        docs_dir = project_root / "docs"
        docs_dir.mkdir(exist_ok=True)

        api_docs = """# API Documentation

## Authentication
Currently no authentication is required.

## Endpoints

### Health Check
- **GET** `/health`
- Returns API health status

### Predictions
- **POST** `/api/v1/predict`
- Make predictions using trained models
- Body: `{"data": {...}}`
- Returns: `{"prediction": ..., "confidence": 0.95}`

### Models
- **GET** `/api/v1/models`
- List available models
- Returns: `{"models": ["model1", "model2"]}`

## Error Responses
All endpoints return standard HTTP status codes:
- 200: Success
- 400: Bad Request
- 500: Internal Server Error
"""

        api_docs_path = docs_dir / "api.md"
        with open(api_docs_path, 'w', encoding='utf-8') as f:
            f.write(api_docs)

        print(f"Created project documentation in {docs_dir}")

    def show_project_summary(self, project_root, project_type):
        """Show summary of created project."""
        print(f"\nProject '{project_root.name}' created successfully!")
        print(f"Location: {project_root}")
        print(f"Type: {project_type}")

        if project_type == "Full-Stack":
            print(f"\nProject structure:")
            print(f"  {project_root.name}/")
            print(f"  ├── backend/     (Python GenAI API)")
            print(f"  ├── frontend/    (React TypeScript)")
            print(f"  ├── docs/        (Documentation)")
            print(f"  └── docker-compose.yml")

            print(f"\nNext steps:")
            print(f"1. cd {project_root.name}")
            print(f"2. Backend setup:")
            print(f"   cd backend")
            print(f"   python -m venv venv")
            print(f"   source venv/bin/activate")
            print(f"   pip install -r requirements.txt")
            print(f"   python main.py")
            print(f"3. Frontend setup (in new terminal):")
            print(f"   cd frontend")
            print(f"   npm install")
            print(f"   npm run dev")
            print(f"4. Or use Docker: docker-compose up --build")

        elif project_type == "Backend":
            print(f"\nNext steps:")
            print(f"1. cd {project_root.name}")
            print(f"2. python -m venv venv")
            print(f"3. source venv/bin/activate")
            print(f"4. pip install -r requirements.txt")
            print(f"5. python main.py")

        elif project_type == "Frontend":
            print(f"\nNext steps:")
            print(f"1. cd {project_root.name}")
            print(f"2. npm install")
            print(f"3. npm run dev")
            print(f"4. Open http://localhost:3000")

    def interactive_setup(self):
        """Interactive setup wizard."""
        print("=== GenAI Project Builder ===")
        print(
            "Create production-ready GenAI projects with Python backend and React frontend")
        print()

        # Check prerequisites for full-stack
        node_available = self.react_cli.check_node_npm()
        python_available = self.check_python()

        print("\nPrerequisites check:")
        if python_available:
            print("✅ Python: Available")
        else:
            print("❌ Python: Not found")

        if node_available:
            print("✅ Node.js/npm: Available")
        else:
            print("❌ Node.js/npm: Not found")

        print(f"\nProject types available:")
        print("1. Full-Stack (Python backend + React frontend)")
        print("2. Backend only (Python GenAI API)")
        print("3. Frontend only (React with framework choice)")

        # Get project type
        while True:
            choice = input("\nSelect project type (1-3): ").strip()
            if choice in ['1', '2', '3']:
                break
            print("Invalid choice. Please enter 1, 2, or 3.")

        # Validate prerequisites based on choice
        if choice == '1' and not (python_available and node_available):
            print(
                "❌ Full-stack requires both Python and Node.js. Please install missing prerequisites.")
            return
        elif choice == '2' and not python_available:
            print("❌ Backend requires Python. Please install Python first.")
            return
        elif choice == '3' and not node_available:
            print("❌ Frontend requires Node.js and npm. Please install them first.")
            return

        # Get project details
        project_name = input("\nEnter project name: ").strip()
        if not project_name:
            print("Project name cannot be empty.")
            return

        project_name = self.sanitize_name(project_name)

        base_path = input(
            "Enter base directory (press Enter for current): ").strip()
        if not base_path:
            base_path = "."

        base_path_obj = Path(base_path).resolve()
        project_path = base_path_obj / project_name

        print(f"\n" + "="*50)
        print("Project Configuration Summary")
        print("="*50)
        print(f"Name: {project_name}")
        print(f"Location: {project_path}")

        if choice == '1':
            print(f"Type: Full-Stack (Python + React)")
        elif choice == '2':
            print(f"Type: Backend only (Python)")
        else:
            print(f"Type: Frontend only (React)")

        confirm = input(
            "\nProceed with project creation? (Y/n): ").strip().lower()
        if confirm in ['n', 'no']:
            print("Project creation cancelled.")
            return

        # Create project based on choice
        success = False
        project_type = ""

        try:
            if choice == '1':
                success = self.create_full_stack_project(
                    project_name, base_path)
                project_type = "Full-Stack"
            elif choice == '2':
                success = self.create_backend_only(project_name, base_path)
                project_type = "Backend"
            elif choice == '3':
                success = self.create_frontend_only(
                    project_name, base_path, interactive=True)
                project_type = "Frontend"

            if success:
                self.show_project_summary(project_path, project_type)
            else:
                print("❌ Project creation failed. Please check the errors above.")

        except KeyboardInterrupt:
            print("\n\nProject creation cancelled by user.")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

    def show_project_summary(self, project_root, project_type):
        """Show summary of created project."""
        print(f"\n" + "="*60)
        print(f"🎉 Project '{project_root.name}' created successfully!")
        print("="*60)
        print(f"📁 Location: {project_root}")
        print(f"🏗️  Type: {project_type}")

        if project_type == "Full-Stack":
            print(f"\n📂 Project structure:")
            print(f"  {project_root.name}/")
            print(f"  ├── backend/         (Python GenAI API)")
            print(f"  ├── frontend/        (React Application)")
            print(f"  ├── docs/            (Documentation)")
            print(f"  ├── docker-compose.yml")
            print(f"  └── README.md")

            print(f"\n🚀 Next steps:")
            print(f"1. cd {project_root.name}")
            print(f"")
            print(f"2. Start Backend:")
            print(f"   cd backend")
            print(f"   python -m venv venv")
            print(f"   source venv/bin/activate  # Windows: venv\\Scripts\\activate")
            print(f"   pip install -r requirements.txt")
            print(f"   python main.py")
            print(f"")
            print(f"3. Start Frontend (in new terminal):")
            print(f"   cd frontend")
            print(f"   npm install")
            print(f"   npm run dev")
            print(f"")
            print(f"4. Or use Docker:")
            print(f"   docker-compose up --build")
            print(f"")
            print(f"🌐 URLs:")
            print(f"   Backend API: http://localhost:8000")
            print(f"   Frontend: http://localhost:3000")

        elif project_type == "Backend":
            print(f"\n🚀 Next steps:")
            print(f"1. cd {project_root.name}")
            print(f"2. python -m venv venv")
            print(f"3. source venv/bin/activate  # Windows: venv\\Scripts\\activate")
            print(f"4. pip install -r requirements.txt")
            print(f"5. python main.py")
            print(f"")
            print(f"🌐 API will be available at: http://localhost:8000")

        elif project_type == "Frontend":
            print(f"\n🚀 Next steps:")
            print(f"1. cd {project_root.name}")
            print(f"2. npm install")
            print(f"3. npm run dev")
            print(f"")
            print(f"🌐 App will be available at: http://localhost:3000")

        print(f"\n📚 Check README.md for detailed information!")
        print("="*60)

    def check_python(self):
        """Check if Python is available."""
        try:
            result = subprocess.run(
                ['python', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                return True
            else:
                # Try python3
                result = subprocess.run(
                    ['python3', '--version'], capture_output=True, text=True)
                return result.returncode == 0
        except FileNotFoundError:
            return False


def main():
    """Main entry point."""
    cli = GenAIProjectCLI()

    if len(sys.argv) > 1:
        # Command line arguments (for future CLI expansion)
        print("Command line mode not yet implemented. Using interactive mode.")

    cli.interactive_setup()


if __name__ == "__main__":
    main()

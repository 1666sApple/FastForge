"""
Python GenAI Project Structure Builder
Creates standardized Python project structures for GenAI/ML projects.
"""

import os
from pathlib import Path


class PythonProjectBuilder:
    """Class to build Python GenAI project structures."""

    def __init__(self, project_name, base_path="."):
        """Initialize project builder."""
        self.project_name = project_name
        self.base_path = Path(base_path).resolve()
        self.project_path = self.base_path / project_name

    def create_directory_structure(self):
        """Create the main directory structure."""
        directories = [
            # Main project structure
            "",  # Root project directory
            "src",
            "src/models",
            "src/data",
            "src/utils",
            "src/api",
            "src/services",
            "src/config",

            # Data directories
            "data",
            "data/raw",
            "data/processed",
            "data/external",

            # Model directories
            "models",
            "models/trained",
            "models/checkpoints",

            # Notebooks and experiments
            "notebooks",
            "experiments",

            # Documentation
            "docs",

            # Tests
            "tests",
            "tests/unit",
            "tests/integration",

            # Scripts
            "scripts",

            # Configuration
            "config",

            # Static files
            "static",
            "static/assets",

            # Logs
            "logs",
        ]

        print(f"Creating project structure for: {self.project_name}")

        for directory in directories:
            dir_path = self.project_path / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {dir_path}")

    def create_python_files(self):
        """Create essential Python files with basic structure."""
        python_files = {
            # Main entry points
            "main.py": self.get_main_py_template(),
            "app.py": self.get_app_py_template(),

            # Source files
            "src/__init__.py": "",
            "src/models/__init__.py": "",
            "src/models/base_model.py": self.get_base_model_template(),
            "src/data/__init__.py": "",
            "src/data/data_loader.py": self.get_data_loader_template(),
            "src/utils/__init__.py": "",
            "src/utils/helpers.py": self.get_helpers_template(),
            "src/api/__init__.py": "",
            "src/api/endpoints.py": self.get_api_template(),
            "src/services/__init__.py": "",
            "src/services/model_service.py": self.get_model_service_template(),
            "src/config/__init__.py": "",
            "src/config/settings.py": self.get_settings_template(),

            # Test files
            "tests/__init__.py": "",
            "tests/test_models.py": self.get_test_template(),
            "tests/unit/__init__.py": "",
            "tests/integration/__init__.py": "",

            # Scripts
            "scripts/train_model.py": self.get_train_script_template(),
            "scripts/evaluate_model.py": self.get_evaluate_script_template(),
        }

        for file_path, content in python_files.items():
            full_path = self.project_path / file_path
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Created file: {full_path}")

    def create_config_files(self):
        """Create configuration and setup files."""
        config_files = {
            # Empty requirement files as requested
            "requirements.txt": "",
            "requirements-dev.txt": "",

            # Empty README as requested
            "README.md": "",

            # Other config files
            ".env.example": self.get_env_template(),
            ".gitignore": self.get_gitignore_template(),
            "Dockerfile": self.get_dockerfile_template(),
            "docker-compose.yml": self.get_docker_compose_template(),
            "setup.py": self.get_setup_py_template(),
            "pyproject.toml": self.get_pyproject_toml_template(),
            "config/model_config.yaml": self.get_model_config_template(),
            "config/data_config.yaml": self.get_data_config_template(),
        }

        for file_path, content in config_files.items():
            full_path = self.project_path / file_path
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Created file: {full_path}")

    # Template methods
    def get_main_py_template(self):
        return '''#!/usr/bin/env python3
"""
Main entry point for the application.
"""

from src.config.settings import Settings
from src.services.model_service import ModelService


def main():
    """Main function."""
    settings = Settings()
    model_service = ModelService(settings)

    print(f"Starting {settings.PROJECT_NAME}...")
    # Add your main logic here


if __name__ == "__main__":
    main()
'''

    def get_app_py_template(self):
        return '''#!/usr/bin/env python3
"""
FastAPI application entry point.
"""

from fastapi import FastAPI
from src.api.endpoints import router
from src.config.settings import Settings

settings = Settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="GenAI API",
    version="1.0.0"
)

app.include_router(router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
'''

    def get_base_model_template(self):
        return '''"""
Base model class for ML models.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseModel(ABC):
    """Abstract base class for all models."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model = None
        self.is_trained = False

    @abstractmethod
    def train(self, X_train, y_train):
        """Train the model."""
        pass

    @abstractmethod
    def predict(self, X):
        """Make predictions."""
        pass

    @abstractmethod
    def save_model(self, path: str):
        """Save the model."""
        pass

    @abstractmethod
    def load_model(self, path: str):
        """Load the model."""
        pass
'''

    def get_data_loader_template(self):
        return '''"""
Data loading utilities.
"""

import pandas as pd
from typing import Tuple, Optional
from pathlib import Path


class DataLoader:
    """Class for loading and preprocessing data."""

    def __init__(self, data_path: str):
        self.data_path = Path(data_path)

    def load_csv(self, filename: str) -> pd.DataFrame:
        """Load CSV file."""
        file_path = self.data_path / filename
        return pd.read_csv(file_path)

    def load_json(self, filename: str) -> dict:
        """Load JSON file."""
        import json
        file_path = self.data_path / filename
        with open(file_path, 'r') as f:
            return json.load(f)

    def split_data(self, df: pd.DataFrame, test_size: float = 0.2) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Split data into train and test sets."""
        from sklearn.model_selection import train_test_split
        return train_test_split(df, test_size=test_size, random_state=42)
'''

    def get_helpers_template(self):
        return '''"""
Utility helper functions.
"""

import logging
from pathlib import Path
from typing import Any, Dict


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """Set up logging configuration."""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)


def ensure_dir(path: str) -> Path:
    """Ensure directory exists."""
    path_obj = Path(path)
    path_obj.mkdir(parents=True, exist_ok=True)
    return path_obj


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    import yaml
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)
'''

    def get_api_template(self):
        return '''"""
API endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter()


class PredictionRequest(BaseModel):
    data: Dict[str, Any]


class PredictionResponse(BaseModel):
    prediction: Any
    confidence: float


@router.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Make a prediction."""
    try:
        # Add your prediction logic here
        prediction = "sample_prediction"
        confidence = 0.95

        return PredictionResponse(
            prediction=prediction,
            confidence=confidence
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models")
async def list_models():
    """List available models."""
    return {"models": ["model1", "model2"]}
'''

    def get_model_service_template(self):
        return '''"""
Model service for handling ML operations.
"""

from typing import Any, Dict, Optional
from src.models.base_model import BaseModel


class ModelService:
    """Service for managing ML models."""

    def __init__(self, settings):
        self.settings = settings
        self.models: Dict[str, BaseModel] = {}

    def load_model(self, model_name: str, model_path: str) -> None:
        """Load a model."""
        # Implementation depends on your specific model type
        pass

    def predict(self, model_name: str, data: Any) -> Any:
        """Make prediction using specified model."""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found")

        return self.models[model_name].predict(data)

    def get_available_models(self) -> list:
        """Get list of available models."""
        return list(self.models.keys())
'''

    def get_settings_template(self):
        return '''"""
Application settings and configuration.
"""

import os
from pathlib import Path


class Settings:
    """Application settings."""

    # Project info
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "GenAI Project")
    VERSION: str = "1.0.0"

    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    MODELS_DIR: Path = BASE_DIR / "models"
    LOGS_DIR: Path = BASE_DIR / "logs"

    # API settings
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))

    # Database (if needed)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")

    # ML settings
    MODEL_NAME: str = os.getenv("MODEL_NAME", "default_model")
    BATCH_SIZE: int = int(os.getenv("BATCH_SIZE", "32"))
    LEARNING_RATE: float = float(os.getenv("LEARNING_RATE", "0.001"))

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    def __init__(self):
        # Ensure directories exist
        self.DATA_DIR.mkdir(exist_ok=True)
        self.MODELS_DIR.mkdir(exist_ok=True)
        self.LOGS_DIR.mkdir(exist_ok=True)
'''

    def get_test_template(self):
        return '''"""
Tests for models.
"""

import unittest
from src.models.base_model import BaseModel


class TestModels(unittest.TestCase):
    """Test cases for models."""

    def setUp(self):
        """Set up test fixtures."""
        pass

    def test_model_initialization(self):
        """Test model initialization."""
        pass

    def test_model_training(self):
        """Test model training."""
        pass

    def test_model_prediction(self):
        """Test model prediction."""
        pass


if __name__ == '__main__':
    unittest.main()
'''

    def get_train_script_template(self):
        return '''#!/usr/bin/env python3
"""
Model training script.
"""

import argparse
from pathlib import Path
from src.config.settings import Settings
from src.data.data_loader import DataLoader


def train_model(config_path: str = None):
    """Train the model."""
    settings = Settings()
    data_loader = DataLoader(settings.DATA_DIR)

    print("Starting model training...")

    # Add your training logic here

    print("Training completed!")


def main():
    parser = argparse.ArgumentParser(description="Train ML model")
    parser.add_argument("--config", type=str, help="Path to config file")
    args = parser.parse_args()

    train_model(args.config)


if __name__ == "__main__":
    main()
'''

    def get_evaluate_script_template(self):
        return '''#!/usr/bin/env python3
"""
Model evaluation script.
"""

import argparse
from src.config.settings import Settings


def evaluate_model(model_path: str):
    """Evaluate the model."""
    settings = Settings()

    print(f"Evaluating model: {model_path}")

    # Add your evaluation logic here

    print("Evaluation completed!")


def main():
    parser = argparse.ArgumentParser(description="Evaluate ML model")
    parser.add_argument("--model", type=str, required=True, help="Path to model file")
    args = parser.parse_args()

    evaluate_model(args.model)


if __name__ == "__main__":
    main()
'''

    def get_env_template(self):
        return '''# Environment variables template
PROJECT_NAME=GenAI Project
API_HOST=0.0.0.0
API_PORT=8000
DATABASE_URL=sqlite:///./app.db
MODEL_NAME=default_model
BATCH_SIZE=32
LEARNING_RATE=0.001
LOG_LEVEL=INFO
'''

    def get_gitignore_template(self):
        return '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
logs/
*.log

# Environment variables
.env

# Data files
data/raw/*
data/processed/*
!data/raw/.gitkeep
!data/processed/.gitkeep

# Model files
models/trained/*
models/checkpoints/*
!models/trained/.gitkeep
!models/checkpoints/.gitkeep

# Jupyter
.ipynb_checkpoints/

# pytest
.pytest_cache/
.coverage
htmlcov/

# mypy
.mypy_cache/
'''

    def get_dockerfile_template(self):
        return '''FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
'''

    def get_docker_compose_template(self):
        return '''version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PROJECT_NAME=GenAI Project
      - API_HOST=0.0.0.0
      - API_PORT=8000
    volumes:
      - ./data:/app/data
      - ./models:/app/models
      - ./logs:/app/logs
'''

    def get_setup_py_template(self):
        return f'''from setuptools import setup, find_packages

setup(
    name="{self.project_name}",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        # Add your dependencies here
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="GenAI Project",
    python_requires=">=3.8",
)
'''

    def get_pyproject_toml_template(self):
        return f'''[build-system]
requires = ["setuptools>=45", "wheel", "setuptools_scm[toml]>=6.2"]
build-backend = "setuptools.build_meta"

[project]
name = "{self.project_name}"
version = "1.0.0"
description = "GenAI Project"
requires-python = ">=3.8"
dependencies = [
    # Add your dependencies here
]

[project.optional-dependencies]
dev = [
    "pytest",
    "black",
    "flake8",
    "mypy",
]

[tool.black]
line-length = 88
target-version = ['py38']

[tool.isort]
profile = "black"
'''

    def get_model_config_template(self):
        return '''# Model Configuration
model:
  name: "default_model"
  type: "classification"

training:
  batch_size: 32
  epochs: 100
  learning_rate: 0.001
  validation_split: 0.2

preprocessing:
  normalize: true
  scale: true

evaluation:
  metrics: ["accuracy", "precision", "recall", "f1"]
'''

    def get_data_config_template(self):
        return '''# Data Configuration
data:
  raw_path: "data/raw"
  processed_path: "data/processed"
  external_path: "data/external"

processing:
  remove_duplicates: true
  handle_missing: "drop"
  encoding: "utf-8"

features:
  categorical: []
  numerical: []
  target: "target"
'''

    def create_gitkeep_files(self):
        """Create .gitkeep files for empty directories."""
        gitkeep_dirs = [
            "data/raw",
            "data/processed",
            "data/external",
            "models/trained",
            "models/checkpoints",
            "logs",
            "static/assets"
        ]

        for dir_path in gitkeep_dirs:
            gitkeep_path = self.project_path / dir_path / ".gitkeep"
            gitkeep_path.touch()
            print(f"Created .gitkeep: {gitkeep_path}")

    def build_project(self):
        """Build the complete project structure."""
        print(f"Building Python GenAI project: {self.project_name}")
        print(f"Location: {self.project_path}")

        if self.project_path.exists():
            response = input(
                f"Directory {self.project_path} already exists. Continue? (y/N): ").strip().lower()
            if response not in ['y', 'yes']:
                print("Project creation cancelled.")
                return

        try:
            self.create_directory_structure()
            self.create_python_files()
            self.create_config_files()
            self.create_gitkeep_files()

            print(f"\n✅ Project '{self.project_name}' created successfully!")
            print(f"📁 Location: {self.project_path}")
            print("\n📋 Next steps:")
            print("1. cd into the project directory")
            print("2. Create a virtual environment: python -m venv venv")
            print(
                "3. Activate it: source venv/bin/activate (Linux/Mac) or venv\\Scripts\\activate (Windows)")
            print("4. Install dependencies: pip install -r requirements.txt")
            print("5. Start developing!")

        except Exception as e:
            print(f"❌ Error creating project: {e}")


def main():
    """Main function for standalone execution."""
    print("=== Python GenAI Project Builder ===")
    print("Creates standardized Python project structures for GenAI/ML projects")
    print()

    project_name = input("Enter project name: ").strip()
    if not project_name:
        print("Project name cannot be empty.")
        return

    # Sanitize project name
    project_name = "".join(
        c for c in project_name if c.isalnum() or c in "-_").lower()

    base_path = input(
        "Enter base directory (or press Enter for current directory): ").strip()
    if not base_path:
        base_path = "."

    print(f"\nProject name: {project_name}")
    print(f"Base directory: {os.path.abspath(base_path)}")

    confirm = input("\nProceed with project creation? (y/N): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("Project creation cancelled.")
        return

    try:
        builder = PythonProjectBuilder(project_name, base_path)
        builder.build_project()

    except Exception as e:
        print(f"\n❌ An error occurred: {e}")


if __name__ == "__main__":
    main()

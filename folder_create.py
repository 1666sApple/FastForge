import os

# Define the directory structure and corresponding placeholder content
structure = {
    "frontend_setup": {
        "__init__.py": "# Init for frontend_setup\n",
        ".py": "# Main parent component\n",
        "core": {
            "__init__.py": "# Init for core\n",
            "base.py": "# Base functionality\n",
            "validator.py": "# System validation\n"
        },
        "frameworks": {
            "__init__.py": "# Init for frameworks\n",
            "create_react_app.py": "# CRA specific functionality\n",
            "nextjs.py": "# Next.js specific functionality\n",
            "vite.py": "# Vite specific functionality\n"
        },
        "setup": {
            "__init__.py": "# Init for setup\n",
            "package_manager.py": "# Package installation\n",
            "project_structure.py": "# Directory structure creation\n",
            "styling.py": "# CSS/Styling setup (Tailwind, etc.)\n"
        },
        "utils": {
            "__init__.py": "# Init for utils\n",
            "command_runner.py": "# Command execution utilities\n",
            "file_operations.py": "# File system operations\n",
            "user_interface.py": "# CLI user interaction\n"
        },
        "config": {
            "__init__.py": "# Init for config\n"
        }
    }
}


def create_structure(base_path, tree):
    for name, content in tree.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, "w") as f:
                f.write(content)


# Set the base directory name
base_dir = "frontend_setup"
create_structure(".", structure)

"Directory structure created successfully."

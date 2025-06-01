"""
File operations utility functionality
"""

from pathlib import Path
import json
import shutil


class FileOperations:
    """Handles file system operations."""

    def __init__(self):
        """Initialize file operations handler."""
        pass

    def write_file(self, file_path, content):
        """Write content to a file."""
        try:
            file_path = Path(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"✅ Created file: {file_path}")
            return True
        except Exception as e:
            print(f"❌ Error writing file {file_path}: {e}")
            return False

    def read_file(self, file_path):
        """Read content from a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"❌ Error reading file {file_path}: {e}")
            return None

    def copy_file(self, source, destination):
        """Copy a file from source to destination."""
        try:
            shutil.copy2(source, destination)
            print(f"✅ Copied: {source} -> {destination}")
            return True
        except Exception as e:
            print(f"❌ Error copying file: {e}")
            return False

    def create_directory(self, dir_path):
        """Create a directory if it doesn't exist."""
        try:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            print(f"❌ Error creating directory {dir_path}: {e}")
            return False

    def file_exists(self, file_path):
        """Check if a file exists."""
        return Path(file_path).exists()

    def read_json(self, file_path):
        """Read JSON content from a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error reading JSON file {file_path}: {e}")
            return None

    def write_json(self, file_path, data):
        """Write JSON data to a file."""
        try:
            file_path = Path(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"✅ Created JSON file: {file_path}")
            return True
        except Exception as e:
            print(f"❌ Error writing JSON file {file_path}: {e}")
            return False

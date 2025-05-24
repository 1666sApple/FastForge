#!/usr/bin/env python3
"""
Directory Cleaner
Removes common cache and build folders from projects.
"""

import os
import shutil
from pathlib import Path


class DirectoryCleaner:
    """Class to handle cleaning of various project types."""

    # Common folders to clean
    PYTHON_CLEAN_TARGETS = [
        '__pycache__',
        '*.pyc',
        '*.pyo',
        '.pytest_cache',
        '.coverage',
        'htmlcov',
        '.tox',
        '.mypy_cache',
        '.ruff_cache',
        'dist',
        'build',
        '*.egg-info'
    ]

    REACT_CLEAN_TARGETS = [
        'node_modules',
        '.next',
        'dist',
        'build',
        '.cache',
        '.parcel-cache',
        '.nuxt',
        '.output',
        '.vite',
        'coverage'
    ]

    def __init__(self, root_dir):
        """Initialize cleaner with root directory."""
        self.root_dir = Path(root_dir).resolve()
        self.removed_count = 0
        self.removed_size = 0

    def get_directory_size(self, path):
        """Calculate total size of a directory."""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        total_size += os.path.getsize(filepath)
                    except (OSError, IOError):
                        pass
        except (OSError, IOError):
            pass
        return total_size

    def remove_folder(self, folder_path):
        """Remove a folder and track statistics."""
        try:
            if os.path.exists(folder_path):
                size = self.get_directory_size(folder_path)
                shutil.rmtree(folder_path)
                self.removed_count += 1
                self.removed_size += size
                print(f"Removed: {folder_path} ({size / (1024*1024):.2f} MB)")
                return True
        except Exception as e:
            print(f"Error removing {folder_path}: {e}")
        return False

    def clean_python_cache(self):
        """Remove Python cache files and folders."""
        print("\n--- Cleaning Python Cache ---")

        for root, dirs, files in os.walk(self.root_dir, topdown=False):
            # Remove __pycache__ directories
            if '__pycache__' in dirs:
                pycache_path = os.path.join(root, '__pycache__')
                self.remove_folder(pycache_path)

            # Remove other Python build/cache directories
            for target_dir in ['.pytest_cache', '.mypy_cache', '.ruff_cache', 'dist', 'build']:
                if target_dir in dirs:
                    target_path = os.path.join(root, target_dir)
                    self.remove_folder(target_path)

            # Remove .egg-info directories
            for dir_name in dirs[:]:  # Create a copy to modify during iteration
                if dir_name.endswith('.egg-info'):
                    egg_info_path = os.path.join(root, dir_name)
                    self.remove_folder(egg_info_path)

            # Remove .pyc and .pyo files
            for file_name in files:
                if file_name.endswith(('.pyc', '.pyo')):
                    file_path = os.path.join(root, file_name)
                    try:
                        os.remove(file_path)
                        print(f"Removed: {file_path}")
                    except Exception as e:
                        print(f"Error removing {file_path}: {e}")

    def clean_react_cache(self):
        """Remove React/Node.js cache files and folders."""
        print("\n--- Cleaning React/Node Cache ---")

        for root, dirs, files in os.walk(self.root_dir, topdown=False):
            # Remove common React/Node build directories
            for target_dir in self.REACT_CLEAN_TARGETS:
                if target_dir in dirs:
                    target_path = os.path.join(root, target_dir)
                    self.remove_folder(target_path)

    def clean_all(self):
        """Clean both Python and React cache."""
        print(f"Cleaning directory: {self.root_dir}")
        initial_count = self.removed_count
        initial_size = self.removed_size

        self.clean_python_cache()
        self.clean_react_cache()

        print(f"\n--- Cleaning Summary ---")
        print(f"Folders removed: {self.removed_count - initial_count}")
        print(
            f"Space freed: {(self.removed_size - initial_size) / (1024*1024):.2f} MB")


def main():
    """Main function for standalone execution."""
    print("=== Directory Cleaner ===")
    print("Removes Python cache (__pycache__, .pyc, etc.) and React cache (node_modules, .next, etc.)")
    print()

    while True:
        root_dir = input("Enter the directory path to clean: ").strip()

        if not root_dir:
            print("Please enter a valid directory path.")
            continue

        if not os.path.exists(root_dir):
            print(f"Directory '{root_dir}' does not exist.")
            continue

        if not os.path.isdir(root_dir):
            print(f"'{root_dir}' is not a directory.")
            continue

        break

    print(f"\nTarget directory: {os.path.abspath(root_dir)}")

    # Show cleaning options
    print("\nCleaning options:")
    print("1. Clean Python cache only")
    print("2. Clean React/Node cache only")
    print("3. Clean both (recommended)")

    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        if choice in ['1', '2', '3']:
            break
        print("Invalid choice. Please enter 1, 2, or 3.")

    confirm = input(f"\nProceed with cleaning? (y/N): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("Operation cancelled.")
        return

    try:
        cleaner = DirectoryCleaner(root_dir)

        if choice == '1':
            cleaner.clean_python_cache()
        elif choice == '2':
            cleaner.clean_react_cache()
        else:
            cleaner.clean_all()

        print("\n✅ Cleaning completed successfully!")

    except Exception as e:
        print(f"\n❌ An error occurred: {e}")


if __name__ == "__main__":
    main()

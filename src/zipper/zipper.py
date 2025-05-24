#!/usr/bin/env python3
"""
Directory Zipper
Creates zip archives of directories with optional cleaning.
"""

import os
import zipfile
from pathlib import Path
from datetime import datetime
from cleaner import DirectoryCleaner


class DirectoryZipper:
    """Class to handle zipping directories with cleaning options."""

    def __init__(self, source_dir):
        """Initialize zipper with source directory."""
        self.source_dir = Path(source_dir).resolve()
        self.exclude_patterns = set()

    def add_exclude_patterns(self, patterns):
        """Add patterns to exclude from zip."""
        if isinstance(patterns, str):
            patterns = [patterns]
        self.exclude_patterns.update(patterns)

    def should_exclude(self, file_path):
        """Check if file/directory should be excluded."""
        path_parts = Path(file_path).parts

        # Check if any part of the path matches exclude patterns
        for part in path_parts:
            if part in self.exclude_patterns:
                return True

        # Check common cache patterns
        cache_patterns = [
            '__pycache__', 'node_modules', '.next', '.git',
            '.vscode', '.idea', 'dist', 'build', '.cache'
        ]

        for pattern in cache_patterns:
            if pattern in path_parts:
                return True

        return False

    def create_zip(self, output_path=None, clean_first=False, compression_level=6):
        """
        Create zip archive of the source directory.

        Args:
            output_path: Path for output zip file
            clean_first: Whether to clean cache before zipping
            compression_level: ZIP compression level (0-9)
        """
        if clean_first:
            print("Cleaning directory before zipping...")
            cleaner = DirectoryCleaner(self.source_dir)
            cleaner.clean_all()

        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"{self.source_dir.name}_cleaned_{timestamp}.zip"

        total_files = 0
        compressed_files = 0

        print(f"\nCreating zip archive: {output_path}")

        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=compression_level) as zipf:
            for root, dirs, files in os.walk(self.source_dir):
                # Remove excluded directories from dirs list to avoid walking into them
                dirs[:] = [d for d in dirs if not self.should_exclude(
                    os.path.join(root, d))]

                for file in files:
                    file_path = os.path.join(root, file)

                    if self.should_exclude(file_path):
                        continue

                    # Calculate relative path from source directory
                    rel_path = os.path.relpath(
                        file_path, self.source_dir.parent)

                    try:
                        zipf.write(file_path, rel_path)
                        compressed_files += 1

                        if compressed_files % 100 == 0:
                            print(f"Compressed {compressed_files} files...")

                    except Exception as e:
                        print(
                            f"Warning: Could not add {file_path} to archive: {e}")

                    total_files += 1

        # Get final zip size
        zip_size = os.path.getsize(output_path)

        print(f"\n--- Zip Summary ---")
        print(f"Total files processed: {total_files}")
        print(f"Files compressed: {compressed_files}")
        print(f"Archive size: {zip_size / (1024*1024):.2f} MB")
        print(f"Archive location: {os.path.abspath(output_path)}")

        return output_path

    def create_clean_zip(self, output_path=None):
        """Create a zip archive after cleaning cache files."""
        return self.create_zip(output_path=output_path, clean_first=True)


def main():
    """Main function for standalone execution."""
    print("=== Directory Zipper ===")
    print("Creates zip archives with optional cache cleaning")
    print()

    while True:
        source_dir = input("Enter the directory path to zip: ").strip()

        if not source_dir:
            print("Please enter a valid directory path.")
            continue

        if not os.path.exists(source_dir):
            print(f"Directory '{source_dir}' does not exist.")
            continue

        if not os.path.isdir(source_dir):
            print(f"'{source_dir}' is not a directory.")
            continue

        break

    print(f"\nSource directory: {os.path.abspath(source_dir)}")

    # Zip options
    print("\nZip options:")
    print("1. Zip as-is (no cleaning)")
    print("2. Clean cache then zip (recommended)")

    while True:
        choice = input("\nEnter your choice (1-2): ").strip()
        if choice in ['1', '2']:
            break
        print("Invalid choice. Please enter 1 or 2.")

    # Custom output path
    output_path = input(
        "\nEnter output zip filename (or press Enter for auto-generated): ").strip()
    if not output_path:
        output_path = None

    # Compression level
    print("\nCompression levels:")
    print("1. Fast (level 1)")
    print("6. Balanced (level 6) - default")
    print("9. Maximum (level 9)")

    compression_input = input(
        "Enter compression level (1-9) or press Enter for default: ").strip()
    try:
        compression_level = int(compression_input) if compression_input else 6
        # Clamp to valid range
        compression_level = max(0, min(9, compression_level))
    except ValueError:
        compression_level = 6

    confirm = input(f"\nProceed with zipping? (y/N): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("Operation cancelled.")
        return

    try:
        zipper = DirectoryZipper(source_dir)

        if choice == '2':
            zip_path = zipper.create_clean_zip(output_path)
        else:
            zip_path = zipper.create_zip(
                output_path, clean_first=False, compression_level=compression_level)

        print("\n✅ Zip creation completed successfully!")

    except Exception as e:
        print(f"\n❌ An error occurred: {e}")


if __name__ == "__main__":
    main()

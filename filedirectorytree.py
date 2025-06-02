#!/usr/bin/env python3
import os
import subprocess

# Directories you want to exclude
EXCLUDED_DIRS = {
    "__pycache__", 
    "node_modules", 
    ".venv", 
    ".git", 
    "__pycache__", 
    "my-local-cache", 
    "files", 
    "dist", 
    "orgchar-view", 
    "logger", 
    "log", 
    "jobstore", 
    "AzureCredentials.py",
    "clear",
    "data-sync-flow.mermaid",
    "Scheduler_Flowchart.png",
    "system-architechture..excalidraw",
    "pyodbc-install-fedora.txt"
    }

def get_gitignored_files(root):
    """
    Get a set of gitignored file paths (relative to the repo root) using Git.
    """
    try:
        # Run git ls-files to list ignored and untracked files as per .gitignore.
        result = subprocess.run(
            ["git", "ls-files", "-i", "-o", "--exclude-standard"],
            cwd=root,
            capture_output=True,
            text=True,
            check=True
        )
        # Normalize paths to current OS style
        ignored = {os.path.normpath(line) for line in result.stdout.splitlines() if line.strip()}
        return ignored
    except subprocess.CalledProcessError:
        return set()
    except FileNotFoundError:
        # Git is not available.
        return set()

def tree(dir_path, prefix, repo_root, gitignored):
    """
    Recursively print a tree structure starting at `dir_path`.
    Files or directories whose relative path (to repo_root) is gitignored will be skipped.
    Directories in EXCLUDED_DIRS are also not recursed into.
    """
    try:
        entries = os.listdir(dir_path)
    except PermissionError:
        return

    # Sort entries: directories first then files, both case-insensitively.
    entries = sorted(entries, key=lambda s: (not os.path.isdir(os.path.join(dir_path, s)), s.lower()))
    
    # Filter entries: skip if the entry is in EXCLUDED_DIRS (if a directory) or is gitignored.
    filtered_entries = []
    for entry in entries:
        full_path = os.path.join(dir_path, entry)
        rel_path = os.path.normpath(os.path.relpath(full_path, repo_root))
        # If the entry is a directory and in the exclusion list, skip it.
        if os.path.isdir(full_path) and entry in EXCLUDED_DIRS:
            continue
        # If the file/directory is gitignored, skip it.
        if rel_path in gitignored:
            continue
        filtered_entries.append(entry)

    count = len(filtered_entries)
    for idx, entry in enumerate(filtered_entries):
        full_path = os.path.join(dir_path, entry)
        connector = "└── " if idx == count - 1 else "├── "
        print(prefix + connector + entry)
        if os.path.isdir(full_path):
            extension = "    " if idx == count - 1 else "│   "
            tree(full_path, prefix + extension, repo_root, gitignored)

if __name__ == "__main__":
    # Assume current working directory is the repository root
    repo_root = os.getcwd()
    gitignored = get_gitignored_files(repo_root)
    
    print(".")
    tree(repo_root, "", repo_root, gitignored)

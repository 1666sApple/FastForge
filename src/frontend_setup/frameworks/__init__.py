"""
Framework-specific setup handlers
"""

from .create_react_app import CreateReactAppSetup
from .nextjs import NextJSSetup
from .vite import ViteSetup

__all__ = ["CreateReactAppSetup", "NextJSSetup", "ViteSetup"]

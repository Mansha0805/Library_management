#!/usr/bin/env python3
"""
Entry point for the Library Management System.

Usage:
    python main.py
"""

from app import LibraryApp


def main():
    """Launch the Library Management System."""
    app = LibraryApp()
    app.run()


if __name__ == "__main__":
    main()

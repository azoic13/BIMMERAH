#!/usr/bin/env python3
"""
BIMMERAH - Free Android version of BIMMERCODE app
Main entry point for the application
"""

from src.app import BimmerahApp


def main():
    """Start the BIMMERAH application"""
    app = BimmerahApp()
    app.run()


if __name__ == "__main__":
    main()

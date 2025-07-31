#!/usr/bin/env python3
"""
PyComix - Comic Reader Application

Main entry point for the PyComix comic reader application.
Run this file to start the application.

Usage:
    python main.py
"""

import sys
import os
from pathlib import Path
from pycomix import PyComixApp

# Add the current directory to Python path so we can import pycomix package
current_dir = Path(__file__).parent.absolute()
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))


def main():
    """Main function to start the PyComix application."""
    try:
        # Create and run the application
        app = PyComixApp()

        # Start the application event loop
        exit_code = app.run()

        # Exit with the return code from the application
        sys.exit(exit_code)

    except ImportError as e:
        print(f"Error importing PyComix modules: {e}")
        print("Make sure all required dependencies are installed.")
        print("Run: `pip install -r requirements.txt`")
        sys.exit(1)

    except Exception as e:
        print(f"Error starting PyComix: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Set up application metadata for better system integration
    os.environ.setdefault("QT_APPLICATION_NAME", "PyComix")

    # Run the main function
    main()

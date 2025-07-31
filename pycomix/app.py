"""
PyComix Application Class

This module contains the main application class that manages the PyQt6 application
lifecycle and coordinates between different components.
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QCoreApplication, Qt
from PyQt6.QtGui import QFont, QPalette, QColor

from pycomix.ui.main_window import MainWindow


class PyComixApp:
    """
    Main application class for PyComix.
    
    Manages the PyQt6 application lifecycle, handles initialization,
    and coordinates between different application components.
    """
    
    def __init__(self):
        """Initialize the PyComix application."""
        self.app = None
        self.main_window = None
        self._setup_application()
    
    def _setup_application(self):
        """Set up the QApplication with proper configuration."""
        # Create QApplication instance
        self.app = QApplication(sys.argv)
        
        # Set application metadata
        QCoreApplication.setApplicationName("PyComix")
        QCoreApplication.setApplicationVersion("0.1.0")
        QCoreApplication.setOrganizationName("PyComix Team")
        QCoreApplication.setOrganizationDomain("pycomix.org")
        
        # Enable high DPI scaling (automatically enabled in PyQt6)
        # Note: High DPI scaling is enabled by default in PyQt6
        
        # Set application style and theme
        self._setup_application_style()
        
        # Set up application-wide shortcuts and behavior
        self.app.setQuitOnLastWindowClosed(True)
    
    def _setup_application_style(self):
        """Configure the application's visual style and theme."""
        # Set a modern font as default
        font = QFont("Segoe UI", 9)  # Will fall back to system default if not available
        self.app.setFont(font)
        
        # You can add custom styling here if needed
        # For now, we'll use the system theme
        pass
    
    def create_main_window(self):
        """Create and configure the main application window."""
        self.main_window = MainWindow()
        return self.main_window
    
    def show_main_window(self):
        """Show the main application window."""
        if self.main_window is None:
            self.create_main_window()
        
        self.main_window.show()
        
        # Bring window to front and activate it
        self.main_window.raise_()
        self.main_window.activateWindow()
    
    def run(self):
        """
        Start the application event loop.
        
        Returns:
            int: Application exit code
        """
        if not self.app:
            raise RuntimeError("Application not properly initialized")
        
        # Create and show main window
        self.show_main_window()
        
        # Start the event loop
        return self.app.exec()
    
    def quit(self):
        """Quit the application gracefully."""
        if self.app:
            self.app.quit()
    
    def get_main_window(self):
        """
        Get the main window instance.
        
        Returns:
            MainWindow: The main window instance, or None if not created yet
        """
        return self.main_window
    
    def get_application(self):
        """
        Get the QApplication instance.
        
        Returns:
            QApplication: The QApplication instance
        """
        return self.app


def create_app():
    """
    Factory function to create a PyComix application instance.
    
    Returns:
        PyComixApp: Configured PyComix application instance
    """
    return PyComixApp() 
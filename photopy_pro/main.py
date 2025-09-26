"""Main entry point for PhotoPy Pro."""

import sys
from PyQt6.QtWidgets import QApplication
from .ui.main_window import MainWindow


def main():
    """Main function to run the application."""
    app = QApplication(sys.argv)
    app.setApplicationName("PhotoPy Pro")
    app.setApplicationVersion("2.0.0")

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
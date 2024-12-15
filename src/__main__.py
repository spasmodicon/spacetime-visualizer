"""
Main entry point for the SpaceTime Visualizer application.
"""

import sys
from PyQt5.QtWidgets import QApplication
from .ui import SpaceTimeVisualizer

def main():
    """Launch the SpaceTime Visualizer application."""
    app = QApplication(sys.argv)
    window = SpaceTimeVisualizer()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

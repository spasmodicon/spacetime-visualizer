#!/usr/bin/env python3
"""
SpaceTime Visualizer - Main Entry Point

This script launches the SpaceTime Visualizer application, a tool for
visualizing special relativity concepts. It handles Python path setup
and provides basic error handling for graceful failure modes.

Usage:
    python run_spacetime_visualizer.py
"""

import sys
import os
import traceback
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add the current directory to Python path so it can find the package
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

def main():
    """
    Main entry point for the application.
    Sets up the QApplication and launches the main window.
    """
    try:
        from src import SpaceTimeVisualizer
        from PyQt5.QtWidgets import QApplication
        
        logger.info("Starting SpaceTime Visualizer...")
        logger.debug(f"Python path: {sys.path}")
        logger.debug(f"Current directory: {current_dir}")
        
        app = QApplication(sys.argv)
        window = SpaceTimeVisualizer()
        window.show()
        return app.exec_()
    
    except ImportError as e:
        logger.error(f"Failed to import required modules: {str(e)}")
        logger.error("Please ensure all dependencies are installed via 'pip install -r requirements.txt'")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.error("Traceback:")
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())

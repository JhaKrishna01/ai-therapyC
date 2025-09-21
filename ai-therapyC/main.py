"""
Main Application Entry Point
AI Therapy System - Emotion & Risk Detection Therapeutic AI
"""

import sys
import os
import logging
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def setup_logging():
    """Setup logging configuration"""
    # Create logs directory
    logs_dir = project_root / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(logs_dir / 'therapy_system.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set specific loggers
    logging.getLogger('tensorflow').setLevel(logging.WARNING)
    logging.getLogger('matplotlib').setLevel(logging.WARNING)
    logging.getLogger('PIL').setLevel(logging.WARNING)

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'customtkinter', 'opencv-python', 'tensorflow', 'numpy', 
        'pandas', 'matplotlib', 'plotly', 'Pillow', 'scikit-learn',
        'nltk', 'textblob'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Missing required packages:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\nPlease install missing packages using:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def create_directories():
    """Create necessary directories"""
    directories = [
        'logs', 'exports', 'config', 'models', 'data'
    ]
    
    for directory in directories:
        dir_path = project_root / directory
        dir_path.mkdir(exist_ok=True)

def main():
    """Main application entry point"""
    try:
        print("AI Therapy System - Starting...")
        
        # Setup
        setup_logging()
        create_directories()
        
        # Check dependencies
        if not check_dependencies():
            print("Please install missing dependencies and try again.")
            return 1
        
        # Import and run the GUI
        from gui.main_gui import AITherapyGUI
        
        print("Initializing AI Therapy System...")
        app = AITherapyGUI()
        
        print("Starting GUI application...")
        app.run()
        
        print("AI Therapy System - Shutdown complete")
        return 0
        
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        return 0
        
    except Exception as e:
        print(f"Fatal error: {e}")
        logging.error(f"Fatal error: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())

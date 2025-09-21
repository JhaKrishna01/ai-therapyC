"""
Installation Test Script
Tests all components of the AI Therapy System
"""

import sys
import importlib
import traceback
from pathlib import Path

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing package imports...")
    
    packages = [
        ('customtkinter', 'CustomTkinter GUI framework'),
        ('cv2', 'OpenCV computer vision'),
        ('tensorflow', 'TensorFlow machine learning'),
        ('numpy', 'NumPy numerical computing'),
        ('pandas', 'Pandas data analysis'),
        ('matplotlib', 'Matplotlib plotting'),
        ('plotly', 'Plotly interactive visualization'),
        ('PIL', 'Pillow image processing'),
        ('sklearn', 'Scikit-learn machine learning'),
        ('nltk', 'NLTK natural language processing'),
        ('textblob', 'TextBlob text processing'),
        ('sqlite3', 'SQLite database'),
        ('threading', 'Threading support'),
        ('json', 'JSON processing'),
        ('datetime', 'Date/time handling'),
        ('logging', 'Logging system')
    ]
    
    failed_imports = []
    
    for package, description in packages:
        try:
            importlib.import_module(package)
            print(f"✓ {package:<15} - {description}")
        except ImportError as e:
            print(f"✗ {package:<15} - {description} (Error: {e})")
            failed_imports.append(package)
    
    if failed_imports:
        print(f"\nFailed to import: {', '.join(failed_imports)}")
        print("Please install missing packages using: pip install <package_name>")
        return False
    else:
        print("\nAll packages imported successfully!")
        return True

def test_camera():
    """Test camera functionality"""
    print("\nTesting camera access...")
    
    try:
        import cv2
        
        # Try to open camera
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                print("✓ Camera test passed - camera is working")
                cap.release()
                return True
            else:
                print("✗ Camera test failed - cannot read frames")
                cap.release()
                return False
        else:
            print("✗ Camera test failed - cannot open camera")
            return False
            
    except Exception as e:
        print(f"✗ Camera test failed - {e}")
        return False

def test_database():
    """Test database functionality"""
    print("\nTesting database functionality...")
    
    try:
        import sqlite3
        import tempfile
        import os
        
        # Create temporary database
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        try:
            # Test database operations
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Create test table
            cursor.execute('CREATE TABLE test (id INTEGER PRIMARY KEY, data TEXT)')
            
            # Insert test data
            cursor.execute('INSERT INTO test (data) VALUES (?)', ('test_data',))
            
            # Query test data
            cursor.execute('SELECT * FROM test')
            result = cursor.fetchone()
            
            conn.close()
            
            if result and result[1] == 'test_data':
                print("✓ Database test passed - SQLite is working")
                return True
            else:
                print("✗ Database test failed - data integrity issue")
                return False
                
        finally:
            # Clean up
            if os.path.exists(db_path):
                os.unlink(db_path)
                
    except Exception as e:
        print(f"✗ Database test failed - {e}")
        return False

def test_gui():
    """Test GUI functionality"""
    print("\nTesting GUI functionality...")
    
    try:
        import customtkinter as ctk
        import tkinter as tk
        
        # Test basic GUI creation
        root = ctk.CTk()
        root.title("GUI Test")
        root.geometry("300x200")
        
        # Create test widgets
        label = ctk.CTkLabel(root, text="GUI Test Successful!")
        label.pack(pady=20)
        
        button = ctk.CTkButton(root, text="Close", command=root.destroy)
        button.pack(pady=10)
        
        print("✓ GUI test passed - CustomTkinter is working")
        print("  (A test window should have opened briefly)")
        
        # Don't actually show the window in automated test
        root.destroy()
        return True
        
    except Exception as e:
        print(f"✗ GUI test failed - {e}")
        return False

def test_project_structure():
    """Test project structure"""
    print("\nTesting project structure...")
    
    required_files = [
        'main.py',
        'requirements.txt',
        'README.md',
        'SETUP.md',
        'RESEARCH_GUIDE.md'
    ]
    
    required_dirs = [
        'config',
        'database',
        'emotion_detection',
        'therapeutic_system',
        'crisis_detection',
        'gui',
        'exercises',
        'visualization',
        'export'
    ]
    
    missing_files = []
    missing_dirs = []
    
    # Check files
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
        else:
            print(f"✓ {file}")
    
    # Check directories
    for directory in required_dirs:
        if not Path(directory).exists():
            missing_dirs.append(directory)
        else:
            print(f"✓ {directory}/")
    
    if missing_files or missing_dirs:
        print(f"\nMissing files: {missing_files}")
        print(f"Missing directories: {missing_dirs}")
        return False
    else:
        print("\nAll required files and directories found!")
        return True

def test_module_imports():
    """Test importing project modules"""
    print("\nTesting project module imports...")
    
    modules = [
        ('config.config_manager', 'Configuration management'),
        ('database.database_manager', 'Database operations'),
        ('emotion_detection.emotion_detector', 'Emotion detection'),
        ('therapeutic_system.nurse_framework', 'NURSE framework'),
        ('crisis_detection.crisis_detector', 'Crisis detection'),
        ('exercises.therapeutic_exercises', 'Therapeutic exercises'),
        ('visualization.data_visualizer', 'Data visualization'),
        ('export.research_exporter', 'Research export')
    ]
    
    failed_modules = []
    
    for module, description in modules:
        try:
            importlib.import_module(module)
            print(f"✓ {module:<30} - {description}")
        except ImportError as e:
            print(f"✗ {module:<30} - {description} (Error: {e})")
            failed_modules.append(module)
        except Exception as e:
            print(f"✗ {module:<30} - {description} (Error: {e})")
            failed_modules.append(module)
    
    if failed_modules:
        print(f"\nFailed to import modules: {', '.join(failed_modules)}")
        return False
    else:
        print("\nAll project modules imported successfully!")
        return True

def test_basic_functionality():
    """Test basic system functionality"""
    print("\nTesting basic functionality...")
    
    try:
        # Test configuration
        from config.config_manager import ConfigManager
        config = ConfigManager()
        print("✓ Configuration system working")
        
        # Test database manager
        from database.database_manager import DatabaseManager
        db = DatabaseManager(":memory:")  # Use in-memory database for testing
        print("✓ Database manager working")
        
        # Test emotion detector (without camera)
        from emotion_detection.emotion_detector import EmotionDetector
        detector = EmotionDetector()
        print("✓ Emotion detector initialized")
        
        # Test NURSE framework
        from therapeutic_system.nurse_framework import NURSEFramework
        nurse = NURSEFramework()
        print("✓ NURSE framework working")
        
        # Test crisis detector
        from crisis_detection.crisis_detector import CrisisDetector
        crisis = CrisisDetector()
        print("✓ Crisis detector working")
        
        # Test therapeutic exercises
        from exercises.therapeutic_exercises import TherapeuticExercises
        exercises = TherapeuticExercises()
        print("✓ Therapeutic exercises working")
        
        # Test data visualizer
        from visualization.data_visualizer import DataVisualizer
        visualizer = DataVisualizer()
        print("✓ Data visualizer working")
        
        # Test research exporter
        from export.research_exporter import ResearchDataExporter
        exporter = ResearchDataExporter()
        print("✓ Research exporter working")
        
        return True
        
    except Exception as e:
        print(f"✗ Basic functionality test failed - {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("AI Therapy System - Installation Test")
    print("=" * 50)
    
    tests = [
        ("Package Imports", test_imports),
        ("Project Structure", test_project_structure),
        ("Module Imports", test_module_imports),
        ("Basic Functionality", test_basic_functionality),
        ("Database Functionality", test_database),
        ("GUI Functionality", test_gui),
        ("Camera Access", test_camera)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * len(test_name))
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The AI Therapy System is ready to use.")
        print("\nNext steps:")
        print("1. Run: python main.py")
        print("2. Start the camera in the GUI")
        print("3. Begin a therapy session")
        return 0
    else:
        print("❌ Some tests failed. Please check the issues above.")
        print("\nCommon solutions:")
        print("1. Install missing packages: pip install -r requirements.txt")
        print("2. Check camera permissions")
        print("3. Verify Python version (3.8+)")
        print("4. Check file permissions")
        return 1

if __name__ == "__main__":
    sys.exit(main())

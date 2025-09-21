# AI Therapy System - Setup Guide

This guide provides detailed setup instructions for the AI Therapy System, including system requirements, installation steps, and configuration options.

## 📋 System Requirements

### Minimum Requirements
- **Operating System**: Windows 10, macOS 10.15, or Ubuntu 18.04
- **Python**: 3.8 or higher
- **RAM**: 8GB
- **Storage**: 2GB free space
- **Camera**: USB webcam or built-in camera
- **Display**: 1920x1080 resolution

### Recommended Requirements
- **Operating System**: Windows 11, macOS 12+, or Ubuntu 20.04+
- **Python**: 3.9 or higher
- **RAM**: 16GB
- **Storage**: 5GB free space (SSD recommended)
- **Camera**: HD webcam (720p or higher)
- **Display**: 2560x1440 resolution or higher

## 🚀 Installation Steps

### Step 1: Python Environment Setup

#### Option A: Using Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv therapy_env

# Activate virtual environment
# Windows:
therapy_env\Scripts\activate
# macOS/Linux:
source therapy_env/bin/activate

# Upgrade pip
python -m pip install --upgrade pip
```

#### Option B: Using Conda
```bash
# Create conda environment
conda create -n therapy_env python=3.9

# Activate environment
conda activate therapy_env
```

### Step 2: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# Verify installation
python -c "import customtkinter, cv2, tensorflow; print('Installation successful!')"
```

### Step 3: Verify Camera Access

```python
# Test camera access
import cv2

cap = cv2.VideoCapture(0)
if cap.isOpened():
    ret, frame = cap.read()
    if ret:
        print("Camera is working correctly!")
    else:
        print("Camera opened but cannot read frames")
else:
    print("Cannot open camera")
cap.release()
```

### Step 4: Run Initial Setup

```bash
# Run the application for first-time setup
python main.py
```

The system will automatically:
- Create necessary directories
- Initialize the database
- Generate default configuration files
- Set up logging

## ⚙️ Configuration

### Basic Configuration

Edit `config/settings.json` to customize system settings:

```json
{
  "system": {
    "debug_mode": false,
    "log_level": "INFO"
  },
  "camera": {
    "default_index": 0,
    "resolution": {
      "width": 640,
      "height": 480
    },
    "fps": 30
  },
  "emotion_detection": {
    "confidence_threshold": 0.3,
    "update_interval": 0.1
  },
  "crisis_detection": {
    "enabled": true,
    "risk_threshold": 7,
    "auto_escalation": true
  }
}
```

### Advanced Configuration

#### Camera Settings
```json
{
  "camera": {
    "default_index": 0,
    "resolution": {
      "width": 1280,
      "height": 720
    },
    "fps": 30,
    "auto_start": false,
    "brightness": 0,
    "contrast": 0
  }
}
```

#### Emotion Detection Settings
```json
{
  "emotion_detection": {
    "model_path": "models/emotion_model.h5",
    "confidence_threshold": 0.3,
    "update_interval": 0.1,
    "calibration_frames": 30,
    "emotion_labels": [
      "Angry", "Disgust", "Fear", "Happy", 
      "Sad", "Surprise", "Neutral"
    ]
  }
}
```

#### Crisis Detection Settings
```json
{
  "crisis_detection": {
    "enabled": true,
    "risk_threshold": 7,
    "monitoring_active": true,
    "auto_escalation": true,
    "crisis_keywords": [
      "suicide", "kill myself", "end it all",
      "not worth living", "hurt myself", "self harm"
    ]
  }
}
```

#### Database Settings
```json
{
  "database": {
    "path": "sessions.db",
    "backup_enabled": true,
    "backup_interval_hours": 24,
    "cleanup_enabled": true,
    "cleanup_interval_days": 7
  }
}
```

## 🔧 Troubleshooting

### Common Installation Issues

#### 1. Python Version Issues
```bash
# Check Python version
python --version

# If version is too old, install newer Python
# Windows: Download from python.org
# macOS: brew install python@3.9
# Ubuntu: sudo apt install python3.9
```

#### 2. Package Installation Failures

**OpenCV Installation Issues:**
```bash
# Try alternative installation
pip install opencv-python-headless

# Or install from conda
conda install opencv
```

**TensorFlow Installation Issues:**
```bash
# Install CPU version
pip install tensorflow-cpu

# Or install GPU version (if you have CUDA)
pip install tensorflow-gpu
```

**CustomTkinter Issues:**
```bash
# Install with specific version
pip install customtkinter==5.2.0

# Or try development version
pip install git+https://github.com/TomSchimansky/CustomTkinter.git
```

#### 3. Camera Access Issues

**Windows:**
- Check camera permissions in Settings > Privacy > Camera
- Ensure no other applications are using the camera
- Update camera drivers

**macOS:**
- Grant camera permissions in System Preferences > Security & Privacy
- Check camera permissions in Terminal app settings

**Linux:**
- Add user to video group: `sudo usermod -a -G video $USER`
- Check camera device: `ls /dev/video*`
- Install v4l2 utilities: `sudo apt install v4l-utils`

#### 4. Database Issues

**Permission Errors:**
```bash
# Check directory permissions
ls -la sessions.db

# Fix permissions if needed
chmod 664 sessions.db
```

**Corruption Issues:**
```bash
# Backup and recreate database
cp sessions.db sessions_backup.db
rm sessions.db
python main.py  # Will recreate database
```

### Performance Issues

#### 1. Slow Emotion Detection
- Reduce camera resolution
- Increase update interval
- Close other applications
- Use CPU-optimized TensorFlow

#### 2. GUI Lag
- Disable real-time visualization
- Reduce GUI update frequency
- Use lighter theme
- Close unnecessary tabs

#### 3. Memory Issues
- Enable database cleanup
- Reduce data retention period
- Close old sessions
- Restart application periodically

### Error Messages

#### "Camera not found"
1. Check camera connection
2. Try different camera index
3. Update camera drivers
4. Check camera permissions

#### "Database locked"
1. Close other instances of the application
2. Check for database backup processes
3. Restart the application
4. Check file permissions

#### "Model loading failed"
1. Check model file path
2. Verify TensorFlow installation
3. Check file permissions
4. Try default model creation

## 🧪 Testing Installation

### Basic Functionality Test

```python
# test_installation.py
import sys
import importlib

def test_imports():
    """Test if all required packages can be imported"""
    packages = [
        'customtkinter', 'cv2', 'tensorflow', 'numpy',
        'pandas', 'matplotlib', 'plotly', 'PIL',
        'sklearn', 'nltk', 'textblob'
    ]
    
    failed_imports = []
    
    for package in packages:
        try:
            importlib.import_module(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package}")
            failed_imports.append(package)
    
    if failed_imports:
        print(f"\nFailed to import: {', '.join(failed_imports)}")
        return False
    else:
        print("\nAll packages imported successfully!")
        return True

def test_camera():
    """Test camera functionality"""
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            if ret:
                print("✓ Camera test passed")
                return True
            else:
                print("✗ Camera test failed - cannot read frames")
                return False
        else:
            print("✗ Camera test failed - cannot open camera")
            return False
    except Exception as e:
        print(f"✗ Camera test failed - {e}")
        return False

def test_database():
    """Test database functionality"""
    try:
        import sqlite3
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE test (id INTEGER)')
        cursor.execute('INSERT INTO test VALUES (1)')
        cursor.execute('SELECT * FROM test')
        result = cursor.fetchone()
        conn.close()
        
        if result[0] == 1:
            print("✓ Database test passed")
            return True
        else:
            print("✗ Database test failed")
            return False
    except Exception as e:
        print(f"✗ Database test failed - {e}")
        return False

if __name__ == "__main__":
    print("Testing AI Therapy System Installation...")
    print("=" * 50)
    
    tests = [
        ("Package Imports", test_imports),
        ("Camera Access", test_camera),
        ("Database Functionality", test_database)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✓ Installation successful! You can now run the application.")
    else:
        print("✗ Some tests failed. Please check the issues above.")
```

Run the test:
```bash
python test_installation.py
```

### GUI Test

```python
# test_gui.py
import customtkinter as ctk

def test_gui():
    """Test basic GUI functionality"""
    try:
        root = ctk.CTk()
        root.title("GUI Test")
        root.geometry("400x300")
        
        label = ctk.CTkLabel(root, text="GUI Test Successful!")
        label.pack(pady=50)
        
        button = ctk.CTkButton(root, text="Close", command=root.destroy)
        button.pack(pady=20)
        
        print("✓ GUI test passed - window should open")
        root.mainloop()
        
    except Exception as e:
        print(f"✗ GUI test failed - {e}")

if __name__ == "__main__":
    test_gui()
```

## 📁 Directory Structure

After installation, your project directory should look like this:

```
ai-therapy-system/
├── main.py                          # Main application entry point
├── requirements.txt                 # Python dependencies
├── README.md                        # Project documentation
├── SETUP.md                         # This setup guide
├── config/
│   ├── settings.json               # Configuration file
│   └── config_manager.py           # Configuration management
├── database/
│   └── database_manager.py         # Database operations
├── emotion_detection/
│   └── emotion_detector.py          # Emotion detection system
├── therapeutic_system/
│   └── nurse_framework.py          # NURSE framework implementation
├── crisis_detection/
│   ├── crisis_detector.py          # Crisis detection system
│   └── safety_manager.py           # Safety protocols
├── gui/
│   └── main_gui.py                 # Main GUI interface
├── exercises/
│   └── therapeutic_exercises.py    # Therapeutic exercises
├── visualization/
│   └── data_visualizer.py         # Data visualization
├── export/
│   └── research_exporter.py        # Research data export
├── logs/                           # Log files (created on first run)
├── exports/                        # Exported data (created on first run)
├── models/                         # ML models (optional)
└── data/                          # Additional data files (optional)
```

## 🔄 Updates and Maintenance

### Updating the System

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Clear old data if needed
rm -rf logs/*.log
```

### Database Maintenance

```bash
# Backup database
cp sessions.db sessions_backup_$(date +%Y%m%d).db

# Clean old data (if configured)
python -c "from database.database_manager import DatabaseManager; db = DatabaseManager(); db.cleanup_old_data(30)"
```

### Log Management

```bash
# View recent logs
tail -f logs/therapy_system.log

# Archive old logs
tar -czf logs_archive_$(date +%Y%m%d).tar.gz logs/
```

## 📞 Support

### Getting Help

1. **Check this setup guide** for common issues
2. **Review the README.md** for general information
3. **Check GitHub Issues** for known problems
4. **Create a new issue** if you can't find a solution

### Reporting Issues

When reporting issues, please include:
- Operating system and version
- Python version
- Error messages or logs
- Steps to reproduce the issue
- Screenshots if applicable

### Community Support

- **GitHub Discussions**: For questions and community support
- **Issues**: For bug reports and feature requests
- **Documentation**: Check code comments and docstrings

---

**Next Steps**: After completing setup, proceed to the main README.md for usage instructions and feature documentation.

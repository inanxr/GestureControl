# Gesture Control - Installation Instructions

## Important: Python Version Requirement

MediaPipe currently supports Python 3.8 through 3.12. **Python 3.13 is NOT supported yet.**

Your system has Python 3.13.5, which is too new for MediaPipe.

## Installation Options

### Option 1: Install Python 3.12 (Recommended)

1. Download Python 3.12 from python.org: https://www.python.org/downloads/
2. Install Python 3.12 (make sure to check "Add Python to PATH")
3. Create virtual environment with Python 3.12:
   ```bash
   py -3.12 -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

### Option 2: Use Existing Python 3.8-3.12 Installation

If you have Python 3.8, 3.9, 3.10, 3.11, or 3.12 installed:

```bash
# Check which Python versions you have
py --list

# Create venv with compatible version (e.g., 3.11)
py -3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Option 3: Try Windows Store Python

```bash
# Install Python 3.12 from Windows Store
# Then:
python3.12 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## After Installing Compatible Python

Once you have a compatible Python version:

1. Navigate to project directory:
   ```bash
   cd c:\Users\ihina\Documents\Projects\Bemation\gesture_control
   ```

2. Remove old virtual environment:
   ```bash
   rmdir /s venv
   ```

3. Create new virtual environment with compatible Python:
   ```bash
   py -3.12 -m venv venv
   # or whatever compatible version you have
   ```

4. Activate virtual environment:
   ```bash
   venv\Scripts\activate
   ```

5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Run setup verification:
   ```bash
   python setup.py
   ```

7. If all checks pass, start the application:
   ```bash
   python main.py
   ```

## MediaPipe Compatibility

**MediaPipe Supported Python Versions:**
- ✓ Python 3.8
- ✓ Python 3.9
- ✓ Python 3.10
- ✓ Python 3.11
- ✓ Python 3.12
- ✗ Python 3.13 (NOT SUPPORTED YET)

## Packages Installed Successfully So Far

The following packages were successfully installed with Python 3.13.5:
- ✓ numpy
- ✓ opencv-python  
- ✓ pyautogui
- ✗ mediapipe (incompatible with Python 3.13)

## Next Steps

1. Install compatible Python version (3.8-3.12)
2. Recreate virtual environment
3. Install all dependencies
4. Run setup.py to verify installation
5. Run main.py to start gesture control

## Need Help?

If you encounter issues:
1. Check you're using Python 3.8-3.12
2. Ensure pip is up to date: `python -m pip install --upgrade pip`
3. Try installing packages one at a time
4. Check Windows camera permissions
5. Run `python setup.py` to verify all components

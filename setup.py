"""
Setup and verification script for Gesture Control application.
Tests camera access, library installations, and PyAutoGUI permissions.
"""
import sys


def check_python_version():
    """Check if Python version is 3.8 or higher."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (Need 3.8+)")
        return False


def test_opencv():
    """Test OpenCV installation and camera access."""
    print("\nTesting OpenCV and camera...")
    try:
        import cv2
        print(f"✓ OpenCV {cv2.__version__} installed")
        
        # Test camera
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print("✓ Camera access successful")
                print(f"  Frame size: {frame.shape[1]}x{frame.shape[0]}")
            else:
                print("✗ Could not read frame from camera")
            cap.release()
        else:
            print("✗ Could not open camera")
            return False
        
        return True
    except ImportError:
        print("✗ OpenCV not installed")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_mediapipe():
    """Test MediaPipe installation."""
    print("\nTesting MediaPipe...")
    try:
        import mediapipe as mp
        print(f"✓ MediaPipe {mp.__version__} installed")
        
        # Test hand detection initialization
        hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7
        )
        print("✓ MediaPipe Hands initialized successfully")
        hands.close()
        
        return True
    except ImportError:
        print("✗ MediaPipe not installed")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_pyautogui():
    """Test PyAutoGUI installation and permissions."""
    print("\nTesting PyAutoGUI...")
    try:
        import pyautogui
        print(f"✓ PyAutoGUI {pyautogui.__version__} installed")
        
        # Test getting cursor position
        pos = pyautogui.position()
        print(f"✓ Can read cursor position: {pos}")
        
        # Test screen size
        size = pyautogui.size()
        print(f"✓ Screen size: {size.width}x{size.height}")
        
        return True
    except ImportError:
        print("✗ PyAutoGUI not installed")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        print("  Note: PyAutoGUI may need admin permissions on Windows")
        return False


def test_numpy():
    """Test NumPy installation."""
    print("\nTesting NumPy...")
    try:
        import numpy as np
        print(f"✓ NumPy {np.__version__} installed")
        return True
    except ImportError:
        print("✗ NumPy not installed")
        return False


def main():
    """Run all setup checks."""
    print("=" * 60)
    print("GESTURE CONTROL - Setup and Verification")
    print("=" * 60)
    
    results = []
    
    # Run all tests
    results.append(("Python Version", check_python_version()))
    results.append(("NumPy", test_numpy()))
    results.append(("OpenCV + Camera", test_opencv()))
    results.append(("MediaPipe", test_mediapipe()))
    results.append(("PyAutoGUI", test_pyautogui()))
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {name}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n✓ All checks passed! You're ready to run the application.")
        print("\nTo start the application, run:")
        print("  python main.py")
    else:
        print("\n✗ Some checks failed. Please install missing dependencies:")
        print("  pip install -r requirements.txt")
        print("\nIf camera issues persist:")
        print("  - Close other apps using the camera")
        print("  - Check Windows camera permissions")
        print("  - Try updating camera drivers")
    
    print()


if __name__ == "__main__":
    main()

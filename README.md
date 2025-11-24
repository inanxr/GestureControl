# Gesture-Controlled Windows Software

Control your Windows PC with hand gestures using your webcam!

## Features

- 👆 **Cursor Control**: Move your index finger to control the cursor
- 👌 **Left Click**: Pinch index finger and thumb together
- 🖐️ **Right Click**: Pinch middle finger and thumb together  
- 📜 **Scroll**: Move two extended fingers (index + middle) up/down vertically
- 🎯 **Visual Feedback**: See hand landmarks and tracking in real-time
- ⚡ **Smooth Performance**: Optimized for 25+ FPS with smoothing algorithms

## System Requirements

- Windows 10 or later
- Python 3.8 or higher
- Webcam (built-in or external)
- Adequate lighting for hand detection

## Installation

### 1. Clone or Download

Place the `gesture_control` folder in your desired location.

### 2. Set Up Virtual Environment (Recommended)

```bash
cd gesture_control
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `opencv-python` - Camera capture and image processing
- `mediapipe` - Hand tracking and landmark detection
- `pyautogui` - System control (mouse and keyboard)
- `numpy` - Numerical operations

## Usage

### Basic Usage

1. Activate your virtual environment (if using one):
   ```bash
   venv\Scripts\activate
   ```

2. Run the application:
   ```bash
   python main.py
   ```

3. Position your hand 1-3 feet from the camera

4. Perform gestures:
   - **Move cursor**: Point with index finger
   - **Left click**: Pinch index + thumb
   - **Right click**: Pinch middle + thumb
   - **Scroll**: Extend index + middle fingers, move vertically

5. Exit the application:
   - Press `ESC` key, or
   - Press `Ctrl+C`, or
   - Move cursor to any screen corner (PyAutoGUI failsafe)

## Configuration

You can customize the gesture sensitivity and behavior by editing `config.py`:

### Detection Thresholds
```python
PINCH_THRESHOLD = 0.03  # Lower = easier to trigger pinch
SCROLL_THRESHOLD = 0.02  # Lower = more sensitive scrolling
```

### Smoothing
```python
SMOOTHING_FRAMES = 7  # Higher = smoother but slower cursor
CURSOR_SPEED_MULTIPLIER = 1.0  # Increase for faster cursor
```

### Cooldown Periods
```python
GESTURE_COOLDOWN = 0.5  # Seconds between gesture triggers
```

### Camera Settings
```python
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_INDEX = 0  # Change if using external camera
```

## Troubleshooting

### Camera Not Working
- Ensure no other application is using the camera
- Check camera permissions in Windows Settings
- Try changing `CAMERA_INDEX` in `config.py` (0, 1, 2...)
- Update camera drivers

### PyAutoGUI Permission Errors
- Run PowerShell/Command Prompt as Administrator
- Check Windows antivirus/security settings
- Whitelist PyAutoGUI if blocked

### Hand Not Detected
- Improve lighting conditions
- Move closer/farther from camera (1-3 feet optimal)
- Ensure hand is fully visible in frame
- Clean camera lens
- Lower `MIN_DETECTION_CONFIDENCE` in `config.py`

### Gestures Not Working
- Check visual feedback window to see if landmarks are detected
- Adjust thresholds in `config.py`:
  - Increase `PINCH_THRESHOLD` if clicks too sensitive
  - Decrease if gestures not triggering
- Ensure cooldown period isn't too long

### Low FPS / Laggy
- Reduce camera resolution in `config.py`
- Close other applications
- Lower `SMOOTHING_FRAMES` for faster response
- Check CPU usage

### Cursor Too Jittery
- Increase `SMOOTHING_FRAMES` (7-15 recommended)
- Ensure stable hand position
- Improve lighting for better tracking

## Project Structure

```
gesture_control/
├── main.py                 # Application entry point
├── camera_handler.py       # Camera capture and preprocessing
├── hand_tracker.py         # MediaPipe hand detection wrapper
├── gesture_recognizer.py   # Gesture detection logic
├── system_controller.py    # PyAutoGUI wrapper
├── config.py              # Configuration parameters
├── utils.py               # Helper functions
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## How It Works

1. **Camera Layer**: Captures webcam frames at 30 FPS, flips horizontally for mirror effect
2. **Hand Tracking**: Uses MediaPipe to detect 21 hand landmarks in real-time
3. **Gesture Recognition**: Analyzes landmark positions and distances to recognize gestures
4. **Smoothing**: Applies moving average filter to prevent jittery cursor movement
5. **System Control**: Executes corresponding mouse/keyboard actions via PyAutoGUI

## Safety Features

- **Failsafe**: Move mouse to any corner to emergency-stop the program
- **Boundary Checking**: Cursor cannot move outside screen bounds
- **Cooldown Timers**: Prevents accidental multiple clicks
- **Keyboard Interrupt**: Ctrl+C to stop anytime
- **State Management**: Clear gesture states prevent conflicts

## Performance Tips

- Use adequate lighting (natural light or desk lamp)
- Keep hand 1-3 feet from camera for best tracking
- Make deliberate, clear gestures
- Avoid rapid hand movements initially
- Practice cursor control before attempting clicks
- Start with higher thresholds and adjust down as you improve

## Known Limitations

- Works best with one hand (configured for single hand tracking)
- Requires good lighting conditions
- May not work well with very dark or very fair skin tones (adjust camera exposure)
- Performance depends on computer specifications
- Not recommended for precision tasks (e.g., photo editing, CAD)

## Future Enhancements

Potential features for future versions:
- Double-click gesture
- Drag-and-drop functionality
- Keyboard shortcuts via gestures
- Multi-hand support
- Gesture customization UI
- User calibration system
- Profile saving
- Application-specific gesture sets

## License

This is a personal project built for educational purposes.

## Credits

Built using:
- [MediaPipe](https://mediapipe.dev/) by Google
- [OpenCV](https://opencv.org/)
- [PyAutoGUI](https://pyautogui.readthedocs.io/)

---

**Enjoy controlling your PC with gestures! 🚀**

For issues or questions, adjust the configuration parameters in `config.py` and test different settings.

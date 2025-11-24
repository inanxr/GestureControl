"""
Configuration constants and tunable parameters for gesture control application.
"""

# Detection thresholds
PINCH_THRESHOLD = 0.03  # Distance threshold for pinch gestures (normalized 0-1)
PINCH_RELEASE_THRESHOLD = 0.045  # Distance to release pinch (prevents flickering)
GESTURE_COOLDOWN = 0.5  # Seconds to wait between gesture triggers

# Smoothing parameters
SMOOTHING_FRAMES = 7  # Number of frames to average for cursor smoothing
CURSOR_SPEED_MULTIPLIER = 1.0  # Cursor movement speed multiplier

# Scroll sensitivity
SCROLL_THRESHOLD = 0.02  # Minimum vertical movement to trigger scroll
SCROLL_MULTIPLIER = 10  # Scroll distance multiplier
SCROLL_SMOOTHING_FRAMES = 3  # Number of frames for scroll smoothing

# Camera settings
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
TARGET_FPS = 30
CAMERA_INDEX = 0  # Default camera (0 = first camera)

# MediaPipe settings
MAX_NUM_HANDS = 1  # Track only one hand for simplicity
MIN_DETECTION_CONFIDENCE = 0.7  # Minimum confidence for hand detection
MIN_TRACKING_CONFIDENCE = 0.5  # Minimum confidence for hand tracking

# Visual feedback
SHOW_LANDMARKS = True  # Draw hand landmarks on video feed
SHOW_FPS = True  # Show FPS counter
LANDMARK_DRAW_COLOR = (0, 255, 0)  # Green color for landmarks (BGR)
CONNECTION_DRAW_COLOR = (255, 0, 0)  # Blue color for connections (BGR)

# Safety features
ENABLE_FAILSAFE = True  # PyAutoGUI failsafe (move to corner to stop)
SCREEN_BOUNDARY_MARGIN = 10  # Pixels margin from screen edge

# Gesture state
STATE_IDLE = "idle"
STATE_HOVERING = "hovering"
STATE_LEFT_CLICKING = "left_clicking"
STATE_RIGHT_CLICKING = "right_clicking"
STATE_SCROLLING = "scrolling"

# Hand landmarks (MediaPipe indices)
THUMB_TIP = 4
INDEX_TIP = 8
INDEX_PIP = 6
MIDDLE_TIP = 12
MIDDLE_PIP = 10
RING_TIP = 16
PINKY_TIP = 20
WRIST = 0

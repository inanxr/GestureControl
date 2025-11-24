"""
Utility functions for gesture control application.
"""
import math
import time
from collections import deque
import pyautogui


class SmoothingBuffer:
    """Moving average buffer for smoothing coordinate values."""
    
    def __init__(self, size=7):
        """
        Initialize smoothing buffer.
        
        Args:
            size: Number of values to keep in buffer
        """
        self.buffer_x = deque(maxlen=size)
        self.buffer_y = deque(maxlen=size)
    
    def add(self, x, y):
        """Add new coordinate to buffer."""
        self.buffer_x.append(x)
        self.buffer_y.append(y)
    
    def get_average(self):
        """Get smoothed average coordinates."""
        if not self.buffer_x or not self.buffer_y:
            return None, None
        
        avg_x = sum(self.buffer_x) / len(self.buffer_x)
        avg_y = sum(self.buffer_y) / len(self.buffer_y)
        return avg_x, avg_y
    
    def clear(self):
        """Clear the buffer."""
        self.buffer_x.clear()
        self.buffer_y.clear()


class FPSCounter:
    """Calculate frames per second."""
    
    def __init__(self):
        self.frame_count = 0
        self.start_time = time.time()
        self.fps = 0
    
    def update(self):
        """Update frame count and calculate FPS."""
        self.frame_count += 1
        elapsed = time.time() - self.start_time
        
        if elapsed >= 1.0:
            self.fps = self.frame_count / elapsed
            self.frame_count = 0
            self.start_time = time.time()
        
        return self.fps


class CooldownTimer:
    """Timer for gesture cooldown periods."""
    
    def __init__(self, cooldown_seconds=0.5):
        """
        Initialize cooldown timer.
        
        Args:
            cooldown_seconds: Seconds to wait between triggers
        """
        self.cooldown_seconds = cooldown_seconds
        self.last_trigger_time = 0
    
    def can_trigger(self):
        """Check if enough time has passed since last trigger."""
        current_time = time.time()
        return (current_time - self.last_trigger_time) >= self.cooldown_seconds
    
    def trigger(self):
        """Mark that a trigger has occurred."""
        self.last_trigger_time = time.time()
    
    def reset(self):
        """Reset the cooldown timer."""
        self.last_trigger_time = 0


def calculate_distance(point1, point2):
    """
    Calculate Euclidean distance between two points.
    
    Args:
        point1: Tuple or object with x, y attributes
        point2: Tuple or object with x, y attributes
    
    Returns:
        Distance between points
    """
    if hasattr(point1, 'x'):
        x1, y1 = point1.x, point1.y
    else:
        x1, y1 = point1
    
    if hasattr(point2, 'x'):
        x2, y2 = point2.x, point2.y
    else:
        x2, y2 = point2
    
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def normalize_to_screen(x, y, frame_width, frame_height):
    """
    Convert normalized coordinates (0-1) to screen pixel coordinates.
    
    Args:
        x: Normalized x coordinate (0-1)
        y: Normalized y coordinate (0-1)
        frame_width: Width of camera frame
        frame_height: Height of camera frame
    
    Returns:
        Tuple of (screen_x, screen_y) in pixels
    """
    screen_width, screen_height = pyautogui.size()
    
    # Map normalized coordinates to screen space
    screen_x = int(x * screen_width)
    screen_y = int(y * screen_height)
    
    return screen_x, screen_y


def is_finger_extended(tip_landmark, pip_landmark, wrist_landmark):
    """
    Check if a finger is extended by comparing tip and PIP joint positions.
    
    Args:
        tip_landmark: Fingertip landmark
        pip_landmark: PIP joint landmark
        wrist_landmark: Wrist landmark
    
    Returns:
        True if finger is extended, False otherwise
    """
    # Calculate distances from wrist
    tip_distance = calculate_distance(tip_landmark, wrist_landmark)
    pip_distance = calculate_distance(pip_landmark, wrist_landmark)
    
    # Finger is extended if tip is farther from wrist than PIP joint
    return tip_distance > pip_distance

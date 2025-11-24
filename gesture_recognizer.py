"""
Gesture recognition logic for detecting and interpreting hand gestures.
"""
import time
import config
from utils import calculate_distance, normalize_to_screen, SmoothingBuffer, CooldownTimer, is_finger_extended


class GestureRecognizer:
    """Recognizes gestures from hand landmarks and manages gesture state."""
    
    def __init__(self, frame_width, frame_height):
        """
        Initialize gesture recognizer.
        
        Args:
            frame_width: Width of camera frame
            frame_height: Height of camera frame
        """
        self.frame_width = frame_width
        self.frame_height = frame_height
        
        # Smoothing buffers
        self.cursor_buffer = SmoothingBuffer(config.SMOOTHING_FRAMES)
        self.scroll_buffer = SmoothingBuffer(config.SCROLL_SMOOTHING_FRAMES)
        
        # Cooldown timers
        self.left_click_cooldown = CooldownTimer(config.GESTURE_COOLDOWN)
        self.right_click_cooldown = CooldownTimer(config.GESTURE_COOLDOWN)
        
        # Gesture state
        self.current_state = config.STATE_IDLE
        self.previous_scroll_y = None
        
        print("Gesture recognizer initialized")
    
    def recognize(self, landmarks):
        """
        Recognize gestures from hand landmarks.
        
        Args:
            landmarks: List of MediaPipe hand landmarks
        
        Returns:
            Dictionary containing recognized gestures and actions:
            {
                'cursor_pos': (x, y) or None,
                'left_click': True/False,
                'right_click': True/False,
                'scroll': amount or None
            }
        """
        if landmarks is None:
            self.cursor_buffer.clear()
            self.previous_scroll_y = None
            self.current_state = config.STATE_IDLE
            return {
                'cursor_pos': None,
                'left_click': False,
                'right_click': False,
                'scroll': None
            }
        
        # Extract key landmarks
        thumb_tip = landmarks[config.THUMB_TIP]
        index_tip = landmarks[config.INDEX_TIP]
        index_pip = landmarks[config.INDEX_PIP]
        middle_tip = landmarks[config.MIDDLE_TIP]
        middle_pip = landmarks[config.MIDDLE_PIP]
        wrist = landmarks[config.WRIST]
        
        # Initialize result
        result = {
            'cursor_pos': None,
            'left_click': False,
            'right_click': False,
            'scroll': None
        }
        
        # 1. Cursor movement (always based on index finger tip)
        cursor_x, cursor_y = self._recognize_cursor_movement(index_tip)
        result['cursor_pos'] = (cursor_x, cursor_y)
        
        # 2. Left click detection (index-thumb pinch)
        result['left_click'] = self._recognize_left_click(index_tip, thumb_tip)
        
        # 3. Right click detection (middle-thumb pinch)
        result['right_click'] = self._recognize_right_click(middle_tip, thumb_tip)
        
        # 4. Scroll detection (two-finger vertical movement)
        result['scroll'] = self._recognize_scroll(index_tip, middle_tip, index_pip, middle_pip, wrist)
        
        return result
    
    def _recognize_cursor_movement(self, index_tip):
        """
        Recognize cursor movement from index finger position.
        
        Args:
            index_tip: Index finger tip landmark
        
        Returns:
            Tuple of (screen_x, screen_y) in pixels
        """
        # Add to smoothing buffer
        self.cursor_buffer.add(index_tip.x, index_tip.y)
        
        # Get smoothed position
        smooth_x, smooth_y = self.cursor_buffer.get_average()
        
        if smooth_x is None or smooth_y is None:
            return None, None
        
        # Convert to screen coordinates
        screen_x, screen_y = normalize_to_screen(
            smooth_x, smooth_y, 
            self.frame_width, self.frame_height
        )
        
        # Apply speed multiplier
        screen_x = int(screen_x * config.CURSOR_SPEED_MULTIPLIER)
        screen_y = int(screen_y * config.CURSOR_SPEED_MULTIPLIER)
        
        return screen_x, screen_y
    
    def _recognize_left_click(self, index_tip, thumb_tip):
        """
        Recognize left click gesture (index-thumb pinch).
        
        Args:
            index_tip: Index finger tip landmark
            thumb_tip: Thumb tip landmark
        
        Returns:
            True if left click should be triggered, False otherwise
        """
        # Calculate distance between index and thumb
        distance = calculate_distance(index_tip, thumb_tip)
        
        # Check if pinching
        if distance < config.PINCH_THRESHOLD:
            # Check cooldown
            if self.left_click_cooldown.can_trigger():
                self.left_click_cooldown.trigger()
                self.current_state = config.STATE_LEFT_CLICKING
                return True
        elif distance > config.PINCH_RELEASE_THRESHOLD:
            # Released - reset state
            if self.current_state == config.STATE_LEFT_CLICKING:
                self.current_state = config.STATE_IDLE
        
        return False
    
    def _recognize_right_click(self, middle_tip, thumb_tip):
        """
        Recognize right click gesture (middle-thumb pinch).
        
        Args:
            middle_tip: Middle finger tip landmark
            thumb_tip: Thumb tip landmark
        
        Returns:
            True if right click should be triggered, False otherwise
        """
        # Calculate distance between middle and thumb
        distance = calculate_distance(middle_tip, thumb_tip)
        
        # Check if pinching
        if distance < config.PINCH_THRESHOLD:
            # Check cooldown
            if self.right_click_cooldown.can_trigger():
                self.right_click_cooldown.trigger()
                self.current_state = config.STATE_RIGHT_CLICKING
                return True
        elif distance > config.PINCH_RELEASE_THRESHOLD:
            # Released - reset state
            if self.current_state == config.STATE_RIGHT_CLICKING:
                self.current_state = config.STATE_IDLE
        
        return False
    
    def _recognize_scroll(self, index_tip, middle_tip, index_pip, middle_pip, wrist):
        """
        Recognize scroll gesture (two-finger vertical movement).
        
        Args:
            index_tip: Index finger tip landmark
            middle_tip: Middle finger tip landmark
            index_pip: Index finger PIP joint landmark
            middle_pip: Middle finger PIP joint landmark
            wrist: Wrist landmark
        
        Returns:
            Scroll amount (positive = up, negative = down), or None
        """
        # Check if both index and middle fingers are extended
        index_extended = is_finger_extended(index_tip, index_pip, wrist)
        middle_extended = is_finger_extended(middle_tip, middle_pip, wrist)
        
        if not (index_extended and middle_extended):
            self.previous_scroll_y = None
            if self.current_state == config.STATE_SCROLLING:
                self.current_state = config.STATE_IDLE
            return None
        
        # Calculate midpoint between two fingers
        midpoint_y = (index_tip.y + middle_tip.y) / 2
        
        # Initialize previous position on first detection
        if self.previous_scroll_y is None:
            self.previous_scroll_y = midpoint_y
            return None
        
        # Calculate vertical displacement
        displacement = self.previous_scroll_y - midpoint_y
        
        # Check if displacement exceeds threshold
        if abs(displacement) > config.SCROLL_THRESHOLD:
            self.current_state = config.STATE_SCROLLING
            scroll_amount = displacement * config.SCROLL_MULTIPLIER
            self.previous_scroll_y = midpoint_y
            return scroll_amount
        
        return None
    
    def get_state(self):
        """
        Get current gesture state.
        
        Returns:
            Current state string
        """
        return self.current_state

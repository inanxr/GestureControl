"""
Hand tracking wrapper using MediaPipe Hands.
"""
import cv2
import mediapipe as mp
import config


class HandTracker:
    """Wrapper for MediaPipe Hands to detect and track hand landmarks."""
    
    def __init__(self):
        """Initialize MediaPipe Hands."""
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Initialize hands detector
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,  # Video mode for better performance
            max_num_hands=config.MAX_NUM_HANDS,
            min_detection_confidence=config.MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=config.MIN_TRACKING_CONFIDENCE
        )
        
        print("Hand tracker initialized")
    
    def process_frame(self, frame):
        """
        Process frame to detect hands.
        
        Args:
            frame: BGR frame from camera
        
        Returns:
            MediaPipe results object containing hand landmarks
        """
        # Convert BGR to RGB (MediaPipe uses RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process and detect hands
        results = self.hands.process(rgb_frame)
        
        return results
    
    def get_landmarks(self, results):
        """
        Extract hand landmarks from results.
        
        Args:
            results: MediaPipe results object
        
        Returns:
            List of normalized landmarks (0-1 range), or None if no hands detected
        """
        if results.multi_hand_landmarks:
            # Return first hand's landmarks
            return results.multi_hand_landmarks[0].landmark
        
        return None
    
    def draw_landmarks(self, frame, results):
        """
        Draw hand landmarks on frame for visual feedback.
        
        Args:
            frame: Frame to draw on
            results: MediaPipe results object
        
        Returns:
            Frame with landmarks drawn
        """
        if not config.SHOW_LANDMARKS:
            return frame
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks and connections
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )
        
        return frame
    
    def release(self):
        """Release MediaPipe resources."""
        if self.hands:
            self.hands.close()
            print("Hand tracker released")

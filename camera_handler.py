"""
Camera handler for capturing and preprocessing webcam frames.
"""
import cv2
import config


class CameraHandler:
    """Manages webcam input and frame preprocessing."""
    
    def __init__(self, camera_index=config.CAMERA_INDEX):
        """
        Initialize camera handler.
        
        Args:
            camera_index: Index of camera to use (0 = default)
        """
        self.camera_index = camera_index
        self.cap = None
        self.frame_width = config.CAMERA_WIDTH
        self.frame_height = config.CAMERA_HEIGHT
    
    def start(self):
        """
        Start camera capture.
        
        Returns:
            True if camera started successfully, False otherwise
        """
        self.cap = cv2.VideoCapture(self.camera_index)
        
        if not self.cap.isOpened():
            print(f"Error: Could not open camera {self.camera_index}")
            return False
        
        # Set camera resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
        self.cap.set(cv2.CAP_PROP_FPS, config.TARGET_FPS)
        
        # Get actual resolution (may differ from requested)
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        print(f"Camera started: {self.frame_width}x{self.frame_height}")
        return True
    
    def read_frame(self):
        """
        Capture and preprocess a frame.
        
        Returns:
            Preprocessed frame (flipped horizontally for mirror effect),
            or None if capture failed
        """
        if self.cap is None or not self.cap.isOpened():
            return None
        
        success, frame = self.cap.read()
        
        if not success:
            print("Error: Failed to capture frame")
            return None
        
        # Flip horizontally for mirror effect (more intuitive)
        frame = cv2.flip(frame, 1)
        
        return frame
    
    def get_dimensions(self):
        """
        Get frame dimensions.
        
        Returns:
            Tuple of (width, height)
        """
        return self.frame_width, self.frame_height
    
    def release(self):
        """Release camera resources."""
        if self.cap is not None:
            self.cap.release()
            print("Camera released")

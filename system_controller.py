"""
System controller for executing mouse and keyboard actions using PyAutoGUI.
"""
import pyautogui
import config


class SystemController:
    """Wrapper for PyAutoGUI to control mouse and keyboard."""
    
    def __init__(self):
        """Initialize system controller."""
        # Set PyAutoGUI settings
        pyautogui.FAILSAFE = config.ENABLE_FAILSAFE
        pyautogui.PAUSE = 0  # No pause between actions for smooth movement
        
        self.screen_width, self.screen_height = pyautogui.size()
        print(f"System controller initialized: {self.screen_width}x{self.screen_height}")
    
    def move_cursor(self, x, y):
        """
        Move cursor to specified screen coordinates.
        
        Args:
            x: X coordinate in pixels
            y: Y coordinate in pixels
        """
        # Apply boundary checking
        x = max(config.SCREEN_BOUNDARY_MARGIN, 
                min(x, self.screen_width - config.SCREEN_BOUNDARY_MARGIN))
        y = max(config.SCREEN_BOUNDARY_MARGIN, 
                min(y, self.screen_height - config.SCREEN_BOUNDARY_MARGIN))
        
        try:
            pyautogui.moveTo(x, y, duration=0)  # Instant movement for smoothness
        except pyautogui.FailSafeException:
            print("Failsafe triggered! Mouse moved to corner.")
            raise
    
    def left_click(self):
        """Perform a left mouse click."""
        try:
            pyautogui.click()
            print("Left click")
        except pyautogui.FailSafeException:
            print("Failsafe triggered!")
            raise
    
    def right_click(self):
        """Perform a right mouse click."""
        try:
            pyautogui.rightClick()
            print("Right click")
        except pyautogui.FailSafeException:
            print("Failsafe triggered!")
            raise
    
    def scroll(self, amount):
        """
        Perform scroll action.
        
        Args:
            amount: Scroll amount (positive = up, negative = down)
        """
        try:
            pyautogui.scroll(int(amount))
        except pyautogui.FailSafeException:
            print("Failsafe triggered!")
            raise
    
    def get_screen_size(self):
        """
        Get screen dimensions.
        
        Returns:
            Tuple of (width, height)
        """
        return self.screen_width, self.screen_height

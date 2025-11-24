"""
Gesture-Controlled Windows Software
Main application entry point.
"""
import cv2
import sys
from camera_handler import CameraHandler
from hand_tracker import HandTracker
from gesture_recognizer import GestureRecognizer
from system_controller import SystemController
from utils import FPSCounter
import config


def main():
    """Main application loop."""
    print("=" * 50)
    print("GESTURE CONTROL - Starting Application")
    print("=" * 50)
    print("\nControls:")
    print("  - Index finger: Move cursor")
    print("  - Index + Thumb pinch: Left click")
    print("  - Middle + Thumb pinch: Right click")
    print("  - Two fingers vertical: Scroll")
    print("  - ESC key: Exit application")
    print("  - Move mouse to corner: Emergency stop")
    print("=" * 50)
    print()
    
    # Initialize components
    camera = CameraHandler()
    if not camera.start():
        print("Failed to start camera. Exiting.")
        return
    
    hand_tracker = HandTracker()
    frame_width, frame_height = camera.get_dimensions()
    gesture_recognizer = GestureRecognizer(frame_width, frame_height)
    system_controller = SystemController()
    fps_counter = FPSCounter()
    
    print("All components initialized. Starting main loop...")
    print("Press ESC to exit.\n")
    
    try:
        while True:
            # Capture frame
            frame = camera.read_frame()
            if frame is None:
                print("Failed to read frame")
                break
            
            # Process frame for hand detection
            results = hand_tracker.process_frame(frame)
            landmarks = hand_tracker.get_landmarks(results)
            
            # Recognize gestures
            gestures = gesture_recognizer.recognize(landmarks)
            
            # Execute actions based on gestures
            if gestures['cursor_pos'] is not None:
                x, y = gestures['cursor_pos']
                system_controller.move_cursor(x, y)
            
            if gestures['left_click']:
                system_controller.left_click()
            
            if gestures['right_click']:
                system_controller.right_click()
            
            if gestures['scroll'] is not None:
                system_controller.scroll(gestures['scroll'])
            
            # Draw visual feedback
            frame = hand_tracker.draw_landmarks(frame, results)
            
            # Display FPS and state
            if config.SHOW_FPS:
                fps = fps_counter.update()
                state = gesture_recognizer.get_state()
                cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f"State: {state}", (10, 70),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                
                # Show hand detection status
                hand_status = "Hand Detected" if landmarks else "No Hand"
                color = (0, 255, 0) if landmarks else (0, 0, 255)
                cv2.putText(frame, hand_status, (10, 110),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
            # Display frame
            cv2.imshow('Gesture Control', frame)
            
            # Check for exit key (ESC)
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC key
                print("\nESC pressed. Exiting...")
                break
    
    except KeyboardInterrupt:
        print("\n\nKeyboard interrupt detected. Exiting...")
    
    except Exception as e:
        print(f"\nError occurred: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        print("\nCleaning up resources...")
        camera.release()
        hand_tracker.release()
        cv2.destroyAllWindows()
        print("Cleanup complete. Goodbye!")


if __name__ == "__main__":
    main()

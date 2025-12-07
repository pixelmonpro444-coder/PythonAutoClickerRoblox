import pyautogui
import keyboard
import time
import threading
from typing import Optional

class AutoClicker:
    def __init__(self):
        self.clicking = False
        self.click_delay = 0.1
        self.click_button = 'left'
        self.hotkey_start = 'F1'
        self.hotkey_stop = 'F2'
        
    def start_clicking(self):
        """Start the auto clicking process"""
        self.clicking = True
        print(f"Auto clicker started! Press {self.hotkey_stop} to stop.")
        
        while self.clicking:
            try:
                pyautogui.click(button=self.click_button)
                time.sleep(self.click_delay)
            except pyautogui.FailSafeException:
                print("Fail-safe triggered! Mouse moved to corner of screen.")
                self.stop_clicking()
                break
                
    def stop_clicking(self):
        """Stop the auto clicking process"""
        self.clicking = False
        print("Auto clicker stopped.")
        
    def set_click_delay(self, delay: float):
        """Set the delay between clicks in seconds"""
        self.click_delay = max(0.01, delay)
        print(f"Click delay set to {self.click_delay} seconds")
        
    def set_click_button(self, button: str):
        """Set the mouse button to click ('left', 'right', 'middle')"""
        if button in ['left', 'right', 'middle']:
            self.click_button = button
            print(f"Click button set to {button}")
        else:
            print("Invalid button. Use 'left', 'right', or 'middle'")
            
    def setup_hotkeys(self):
        """Setup keyboard hotkeys"""
        keyboard.add_hotkey(self.hotkey_start, self.start_clicking_thread)
        keyboard.add_hotkey(self.hotkey_stop, self.stop_clicking)
        print(f"Hotkeys set: {self.hotkey_start} to start, {self.hotkey_stop} to stop")
        
    def start_clicking_thread(self):
        """Start clicking in a separate thread"""
        if not self.clicking:
            click_thread = threading.Thread(target=self.start_clicking)
            click_thread.daemon = True
            click_thread.start()
            
    def run(self):
        """Main method to run the auto clicker"""
        print("=== Python Auto Clicker ===")
        print("Controls:")
        print(f"  {self.hotkey_start} - Start clicking")
        print(f"  {self.hotkey_stop} - Stop clicking")
        print("  ESC - Exit program")
        print("\nSettings:")
        print(f"  Click delay: {self.click_delay} seconds")
        print(f"  Click button: {self.click_button}")
        print("\nMove mouse to corner of screen to trigger emergency stop.")
        
        self.setup_hotkeys()
        
        try:
            keyboard.wait('esc')
        except KeyboardInterrupt:
            pass
        finally:
            self.stop_clicking()
            print("Program exited.")

if __name__ == "__main__":
    # Disable pyautogui failsafe for 3 seconds to allow setup
    pyautogui.FAILSAFE = True
    
    clicker = AutoClicker()
    
    # Optional: Configure settings here
    # clicker.set_click_delay(0.05)  # Faster clicking
    # clicker.set_click_button('right')  # Right-click instead
    
    clicker.run()
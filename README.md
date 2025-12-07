# Python Auto Clicker

A simple and effective auto clicker application for Python that can be used for various purposes including gaming automation.

## Features

- **Hotkey Control**: Start/stop clicking with customizable hotkeys (F1/F2 by default)
- **Adjustable Click Speed**: Set custom delay between clicks
- **Multiple Mouse Buttons**: Support for left, right, and middle mouse buttons
- **Emergency Stop**: Move mouse to screen corner to trigger failsafe
- **Clean Exit**: Press ESC to safely exit the program

## Installation

1. Clone this repository:
```bash
git clone https://github.com/pixelmonpro444-coder/PythonAutoClickerRoblox.git
cd PythonAutoClickerRoblox
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the auto clicker:
```bash
python autoclicker.py
```

### Controls
- **F1**: Start clicking
- **F2**: Stop clicking  
- **ESC**: Exit program
- **Mouse to corner**: Emergency stop (failsafe)

### Customization

You can modify the settings in the `if __name__ == "__main__":` section of `autoclicker.py`:

```python
# Example custom settings
clicker.set_click_delay(0.05)  # Click every 50ms
clicker.set_click_button('right')  # Use right mouse button
```

## Safety Features

- **FailSafe**: Moving mouse to top-left corner of screen immediately stops clicking
- **Clean Threading**: Proper thread management prevents resource leaks
- **Keyboard Interrupt Handling**: Graceful shutdown on Ctrl+C

## Requirements

- Python 3.7+
- pyautogui >= 0.9.54
- keyboard >= 0.13.5

## Disclaimer

This software is intended for educational and legitimate automation purposes only. Users are responsible for ensuring compliance with applicable terms of service and laws.
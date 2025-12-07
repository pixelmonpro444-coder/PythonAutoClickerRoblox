# 🦅 Raven Inc Auto Clicker - Professional Edition

An enterprise-grade auto clicker application with advanced anti-detection features and a modern GUI interface. Built by Raven Inc for professional automation needs.

## ✨ Features

### 🎯 Core Functionality
- **Modern PyQt6 GUI**: Enterprise-grade dark theme interface
- **Advanced Anti-Detection**: Human-like movement patterns and random delays
- **Profile Management**: Save and load custom clicking profiles
- **Real-time Statistics**: Live CPS tracking and session analytics
- **System Tray Integration**: Minimize to tray with quick controls

### 🛡️ Anti-Detection Technology
- **Human-like Mouse Movement**: Bezier curve paths for natural motion
- **Random Position Variance**: Click within configurable radius
- **Intelligent Delays**: Random variance with occasional micro-pauses
- **Click Patterns**: Single, double, burst, and random patterns
- **Behavioral Mimicry**: Simulates human clicking behavior

### ⚙️ Advanced Features
- **Configurable Limits**: Max clicks and duration limits
- **Multiple Mouse Buttons**: Left, right, and middle button support
- **Hotkey Control**: Customizable start/stop hotkeys
- **Emergency Failsafe**: Mouse corner detection for instant stop
- **Session History**: Track clicking sessions with detailed statistics

### 🎨 User Interface
- **Dark Theme**: Modern, easy-on-the-eyes interface
- **Tabbed Layout**: Organized controls in Main, Profiles, Statistics, and Settings tabs
- **Live Status Display**: Real-time feedback and progress indicators
- **Responsive Design**: Smooth animations and hover effects

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/pixelmonpro444-coder/PythonAutoClickerRoblox.git
cd PythonAutoClickerRoblox
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## 🎮 Usage

### GUI Application (Recommended)
```bash
python raven_autoclicker.py
```

### Command Line Interface
```bash
python autoclicker.py
```

## 🎛️ Controls

### GUI Controls
- **Start Button**: Begin clicking with current settings
- **Stop Button**: Stop clicking immediately
- **System Tray**: Right-click tray icon for quick controls

### Hotkeys (Default)
- **F1**: Start clicking
- **F2**: Stop clicking
- **ESC**: Exit application
- **Mouse Corner**: Emergency stop (failsafe)

## 📊 Profile System

Create and manage multiple clicking profiles:

1. **Configure Settings**: Set delay, pattern, and anti-detection options
2. **Save Profile**: Click "Save Current Profile" and enter a name
3. **Load Profile**: Select from table and click "Load Selected"
4. **Quick Switch**: Easily switch between different configurations

### Profile Settings
- **Base Delay**: Primary delay between clicks (1-10000ms)
- **Random Variance**: Percentage of randomization (0-100%)
- **Click Pattern**: Single, Double, Burst, or Random
- **Anti-Detection**: Enable human-like behavior
- **Position Radius**: Random click area around cursor
- **Click Limits**: Maximum clicks or duration limits

## 🛡️ Safety Features

### Anti-Detection
- **Bezier Curve Movement**: Natural mouse paths
- **Random Timing**: Variable delays with micro-pauses
- **Position Jitter**: Slight random movements
- **Behavioral Patterns**: Mimics human clicking habits

### Safety Mechanisms
- **FailSafe Detection**: Mouse corner triggers instant stop
- **Focus Loss Detection**: Optional auto-stop on app focus loss
- **Clean Threading**: Proper resource management
- **Emergency Controls**: Multiple stop methods

## 📈 Statistics & Analytics

### Real-time Metrics
- **Current CPS**: Live clicks per second
- **Total Clicks**: Session click counter
- **Elapsed Time**: Session duration tracker
- **Progress Bar**: Visual progress toward limits

### Session History
- **Timestamp**: Record of each session
- **Profile Used**: Which configuration was active
- **Performance Metrics**: CPS and duration data
- **Export Capability**: Save session data

## ⚙️ Configuration

### Application Settings
- **Hotkey Customization**: Configure start/stop hotkeys
- **System Tray**: Enable/disable tray integration
- **Failsafe Options**: Toggle safety features
- **Auto-save Settings**: Preserve configuration

### Profile Storage
- **JSON Format**: Human-readable profile files
- **Auto-backup**: Automatic profile saving
- **Import/Export**: Share profiles between users

## 🔧 Requirements

- **Python 3.8+**: Modern Python features required
- **PyQt6 >= 6.5.0**: GUI framework
- **pyautogui >= 0.9.54**: Mouse automation
- **keyboard >= 0.13.5**: Hotkey handling
- **numpy >= 1.24.0**: Mathematical operations

## 🖥️ Platform Support

- **Windows 10/11**: Primary platform with full feature support
- **macOS**: Limited support (keyboard permissions required)
- **Linux**: Basic support (X11 display required)

## 📝 License & Disclaimer

© 2024 Raven Inc. All rights reserved.

**IMPORTANT**: This software is intended for legitimate automation and testing purposes only. Users are responsible for:

- Compliance with applicable terms of service
- Adherence to local laws and regulations
- Ethical use of automation features
- Respecting anti-cheat policies in games

Raven Inc is not responsible for misuse of this software.

## 🐛 Troubleshooting

### Common Issues
- **Permission Errors**: Run as administrator on Windows
- **Keyboard Hotkeys**: Check for conflicting applications
- **Anti-Virus**: Add to exclusions if flagged
- **Display Scaling**: Adjust DPI settings for proper clicking

### Support
For issues and feature requests, please use the GitHub Issues page.

---

**🦅 Raven Inc - Professional Automation Solutions**
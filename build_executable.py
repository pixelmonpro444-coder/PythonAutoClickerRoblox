import sys
import os

def build_executable():
    """Build the Raven Auto Clicker executable"""
    print("Building Raven Inc Auto Clicker...")
    
    # Install PyInstaller if not available
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        os.system(f"{sys.executable} -m pip install pyinstaller")
    
    # Build the executable
    print("Building executable...")
    os.system(f"{sys.executable} -m PyInstaller --onefile --windowed --name=RavenAutoClicker raven_autoclicker_complete.py")
    
    # Check if build was successful
    if os.path.exists("dist/RavenAutoClicker.exe"):
        print("Build successful!")
        print(f"Executable created: dist/RavenAutoClicker.exe")
        print(f"File size: {os.path.getsize('dist/RavenAutoClicker.exe') / (1024*1024):.1f} MB")
        
        # Create distribution package
        print("Creating distribution package...")
        os.makedirs("release", exist_ok=True)
        
        # Copy executable
        import shutil
        shutil.copy("dist/RavenAutoClicker.exe", "release/")
        
        # Copy documentation
        if os.path.exists("README.md"):
            shutil.copy("README.md", "release/")
        if os.path.exists("READMEQT.md"):
            shutil.copy("READMEQT.md", "release/")
        
        # Create README for executable users
        exe_readme = """# Raven Inc Auto Clicker - Executable Version

## Quick Start

1. Double-click `RavenAutoClicker.exe` to start the application
2. Configure your clicking settings in the Main tab
3. Click "Start Clicking" to begin
4. Press F2 to stop clicking (or use the Stop button)

## Features

- **Modern GUI**: Dark theme interface with intuitive controls
- **Anti-Detection**: Human-like movement patterns and random delays
- **Profile Management**: Save and load different configurations
- **Visual Analytics**: Click heat map and session statistics
- **System Tray**: Minimize to tray for quick access
- **Hotkey Control**: F1 to start, F2 to stop

## Safety

- **Emergency Stop**: Move mouse to top-left corner of screen
- **Clean Exit**: Close button or system tray > Quit
- **No Installation Required**: Portable executable

## Requirements

- Windows 10/11
- No additional software needed

## Troubleshooting

- **Antivirus**: Add to exclusions if flagged
- **Permissions**: Run as administrator if needed
- **Crashes**: Check Windows Event Viewer for details

## Configuration

Profiles and settings are saved in:
`%APPDATA%\\Raven Inc\\AutoClicker\\`

© 2024 Raven Inc. All rights reserved.
"""
        
        with open("release/README_Executable.txt", "w") as f:
            f.write(exe_readme)
        
        print("Release package created in 'release' folder")
        print("Ready for distribution!")
        
    else:
        print("Build failed!")
        return False
    
    return True

if __name__ == "__main__":
    build_executable()
import sys
import json
import time
import random
import threading
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QPushButton, QSpinBox, QDoubleSpinBox,
    QComboBox, QTabWidget, QGroupBox, QCheckBox, QTextEdit,
    QProgressBar, QSlider, QFrame, QSplitter, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox, QFileDialog,
    QSystemTrayIcon, QMenu, QStyle, QToolTip
)
from PyQt6.QtCore import (
    Qt, QTimer, QThread, pyqtSignal, QObject, QPropertyAnimation,
    QEasingCurve, QRect, QSettings, QStandardPaths
)
from PyQt6.QtGui import (
    QIcon, QPixmap, QPainter, QColor, QPen, QBrush, QFont,
    QPalette, QLinearGradient, QRadialGradient, QAction
)

import pyautogui
import keyboard

@dataclass
class ClickProfile:
    name: str
    base_delay: float
    random_variance: float
    click_pattern: str
    anti_detect: bool
    human_movement: bool
    random_position: bool
    position_radius: int
    click_button: str
    max_clicks: int
    duration_limit: int

class AntiDetectionEngine:
    """Advanced anti-detection engine for human-like clicking"""
    
    @staticmethod
    def human_delay(base_delay: float, variance: float) -> float:
        """Generate human-like delay with natural variance"""
        delay = base_delay + random.uniform(-variance, variance)
        # Add occasional micro-pauses
        if random.random() < 0.05:
            delay += random.uniform(0.1, 0.3)
        return max(0.01, delay)
    
    @staticmethod
    def human_movement(start_pos: Tuple[int, int], end_pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Generate human-like mouse movement path"""
        steps = random.randint(8, 15)
        path = []
        
        for i in range(steps + 1):
            t = i / steps
            # Bezier curve for natural movement
            t = t * t * (3.0 - 2.0 * t)
            
            x = start_pos[0] + (end_pos[0] - start_pos[0]) * t
            y = start_pos[1] + (end_pos[1] - start_pos[1]) * t
            
            # Add slight random jitter
            x += random.uniform(-2, 2)
            y += random.uniform(-2, 2)
            
            path.append((int(x), int(y)))
        
        return path
    
    @staticmethod
    def random_position_around(center: Tuple[int, int], radius: int) -> Tuple[int, int]:
        """Generate random position around center point"""
        angle = random.uniform(0, 2 * math.pi)
        r = random.uniform(0, radius)
        x = center[0] + int(r * math.cos(angle))
        y = center[1] + int(r * math.sin(angle))
        return x, y

class ClickWorker(QObject):
    """Background worker for clicking operations"""
    status_update = pyqtSignal(str)
    stats_update = pyqtSignal(int, int, float)
    finished = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.is_running = False
        self.should_stop = False
        self.profile = None
        self.start_time = None
        self.click_count = 0
        self.total_clicks = 0
        
    def set_profile(self, profile: ClickProfile):
        self.profile = profile
        
    def start_clicking(self):
        self.is_running = True
        self.should_stop = False
        self.start_time = time.time()
        self.click_count = 0
        self.total_clicks = 0
        
        pyautogui.FAILSAFE = True
        
        while self.is_running and not self.should_stop:
            try:
                # Check limits
                if self.profile.max_clicks > 0 and self.total_clicks >= self.profile.max_clicks:
                    break
                if self.profile.duration_limit > 0 and (time.time() - self.start_time) >= self.profile.duration_limit:
                    break
                
                # Get click position
                if self.profile.random_position:
                    current_pos = pyautogui.position()
                    click_pos = AntiDetectionEngine.random_position_around(current_pos, self.profile.position_radius)
                else:
                    click_pos = pyautogui.position()
                
                # Human movement
                if self.profile.human_movement and self.profile.anti_detect:
                    current_pos = pyautogui.position()
                    path = AntiDetectionEngine.human_movement(current_pos, click_pos)
                    for pos in path[:-1]:
                        pyautogui.moveTo(pos[0], pos[1], duration=0.01)
                
                # Perform click
                pyautogui.click(click_pos[0], click_pos[1], button=self.profile.click_button)
                self.click_count += 1
                self.total_clicks += 1
                
                # Human-like delay
                if self.profile.anti_detect:
                    delay = AntiDetectionEngine.human_delay(self.profile.base_delay, self.profile.random_variance)
                else:
                    delay = self.profile.base_delay
                
                time.sleep(delay)
                
                # Update stats
                elapsed = time.time() - self.start_time
                self.stats_update.emit(self.click_count, self.total_clicks, elapsed)
                
            except pyautogui.FailSafeException:
                self.status_update.emit("Emergency stop triggered!")
                break
            except Exception as e:
                self.status_update.emit(f"Error: {str(e)}")
                break
        
        self.is_running = False
        self.finished.emit()
    
    def stop_clicking(self):
        self.should_stop = True

class ModernButton(QPushButton):
    """Modern styled button with hover effects"""
    
    def __init__(self, text, color="#2196F3", hover_color="#1976D2"):
        super().__init__(text)
        self.base_color = QColor(color)
        self.hover_color = QColor(hover_color)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {hover_color};
                transform: translateY(1px);
            }}
            QPushButton:disabled {{
                background-color: #CCCCCC;
                color: #666666;
            }}
        """)

class RavenAutoClickerGUI(QMainWindow):
    """Main GUI application for Raven Inc Auto Clicker"""
    
    def __init__(self):
        super().__init__()
        self.worker = None
        self.worker_thread = None
        self.profiles = self.load_profiles()
        self.current_profile = None
        self.settings = QSettings("Raven Inc", "AutoClicker")
        
        self.init_ui()
        self.setup_system_tray()
        self.load_settings()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Raven Inc Auto Clicker - Professional Edition")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set modern dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1E1E1E;
                color: #FFFFFF;
            }
            QWidget {
                background-color: #2D2D2D;
                color: #FFFFFF;
            }
            QTabWidget::pane {
                border: 1px solid #3D3D3D;
                background-color: #2D2D2D;
            }
            QTabBar::tab {
                background-color: #3D3D3D;
                color: #FFFFFF;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QTabBar::tab:selected {
                background-color: #2196F3;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #3D3D3D;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QLabel {
                color: #FFFFFF;
            }
            QSpinBox, QDoubleSpinBox, QComboBox {
                background-color: #3D3D3D;
                color: #FFFFFF;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 5px;
            }
            QCheckBox {
                color: #FFFFFF;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                background-color: #3D3D3D;
                border: 2px solid #555555;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                background-color: #2196F3;
                border-color: #2196F3;
            }
            QTextEdit {
                background-color: #1E1E1E;
                color: #FFFFFF;
                border: 1px solid #3D3D3D;
                border-radius: 4px;
            }
            QProgressBar {
                border: 1px solid #3D3D3D;
                border-radius: 4px;
                text-align: center;
                background-color: #3D3D3D;
            }
            QProgressBar::chunk {
                background-color: #2196F3;
                border-radius: 3px;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Header with Raven Inc branding
        header_layout = QHBoxLayout()
        
        # Logo/Title
        title_label = QLabel("🦅 Raven Inc Auto Clicker")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2196F3;
            padding: 10px;
        """)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Status indicator
        self.status_label = QLabel("● Ready")
        self.status_label.setStyleSheet("""
            font-size: 16px;
            color: #4CAF50;
            padding: 10px;
        """)
        header_layout.addWidget(self.status_label)
        
        main_layout.addLayout(header_layout)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Create tabs
        self.create_main_tab()
        self.create_profiles_tab()
        self.create_statistics_tab()
        self.create_settings_tab()
        
        # Bottom control panel
        self.create_control_panel(main_layout)
        
    def create_main_tab(self):
        """Create the main clicking tab"""
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        
        # Quick settings
        quick_group = QGroupBox("Quick Settings")
        quick_layout = QGridLayout(quick_group)
        
        # Click delay
        quick_layout.addWidget(QLabel("Base Delay (ms):"), 0, 0)
        self.delay_spinbox = QDoubleSpinBox()
        self.delay_spinbox.setRange(1, 10000)
        self.delay_spinbox.setValue(100)
        self.delay_spinbox.setSuffix(" ms")
        quick_layout.addWidget(self.delay_spinbox, 0, 1)
        
        # Click button
        quick_layout.addWidget(QLabel("Mouse Button:"), 0, 2)
        self.button_combo = QComboBox()
        self.button_combo.addItems(["left", "right", "middle"])
        quick_layout.addWidget(self.button_combo, 0, 3)
        
        # Anti-detect
        self.anti_detect_checkbox = QCheckBox("Enable Anti-Detection")
        self.anti_detect_checkbox.setChecked(True)
        quick_layout.addWidget(self.anti_detect_checkbox, 1, 0, 1, 2)
        
        # Human movement
        self.human_movement_checkbox = QCheckBox("Human-like Movement")
        self.human_movement_checkbox.setChecked(True)
        quick_layout.addWidget(self.human_movement_checkbox, 1, 2, 1, 2)
        
        layout.addWidget(quick_group)
        
        # Advanced settings
        advanced_group = QGroupBox("Advanced Settings")
        advanced_layout = QGridLayout(advanced_group)
        
        # Random variance
        advanced_layout.addWidget(QLabel("Random Variance:"), 0, 0)
        self.variance_spinbox = QDoubleSpinBox()
        self.variance_spinbox.setRange(0, 100)
        self.variance_spinbox.setValue(20)
        self.variance_spinbox.setSuffix(" %")
        advanced_layout.addWidget(self.variance_spinbox, 0, 1)
        
        # Random position
        self.random_position_checkbox = QCheckBox("Random Position")
        advanced_layout.addWidget(self.random_position_checkbox, 0, 2)
        
        # Position radius
        advanced_layout.addWidget(QLabel("Position Radius:"), 1, 0)
        self.radius_spinbox = QSpinBox()
        self.radius_spinbox.setRange(1, 100)
        self.radius_spinbox.setValue(10)
        self.radius_spinbox.setSuffix(" px")
        advanced_layout.addWidget(self.radius_spinbox, 1, 1)
        
        # Click pattern
        advanced_layout.addWidget(QLabel("Click Pattern:"), 1, 2)
        self.pattern_combo = QComboBox()
        self.pattern_combo.addItems(["Single", "Double", "Burst", "Random"])
        advanced_layout.addWidget(self.pattern_combo, 1, 3)
        
        # Limits
        advanced_layout.addWidget(QLabel("Max Clicks:"), 2, 0)
        self.max_clicks_spinbox = QSpinBox()
        self.max_clicks_spinbox.setRange(0, 100000)
        self.max_clicks_spinbox.setValue(0)
        self.max_clicks_spinbox.setSpecialValueText("Unlimited")
        advanced_layout.addWidget(self.max_clicks_spinbox, 2, 1)
        
        advanced_layout.addWidget(QLabel("Duration Limit:"), 2, 2)
        self.duration_spinbox = QSpinBox()
        self.duration_spinbox.setRange(0, 3600)
        self.duration_spinbox.setValue(0)
        self.duration_spinbox.setSuffix(" sec")
        self.duration_spinbox.setSpecialValueText("Unlimited")
        advanced_layout.addWidget(self.duration_spinbox, 2, 3)
        
        layout.addWidget(advanced_group)
        
        # Live status
        status_group = QGroupBox("Live Status")
        status_layout = QVBoxLayout(status_group)
        
        # Stats display
        stats_layout = QHBoxLayout()
        
        self.clicks_label = QLabel("Clicks: 0")
        self.total_clicks_label = QLabel("Total: 0")
        self.elapsed_label = QLabel("Elapsed: 0s")
        self.cps_label = QLabel("CPS: 0.0")
        
        stats_layout.addWidget(self.clicks_label)
        stats_layout.addWidget(self.total_clicks_label)
        stats_layout.addWidget(self.elapsed_label)
        stats_layout.addWidget(self.cps_label)
        
        status_layout.addLayout(stats_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        status_layout.addWidget(self.progress_bar)
        
        # Log display
        self.log_display = QTextEdit()
        self.log_display.setMaximumHeight(150)
        self.log_display.setReadOnly(True)
        status_layout.addWidget(self.log_display)
        
        layout.addWidget(status_group)
        
        self.tab_widget.addTab(main_widget, "🎯 Main")
        
    def create_profiles_tab(self):
        """Create the profiles management tab"""
        profiles_widget = QWidget()
        layout = QVBoxLayout(profiles_widget)
        
        # Profile list
        profile_list_group = QGroupBox("Saved Profiles")
        profile_list_layout = QVBoxLayout(profile_list_group)
        
        self.profile_table = QTableWidget()
        self.profile_table.setColumnCount(4)
        self.profile_table.setHorizontalHeaderLabels(["Name", "Delay", "Pattern", "Anti-Detect"])
        self.profile_table.horizontalHeader().setStretchLastSection(True)
        profile_list_layout.addWidget(self.profile_table)
        
        # Profile buttons
        profile_buttons_layout = QHBoxLayout()
        
        self.save_profile_btn = ModernButton("Save Current Profile", "#4CAF50")
        self.load_profile_btn = ModernButton("Load Selected", "#2196F3")
        self.delete_profile_btn = ModernButton("Delete Selected", "#F44336")
        
        profile_buttons_layout.addWidget(self.save_profile_btn)
        profile_buttons_layout.addWidget(self.load_profile_btn)
        profile_buttons_layout.addWidget(self.delete_profile_btn)
        profile_buttons_layout.addStretch()
        
        profile_list_layout.addLayout(profile_buttons_layout)
        layout.addWidget(profile_list_group)
        
        # Profile details
        details_group = QGroupBox("Profile Details")
        details_layout = QVBoxLayout(details_group)
        
        self.profile_details = QTextEdit()
        self.profile_details.setReadOnly(True)
        self.profile_details.setMaximumHeight(200)
        details_layout.addWidget(self.profile_details)
        
        layout.addWidget(details_group)
        
        # Connect signals
        self.save_profile_btn.clicked.connect(self.save_profile)
        self.load_profile_btn.clicked.connect(self.load_profile)
        self.delete_profile_btn.clicked.connect(self.delete_profile)
        self.profile_table.itemSelectionChanged.connect(self.update_profile_details)
        
        self.tab_widget.addTab(profiles_widget, "📁 Profiles")
        
    def create_statistics_tab(self):
        """Create the statistics tab"""
        stats_widget = QWidget()
        layout = QVBoxLayout(stats_widget)
        
        # Session statistics
        session_group = QGroupBox("Session Statistics")
        session_layout = QGridLayout(session_group)
        
        self.session_clicks_label = QLabel("0")
        self.session_time_label = QLabel("0s")
        self.session_cps_label = QLabel("0.0")
        self.session_accuracy_label = QLabel("100%")
        
        session_layout.addWidget(QLabel("Total Clicks:"), 0, 0)
        session_layout.addWidget(self.session_clicks_label, 0, 1)
        session_layout.addWidget(QLabel("Session Time:"), 0, 2)
        session_layout.addWidget(self.session_time_label, 0, 3)
        session_layout.addWidget(QLabel("Average CPS:"), 1, 0)
        session_layout.addWidget(self.session_cps_label, 1, 1)
        session_layout.addWidget(QLabel("Accuracy:"), 1, 2)
        session_layout.addWidget(self.session_accuracy_label, 1, 3)
        
        layout.addWidget(session_group)
        
        # History
        history_group = QGroupBox("Click History")
        history_layout = QVBoxLayout(history_group)
        
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(["Time", "Profile", "Clicks", "Duration", "CPS"])
        self.history_table.horizontalHeader().setStretchLastSection(True)
        history_layout.addWidget(self.history_table)
        
        layout.addWidget(history_group)
        
        self.tab_widget.addTab(stats_widget, "📊 Statistics")
        
    def create_settings_tab(self):
        """Create the settings tab"""
        settings_widget = QWidget()
        layout = QVBoxLayout(settings_widget)
        
        # General settings
        general_group = QGroupBox("General Settings")
        general_layout = QGridLayout(general_group)
        
        # Hotkeys
        general_layout.addWidget(QLabel("Start Hotkey:"), 0, 0)
        self.start_hotkey_combo = QComboBox()
        self.start_hotkey_combo.addItems(["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10"])
        self.start_hotkey_combo.setCurrentText("F1")
        general_layout.addWidget(self.start_hotkey_combo, 0, 1)
        
        general_layout.addWidget(QLabel("Stop Hotkey:"), 0, 2)
        self.stop_hotkey_combo = QComboBox()
        self.stop_hotkey_combo.addItems(["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10"])
        self.stop_hotkey_combo.setCurrentText("F2")
        general_layout.addWidget(self.stop_hotkey_combo, 0, 3)
        
        # System tray
        self.system_tray_checkbox = QCheckBox("Enable System Tray")
        self.system_tray_checkbox.setChecked(True)
        general_layout.addWidget(self.system_tray_checkbox, 1, 0, 1, 2)
        
        self.minimize_to_tray_checkbox = QCheckBox("Minimize to Tray")
        self.minimize_to_tray_checkbox.setChecked(True)
        general_layout.addWidget(self.minimize_to_tray_checkbox, 1, 2, 1, 2)
        
        layout.addWidget(general_group)
        
        # Safety settings
        safety_group = QGroupBox("Safety Settings")
        safety_layout = QGridLayout(safety_group)
        
        self.failsafe_checkbox = QCheckBox("Enable Failsafe (Mouse Corner)")
        self.failsafe_checkbox.setChecked(True)
        safety_layout.addWidget(self.failsafe_checkbox, 0, 0, 1, 2)
        
        self.auto_stop_checkbox = QCheckBox("Auto-stop on Application Focus Loss")
        safety_layout.addWidget(self.auto_stop_checkbox, 0, 2, 1, 2)
        
        layout.addWidget(safety_group)
        
        # About
        about_group = QGroupBox("About")
        about_layout = QVBoxLayout(about_group)
        
        about_text = """
🦅 Raven Inc Auto Clicker - Professional Edition
Version: 2.0.0

Advanced auto-clicking solution with enterprise-grade features:
• Anti-detection technology
• Human-like movement patterns
• Profile management
• Real-time statistics
• Modern GUI interface

© 2024 Raven Inc. All rights reserved.
        """
        
        about_label = QLabel(about_text)
        about_label.setStyleSheet("color: #CCCCCC;")
        about_layout.addWidget(about_label)
        
        layout.addWidget(about_group)
        layout.addStretch()
        
        self.tab_widget.addTab(settings_widget, "⚙️ Settings")
        
    def create_control_panel(self, main_layout):
        """Create the bottom control panel"""
        control_frame = QFrame()
        control_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        control_frame.setStyleSheet("""
            QFrame {
                background-color: #1E1E1E;
                border-top: 2px solid #3D3D3D;
                padding: 10px;
            }
        """)
        
        control_layout = QHBoxLayout(control_frame)
        
        # Control buttons
        self.start_btn = ModernButton("🚀 Start Clicking", "#4CAF50", "#45A049")
        self.stop_btn = ModernButton("⏹️ Stop", "#F44336", "#D32F2F")
        self.stop_btn.setEnabled(False)
        
        control_layout.addWidget(self.start_btn)
        control_layout.addWidget(self.stop_btn)
        control_layout.addStretch()
        
        # Quick status
        self.quick_status_label = QLabel("Ready to start")
        self.quick_status_label.setStyleSheet("color: #CCCCCC; font-size: 14px;")
        control_layout.addWidget(self.quick_status_label)
        
        main_layout.addWidget(control_frame)
        
        # Connect signals
        self.start_btn.clicked.connect(self.start_clicking)
        self.stop_btn.clicked.connect(self.stop_clicking)
        
    def setup_system_tray(self):
        """Setup system tray icon"""
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon = QSystemTrayIcon(self)
            self.tray_icon.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))
            
            # Create tray menu
            tray_menu = QMenu()
            
            show_action = QAction("Show", self)
            show_action.triggered.connect(self.show)
            tray_menu.addAction(show_action)
            
            start_action = QAction("Start", self)
            start_action.triggered.connect(self.start_clicking)
            tray_menu.addAction(start_action)
            
            stop_action = QAction("Stop", self)
            stop_action.triggered.connect(self.stop_clicking)
            tray_menu.addAction(stop_action)
            
            tray_menu.addSeparator()
            
            quit_action = QAction("Quit", self)
            quit_action.triggered.connect(QApplication.instance().quit)
            tray_menu.addAction(quit_action)
            
            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.setToolTip("Raven Inc Auto Clicker")
            
    def start_clicking(self):
        """Start the clicking process"""
        if self.worker and self.worker.is_running:
            return
            
        # Create profile from current settings
        profile = ClickProfile(
            name="Current Session",
            base_delay=self.delay_spinbox.value() / 1000,
            random_variance=self.variance_spinbox.value() / 100,
            click_pattern=self.pattern_combo.currentText(),
            anti_detect=self.anti_detect_checkbox.isChecked(),
            human_movement=self.human_movement_checkbox.isChecked(),
            random_position=self.random_position_checkbox.isChecked(),
            position_radius=self.radius_spinbox.value(),
            click_button=self.button_combo.currentText(),
            max_clicks=self.max_clicks_spinbox.value(),
            duration_limit=self.duration_spinbox.value()
        )
        
        # Setup worker
        self.worker = ClickWorker()
        self.worker.set_profile(profile)
        self.worker_thread = QThread()
        self.worker.moveToThread(self.worker_thread)
        
        # Connect signals
        self.worker.started = self.worker.start_clicking
        self.worker.status_update.connect(self.update_status)
        self.worker.stats_update.connect(self.update_stats)
        self.worker.finished.connect(self.on_clicking_finished)
        
        # Start thread
        self.worker_thread.start()
        self.worker.started.emit()
        
        # Update UI
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.status_label.setText("● Running")
        self.status_label.setStyleSheet("color: #FF9800; font-size: 16px; padding: 10px;")
        self.quick_status_label.setText("Clicking in progress...")
        
        self.log_message("🚀 Auto clicker started")
        
    def stop_clicking(self):
        """Stop the clicking process"""
        if self.worker:
            self.worker.stop_clicking()
            self.log_message("⏹️ Stop requested")
            
    def on_clicking_finished(self):
        """Called when clicking finishes"""
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_label.setText("● Ready")
        self.status_label.setStyleSheet("color: #4CAF50; font-size: 16px; padding: 10px;")
        self.quick_status_label.setText("Ready to start")
        
        self.log_message("✅ Auto clicker stopped")
        
        # Cleanup thread
        if self.worker_thread:
            self.worker_thread.quit()
            self.worker_thread.wait()
            self.worker_thread = None
        self.worker = None
        
    def update_status(self, message):
        """Update status message"""
        self.quick_status_label.setText(message)
        self.log_message(f"ℹ️ {message}")
        
    def update_stats(self, clicks, total_clicks, elapsed):
        """Update statistics display"""
        self.clicks_label.setText(f"Clicks: {clicks}")
        self.total_clicks_label.setText(f"Total: {total_clicks}")
        self.elapsed_label.setText(f"Elapsed: {elapsed:.1f}s")
        
        cps = clicks / elapsed if elapsed > 0 else 0
        self.cps_label.setText(f"CPS: {cps:.1f}")
        
        # Update progress bar based on limits
        progress = 0
        if self.max_clicks_spinbox.value() > 0:
            progress = (total_clicks / self.max_clicks_spinbox.value()) * 100
        elif self.duration_spinbox.value() > 0:
            progress = (elapsed / self.duration_spinbox.value()) * 100
        else:
            progress = min(100, (elapsed / 60) * 100)  # Progress per minute
            
        self.progress_bar.setValue(int(progress))
        
    def log_message(self, message):
        """Add message to log display"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_display.append(f"[{timestamp}] {message}")
        
    def save_profile(self):
        """Save current settings as a profile"""
        name, ok = QMessageBox.getText(self, "Save Profile", "Enter profile name:")
        if ok and name:
            profile = ClickProfile(
                name=name,
                base_delay=self.delay_spinbox.value() / 1000,
                random_variance=self.variance_spinbox.value() / 100,
                click_pattern=self.pattern_combo.currentText(),
                anti_detect=self.anti_detect_checkbox.isChecked(),
                human_movement=self.human_movement_checkbox.isChecked(),
                random_position=self.random_position_checkbox.isChecked(),
                position_radius=self.radius_spinbox.value(),
                click_button=self.button_combo.currentText(),
                max_clicks=self.max_clicks_spinbox.value(),
                duration_limit=self.duration_spinbox.value()
            )
            
            self.profiles[name] = profile
            self.save_profiles()
            self.update_profile_table()
            self.log_message(f"📁 Profile '{name}' saved")
            
    def load_profile(self):
        """Load selected profile"""
        current_row = self.profile_table.currentRow()
        if current_row >= 0:
            profile_name = self.profile_table.item(current_row, 0).text()
            if profile_name in self.profiles:
                profile = self.profiles[profile_name]
                self.apply_profile(profile)
                self.log_message(f"📂 Profile '{profile_name}' loaded")
                
    def delete_profile(self):
        """Delete selected profile"""
        current_row = self.profile_table.currentRow()
        if current_row >= 0:
            profile_name = self.profile_table.item(current_row, 0).text()
            reply = QMessageBox.question(self, "Delete Profile", f"Delete profile '{profile_name}'?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                del self.profiles[profile_name]
                self.save_profiles()
                self.update_profile_table()
                self.log_message(f"🗑️ Profile '{profile_name}' deleted")
                
    def apply_profile(self, profile: ClickProfile):
        """Apply profile settings to UI"""
        self.delay_spinbox.setValue(profile.base_delay * 1000)
        self.variance_spinbox.setValue(profile.random_variance * 100)
        self.pattern_combo.setCurrentText(profile.click_pattern)
        self.anti_detect_checkbox.setChecked(profile.anti_detect)
        self.human_movement_checkbox.setChecked(profile.human_movement)
        self.random_position_checkbox.setChecked(profile.random_position)
        self.radius_spinbox.setValue(profile.position_radius)
        self.button_combo.setCurrentText(profile.click_button)
        self.max_clicks_spinbox.setValue(profile.max_clicks)
        self.duration_spinbox.setValue(profile.duration_limit)
        
    def update_profile_table(self):
        """Update the profile table"""
        self.profile_table.setRowCount(len(self.profiles))
        
        for row, (name, profile) in enumerate(self.profiles.items()):
            self.profile_table.setItem(row, 0, QTableWidgetItem(name))
            self.profile_table.setItem(row, 1, QTableWidgetItem(f"{profile.base_delay*1000:.0f}ms"))
            self.profile_table.setItem(row, 2, QTableWidgetItem(profile.click_pattern))
            self.profile_table.setItem(row, 3, QTableWidgetItem("✓" if profile.anti_detect else "✗"))
            
    def update_profile_details(self):
        """Update profile details display"""
        current_row = self.profile_table.currentRow()
        if current_row >= 0:
            profile_name = self.profile_table.item(current_row, 0).text()
            if profile_name in self.profiles:
                profile = self.profiles[profile_name]
                details = f"""
Profile: {profile.name}
Base Delay: {profile.base_delay*1000:.0f}ms
Random Variance: {profile.random_variance*100:.0f}%
Click Pattern: {profile.click_pattern}
Anti-Detection: {'Enabled' if profile.anti_detect else 'Disabled'}
Human Movement: {'Enabled' if profile.human_movement else 'Disabled'}
Random Position: {'Enabled' if profile.random_position else 'Disabled'}
Position Radius: {profile.position_radius}px
Mouse Button: {profile.click_button}
Max Clicks: {profile.max_clicks if profile.max_clicks > 0 else 'Unlimited'}
Duration Limit: {profile.duration_limit if profile.duration_limit > 0 else 'Unlimited'}
                """
                self.profile_details.setPlainText(details.strip())
                
    def load_profiles(self) -> Dict[str, ClickProfile]:
        """Load profiles from file"""
        profiles_file = Path("profiles.json")
        if profiles_file.exists():
            try:
                with open(profiles_file, 'r') as f:
                    data = json.load(f)
                    return {name: ClickProfile(**profile_data) for name, profile_data in data.items()}
            except Exception as e:
                print(f"Error loading profiles: {e}")
        return {}
        
    def save_profiles(self):
        """Save profiles to file"""
        try:
            data = {name: asdict(profile) for name, profile in self.profiles.items()}
            with open("profiles.json", 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving profiles: {e}")
            
    def load_settings(self):
        """Load application settings"""
        self.start_hotkey_combo.setCurrentText(self.settings.value("start_hotkey", "F1"))
        self.stop_hotkey_combo.setCurrentText(self.settings.value("stop_hotkey", "F2"))
        self.system_tray_checkbox.setChecked(self.settings.value("system_tray", True, type=bool))
        self.minimize_to_tray_checkbox.setChecked(self.settings.value("minimize_to_tray", True, type=bool))
        self.failsafe_checkbox.setChecked(self.settings.value("failsafe", True, type=bool))
        self.auto_stop_checkbox.setChecked(self.settings.value("auto_stop", False, type=bool))
        
        # Update profile table
        self.update_profile_table()
        
    def save_settings(self):
        """Save application settings"""
        self.settings.setValue("start_hotkey", self.start_hotkey_combo.currentText())
        self.settings.setValue("stop_hotkey", self.stop_hotkey_combo.currentText())
        self.settings.setValue("system_tray", self.system_tray_checkbox.isChecked())
        self.settings.setValue("minimize_to_tray", self.minimize_to_tray_checkbox.isChecked())
        self.settings.setValue("failsafe", self.failsafe_checkbox.isChecked())
        self.settings.setValue("auto_stop", self.auto_stop_checkbox.isChecked())
        
    def closeEvent(self, event):
        """Handle application close"""
        if self.worker and self.worker.is_running:
            reply = QMessageBox.question(self, "Confirm Exit", "Auto clicker is still running. Stop and exit?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.stop_clicking()
                time.sleep(0.5)  # Give time for cleanup
            else:
                event.ignore()
                return
                
        self.save_settings()
        
        if self.system_tray_checkbox.isChecked() and self.minimize_to_tray_checkbox.isChecked():
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "Raven Inc Auto Clicker",
                "Application minimized to tray",
                QSystemTrayIcon.MessageIcon.Information,
                2000
            )
        else:
            event.accept()

def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Raven Inc Auto Clicker")
    app.setOrganizationName("Raven Inc")
    
    # Set application icon and style
    app.setStyle("Fusion")
    
    # Create and show main window
    window = RavenAutoClickerGUI()
    window.show()
    
    # Show system tray if available
    if hasattr(window, 'tray_icon'):
        window.tray_icon.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
import sys
import json
import time
import random
import threading
import math
import pickle
import hashlib
import base64
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass, asdict
from pathlib import Path
from collections import defaultdict, deque
from enum import Enum

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QPushButton, QSpinBox, QDoubleSpinBox,
    QComboBox, QTabWidget, QGroupBox, QCheckBox, QTextEdit,
    QProgressBar, QSlider, QFrame, QSplitter, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox, QFileDialog,
    QSystemTrayIcon, QMenu, QStyle, QToolTip, QTreeWidget,
    QTreeWidgetItem, QListWidget, QListWidgetItem, QCalendarWidget,
    QTimeEdit, QDateEdit, QSpinBox as QSpinBoxInt, QDial, QLCDNumber,
    QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsRectItem,
    QGraphicsLineItem, QScrollArea, QWizard, QWizardPage, QFormLayout,
    QRadioButton, QButtonGroup, QSlider, QDial, QProgressBar, QLCDNumber
)
from PyQt6.QtCore import (
    Qt, QTimer, QThread, pyqtSignal, QObject, QPropertyAnimation,
    QEasingCurve, QRect, QSettings, QStandardPaths, QDate, QTime,
    QDateTime, QEvent, QPointF, QRectF, pyqtSlot, QThreadPool,
    QRunnable, QMutex, QWaitCondition, QSemaphore
)
from PyQt6.QtGui import (
    QIcon, QPixmap, QPainter, QColor, QPen, QBrush, QFont,
    QPalette, QLinearGradient, QRadialGradient, QAction,
    QMouseEvent, QWheelEvent, QKeyEvent, QPolygonF, QPainterPath,
    QTransform, QMovie, QTextCursor, QTextCharFormat, QTextDocument
)

import pyautogui
import keyboard
import numpy as np

# Enhanced Enums and Data Classes
class ActionType(Enum):
    CLICK = "click"
    MOVE = "move"
    DRAG = "drag"
    SCROLL = "scroll"
    KEY_PRESS = "key_press"
    WAIT = "wait"
    LOOP_START = "loop_start"
    LOOP_END = "loop_end"

class DetectionLevel(Enum):
    NONE = "none"
    BASIC = "basic"
    ADVANCED = "advanced"
    EXPERT = "expert"

@dataclass
class MacroAction:
    action_type: ActionType
    timestamp: float
    x: int = 0
    y: int = 0
    button: str = "left"
    key: str = ""
    duration: float = 0.0
    scroll_amount: int = 0
    loop_count: int = 0
    description: str = ""

@dataclass
class ScheduledTask:
    name: str
    profile_name: str
    start_time: QDateTime
    end_time: Optional[QDateTime]
    repeat_interval: str  # daily, weekly, monthly, custom
    enabled: bool
    last_run: Optional[QDateTime]
    next_run: QDateTime

@dataclass
class ClickHeatPoint:
    x: int
    y: int
    intensity: float
    timestamp: datetime

class AdvancedAntiDetection:
    """AI-powered anti-detection with machine learning patterns"""
    
    def __init__(self):
        self.movement_patterns = self._load_movement_patterns()
        self.timing_variance = self._load_timing_patterns()
        self.behavioral_models = self._load_behavioral_models()
        
    def _load_movement_patterns(self) -> List[Callable]:
        """Load various human movement patterns"""
        return [
            self._bezier_movement,
            self._jitter_movement,
            self._acceleration_movement,
            self._hesitation_movement,
            self._drift_movement
        ]
    
    def _load_timing_patterns(self) -> List[Callable]:
        """Load human timing patterns"""
        return [
            self._rhythm_timing,
            self._fatigue_timing,
            self._distraction_timing,
            self._focus_timing
        ]
    
    def _load_behavioral_models(self) -> Dict[str, Any]:
        """Load behavioral models for different scenarios"""
        return {
            "gaming": {"speed": 1.2, "precision": 0.8, "rhythm": 0.9},
            "productivity": {"speed": 0.8, "precision": 1.0, "rhythm": 0.7},
            "casual": {"speed": 1.0, "precision": 0.9, "rhythm": 0.8}
        }
    
    def generate_movement_path(self, start: Tuple[int, int], end: Tuple[int, int], 
                               context: str = "casual") -> List[Tuple[int, int]]:
        """Generate human-like movement path using AI patterns"""
        pattern = random.choice(self.movement_patterns)
        return pattern(start, end, context)
    
    def _bezier_movement(self, start: Tuple[int, int], end: Tuple[int, int], 
                        context: str) -> List[Tuple[int, int]]:
        """Bezier curve movement with control points"""
        steps = random.randint(8, 15)
        path = []
        
        # Generate control points for natural curve
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        
        # Add curve offset
        offset_x = random.uniform(-50, 50)
        offset_y = random.uniform(-50, 50)
        
        control1 = (mid_x + offset_x, mid_y + offset_y)
        control2 = (mid_x - offset_x/2, mid_y - offset_y/2)
        
        for i in range(steps + 1):
            t = i / steps
            # Cubic Bezier formula
            x = (1-t)**3 * start[0] + 3*(1-t)**2*t * control1[0] + \
                3*(1-t)*t**2 * control2[0] + t**3 * end[0]
            y = (1-t)**3 * start[1] + 3*(1-t)**2*t * control1[1] + \
                3*(1-t)*t**2 * control2[1] + t**3 * end[1]
            
            # Add micro-jitter
            x += random.uniform(-1, 1)
            y += random.uniform(-1, 1)
            
            path.append((int(x), int(y)))
        
        return path
    
    def _jitter_movement(self, start: Tuple[int, int], end: Tuple[int, int], 
                        context: str) -> List[Tuple[int, int]]:
        """Movement with natural hand jitter"""
        steps = random.randint(10, 20)
        path = []
        
        for i in range(steps + 1):
            t = i / steps
            x = start[0] + (end[0] - start[0]) * t
            y = start[1] + (end[1] - start[1]) * t
            
            # Add jitter
            jitter_x = random.gauss(0, 2)
            jitter_y = random.gauss(0, 2)
            
            path.append((int(x + jitter_x), int(y + jitter_y)))
        
        return path
    
    def _acceleration_movement(self, start: Tuple[int, int], end: Tuple[int, int], 
                               context: str) -> List[Tuple[int, int]]:
        """Movement with acceleration and deceleration"""
        steps = random.randint(12, 18)
        path = []
        
        for i in range(steps + 1):
            t = i / steps
            # Ease-in-out curve
            if t < 0.5:
                ease = 2 * t * t
            else:
                ease = 1 - pow(-2 * t + 2, 2) / 2
            
            x = start[0] + (end[0] - start[0]) * ease
            y = start[1] + (end[1] - start[1]) * ease
            
            path.append((int(x), int(y)))
        
        return path
    
    def _hesitation_movement(self, start: Tuple[int, int], end: Tuple[int, int], 
                            context: str) -> List[Tuple[int, int]]:
        """Movement with hesitation points"""
        steps = random.randint(15, 25)
        path = []
        hesitation_points = random.randint(1, 3)
        
        for i in range(steps + 1):
            t = i / steps
            x = start[0] + (end[0] - start[0]) * t
            y = start[1] + (end[1] - start[1]) * t
            
            # Add hesitation pauses
            if i % (steps // hesitation_points) == 0:
                time.sleep(random.uniform(0.01, 0.03))
            
            path.append((int(x), int(y)))
        
        return path
    
    def _drift_movement(self, start: Tuple[int, int], end: Tuple[int, int], 
                       context: str) -> List[Tuple[int, int]]:
        """Movement with natural drift"""
        steps = random.randint(10, 16)
        path = []
        drift_angle = random.uniform(0, 2 * math.pi)
        drift_magnitude = random.uniform(5, 15)
        
        for i in range(steps + 1):
            t = i / steps
            x = start[0] + (end[0] - start[0]) * t
            y = start[1] + (end[1] - start[1]) * t
            
            # Add drift
            drift_x = drift_magnitude * math.cos(drift_angle) * math.sin(t * math.pi)
            drift_y = drift_magnitude * math.sin(drift_angle) * math.sin(t * math.pi)
            
            path.append((int(x + drift_x), int(y + drift_y)))
        
        return path
    
    def generate_timing_delay(self, base_delay: float, context: str = "casual") -> float:
        """Generate human-like timing delay"""
        pattern = random.choice(self.timing_variance)
        return pattern(base_delay, context)
    
    def _rhythm_timing(self, base_delay: float, context: str) -> float:
        """Rhythmic timing with slight variations"""
        rhythm_factor = math.sin(time.time() * 2) * 0.1
        return base_delay * (1 + rhythm_factor + random.uniform(-0.05, 0.05))
    
    def _fatigue_timing(self, base_delay: float, context: str) -> float:
        """Timing that simulates fatigue"""
        fatigue_factor = 1 + (time.time() % 300) / 3000  # Increases over 5 minutes
        return base_delay * fatigue_factor * random.uniform(0.9, 1.1)
    
    def _distraction_timing(self, base_delay: float, context: str) -> float:
        """Timing with occasional distractions"""
        if random.random() < 0.05:  # 5% chance of distraction
            return base_delay * random.uniform(2, 5)
        return base_delay * random.uniform(0.8, 1.2)
    
    def _focus_timing(self, base_delay: float, context: str) -> float:
        """Timing that simulates focus periods"""
        focus_cycle = math.sin(time.time() * 0.1)  # Slow focus cycle
        return base_delay * (1 + focus_cycle * 0.2)

class MacroRecorder(QObject):
    """Advanced macro recording system"""
    
    recording_started = pyqtSignal()
    recording_stopped = pyqtSignal()
    action_recorded = pyqtSignal(MacroAction)
    
    def __init__(self):
        super().__init__()
        self.is_recording = False
        self.actions = []
        self.start_time = 0
        self.recording_thread = None
        self.mutex = QMutex()
        
    def start_recording(self):
        """Start recording user actions"""
        self.mutex.lock()
        self.is_recording = True
        self.actions = []
        self.start_time = time.time()
        self.mutex.unlock()
        
        self.recording_started.emit()
        
        # Start recording thread
        self.recording_thread = threading.Thread(target=self._record_actions)
        self.recording_thread.daemon = True
        self.recording_thread.start()
        
    def stop_recording(self):
        """Stop recording and return actions"""
        self.mutex.lock()
        self.is_recording = False
        self.mutex.unlock()
        
        self.recording_stopped.emit()
        
        if self.recording_thread:
            self.recording_thread.join(timeout=1)
        
        return self.actions.copy()
    
    def _record_actions(self):
        """Record mouse and keyboard actions"""
        mouse_events = []
        keyboard_events = []
        
        # Mouse event hooks
        def on_click(x, y, button, pressed):
            if not self.is_recording:
                return
            
            if pressed:
                action = MacroAction(
                    action_type=ActionType.CLICK,
                    timestamp=time.time() - self.start_time,
                    x=x, y=y,
                    button=button.name,
                    description=f"Click at ({x}, {y}) with {button.name}"
                )
                self.actions.append(action)
                self.action_recorded.emit(action)
        
        def on_move(x, y):
            if not self.is_recording:
                return
            
            # Record movement only if significant change
            if len(self.actions) == 0 or \
               self.actions[-1].action_type != ActionType.MOVE or \
               (abs(self.actions[-1].x - x) > 10 or abs(self.actions[-1].y - y) > 10):
                
                action = MacroAction(
                    action_type=ActionType.MOVE,
                    timestamp=time.time() - self.start_time,
                    x=x, y=y,
                    description=f"Move to ({x}, {y})"
                )
                self.actions.append(action)
                self.action_recorded.emit(action)
        
        def on_scroll(x, y, dx, dy):
            if not self.is_recording:
                return
            
            action = MacroAction(
                action_type=ActionType.SCROLL,
                timestamp=time.time() - self.start_time,
                x=x, y=y,
                scroll_amount=dy,
                description=f"Scroll at ({x}, {y}) by {dy}"
            )
            self.actions.append(action)
            self.action_recorded.emit(action)
        
        # Keyboard event hooks
        def on_key_press(event):
            if not self.is_recording:
                return
            
            if event.name == 'esc':  # Stop recording on ESC
                self.stop_recording()
                return
            
            action = MacroAction(
                action_type=ActionType.KEY_PRESS,
                timestamp=time.time() - self.start_time,
                key=event.name,
                description=f"Press {event.name}"
            )
            self.actions.append(action)
            self.action_recorded.emit(action)
        
        # Set up hooks (simplified for demo)
        # In real implementation, use pynput or similar library
        try:
            import pynput
            from pynput import mouse, keyboard
            
            mouse_listener = mouse.Listener(
                on_click=on_click,
                on_move=on_move,
                on_scroll=on_scroll
            )
            keyboard_listener = keyboard.Listener(on_press=on_key_press)
            
            mouse_listener.start()
            keyboard_listener.start()
            
            # Keep recording until stopped
            while self.is_recording:
                time.sleep(0.1)
            
            mouse_listener.stop()
            keyboard_listener.stop()
            
        except ImportError:
            # Fallback to basic recording
            self._basic_recording()
    
    def _basic_recording(self):
        """Basic recording without pynput"""
        while self.is_recording:
            time.sleep(0.1)
            # Add basic click recording
            if pyautogui.mouseInfo() is not None:
                x, y = pyautogui.position()
                action = MacroAction(
                    action_type=ActionType.CLICK,
                    timestamp=time.time() - self.start_time,
                    x=x, y=y,
                    description=f"Click at ({x}, {y})"
                )
                self.actions.append(action)
                self.action_recorded.emit(action)

class MacroPlayer(QObject):
    """Advanced macro playback system"""
    
    playback_started = pyqtSignal()
    playback_stopped = pyqtSignal()
    action_executed = pyqtSignal(MacroAction)
    progress_updated = pyqtSignal(int, int)
    
    def __init__(self, anti_detection: AdvancedAntiDetection):
        super().__init__()
        self.actions = []
        self.is_playing = False
        self.current_action_index = 0
        self.playback_thread = None
        self.anti_detection = anti_detection
        self.loop_count = 1
        self.current_loop = 0
        
    def set_actions(self, actions: List[MacroAction]):
        """Set actions to play"""
        self.actions = actions
        self.current_action_index = 0
        
    def set_loop_count(self, count: int):
        """Set number of times to loop"""
        self.loop_count = count
        
    def start_playback(self):
        """Start playing recorded actions"""
        if not self.actions:
            return
        
        self.is_playing = True
        self.current_action_index = 0
        self.current_loop = 0
        
        self.playback_started.emit()
        
        self.playback_thread = threading.Thread(target=self._play_actions)
        self.playback_thread.daemon = True
        self.playback_thread.start()
        
    def stop_playback(self):
        """Stop playback"""
        self.is_playing = False
        
        if self.playback_thread:
            self.playback_thread.join(timeout=1)
        
        self.playback_stopped.emit()
    
    def _play_actions(self):
        """Play recorded actions with human-like timing"""
        while self.is_playing and self.current_loop < self.loop_count:
            for i, action in enumerate(self.actions):
                if not self.is_playing:
                    break
                
                self.current_action_index = i
                self.action_executed.emit(action)
                self.progress_updated.emit(i, len(self.actions))
                
                # Execute action based on type
                if action.action_type == ActionType.CLICK:
                    self._execute_click(action)
                elif action.action_type == ActionType.MOVE:
                    self._execute_move(action)
                elif action.action_type == ActionType.SCROLL:
                    self._execute_scroll(action)
                elif action.action_type == ActionType.KEY_PRESS:
                    self._execute_key_press(action)
                elif action.action_type == ActionType.WAIT:
                    self._execute_wait(action)
                
                # Wait for next action timing
                if i < len(self.actions) - 1:
                    next_action = self.actions[i + 1]
                    delay = next_action.timestamp - action.timestamp
                    delay = self.anti_detection.generate_timing_delay(delay)
                    time.sleep(max(0, delay))
            
            self.current_loop += 1
        
        self.is_playing = False
        self.playback_stopped.emit()
    
    def _execute_click(self, action: MacroAction):
        """Execute click action"""
        # Move to position with human movement
        current_pos = pyautogui.position()
        path = self.anti_detection.generate_movement_path(current_pos, (action.x, action.y))
        
        for pos in path[:-1]:
            pyautogui.moveTo(pos[0], pos[1], duration=0.01)
        
        pyautogui.click(action.x, action.y, button=action.button)
    
    def _execute_move(self, action: MacroAction):
        """Execute move action"""
        current_pos = pyautogui.position()
        path = self.anti_detection.generate_movement_path(current_pos, (action.x, action.y))
        
        for pos in path:
            pyautogui.moveTo(pos[0], pos[1], duration=0.01)
    
    def _execute_scroll(self, action: MacroAction):
        """Execute scroll action"""
        pyautogui.scroll(action.scroll_amount, x=action.x, y=action.y)
    
    def _execute_key_press(self, action: MacroAction):
        """Execute key press action"""
        keyboard.press_and_release(action.key)
    
    def _execute_wait(self, action: MacroAction):
        """Execute wait action"""
        time.sleep(action.duration)

class ClickHeatMap(QWidget):
    """Visual click heat map widget"""
    
    def __init__(self):
        super().__init__()
        self.heat_points = []
        self.max_intensity = 1.0
        self.setMinimumSize(400, 300)
        self.setStyleSheet("background-color: #1E1E1E; border: 1px solid #3D3D3D;")
        
    def add_click_point(self, x: int, y: int, intensity: float = 1.0):
        """Add a click point to the heat map"""
        point = ClickHeatPoint(x, y, intensity, datetime.now())
        self.heat_points.append(point)
        self.max_intensity = max(self.max_intensity, intensity)
        self.update()
        
    def clear_heat_map(self):
        """Clear all heat points"""
        self.heat_points = []
        self.max_intensity = 1.0
        self.update()
        
    def paintEvent(self, event):
        """Paint the heat map"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw background
        painter.fillRect(self.rect(), QColor("#1E1E1E"))
        
        # Draw heat points
        for point in self.heat_points:
            # Calculate color based on intensity
            intensity = point.intensity / self.max_intensity
            color = self._heat_color(intensity)
            
            # Draw heat circle
            radius = 20 + intensity * 30
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QPointF(point.x, point.y), radius, radius)
        
        # Draw grid
        painter.setPen(QPen(QColor("#3D3D3D"), 1, Qt.PenStyle.DotLine))
        for x in range(0, self.width(), 50):
            painter.drawLine(x, 0, x, self.height())
        for y in range(0, self.height(), 50):
            painter.drawLine(0, y, self.width(), y)
    
    def _heat_color(self, intensity: float) -> QColor:
        """Get heat color based on intensity"""
        # Gradient from blue -> green -> yellow -> red
        if intensity < 0.25:
            # Blue to cyan
            t = intensity * 4
            return QColor(0, int(255 * t), 255)
        elif intensity < 0.5:
            # Cyan to green
            t = (intensity - 0.25) * 4
            return QColor(0, 255, int(255 * (1 - t)))
        elif intensity < 0.75:
            # Green to yellow
            t = (intensity - 0.5) * 4
            return QColor(int(255 * t), 255, 0)
        else:
            # Yellow to red
            t = (intensity - 0.75) * 4
            return QColor(255, int(255 * (1 - t)), 0)

class TaskScheduler(QObject):
    """Advanced task scheduling system"""
    
    task_triggered = pyqtSignal(ScheduledTask)
    
    def __init__(self):
        super().__init__()
        self.tasks = []
        self.timer = QTimer()
        self.timer.timeout.connect(self._check_tasks)
        self.timer.start(1000)  # Check every second
        
    def add_task(self, task: ScheduledTask):
        """Add a scheduled task"""
        self.tasks.append(task)
        self._sort_tasks()
        
    def remove_task(self, task: ScheduledTask):
        """Remove a scheduled task"""
        if task in self.tasks:
            self.tasks.remove(task)
            
    def _sort_tasks(self):
        """Sort tasks by next run time"""
        self.tasks.sort(key=lambda t: t.next_run)
        
    def _check_tasks(self):
        """Check for tasks that need to run"""
        current_time = QDateTime.currentDateTime()
        
        for task in self.tasks[:]:  # Copy list to avoid modification during iteration
            if task.enabled and current_time >= task.next_run:
                self.task_triggered.emit(task)
                
                # Update task timing
                task.last_run = current_time
                self._update_next_run(task)
                
    def _update_next_run(self, task: ScheduledTask):
        """Update next run time for task"""
        current = QDateTime.currentDateTime()
        
        if task.repeat_interval == "daily":
            task.next_run = current.addDays(1)
        elif task.repeat_interval == "weekly":
            task.next_run = current.addDays(7)
        elif task.repeat_interval == "monthly":
            task.next_run = current.addMonths(1)
        elif task.repeat_interval == "custom":
            # Custom interval would be stored in task
            pass
        else:
            # One-time task, disable
            task.enabled = False

# Continue with the main GUI class...
# [The rest of the RavenAutoClickerGUI class would be here, updated with new features]

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Raven Inc Auto Clicker - Professional Edition")
    app.setOrganizationName("Raven Inc")
    
    # Test the new components
    heat_map = ClickHeatMap()
    heat_map.show()
    
    sys.exit(app.exec())
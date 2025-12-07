import json
import hashlib
import requests
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QLineEdit, QTextEdit, QGroupBox, QCheckBox, QProgressBar,
    QTabWidget, QFormLayout, QSpinBox, QComboBox
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject, QThread
from PyQt6.QtGui import QFont, QPixmap

@dataclass
class CloudSyncConfig:
    api_endpoint: str
    api_key: str
    user_id: str
    encryption_key: str
    auto_sync: bool = True
    sync_interval: int = 300  # 5 minutes
    last_sync: Optional[datetime] = None

class CloudSyncManager(QObject):
    """Cloud synchronization manager for profiles and settings"""
    
    sync_started = pyqtSignal()
    sync_completed = pyqtSignal(bool, str)
    sync_progress = pyqtSignal(int, str)
    conflict_detected = pyqtSignal(str, Any, Any)
    
    def __init__(self):
        super().__init__()
        self.config: Optional[CloudSyncConfig] = None
        self.sync_timer = QTimer()
        self.sync_timer.timeout.connect(self.auto_sync)
        self.is_syncing = False
        self.local_data = {}
        self.cloud_data = {}
        
    def set_config(self, config: CloudSyncConfig):
        """Set cloud sync configuration"""
        self.config = config
        if config.auto_sync:
            self.sync_timer.start(config.sync_interval * 1000)
        else:
            self.sync_timer.stop()
    
    def load_local_data(self, data_path: Path):
        """Load local data for sync"""
        try:
            with open(data_path, 'r') as f:
                self.local_data = json.load(f)
        except Exception:
            self.local_data = {}
    
    def save_local_data(self, data_path: Path):
        """Save local data"""
        try:
            with open(data_path, 'w') as f:
                json.dump(self.local_data, f, indent=2)
        except Exception as e:
            print(f"Error saving local data: {e}")
    
    def start_sync(self):
        """Start manual synchronization"""
        if not self.config or self.is_syncing:
            return
        
        sync_thread = threading.Thread(target=self._perform_sync)
        sync_thread.daemon = True
        sync_thread.start()
    
    def auto_sync(self):
        """Perform automatic sync"""
        if self.config and self.config.auto_sync and not self.is_syncing:
            self.start_sync()
    
    def _perform_sync(self):
        """Perform the actual synchronization"""
        self.is_syncing = True
        self.sync_started.emit()
        
        try:
            # Step 1: Authenticate
            self.sync_progress.emit(10, "Authenticating...")
            if not self._authenticate():
                self.sync_completed.emit(False, "Authentication failed")
                return
            
            # Step 2: Download cloud data
            self.sync_progress.emit(30, "Downloading cloud data...")
            cloud_data = self._download_data()
            if cloud_data is None:
                self.sync_completed.emit(False, "Failed to download cloud data")
                return
            
            # Step 3: Compare and resolve conflicts
            self.sync_progress.emit(50, "Comparing data...")
            conflicts = self._compare_data(cloud_data)
            
            if conflicts:
                # Handle conflicts
                for conflict_key, (local_val, cloud_val) in conflicts.items():
                    self.conflict_detected.emit(conflict_key, local_val, cloud_val)
                    # For now, prefer local data
                    # In a real implementation, you'd show a dialog to user
            
            # Step 4: Upload merged data
            self.sync_progress.emit(70, "Uploading merged data...")
            if self._upload_data(self.local_data):
                self.sync_progress.emit(100, "Sync completed")
                self.config.last_sync = datetime.now()
                self.sync_completed.emit(True, "Synchronization completed successfully")
            else:
                self.sync_completed.emit(False, "Failed to upload data")
                
        except Exception as e:
            self.sync_completed.emit(False, f"Sync error: {str(e)}")
        finally:
            self.is_syncing = False
    
    def _authenticate(self) -> bool:
        """Authenticate with cloud service"""
        try:
            # Simulate API authentication
            headers = {
                'Authorization': f'Bearer {self.config.api_key}',
                'User-ID': self.config.user_id
            }
            
            # In a real implementation, make actual API call
            # response = requests.get(f"{self.config.api_endpoint}/auth", headers=headers)
            # return response.status_code == 200
            
            # For demo, always succeed
            return True
        except Exception:
            return False
    
    def _download_data(self) -> Optional[Dict[str, Any]]:
        """Download data from cloud"""
        try:
            headers = {
                'Authorization': f'Bearer {self.config.api_key}',
                'User-ID': self.config.user_id
            }
            
            # In a real implementation:
            # response = requests.get(f"{self.config.api_endpoint}/data", headers=headers)
            # if response.status_code == 200:
            #     return self._decrypt_data(response.json())
            
            # For demo, return empty data
            return {}
        except Exception:
            return None
    
    def _upload_data(self, data: Dict[str, Any]) -> bool:
        """Upload data to cloud"""
        try:
            headers = {
                'Authorization': f'Bearer {self.config.api_key}',
                'User-ID': self.config.user_id,
                'Content-Type': 'application/json'
            }
            
            # Encrypt data
            encrypted_data = self._encrypt_data(data)
            
            # In a real implementation:
            # response = requests.post(f"{self.config.api_endpoint}/data", 
            #                        json=encrypted_data, headers=headers)
            # return response.status_code == 200
            
            # For demo, always succeed
            return True
        except Exception:
            return False
    
    def _compare_data(self, cloud_data: Dict[str, Any]) -> Dict[str, Any]:
        """Compare local and cloud data, return conflicts"""
        conflicts = {}
        
        # Check for conflicts
        for key, local_value in self.local_data.items():
            if key in cloud_data:
                cloud_value = cloud_data[key]
                
                # Compare timestamps if available
                if isinstance(local_value, dict) and isinstance(cloud_value, dict):
                    local_time = local_value.get('last_modified')
                    cloud_time = cloud_value.get('last_modified')
                    
                    if local_time and cloud_time:
                        if local_time != cloud_time:
                            conflicts[key] = (local_value, cloud_value)
                elif local_value != cloud_value:
                    conflicts[key] = (local_value, cloud_value)
        
        return conflicts
    
    def _encrypt_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Encrypt data before upload"""
        # Simple encryption for demo
        # In production, use proper encryption like AES
        json_str = json.dumps(data)
        encrypted = hashlib.sha256(json_str.encode()).hexdigest()
        return {'encrypted': encrypted, 'timestamp': time.time()}
    
    def _decrypt_data(self, encrypted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Decrypt downloaded data"""
        # Simple decryption for demo
        # In production, use proper decryption
        return encrypted_data.get('data', {})

class CloudSyncWidget(QWidget):
    """Cloud sync configuration and management widget"""
    
    def __init__(self, cloud_manager: CloudSyncManager):
        super().__init__()
        self.cloud_manager = cloud_manager
        self.init_ui()
        self.connect_signals()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Configuration tab
        config_group = QGroupBox("Cloud Sync Configuration")
        config_layout = QFormLayout(config_group)
        
        self.api_endpoint_edit = QLineEdit()
        self.api_key_edit = QLineEdit()
        self.api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.user_id_edit = QLineEdit()
        
        config_layout.addRow("API Endpoint:", self.api_endpoint_edit)
        config_layout.addRow("API Key:", self.api_key_edit)
        config_layout.addRow("User ID:", self.user_id_edit)
        
        # Sync options
        self.auto_sync_checkbox = QCheckBox("Enable automatic sync")
        self.auto_sync_checkbox.setChecked(True)
        
        self.sync_interval_spinbox = QSpinBox()
        self.sync_interval_spinbox.setRange(60, 3600)
        self.sync_interval_spinbox.setValue(300)
        self.sync_interval_spinbox.setSuffix(" seconds")
        
        config_layout.addRow(self.auto_sync_checkbox)
        config_layout.addRow("Sync Interval:", self.sync_interval_spinbox)
        
        layout.addWidget(config_group)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.connect_btn = QPushButton("🔗 Connect")
        self.sync_btn = QPushButton("🔄 Sync Now")
        self.disconnect_btn = QPushButton("🔌 Disconnect")
        
        button_layout.addWidget(self.connect_btn)
        button_layout.addWidget(self.sync_btn)
        button_layout.addWidget(self.disconnect_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Status and progress
        status_group = QGroupBox("Sync Status")
        status_layout = QVBoxLayout(status_group)
        
        self.status_label = QLabel("Not connected")
        self.status_label.setStyleSheet("color: #FF6B6B; font-weight: bold;")
        
        self.last_sync_label = QLabel("Last sync: Never")
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        self.sync_log = QTextEdit()
        self.sync_log.setMaximumHeight(150)
        self.sync_log.setReadOnly(True)
        
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.last_sync_label)
        status_layout.addWidget(self.progress_bar)
        status_layout.addWidget(self.sync_log)
        
        layout.addWidget(status_group)
        
        # Data overview
        data_group = QGroupBox("Sync Data Overview")
        data_layout = QVBoxLayout(data_group)
        
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(3)
        self.data_table.setHorizontalHeaderLabels(["Type", "Local Items", "Cloud Items"])
        self.data_table.horizontalHeader().setStretchLastSection(True)
        
        data_layout.addWidget(self.data_table)
        layout.addWidget(data_group)
        
    def connect_signals(self):
        """Connect signals"""
        self.connect_btn.clicked.connect(self.connect_to_cloud)
        self.sync_btn.clicked.connect(self.start_manual_sync)
        self.disconnect_btn.clicked.connect(self.disconnect_from_cloud)
        
        self.cloud_manager.sync_started.connect(self.on_sync_started)
        self.cloud_manager.sync_completed.connect(self.on_sync_completed)
        self.cloud_manager.sync_progress.connect(self.on_sync_progress)
        self.cloud_manager.conflict_detected.connect(self.on_conflict_detected)
        
    def connect_to_cloud(self):
        """Connect to cloud service"""
        config = CloudSyncConfig(
            api_endpoint=self.api_endpoint_edit.text(),
            api_key=self.api_key_edit.text(),
            user_id=self.user_id_edit.text(),
            encryption_key="demo_key",  # In production, generate properly
            auto_sync=self.auto_sync_checkbox.isChecked(),
            sync_interval=self.sync_interval_spinbox.value()
        )
        
        self.cloud_manager.set_config(config)
        self.status_label.setText("Connected")
        self.status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
        self.sync_log.append("🔗 Connected to cloud sync service")
        
    def start_manual_sync(self):
        """Start manual synchronization"""
        self.cloud_manager.start_sync()
        
    def disconnect_from_cloud(self):
        """Disconnect from cloud service"""
        self.cloud_manager.sync_timer.stop()
        self.status_label.setText("Disconnected")
        self.status_label.setStyleSheet("color: #FF6B6B; font-weight: bold;")
        self.sync_log.append("🔌 Disconnected from cloud sync service")
        
    def on_sync_started(self):
        """Handle sync started"""
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.sync_btn.setEnabled(False)
        self.sync_log.append("🔄 Synchronization started...")
        
    def on_sync_completed(self, success: bool, message: str):
        """Handle sync completed"""
        self.progress_bar.setVisible(False)
        self.sync_btn.setEnabled(True)
        
        if success:
            self.status_label.setText("Sync completed")
            self.status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
            self.sync_log.append(f"✅ {message}")
            
            # Update last sync time
            if self.cloud_manager.config and self.cloud_manager.config.last_sync:
                self.last_sync_label.setText(f"Last sync: {self.cloud_manager.config.last_sync.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            self.status_label.setText("Sync failed")
            self.status_label.setStyleSheet("color: #FF6B6B; font-weight: bold;")
            self.sync_log.append(f"❌ {message}")
        
    def on_sync_progress(self, progress: int, message: str):
        """Handle sync progress"""
        self.progress_bar.setValue(progress)
        self.sync_log.append(f"📊 {message}")
        
    def on_conflict_detected(self, key: str, local_value: Any, cloud_value: Any):
        """Handle conflict detection"""
        self.sync_log.append(f"⚠️ Conflict detected for '{key}': Using local value")
        
        # In a real implementation, show a dialog to let user choose
        reply = QMessageBox.question(
            self, "Sync Conflict", 
            f"Conflict detected for '{key}'.\n\nUse local value?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.No:
            # Use cloud value
            self.cloud_manager.local_data[key] = cloud_value

# Multi-monitor support
class MultiMonitorManager:
    """Multi-monitor support and window targeting"""
    
    def __init__(self):
        self.monitors = self._detect_monitors()
        
    def _detect_monitors(self) -> List[Dict[str, Any]]:
        """Detect all connected monitors"""
        try:
            import pyautogui
            screen_width, screen_height = pyautogui.size()
            
            # For demo, return primary monitor info
            # In production, use platform-specific APIs to detect all monitors
            return [{
                'id': 0,
                'name': 'Primary Monitor',
                'width': screen_width,
                'height': screen_height,
                'x': 0,
                'y': 0,
                'is_primary': True
            }]
        except Exception:
            return [{'id': 0, 'name': 'Default', 'width': 1920, 'height': 1080, 'x': 0, 'y': 0, 'is_primary': True}]
    
    def get_monitor_by_point(self, x: int, y: int) -> Optional[Dict[str, Any]]:
        """Get monitor containing the given point"""
        for monitor in self.monitors:
            if (monitor['x'] <= x < monitor['x'] + monitor['width'] and
                monitor['y'] <= y < monitor['y'] + monitor['height']):
                return monitor
        return None
    
    def get_all_monitors(self) -> List[Dict[str, Any]]:
        """Get all monitors"""
        return self.monitors
    
    def constrain_to_monitor(self, x: int, y: int, monitor_id: int = None) -> Tuple[int, int]:
        """Constrain coordinates to specific monitor"""
        if monitor_id is not None:
            monitor = next((m for m in self.monitors if m['id'] == monitor_id), None)
        else:
            monitor = self.get_monitor_by_point(x, y)
        
        if monitor:
            x = max(monitor['x'], min(x, monitor['x'] + monitor['width'] - 1))
            y = max(monitor['y'], min(y, monitor['y'] + monitor['height'] - 1))
        
        return x, y

# Tutorial and help system
class TutorialManager(QObject):
    """Built-in tutorial and help system"""
    
    tutorial_completed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.tutorials = self._load_tutorials()
        self.completed_tutorials = set()
        
    def _load_tutorials(self) -> Dict[str, Dict[str, Any]]:
        """Load tutorial content"""
        return {
            "getting_started": {
                "title": "Getting Started",
                "steps": [
                    "Welcome to Raven Inc Auto Clicker!",
                    "This tutorial will guide you through the basic features.",
                    "Let's start by exploring the main interface.",
                    "The Main tab contains all the essential controls.",
                    "You can adjust click delay, mouse button, and anti-detection settings.",
                    "Try clicking the 'Start Clicking' button to begin!"
                ],
                "duration": 300  # seconds
            },
            "profiles": {
                "title": "Profile Management",
                "steps": [
                    "Profiles allow you to save and reuse configurations.",
                    "Create a profile by adjusting your settings and clicking 'Save Current Profile'.",
                    "Give your profile a descriptive name.",
                    "Load profiles from the Profiles tab.",
                    "You can create profiles for different games or applications."
                ],
                "duration": 240
            },
            "anti_detection": {
                "title": "Anti-Detection Features",
                "steps": [
                    "Anti-detection features make your clicking appear more human-like.",
                    "Enable 'Anti-Detection' to add random delays and movements.",
                    "Human-like movement creates natural mouse paths.",
                    "Random position adds slight variations to click locations.",
                    "These features help avoid detection in games and applications."
                ],
                "duration": 180
            },
            "advanced": {
                "title": "Advanced Features",
                "steps": [
                    "Explore advanced features in the Settings tab.",
                    "Configure custom hotkeys for start/stop controls.",
                    "Enable system tray for quick access.",
                    "Set up failsafe options for emergency stops.",
                    "Check the Statistics tab to track your performance."
                ],
                "duration": 200
            }
        }
    
    def get_tutorial(self, tutorial_id: str) -> Optional[Dict[str, Any]]:
        """Get tutorial by ID"""
        return self.tutorials.get(tutorial_id)
    
    def get_all_tutorials(self) -> Dict[str, Dict[str, Any]]:
        """Get all available tutorials"""
        return self.tutorials
    
    def mark_completed(self, tutorial_id: str):
        """Mark tutorial as completed"""
        self.completed_tutorials.add(tutorial_id)
        self.tutorial_completed.emit(tutorial_id)
    
    def is_completed(self, tutorial_id: str) -> bool:
        """Check if tutorial is completed"""
        return tutorial_id in self.completed_tutorials

class TutorialWidget(QWidget):
    """Tutorial display widget"""
    
    def __init__(self, tutorial_manager: TutorialManager):
        super().__init__()
        self.tutorial_manager = tutorial_manager
        self.current_tutorial = None
        self.current_step = 0
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Tutorial selection
        selection_layout = QHBoxLayout()
        
        self.tutorial_combo = QComboBox()
        tutorials = self.tutorial_manager.get_all_tutorials()
        for tutorial_id, tutorial in tutorials.items():
            status = "✅" if self.tutorial_manager.is_completed(tutorial_id) else "📚"
            self.tutorial_combo.addItem(f"{status} {tutorial['title']}", tutorial_id)
        
        selection_layout.addWidget(QLabel("Select Tutorial:"))
        selection_layout.addWidget(self.tutorial_combo)
        selection_layout.addStretch()
        
        layout.addLayout(selection_layout)
        
        # Tutorial content
        content_group = QGroupBox("Tutorial Content")
        content_layout = QVBoxLayout(content_group)
        
        self.step_label = QLabel("Step 0 of 0")
        self.step_label.setStyleSheet("font-weight: bold; color: #2196F3;")
        
        self.content_text = QTextEdit()
        self.content_text.setReadOnly(True)
        self.content_text.setMinimumHeight(200)
        
        content_layout.addWidget(self.step_label)
        content_layout.addWidget(self.content_text)
        
        layout.addWidget(content_group)
        
        # Navigation buttons
        nav_layout = QHBoxLayout()
        
        self.prev_btn = QPushButton("⬅️ Previous")
        self.next_btn = QPushButton("Next ➡️")
        self.complete_btn = QPushButton("✅ Mark Complete")
        
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addWidget(self.complete_btn)
        nav_layout.addWidget(self.next_btn)
        
        layout.addLayout(nav_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)
        
        # Connect signals
        self.tutorial_combo.currentTextChanged.connect(self.load_tutorial)
        self.prev_btn.clicked.connect(self.previous_step)
        self.next_btn.clicked.connect(self.next_step)
        self.complete_btn.clicked.connect(self.mark_complete)
        
        # Load first tutorial
        if self.tutorial_combo.count() > 0:
            self.load_tutorial()
    
    def load_tutorial(self):
        """Load selected tutorial"""
        tutorial_id = self.tutorial_combo.currentData()
        if tutorial_id:
            self.current_tutorial = self.tutorial_manager.get_tutorial(tutorial_id)
            self.current_step = 0
            self.update_display()
    
    def update_display(self):
        """Update tutorial display"""
        if not self.current_tutorial:
            return
        
        steps = self.current_tutorial['steps']
        total_steps = len(steps)
        
        if self.current_step < total_steps:
            self.step_label.setText(f"Step {self.current_step + 1} of {total_steps}")
            self.content_text.setPlainText(steps[self.current_step])
            self.progress_bar.setValue(int((self.current_step + 1) / total_steps * 100))
        
        # Update button states
        self.prev_btn.setEnabled(self.current_step > 0)
        self.next_btn.setEnabled(self.current_step < total_steps - 1)
    
    def previous_step(self):
        """Go to previous step"""
        if self.current_step > 0:
            self.current_step -= 1
            self.update_display()
    
    def next_step(self):
        """Go to next step"""
        if self.current_tutorial and self.current_step < len(self.current_tutorial['steps']) - 1:
            self.current_step += 1
            self.update_display()
    
    def mark_complete(self):
        """Mark tutorial as complete"""
        tutorial_id = self.tutorial_combo.currentData()
        if tutorial_id:
            self.tutorial_manager.mark_completed(tutorial_id)
            QMessageBox.information(self, "Tutorial Completed", 
                                   f"✅ Tutorial '{self.current_tutorial['title']}' completed!")
            
            # Update combo box
            index = self.tutorial_combo.currentIndex()
            status = "✅"
            self.tutorial_combo.setItemText(index, f"{status} {self.current_tutorial['title']}")

if __name__ == "__main__":
    # Test cloud sync
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    cloud_manager = CloudSyncManager()
    cloud_widget = CloudSyncWidget(cloud_manager)
    cloud_widget.show()
    
    sys.exit(app.exec())
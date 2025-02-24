from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer
from utils.ip_utils import get_host_ip
import datetime

class IPDisplayWidget(QFrame):
    def __init__(self, alert_manager):
        super().__init__()
        self.alert_manager = alert_manager
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.normal_style = """
            QFrame {
                background-color: #2c3e50;
                border-radius: 10px;
                padding: 10px;
            }
            QLabel {
                color: white;
            }
        """
        self.alert_style = """
            QFrame {
                background-color: #c0392b;
                border-radius: 10px;
                padding: 10px;
            }
            QLabel {
                color: white;
            }
        """
        self.setStyleSheet(self.normal_style)
        
        layout = QVBoxLayout(self)
        
        title = QLabel("Honeypot IP Address")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        
        self.ip_label = QLabel(get_host_ip())
        self.ip_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ip_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #3498db;")
        
        layout.addWidget(title)
        layout.addWidget(self.ip_label)
        
        # Check for alerts periodically
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_alerts)
        self.timer.start(1000)
    
    def check_alerts(self):
        recent_alerts = self.alert_manager.get_recent_alerts(1)
        if recent_alerts and (datetime.datetime.now() - datetime.datetime.fromisoformat(recent_alerts[0]['timestamp'])).total_seconds() < 60:
            self.setStyleSheet(self.alert_style)
        else:
            self.setStyleSheet(self.normal_style) 
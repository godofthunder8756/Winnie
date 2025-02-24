from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QFrame, QGridLayout)
from PyQt6.QtCore import Qt, QTimer

class StatisticWidget(QFrame):
    def __init__(self, title, value="0"):
        super().__init__()
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        
        layout = QVBoxLayout(self)
        
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)

class Dashboard(QWidget):
    def __init__(self, logger, analyzer):
        super().__init__()
        self.logger = logger
        self.analyzer = analyzer
        
        # Update stats every 5 seconds
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_statistics)
        self.timer.start(5000)
        
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Statistics section
        stats_layout = QGridLayout()
        
        self.total_attacks = StatisticWidget("Total Attacks")
        self.active_connections = StatisticWidget("Active Connections")
        self.unique_ips = StatisticWidget("Unique IPs")
        self.alerts_today = StatisticWidget("Alerts Today")
        
        stats_layout.addWidget(self.total_attacks, 0, 0)
        stats_layout.addWidget(self.active_connections, 0, 1)
        stats_layout.addWidget(self.unique_ips, 1, 0)
        stats_layout.addWidget(self.alerts_today, 1, 1)
        
        # Activity Feed
        activity_frame = QFrame()
        activity_frame.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        activity_layout = QVBoxLayout(activity_frame)
        
        activity_title = QLabel("Recent Activity")
        activity_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.activity_feed = QLabel("No recent activity")
        
        activity_layout.addWidget(activity_title)
        activity_layout.addWidget(self.activity_feed)
        
        # Add all sections to main layout
        layout.addLayout(stats_layout)
        layout.addWidget(activity_frame)
        layout.addStretch()
    
    def update_statistics(self):
        # In a real implementation, these would get actual values from the logger/analyzer
        # For now, we'll just show placeholder values
        pass 
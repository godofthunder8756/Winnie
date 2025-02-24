from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QFrame, QGridLayout)
from PyQt6.QtCore import Qt, QTimer
import datetime

class StatisticWidget(QFrame):
    def __init__(self, title, value="0"):
        super().__init__()
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 8px;
                padding: 15px;
                border: 1px solid #e0e0e0;
            }
        """)
        
        layout = QVBoxLayout(self)
        
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("font-size: 14px; color: #666;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.value_label = QLabel(value)
        self.value_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
    
    def update_value(self, value):
        print(f"Updating {self.title_label.text()} to {value}")  # Debug print
        self.value_label.setText(str(value))

class Dashboard(QWidget):
    def __init__(self, logger, analyzer):
        super().__init__()
        self.logger = logger
        self.analyzer = analyzer
        
        layout = QVBoxLayout(self)
        
        # Create statistics widgets
        stats_layout = QHBoxLayout()
        
        self.total_attacks = StatisticWidget("Total Attacks")
        self.active_connections = StatisticWidget("Active Connections")
        self.unique_ips = StatisticWidget("Unique IPs")
        
        stats_layout.addWidget(self.total_attacks)
        stats_layout.addWidget(self.active_connections)
        stats_layout.addWidget(self.unique_ips)
        
        layout.addLayout(stats_layout)
        
        # Add attack types breakdown
        self.attack_types_layout = QVBoxLayout()
        layout.addLayout(self.attack_types_layout)
        
        # Add stretch to push everything to the top
        layout.addStretch()
        
        # Update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_statistics)
        self.timer.start(1000)  # Update every second
        
        # Initial update
        self.update_statistics()
    
    def update_statistics(self):
        try:
            stats = self.analyzer.get_statistics()
            print(f"Dashboard updating with stats: {stats}")  # Debug print
            
            # Update main statistics
            self.total_attacks.update_value(stats['total_attacks'])
            self.active_connections.update_value(stats['active_connections'])
            self.unique_ips.update_value(stats['unique_ips'])
            
            # Clear existing attack type widgets
            while self.attack_types_layout.count():
                item = self.attack_types_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            
            # Add attack types breakdown
            if stats['attacks_by_type']:
                title = QLabel("Attacks by Type")
                title.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 20px;")
                self.attack_types_layout.addWidget(title)
                
                for attack_type, count in stats['attacks_by_type'].items():
                    attack_widget = QFrame()
                    attack_widget.setStyleSheet("""
                        QFrame {
                            background-color: #f8f9fa;
                            border-radius: 4px;
                            padding: 8px;
                            margin: 2px;
                        }
                    """)
                    attack_layout = QHBoxLayout(attack_widget)
                    
                    type_label = QLabel(attack_type)
                    type_label.setStyleSheet("font-weight: bold;")
                    count_label = QLabel(str(count))
                    
                    attack_layout.addWidget(type_label)
                    attack_layout.addWidget(count_label)
                    
                    self.attack_types_layout.addWidget(attack_widget)
        
        except Exception as e:
            print(f"Error updating dashboard: {e}")  # Debug print 
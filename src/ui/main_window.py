from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                           QTabWidget, QPushButton, QLabel)
from PyQt6.QtCore import Qt
from .dashboard import Dashboard

class MainWindow(QMainWindow):
    def __init__(self, logger, analyzer, alert_manager):
        super().__init__()
        self.logger = logger
        self.analyzer = analyzer
        self.alert_manager = alert_manager
        
        self.setWindowTitle("Winnie - Honeypot Monitor")
        self.setMinimumSize(1200, 800)
        
        self.init_ui()
        
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        tabs = QTabWidget()
        
        # Add dashboard tab
        dashboard = Dashboard(self.logger, self.analyzer)
        tabs.addTab(dashboard, "Dashboard")
        
        # Add services tab
        services_widget = QWidget()
        tabs.addTab(services_widget, "Services")
        
        # Add alerts tab
        alerts_widget = QWidget()
        tabs.addTab(alerts_widget, "Alerts")
        
        # Add reports tab
        reports_widget = QWidget()
        tabs.addTab(reports_widget, "Reports")
        
        layout.addWidget(tabs) 
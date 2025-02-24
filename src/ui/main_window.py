from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                           QTabWidget, QPushButton, QLabel,
                           QGridLayout, QGroupBox, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor
from .dashboard import Dashboard
from services.service_manager import ServiceManager
from utils.ip_utils import get_host_ip
from .alert_widget import AlertWidget
from .reports_widget import ReportsWidget
from .api_config_widget import APIConfigWidget
from .ip_display_widget import IPDisplayWidget

class ServiceControlWidget(QGroupBox):
    def __init__(self, service_manager):
        super().__init__("Service Control")
        self.service_manager = service_manager
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #3498db;
                border-radius: 5px;
                margin-top: 1em;
                padding: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:checked {
                background-color: #e74c3c;
            }
            QPushButton:hover {
                opacity: 0.8;
            }
        """)
        
        layout = QGridLayout()
        
        # Create control buttons for each service
        self.buttons = {}
        for i, service in enumerate(service_manager.services.keys()):
            btn = QPushButton(f"Start {service.upper()}")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, s=service: self._toggle_service(s, checked))
            layout.addWidget(btn, i // 2, i % 2)
            self.buttons[service] = btn
        
        self.setLayout(layout)
    
    def _toggle_service(self, service, checked):
        if checked:
            self.service_manager.start_service(service)
            self.buttons[service].setText(f"Stop {service.upper()}")
        else:
            self.service_manager.stop_service(service)
            self.buttons[service].setText(f"Start {service.upper()}")

class MainWindow(QMainWindow):
    def __init__(self, logger, analyzer, alert_manager):
        super().__init__()
        self.logger = logger
        self.analyzer = analyzer
        self.alert_manager = alert_manager
        self.service_manager = ServiceManager(logger, alert_manager)
        
        self.setWindowTitle("Winnie - Honeypot Monitor")
        self.setMinimumSize(1200, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f6fa;
            }
            QTabWidget::pane {
                border: 1px solid #dcdde1;
                border-radius: 5px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #dcdde1;
                padding: 8px 20px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: none;
            }
        """)
        
        self.init_ui()
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Add IP display at the top
        layout.addWidget(IPDisplayWidget(self.alert_manager))
        
        # Create tab widget
        tabs = QTabWidget()
        
        # Add dashboard tab
        dashboard = Dashboard(self.logger, self.analyzer)
        tabs.addTab(dashboard, "Dashboard")
        
        # Add services tab
        services_widget = QWidget()
        services_layout = QVBoxLayout(services_widget)
        services_layout.addWidget(ServiceControlWidget(self.service_manager))
        services_layout.addStretch()
        tabs.addTab(services_widget, "Services")
        
        # Add alerts tab
        alerts_widget = AlertWidget(self.alert_manager)
        tabs.addTab(alerts_widget, "Alerts")
        
        # Add reports tab
        reports_widget = ReportsWidget(self.alert_manager)
        tabs.addTab(reports_widget, "Reports")
        
        # Add API configuration tab
        api_config_widget = APIConfigWidget()
        tabs.addTab(api_config_widget, "API Configuration")
        
        layout.addWidget(tabs) 
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QListWidget, 
                           QLabel, QFileDialog)
from PyQt6.QtCore import Qt
import datetime
import json
from pathlib import Path

class ReportsWidget(QWidget):
    def __init__(self, alert_manager):
        super().__init__()
        self.alert_manager = alert_manager
        self.reports_dir = Path("reports")
        self.reports_dir.mkdir(exist_ok=True)
        
        layout = QVBoxLayout(self)
        
        # Add Generate Report button
        generate_btn = QPushButton("Generate Report")
        generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        generate_btn.clicked.connect(self.generate_report)
        layout.addWidget(generate_btn)
        
        # Add list of reports
        self.reports_list = QListWidget()
        self.reports_list.itemDoubleClicked.connect(self.open_report)
        layout.addWidget(self.reports_list)
        
        self.update_reports_list()
    
    def generate_report(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"honeypot_report_{timestamp}.txt"
        report_path = self.reports_dir / filename
        
        with open(report_path, "w") as f:
            f.write("Honeypot Activity Report\n")
            f.write("=======================\n\n")
            f.write(f"Generated: {datetime.datetime.now().isoformat()}\n\n")
            
            # Get all alerts
            alerts = self.alert_manager.get_recent_alerts(1000)
            
            # Write summary
            f.write("Summary:\n")
            f.write(f"Total Alerts: {len(alerts)}\n")
            
            # Count by type
            types = {}
            sources = set()
            for alert in alerts:
                types[alert['type']] = types.get(alert['type'], 0) + 1
                sources.add(alert['source_ip'])
            
            f.write(f"Unique Sources: {len(sources)}\n\n")
            f.write("Alert Types:\n")
            for type_, count in types.items():
                f.write(f"- {type_}: {count}\n")
            
            # Write detailed alerts
            f.write("\nDetailed Alerts:\n")
            for alert in alerts:
                f.write("\n---\n")
                f.write(f"Type: {alert['type']}\n")
                f.write(f"Source: {alert['source_ip']}\n")
                f.write(f"Service: {alert['service']}\n")
                f.write(f"Time: {alert['timestamp']}\n")
                f.write(f"Details: {json.dumps(alert['details'], indent=2)}\n")
        
        self.update_reports_list()
    
    def update_reports_list(self):
        self.reports_list.clear()
        for report in sorted(self.reports_dir.glob("*.txt"), reverse=True):
            self.reports_list.addItem(report.name)
    
    def open_report(self, item):
        report_path = self.reports_dir / item.text()
        QFileDialog.getOpenFileName(self, "Open Report", str(report_path)) 
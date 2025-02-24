from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt6.QtCore import Qt, QTimer

class AlertWidget(QWidget):
    def __init__(self, alert_manager):
        super().__init__()
        self.alert_manager = alert_manager
        
        layout = QVBoxLayout(self)
        
        # Create scrollable area for alerts
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        self.alert_container = QWidget()
        self.alert_layout = QVBoxLayout(self.alert_container)
        scroll.setWidget(self.alert_container)
        
        layout.addWidget(scroll)
        
        # Update alerts every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_alerts)
        self.timer.start(1000)
        
    def update_alerts(self):
        # Clear existing alerts
        for i in reversed(range(self.alert_layout.count())): 
            self.alert_layout.itemAt(i).widget().setParent(None)
        
        # Add recent alerts
        alerts = self.alert_manager.get_recent_alerts(20)  # Get last 20 alerts
        for alert in reversed(alerts):  # Show newest first
            alert_widget = QLabel()
            alert_widget.setStyleSheet("""
                QLabel {
                    background-color: #f8d7da;
                    color: #721c24;
                    padding: 10px;
                    border-radius: 5px;
                    margin: 2px;
                }
            """)
            
            # Format alert text
            alert_text = f"""
                <b>Alert:</b> {alert['type']}<br>
                <b>Source:</b> {alert['source_ip']}<br>
                <b>Service:</b> {alert['service']}<br>
                <b>Time:</b> {alert['timestamp']}<br>
                <b>Details:</b> {alert['details']}
            """
            alert_widget.setText(alert_text)
            self.alert_layout.addWidget(alert_widget) 
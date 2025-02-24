from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, 
                           QPushButton, QComboBox, QLabel, QGroupBox)
import json
from pathlib import Path

class APIConfigWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.config_file = Path("config/api_config.json")
        self.config_file.parent.mkdir(exist_ok=True)
        
        layout = QVBoxLayout(self)
        
        # Webhook Configuration
        webhook_group = QGroupBox("Webhook Configuration")
        webhook_layout = QFormLayout()
        
        self.webhook_url = QLineEdit()
        webhook_layout.addRow("Webhook URL:", self.webhook_url)
        
        self.webhook_method = QComboBox()
        self.webhook_method.addItems(["POST", "PUT"])
        webhook_layout.addRow("HTTP Method:", self.webhook_method)
        
        webhook_group.setLayout(webhook_layout)
        layout.addWidget(webhook_group)
        
        # API Key Configuration
        api_group = QGroupBox("API Authentication")
        api_layout = QFormLayout()
        
        self.api_key = QLineEdit()
        self.api_key.setEchoMode(QLineEdit.EchoMode.Password)
        api_layout.addRow("API Key:", self.api_key)
        
        self.header_name = QLineEdit()
        self.header_name.setText("X-API-Key")
        api_layout.addRow("Header Name:", self.header_name)
        
        api_group.setLayout(api_layout)
        layout.addWidget(api_group)
        
        # Save Button
        save_btn = QPushButton("Save Configuration")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        save_btn.clicked.connect(self.save_config)
        layout.addWidget(save_btn)
        
        # Status Label
        self.status_label = QLabel()
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
        self.load_config()
    
    def load_config(self):
        if self.config_file.exists():
            with open(self.config_file) as f:
                config = json.load(f)
                self.webhook_url.setText(config.get('webhook_url', ''))
                self.webhook_method.setCurrentText(config.get('method', 'POST'))
                self.api_key.setText(config.get('api_key', ''))
                self.header_name.setText(config.get('header_name', 'X-API-Key'))
    
    def save_config(self):
        config = {
            'webhook_url': self.webhook_url.text(),
            'method': self.webhook_method.currentText(),
            'api_key': self.api_key.text(),
            'header_name': self.header_name.text()
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)
        
        self.status_label.setText("Configuration saved successfully!")
        self.status_label.setStyleSheet("color: green;") 
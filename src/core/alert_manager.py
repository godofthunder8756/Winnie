import datetime
from collections import deque
import json
from pathlib import Path

class AlertManager:
    def __init__(self, max_alerts=1000):
        self.alerts = deque(maxlen=max_alerts)
        self.alert_handlers = []
        self.alert_dir = Path("alerts")
        self.alert_dir.mkdir(exist_ok=True)
        
    def add_alert(self, alert_type, source_ip, service, details, severity="medium"):
        """Create and store a new alert"""
        alert = {
            "timestamp": datetime.datetime.now().isoformat(),
            "type": alert_type,
            "source_ip": source_ip,
            "service": service,
            "details": details,
            "severity": severity
        }
        
        self.alerts.append(alert)
        self._save_alert(alert)
        self._notify_handlers(alert)
        
        return alert
    
    def _save_alert(self, alert):
        """Save alert to disk"""
        date_str = datetime.datetime.now().strftime('%Y%m%d')
        alert_file = self.alert_dir / f"alerts_{date_str}.log"
        
        with open(alert_file, "a") as f:
            json.dump(alert, f)
            f.write("\n")
    
    def _notify_handlers(self, alert):
        """Notify all registered alert handlers"""
        for handler in self.alert_handlers:
            handler(alert)
    
    def register_handler(self, handler):
        """Register a new alert handler"""
        self.alert_handlers.append(handler)
    
    def get_recent_alerts(self, limit=10):
        """Get most recent alerts"""
        return list(self.alerts)[-limit:] 
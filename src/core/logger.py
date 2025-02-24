import datetime
import json
from pathlib import Path

class Logger:
    def __init__(self):
        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)
        self.current_log_file = self.log_dir / f"winnie_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
    def log_event(self, event_type, source_ip, service, details):
        event = {
            "timestamp": datetime.datetime.now().isoformat(),
            "type": event_type,
            "source_ip": source_ip,
            "service": service,
            "details": details
        }
        
        with open(self.current_log_file, "a") as f:
            json.dump(event, f)
            f.write("\n")
        
        return event 
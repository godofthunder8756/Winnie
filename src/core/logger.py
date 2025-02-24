import datetime
import json
from pathlib import Path

class Logger:
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)
        
    def log_event(self, event_type, source_ip, service, details):
        """Log a security event"""
        timestamp = datetime.datetime.now().isoformat()
        
        event = {
            "timestamp": timestamp,
            "type": event_type,
            "source_ip": source_ip,
            "service": service,
            "details": details
        }
        
        # Send event to analyzer
        self.analyzer.analyze_event(event)
        
        # Log to file
        log_file = self.log_dir / f"winnie_{datetime.date.today().strftime('%Y%m%d')}.log"
        with open(log_file, "a") as f:
            json.dump(event, f)
            f.write("\n")
        
        print(f"Logged event: {event_type} from {source_ip}")  # Debug print 
import datetime
from collections import defaultdict

class Analyzer:
    def __init__(self):
        self.attack_counts = defaultdict(int)
        self.ip_addresses = set()
        self.active_connections = defaultdict(list)
        
    def analyze_event(self, event):
        """Analyze a single event from the logger"""
        # Increment attack count
        self.attack_counts[event['type']] += 1
        
        # Track unique IPs
        self.ip_addresses.add(event['source_ip'])
        
        # Track active connections
        if event['type'] == 'connection_attempt':
            self.active_connections[event['service']].append({
                'ip': event['source_ip'],
                'timestamp': event['timestamp']
            })
        
    def get_statistics(self):
        """Get current statistics for the dashboard"""
        # Clean up old connections (older than 5 minutes)
        self._cleanup_old_connections()
        
        return {
            'total_attacks': sum(self.attack_counts.values()),
            'active_connections': sum(len(conns) for conns in self.active_connections.values()),
            'unique_ips': len(self.ip_addresses),
            'attacks_by_type': dict(self.attack_counts)
        }
    
    def _cleanup_old_connections(self):
        """Remove connections older than 5 minutes"""
        current_time = datetime.datetime.now()
        
        for service in self.active_connections:
            self.active_connections[service] = [
                conn for conn in self.active_connections[service]
                if (current_time - datetime.datetime.fromisoformat(conn['timestamp'])).total_seconds() < 300
            ]
    
    def get_recent_activity(self, limit=5):
        """Get recent activity for the activity feed"""
        # In a real implementation, this would fetch from a database or event queue
        return [] 
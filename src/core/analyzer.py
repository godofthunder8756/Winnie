import datetime
from collections import defaultdict

class Analyzer:
    def __init__(self):
        self.attack_counts = defaultdict(int)
        self.ip_addresses = set()
        self.active_connections = defaultdict(list)
        
    def analyze_event(self, event):
        """Analyze a single event from the logger"""
        print(f"Analyzer received event: {event['type']}")  # Debug print
        
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
        
        print(f"Current stats: {self.get_statistics()}")  # Debug print
    
    def get_statistics(self):
        """Get current statistics for the dashboard"""
        # Clean up old connections (older than 5 minutes)
        self._cleanup_old_connections()
        
        # Get total attacks by summing all attack counts
        total_attacks = sum(self.attack_counts.values())
        
        # Get active connections count
        active_connections = sum(len(conns) for conns in self.active_connections.values())
        
        # Get unique IPs count
        unique_ips = len(self.ip_addresses)
        
        # Get attacks by type
        attacks_by_type = dict(self.attack_counts)
        
        stats = {
            'total_attacks': total_attacks,
            'active_connections': active_connections,
            'unique_ips': unique_ips,
            'attacks_by_type': attacks_by_type
        }
        
        return stats
    
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
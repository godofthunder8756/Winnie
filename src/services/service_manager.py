from .ftp_service import FTPHoneypot
from .ssh_service import SSHServer

class ServiceManager:
    def __init__(self, logger, alert_manager):
        self.logger = logger
        self.alert_manager = alert_manager
        self.services = {}
        
        # Initialize services
        self.services['ftp'] = FTPHoneypot(logger, alert_manager)
        self.services['ssh'] = SSHServer(logger, alert_manager)
        
    def start_service(self, service_name):
        """Start a specific service"""
        if service_name in self.services:
            self.services[service_name].start()
            return True
        return False
    
    def stop_service(self, service_name):
        """Stop a specific service"""
        if service_name in self.services:
            self.services[service_name].stop()
            return True
        return False
    
    def start_all(self):
        """Start all services"""
        for service in self.services.values():
            try:
                service.start()
            except Exception as e:
                print(f"Error starting service: {e}")
    
    def stop_all(self):
        """Stop all services"""
        for service in self.services.values():
            try:
                service.stop()
            except Exception as e:
                print(f"Error stopping service: {e}") 
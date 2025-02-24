from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import threading

class HoneypotFTPHandler(FTPHandler):
    def on_connect(self):
        super().on_connect()
        # Log connection attempt
        self.server.logger.log_event(
            "connection_attempt",
            self.remote_ip,
            "ftp",
            {"port": self.remote_port}
        )

class FTPHoneypot:
    def __init__(self, logger, port=21):
        self.logger = logger
        self.port = port
        self.authorizer = DummyAuthorizer()
        
        # Add a dummy user
        self.authorizer.add_user("user", "password123", ".", perm="elradfmw")
        
    def start(self):
        handler = HoneypotFTPHandler
        handler.authorizer = self.authorizer
        handler.banner = "FTP Server Ready"
        
        self.server = FTPServer(("0.0.0.0", self.port), handler)
        self.server.logger = self.logger
        
        # Start server in a separate thread
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        
    def stop(self):
        if hasattr(self, 'server'):
            self.server.close_all() 
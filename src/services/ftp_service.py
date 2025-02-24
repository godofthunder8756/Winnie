import socket
import threading
import logging
import datetime
from pathlib import Path

class FTPHoneypot:
    def __init__(self, logger, alert_manager, port=21):
        self.logger = logger
        self.alert_manager = alert_manager
        self.port = port
        self.running = False
        self.sock = None
        self.thread = None
        
        # Create a directory for FTP files
        self.ftp_dir = Path("ftp_files")
        self.ftp_dir.mkdir(exist_ok=True)
        
    def start(self):
        """Start the FTP server"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(('0.0.0.0', self.port))
            self.sock.listen(5)
            
            self.running = True
            self.thread = threading.Thread(target=self._run_server)
            self.thread.daemon = True
            self.thread.start()
            
            logging.info(f"FTP Honeypot started on port {self.port}")
        except Exception as e:
            logging.error(f"Failed to start FTP server: {e}")
            self.stop()
    
    def _run_server(self):
        """Main server loop"""
        while self.running:
            try:
                client, addr = self.sock.accept()
                client.settimeout(5)  # Set timeout immediately
                
                # Log IMMEDIATELY on connection, before any FTP handling
                details = {
                    "port": addr[1],
                    "timestamp": datetime.datetime.now().isoformat(),
                    "type": "initial_connection"
                }
                self.logger.log_event("connection_attempt", addr[0], "ftp", details)
                self.alert_manager.add_alert(
                    "port_scan",
                    addr[0],
                    "ftp",
                    details,
                    severity="medium"
                )
                
                try:
                    # Send welcome message
                    client.send(b"220 FTP Server Ready\r\n")
                except socket.error:
                    # If we can't even send the welcome message, it's probably a scan
                    scan_details = {
                        "timestamp": datetime.datetime.now().isoformat(),
                        "type": "quick_disconnect"
                    }
                    self.alert_manager.add_alert(
                        "port_scan",
                        addr[0],
                        "ftp",
                        scan_details,
                        severity="medium"
                    )
                
                # Handle the connection in a separate thread
                t = threading.Thread(target=self._handle_client, args=(client, addr))
                t.daemon = True
                t.start()
                
            except Exception as e:
                if self.running:
                    logging.error(f"FTP Server error: {e}")
                    if isinstance(e, socket.error):
                        # Log socket errors as potential scan attempts
                        details = {
                            "error": str(e),
                            "timestamp": datetime.datetime.now().isoformat(),
                            "type": "connection_error"
                        }
                        self.alert_manager.add_alert(
                            "port_scan",
                            "unknown",
                            "ftp",
                            details,
                            severity="medium"
                        )
    
    def _handle_client(self, client, addr):
        """Handle individual FTP client connections"""
        try:
            while self.running:
                try:
                    data = client.recv(1024)
                    if not data:
                        break
                    
                    # Try to decode as UTF-8, if fails, use raw bytes
                    try:
                        command = data.decode('utf-8').strip()
                    except UnicodeDecodeError:
                        command = f"RAW_BYTES: {data.hex()}"
                    
                    # Log and alert for command
                    details = {
                        "command": command,
                        "timestamp": datetime.datetime.now().isoformat()
                    }
                    self.logger.log_event("ftp_command", addr[0], "ftp", details)
                    
                    if "USER" in command.upper() or "PASS" in command.upper():
                        self.alert_manager.add_alert(
                            "ftp_auth_attempt",
                            addr[0],
                            "ftp",
                            details,
                            severity="medium"
                        )
                    
                    # Handle basic FTP commands
                    cmd = command.split(' ')[0].upper()
                    if cmd == "USER":
                        client.send(b"331 Please specify the password.\r\n")
                    elif cmd == "PASS":
                        client.send(b"530 Login incorrect.\r\n")
                    elif cmd == "QUIT":
                        client.send(b"221 Goodbye.\r\n")
                        break
                    else:
                        client.send(b"500 Unknown command.\r\n")
                    
                except socket.error:
                    break
                    
        except Exception as e:
            logging.error(f"Error handling FTP client: {e}")
        finally:
            try:
                client.close()
            except:
                pass
    
    def stop(self):
        """Stop the FTP server"""
        self.running = False
        if self.sock:
            try:
                self.sock.close()
            except Exception as e:
                logging.error(f"Error stopping FTP server: {e}") 
import socket
import threading
import paramiko
import logging
import datetime

class SSHHoneypot(paramiko.ServerInterface):
    def __init__(self, logger, alert_manager):
        self.logger = logger
        self.alert_manager = alert_manager
        self.event = threading.Event()

    def check_auth_password(self, username, password):
        details = {
            "username": username,
            "password": password,
            "success": False,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        self.logger.log_event("auth_attempt", self.client_ip, "ssh", details)
        self.alert_manager.add_alert(
            "ssh_auth_attempt",
            self.client_ip,
            "ssh",
            details,
            severity="medium"
        )
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return 'password'

    def check_channel_request(self, kind, chanid):
        details = {
            "channel_type": kind,
            "channel_id": chanid,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        self.logger.log_event("channel_request", self.client_ip, "ssh", details)
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

class SSHServer:
    def __init__(self, logger, alert_manager, port=2222):
        self.logger = logger
        self.alert_manager = alert_manager
        self.port = port
        self.sock = None
        self.thread = None
        self.running = False
        
        # Set up server key
        self.host_key = paramiko.RSAKey.generate(2048)
        
    def start(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(('0.0.0.0', self.port))
            self.sock.listen(100)
            
            self.running = True
            self.thread = threading.Thread(target=self._run_server)
            self.thread.daemon = True
            self.thread.start()
            
            logging.info(f"SSH Honeypot started on port {self.port}")
        except Exception as e:
            logging.error(f"Failed to start SSH server: {e}")
            self.stop()
    
    def _run_server(self):
        while self.running:
            try:
                client, addr = self.sock.accept()
                client.settimeout(5)  # Set timeout immediately
                
                # Log IMMEDIATELY on connection, before any SSH handling
                details = {
                    "port": addr[1],
                    "timestamp": datetime.datetime.now().isoformat(),
                    "type": "initial_connection"
                }
                self.logger.log_event("connection_attempt", addr[0], "ssh", details)
                self.alert_manager.add_alert(
                    "port_scan",
                    addr[0],
                    "ssh",
                    details,
                    severity="medium"
                )
                
                # Handle the connection in a separate thread
                t = threading.Thread(target=self._handle_connection, args=(client, addr))
                t.daemon = True
                t.start()
                
            except Exception as e:
                if self.running:
                    logging.error(f"SSH Server error: {e}")
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
                            "ssh",
                            details,
                            severity="medium"
                        )
    
    def _handle_connection(self, client, addr):
        try:
            # First, try to read the client's version string
            client.settimeout(5)
            try:
                initial_data = client.recv(1024)
                if initial_data:
                    try:
                        client_version = initial_data.decode('utf-8').strip()
                    except UnicodeDecodeError:
                        client_version = f"RAW_BYTES: {initial_data.hex()}"
                        
                    # Log the client version/probe attempt
                    details = {
                        "client_version": client_version,
                        "timestamp": datetime.datetime.now().isoformat()
                    }
                    self.logger.log_event("ssh_probe", addr[0], "ssh", details)
                    self.alert_manager.add_alert(
                        "ssh_probe",
                        addr[0],
                        "ssh",
                        details,
                        severity="medium"
                    )
                    
                    # Send our version string
                    client.send(b"SSH-2.0-OpenSSH_8.2p1\r\n")
            except socket.timeout:
                logging.debug("Timeout waiting for client version")
                return
            
            # Now try to establish SSH connection
            transport = paramiko.Transport(client)
            transport.add_server_key(self.host_key)
            transport.local_version = "SSH-2.0-OpenSSH_8.2p1"
            
            server = SSHHoneypot(self.logger, self.alert_manager)
            server.client_ip = addr[0]
            
            try:
                transport.start_server(server=server)
                channel = transport.accept(20)
                if channel is None:
                    transport.close()
                    return
                channel.close()
                
            except (paramiko.SSHException, EOFError) as e:
                # Log these common exceptions as probe attempts
                details = {
                    "error": str(e),
                    "timestamp": datetime.datetime.now().isoformat()
                }
                self.logger.log_event("ssh_probe_error", addr[0], "ssh", details)
                self.alert_manager.add_alert(
                    "ssh_probe_error",
                    addr[0],
                    "ssh",
                    details,
                    severity="medium"
                )
            finally:
                transport.close()
                
        except Exception as e:
            logging.error(f"SSH handling error: {e}")
            # Log unexpected errors
            details = {
                "error": str(e),
                "timestamp": datetime.datetime.now().isoformat()
            }
            self.logger.log_event("ssh_error", addr[0], "ssh", details)
            self.alert_manager.add_alert(
                "ssh_error",
                addr[0],
                "ssh",
                details,
                severity="high"
            )
        finally:
            try:
                client.close()
            except:
                pass
    
    def stop(self):
        self.running = False
        if self.sock:
            try:
                self.sock.close()
            except Exception as e:
                logging.error(f"Error stopping SSH server: {e}") 
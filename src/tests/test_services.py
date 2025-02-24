import ftplib
import paramiko
import time
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_ftp_honeypot():
    """Test FTP honeypot by attempting common FTP operations"""
    logger.info("Testing FTP Honeypot...")
    
    try:
        # Connect to FTP server
        ftp = ftplib.FTP()
        ftp.connect('localhost', 21)
        
        # Try to login
        try:
            ftp.login('admin', 'password123')
        except ftplib.error_perm as e:
            logger.info(f"Expected login failure: {e}")
        
        # Try some commands
        try:
            ftp.dir()
        except ftplib.error_perm as e:
            logger.info(f"Expected command failure: {e}")
            
        ftp.quit()
        logger.info("FTP test completed successfully")
        
    except Exception as e:
        logger.error(f"FTP test error: {e}")

def test_ssh_honeypot():
    """Test SSH honeypot by attempting SSH connections"""
    logger.info("Testing SSH Honeypot...")
    
    try:
        # Connect to SSH server
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Try to connect with credentials
        try:
            ssh.connect('localhost', port=2222, username='admin', password='password123')
        except paramiko.AuthenticationException as e:
            logger.info(f"Expected authentication failure: {e}")
        except Exception as e:
            logger.info(f"Connection attempt recorded: {e}")
            
        ssh.close()
        logger.info("SSH test completed successfully")
        
    except Exception as e:
        logger.error(f"SSH test error: {e}")

if __name__ == "__main__":
    # Create logs directory if it doesn't exist
    Path("logs").mkdir(exist_ok=True)
    
    # Run tests
    test_ftp_honeypot()
    time.sleep(1)  # Small delay between tests
    test_ssh_honeypot() 
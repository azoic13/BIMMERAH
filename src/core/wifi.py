"""
ELM327 WiFi connection manager for BIMMERAH
"""

import socket
import time
import logging

logger = logging.getLogger(__name__)

ELM327_IP = "192.168.0.10"
ELM327_PORT = 35000
TIMEOUT = 10


class WiFiManager:
    """Manages WiFi socket connection to ELM327 adapter"""

    def __init__(self):
        self.socket = None
        self._connected = False
        self.paired_devices = {}
        self.current_device = None

    def pair(self, ip: str, port: int, pairing_code: str) -> bool:
        """
        Pair with an ELM327 adapter using pairing code
        
        Args:
            ip: IP address of the ELM327 adapter
            port: Port number of the ELM327 adapter
            pairing_code: 6-digit pairing code for the device
            
        Returns:
            bool: True if pairing successful
        """
        try:
            logger.info(f"Attempting to pair with {ip}:{port} using code {pairing_code}")
            
            # Create temporary socket for pairing
            temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            temp_socket.settimeout(TIMEOUT)
            temp_socket.connect((ip, port))
            
            # Send pairing code
            pair_cmd = f"PAIR:{pairing_code}\r"
            temp_socket.sendall(pair_cmd.encode())
            time.sleep(0.5)
            
            # Read pairing response
            response = b""
            try:
                while True:
                    chunk = temp_socket.recv(1024)
                    if not chunk:
                        break
                    response += chunk
                    if b"OK" in response or b"PAIRED" in response:
                        break
            except socket.timeout:
                pass
            
            temp_socket.close()
            response_text = response.decode(errors="ignore").strip()
            logger.info(f"Pairing response: {response_text}")
            
            # Store paired device
            device_id = f"{ip}:{port}"
            self.paired_devices[device_id] = {
                "ip": ip,
                "port": port,
                "pairing_code": pairing_code,
                "paired_at": time.time()
            }
            self.current_device = device_id
            
            logger.info(f"Device {device_id} paired successfully")
            return True
            
        except Exception as e:
            logger.error(f"Pairing failed: {e}")
            return False

    def connect(self, ip=None, port=None) -> bool:
        """Connect to ELM327 adapter via WiFi socket"""
        try:
            # Use provided IP/port, or use current paired device, or use defaults
            if ip is None or port is None:
                if self.current_device and self.current_device in self.paired_devices:
                    device_info = self.paired_devices[self.current_device]
                    ip = device_info["ip"]
                    port = device_info["port"]
                else:
                    ip = ip or ELM327_IP
                    port = port or ELM327_PORT
            
            logger.info(f"Connecting to ELM327 at {ip}:{port}")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(TIMEOUT)
            self.socket.connect((ip, port))
            self._connected = True
            logger.info("Socket connected — initializing ELM327...")
            return self._initialize_elm()
        except Exception as e:
            logger.error(f"WiFi connect failed: {e}")
            self._connected = False
            return False

    def _initialize_elm(self) -> bool:
        """Send initialization AT commands to ELM327"""
        init_commands = [
            "ATZ",      # Reset
            "ATE0",     # Echo off
            "ATL0",     # Linefeeds off
            "ATH1",     # Headers on
            "ATSP0",    # Auto-detect protocol
        ]
        time.sleep(1)  # Wait after reset
        for cmd in init_commands:
            response = self.send_command(cmd)
            logger.info(f"{cmd} → {response}")
            if response is None:
                return False
        logger.info("ELM327 initialized successfully")
        return True

    def send_command(self, command: str, timeout=5) -> str | None:
        """Send a command and return the response"""
        if not self._connected or not self.socket:
            return None
        try:
            self.socket.sendall((command + "\r").encode())
            time.sleep(0.3)
            response = b""
            self.socket.settimeout(timeout)
            while True:
                chunk = self.socket.recv(1024)
                if not chunk:
                    break
                response += chunk
                if b">" in response:  # ELM327 prompt = done
                    break
            return response.decode(errors="ignore").strip()
        except socket.timeout:
            return response.decode(errors="ignore").strip() if response else None
        except Exception as e:
            logger.error(f"send_command error: {e}")
            return None

    def is_connected(self) -> bool:
        return self._connected

    def disconnect(self):
        """Close the socket connection"""
        if self.socket:
            try:
                self.socket.close()
            except Exception:
                pass
        self._connected = False
        self.socket = None
        logger.info("WiFi disconnected")

    def scan_networks(self) -> list:
        """Placeholder — Android WiFi scanning is handled by system settings"""
        return [{"ssid": "OBDII", "note": "Connect manually via Android WiFi settings"}]
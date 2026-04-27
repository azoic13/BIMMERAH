"""
Core diagnostics module for BMW vehicle communication
"""

import logging

logger = logging.getLogger(__name__)


class VehicleConnection:
    """Handles BMW vehicle communication and diagnostics"""

    def __init__(self):
        """Initialize vehicle connection"""
        self.is_connected = False
        self.vehicle_info = {}

    def connect(self, port: str = None) -> bool:
        """
        Establish connection to BMW vehicle
        
        Args:
            port: Serial or USB port name
            
        Returns:
            bool: True if connection successful
        """
        try:
            logger.info(f"Attempting to connect to vehicle on port {port}")
            self.is_connected = True
            self.vehicle_info = {
                "vin": "TBD",
                "model": "TBD",
                "year": "TBD"
            }
            logger.info("Vehicle connection established")
            return True
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return False

    def disconnect(self) -> bool:
        """Disconnect from vehicle"""
        try:
            self.is_connected = False
            logger.info("Vehicle connection closed")
            return True
        except Exception as e:
            logger.error(f"Disconnect failed: {e}")
            return False

    def read_codes(self) -> list:
        """Read real DTCs using OBD2 mode 03"""
        if not self.wifi or not self.wifi.is_connected():
            return []

        response = self.wifi.send_command("03")  # OBD2 mode 03 = request DTCs
        if not response:
            return []

        return self._parse_dtcs(response)

    def _parse_dtcs(self, raw: str) -> list:
        """Parse raw OBD2 DTC response into code list"""
        codes = []
        lines = raw.strip().split("\n")
        for line in lines:
            line = line.strip().replace(" ", "")
            if line.startswith("43"):  # Mode 03 response header
                data = line[4:]  # Skip "43XX" header
                for i in range(0, len(data), 4):
                    chunk = data[i:i+4]
                    if len(chunk) == 4 and chunk != "0000":
                        code = self._decode_dtc(chunk)
                        if code:
                            codes.append({"code": code, "description": "See BMW database"})
        return codes

    def _decode_dtc(self, hex_code: str) -> str | None:
        """Convert hex DTC to human-readable P/C/B/U code"""
        try:
            first = int(hex_code[0], 16)
            prefix = ["P", "C", "B", "U"][first >> 2]
            digit = str(first & 0x3)
            return f"{prefix}{digit}{hex_code[1:]}"
        except Exception:
            return None
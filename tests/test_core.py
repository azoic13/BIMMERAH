"""
Test suite for BIMMERAH
"""

import unittest
from src.core import VehicleConnection, BluetoothManager, WiFiManager
from src.utils import validate_port


class TestVehicleConnection(unittest.TestCase):
    """Test cases for VehicleConnection"""

    def setUp(self):
        """Set up test fixtures"""
        self.vehicle = VehicleConnection()

    def test_connection_init(self):
        """Test vehicle connection initialization"""
        self.assertFalse(self.vehicle.is_connected)
        self.assertEqual(self.vehicle.vehicle_info, {})

    def test_connect(self):
        """Test vehicle connection"""
        result = self.vehicle.connect("/dev/ttyUSB0")
        self.assertTrue(result)
        self.assertTrue(self.vehicle.is_connected)

    def test_disconnect(self):
        """Test vehicle disconnection"""
        self.vehicle.connect()
        result = self.vehicle.disconnect()
        self.assertTrue(result)
        self.assertFalse(self.vehicle.is_connected)

    def test_read_codes(self):
        """Test reading diagnostic codes"""
        self.vehicle.connect()
        codes = self.vehicle.read_codes()
        self.assertIsInstance(codes, list)
        self.assertGreater(len(codes), 0)


class TestBluetoothManager(unittest.TestCase):
    """Test cases for BluetoothManager"""

    def setUp(self):
        """Set up test fixtures"""
        self.bluetooth = BluetoothManager()

    def test_bluetooth_init(self):
        """Test Bluetooth manager initialization"""
        self.assertFalse(self.bluetooth.is_scanning)
        self.assertEqual(self.bluetooth.paired_devices, [])
        self.assertIsNone(self.bluetooth.connected_device)

    def test_scan_devices(self):
        """Test Bluetooth device scanning"""
        devices = self.bluetooth.scan_devices()
        self.assertIsInstance(devices, list)
        self.assertGreater(len(devices), 0)
        self.assertIn("name", devices[0])
        self.assertIn("mac", devices[0])

    def test_connect_device(self):
        """Test Bluetooth device connection"""
        result = self.bluetooth.connect("00:1A:7D:DA:71:13")
        self.assertTrue(result)
        self.assertTrue(self.bluetooth.is_connected())

    def test_disconnect_device(self):
        """Test Bluetooth device disconnection"""
        self.bluetooth.connect("00:1A:7D:DA:71:13")
        result = self.bluetooth.disconnect()
        self.assertTrue(result)
        self.assertFalse(self.bluetooth.is_connected())

    def test_send_data(self):
        """Test sending data over Bluetooth"""
        self.bluetooth.connect("00:1A:7D:DA:71:13")
        result = self.bluetooth.send_data(b"test data")
        self.assertTrue(result)

    def test_send_data_disconnected(self):
        """Test sending data when not connected"""
        result = self.bluetooth.send_data(b"test data")
        self.assertFalse(result)


class TestWiFiManager(unittest.TestCase):
    """Test cases for WiFiManager"""

    def setUp(self):
        """Set up test fixtures"""
        self.wifi = WiFiManager()

    def test_wifi_init(self):
        """Test WiFi manager initialization"""
        self.assertFalse(self.wifi.is_scanning)
        self.assertEqual(self.wifi.available_networks, [])
        self.assertIsNone(self.wifi.connected_network)

    def test_scan_networks(self):
        """Test WiFi network scanning"""
        networks = self.wifi.scan_networks()
        self.assertIsInstance(networks, list)
        self.assertGreater(len(networks), 0)
        self.assertIn("ssid", networks[0])
        self.assertIn("signal_strength", networks[0])

    def test_connect_network(self):
        """Test WiFi network connection"""
        result = self.wifi.connect("BMW-CarPlay", "password123")
        self.assertTrue(result)
        self.assertTrue(self.wifi.is_connected())

    def test_disconnect_network(self):
        """Test WiFi network disconnection"""
        self.wifi.connect("BMW-CarPlay")
        result = self.wifi.disconnect()
        self.assertTrue(result)
        self.assertFalse(self.wifi.is_connected())

    def test_get_ip_address(self):
        """Test getting IP address"""
        self.wifi.connect("BMW-CarPlay")
        ip = self.wifi.get_ip_address()
        self.assertIsNotNone(ip)
        self.assertIn("192.168", ip)

    def test_get_ip_when_disconnected(self):
        """Test getting IP when not connected"""
        ip = self.wifi.get_ip_address()
        self.assertIsNone(ip)

    def test_http_request(self):
        """Test HTTP request over WiFi"""
        self.wifi.connect("BMW-CarPlay")
        result = self.wifi.send_http_request("http://example.com")
        self.assertIsNotNone(result)

    def test_http_request_disconnected(self):
        """Test HTTP request when not connected"""
        result = self.wifi.send_http_request("http://example.com")
        self.assertIsNone(result)


class TestValidatePort(unittest.TestCase):
    """Test cases for port validation"""

    def test_valid_port(self):
        """Test valid port"""
        self.assertTrue(validate_port("/dev/ttyUSB0"))
        self.assertTrue(validate_port("COM3"))

    def test_invalid_port(self):
        """Test invalid port"""
        self.assertFalse(validate_port(""))
        self.assertFalse(validate_port(None))


if __name__ == "__main__":
    unittest.main()

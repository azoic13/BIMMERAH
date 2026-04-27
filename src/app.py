"""
BIMMERAH Application main class
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

from src.core import BluetoothManager, WiFiManager, VehicleConnection


class BimmerahApp(App):
    """Main application class for BIMMERAH"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bluetooth = BluetoothManager()
        self.wifi = WiFiManager()
        self.vehicle = VehicleConnection()
        self.status_label = None

    def build(self):
        """Build and return the root widget"""
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        
        # Title
        title = Label(
            text="BIMMERAH v0.1.0",
            size_hint_y=0.15,
            bold=True,
            font_size="28sp",
            color=(0.2, 0.6, 1, 1)
        )
        layout.add_widget(title)
        
        # Subtitle
        subtitle = Label(
            text="Free Android BMW Diagnostics Tool",
            size_hint_y=0.1,
            font_size="14sp"
        )
        layout.add_widget(subtitle)
        
        # Button grid for connectivity options
        button_grid = GridLayout(cols=2, spacing=10, size_hint_y=0.5)
        
        # Bluetooth buttons
        btn_bt_scan = Button(text="Bluetooth Scan")
        btn_bt_scan.bind(on_press=self.on_bluetooth_scan)
        button_grid.add_widget(btn_bt_scan)
        
        btn_bt_connect = Button(text="BT Connect")
        btn_bt_connect.bind(on_press=self.on_bluetooth_connect)
        button_grid.add_widget(btn_bt_connect)
        
        # WiFi buttons
        btn_wifi_scan = Button(text="WiFi Scan")
        btn_wifi_scan.bind(on_press=self.on_wifi_scan)
        button_grid.add_widget(btn_wifi_scan)
        
        btn_wifi_connect = Button(text="WiFi Connect")
        btn_wifi_connect.bind(on_press=self.on_wifi_connect)
        button_grid.add_widget(btn_wifi_connect)
        
        # Diagnostics buttons
        btn_read_codes = Button(text="Read Codes")
        btn_read_codes.bind(on_press=self.on_read_codes)
        button_grid.add_widget(btn_read_codes)
        
        btn_clear_codes = Button(text="Clear Codes")
        btn_clear_codes.bind(on_press=self.on_clear_codes)
        button_grid.add_widget(btn_clear_codes)
        
        # Settings button
        btn_settings = Button(text="Settings")
        btn_settings.bind(on_press=self.on_settings)
        button_grid.add_widget(btn_settings)
        
        # Exit button
        btn_exit = Button(text="Exit")
        btn_exit.bind(on_press=self.on_exit)
        button_grid.add_widget(btn_exit)
        
        layout.add_widget(button_grid)
        
        # Status bar
        self.status_label = Label(
            text="Status: Ready",
            size_hint_y=0.15,
            color=(0, 1, 0, 1),
            font_size="12sp"
        )
        layout.add_widget(self.status_label)
        
        return layout

    def update_status(self, message: str, color=(0, 1, 0, 1)):
        """Update status label"""
        if self.status_label:
            self.status_label.text = f"Status: {message}"
            self.status_label.color = color

    def on_bluetooth_scan(self, instance):
        """Handle Bluetooth scan button"""
        self.update_status("Scanning Bluetooth devices...", (1, 1, 0, 1))
        devices = self.bluetooth.scan_devices()
        
        if devices:
            device_list = "\n".join([f"{d['name']} ({d['mac']})" for d in devices])
            self.update_status(f"Found {len(devices)} devices", (0, 1, 0, 1))
        else:
            self.update_status("No Bluetooth devices found", (1, 0, 0, 1))

    def on_bluetooth_connect(self, instance):
        """Handle Bluetooth connect button"""
        self.update_status("Connecting to Bluetooth...", (1, 1, 0, 1))
        # Using first available device for demo
        if self.bluetooth.connect("00:1A:7D:DA:71:13"):
            self.update_status("Bluetooth connected!", (0, 1, 0, 1))
        else:
            self.update_status("Bluetooth connection failed", (1, 0, 0, 1))

    def on_wifi_scan(self, instance):
        """Handle WiFi scan button"""
        self.update_status("Scanning WiFi networks...", (1, 1, 0, 1))
        networks = self.wifi.scan_networks()
        
        if networks:
            self.update_status(f"Found {len(networks)} networks", (0, 1, 0, 1))
        else:
            self.update_status("No WiFi networks found", (1, 0, 0, 1))

    def on_wifi_connect(self, instance):
        """Handle WiFi connect button"""
        self.update_status("Connecting to WiFi...", (1, 1, 0, 1))
        if self.wifi.connect("BMW-CarPlay"):
            self.update_status("WiFi connected!", (0, 1, 0, 1))
        else:
            self.update_status("WiFi connection failed", (1, 0, 0, 1))

    def on_read_codes(self, instance):
        """Handle read diagnostic codes button"""
        if self.bluetooth.is_connected() or self.wifi.is_connected():
            self.update_status("Reading diagnostic codes...", (1, 1, 0, 1))
            codes = self.vehicle.read_codes()
            self.update_status(f"Found {len(codes)} diagnostic codes", (0, 1, 0, 1))
        else:
            self.update_status("Connect to vehicle first", (1, 0, 0, 1))

    def on_clear_codes(self, instance):
        """Handle clear diagnostic codes button"""
        if self.bluetooth.is_connected() or self.wifi.is_connected():
            self.update_status("Clearing diagnostic codes...", (1, 1, 0, 1))
            if self.vehicle.clear_codes():
                self.update_status("Codes cleared successfully", (0, 1, 0, 1))
            else:
                self.update_status("Failed to clear codes", (1, 0, 0, 1))
        else:
            self.update_status("Connect to vehicle first", (1, 0, 0, 1))

    def on_settings(self, instance):
        """Handle settings button"""
        self.update_status("Settings not yet implemented", (1, 1, 0, 1))

    def on_exit(self, instance):
        """Handle exit button"""
        # Clean disconnect
        if self.bluetooth.is_connected():
            self.bluetooth.disconnect()
        if self.wifi.is_connected():
            self.wifi.disconnect()
        
        self.stop()


def main():
    """Start the application"""
    app = BimmerahApp()
    app.run()


if __name__ == "__main__":
    main()

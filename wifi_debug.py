#!/usr/bin/env python3
"""
BIMMERAH WiFi ADB Setup and Installation Helper
Guides setup of wireless debugging and APK installation
"""

import os
import subprocess
import sys
import platform
from pathlib import Path


def run_command(cmd, shell=False):
    """Run shell command and return output"""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=shell)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)


def check_adb_installed():
    """Check if ADB is installed"""
    code, output, error = run_command("adb --version", shell=True)
    return code == 0


def get_android_sdk_path():
    """Get Android SDK path"""
    if platform.system() == "Windows":
        default_paths = [
            os.path.expandvars(r"%LOCALAPPDATA%\Android\sdk"),
            os.path.expandvars(r"%ProgramFiles%\Android\sdk"),
            r"C:\Android\sdk"
        ]
    else:
        default_paths = [
            os.path.expandvars("~/Android/sdk"),
            "/usr/local/opt/android-sdk"
        ]
    
    for path in default_paths:
        if os.path.exists(path):
            return path
    return None


def list_devices():
    """List connected devices"""
    code, output, error = run_command("adb devices", shell=True)
    if code == 0:
        return output
    return None


def list_devices_long():
    """List devices with more details"""
    code, output, error = run_command("adb devices -l", shell=True)
    if code == 0:
        return output
    return None


def install_apk(apk_path):
    """Install APK on connected device"""
    if not os.path.exists(apk_path):
        print(f"❌ APK not found: {apk_path}")
        return False
    
    print(f"📦 Installing APK: {apk_path}")
    code, output, error = run_command(f"adb install \"{apk_path}\"", shell=True)
    
    if code == 0:
        print("✅ APK installed successfully!")
        print(output)
        return True
    else:
        print(f"❌ Installation failed")
        print(error)
        return False


def launch_app():
    """Launch BIMMERAH app on device"""
    package_name = "org.bimmerah.app"
    activity = "MainActivity"
    
    cmd = f"adb shell am start -n {package_name}/.{activity}"
    code, output, error = run_command(cmd, shell=True)
    
    if code == 0:
        print(f"✅ Launched {package_name}")
        return True
    else:
        print(f"❌ Failed to launch app")
        print(error)
        return False


def show_setup_steps():
    """Show WiFi debugging setup steps"""
    print("\n" + "="*60)
    print("📱 WIRELESS DEBUGGING SETUP FOR ANDROID 12+")
    print("="*60)
    
    steps = [
        ("1. Enable Wireless Debugging", [
            "Go to Settings > Developer Options",
            "Enable 'Wireless debugging'",
            "A popup will ask to allow wireless debugging"
        ]),
        ("2. Get Device IP", [
            "In Settings > Developer Options > Wireless debugging",
            "Note the IP address shown (e.g., 192.168.x.x)"
        ]),
        ("3. Connect with ADB", [
            "Run: adb connect <DEVICE_IP>:5555",
            "Example: adb connect 192.168.1.100:5555"
        ]),
        ("4. Verify Connection", [
            "Run: adb devices",
            "You should see your device listed"
        ])
    ]
    
    for title, steps_list in steps:
        print(f"\n{title}")
        for step in steps_list:
            print(f"  → {step}")


def main():
    """Main execution"""
    print("\n" + "="*60)
    print("🚀 BIMMERAH WiFi ADB Installation Helper")
    print("="*60)
    
    # Check ADB
    print("\n1️⃣  Checking ADB installation...")
    if check_adb_installed():
        print("✅ ADB is installed and accessible")
    else:
        print("❌ ADB not found in PATH")
        print("\n📦 To install ADB:")
        if platform.system() == "Windows":
            print("  Option A: Install Android Studio")
            print("  Option B: Download Android SDK Command Line Tools")
            print("           https://developer.android.com/studio")
            print("  Option C: Use Windows Package Manager:")
            print("           winget install Google.AndroidStudio")
        else:
            print("  macOS: brew install android-platform-tools")
            print("  Linux: apt-get install adb")
        return False
    
    # Show WiFi debugging setup
    show_setup_steps()
    
    # List devices
    print("\n2️⃣  Checking connected devices...")
    devices = list_devices()
    if devices:
        print(devices)
    else:
        print("❌ No devices connected. Follow steps above to connect.")
        return False
    
    # List devices with details
    print("3️⃣  Device Details:")
    devices_long = list_devices_long()
    if devices_long:
        print(devices_long)
    
    # Look for APK
    print("\n4️⃣  Checking for APK file...")
    apk_paths = [
        "bin/bimmerah-0.1.0-debug.apk",
        "bin/bimmerah-debug.apk",
        "bin/*.apk"
    ]
    
    apk_found = None
    for pattern in apk_paths:
        if '*' in pattern:
            from glob import glob
            matches = glob(pattern)
            if matches:
                apk_found = matches[0]
                break
        elif os.path.exists(pattern):
            apk_found = pattern
            break
    
    if apk_found:
        print(f"✅ Found APK: {apk_found}")
        
        # Ask to install
        response = input("\n5️⃣  Install APK on device? (y/n): ").strip().lower()
        if response == 'y':
            if install_apk(apk_found):
                # Ask to launch
                response = input("\n6️⃣  Launch app? (y/n): ").strip().lower()
                if response == 'y':
                    launch_app()
    else:
        print("❌ No APK found")
        print("\n   To build APK, ensure you have:")
        print("   - Java Development Kit (JDK 11+)")
        print("   - Android SDK")
        print("   - Then run: buildozer android debug")
    
    print("\n" + "="*60)
    print("✅ Setup complete!")
    print("="*60)
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

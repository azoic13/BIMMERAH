#!/usr/bin/env python3
"""
BIMMERAH APK Build Helper
Generates APK with proper configuration for Android
"""

import os
import json
import subprocess
import sys
from pathlib import Path


def check_requirements():
    """Check if required tools are installed"""
    requirements = {
        "java": "Java Development Kit (JDK)",
        "android": "Android SDK",
        "gradlew": "Gradle"
    }
    
    missing = []
    for cmd, desc in requirements.items():
        result = subprocess.run(["where", cmd], capture_output=True)
        if result.returncode != 0:
            missing.append(desc)
    
    return missing


def create_apk_config():
    """Create APK configuration"""
    config = {
        "app_name": "BIMMERAH",
        "package": "org.bimmerah.app",
        "version": "0.1.0",
        "android_api": 33,
        "android_minapi": 21,
        "permissions": [
            "INTERNET",
            "BLUETOOTH",
            "BLUETOOTH_ADMIN",
            "BLUETOOTH_SCAN",
            "BLUETOOTH_CONNECT",
            "ACCESS_FINE_LOCATION",
            "ACCESS_COARSE_LOCATION",
            "CHANGE_WIFI_STATE",
            "ACCESS_WIFI_STATE"
        ],
        "features": [
            "android.hardware.bluetooth",
            "android.hardware.bluetooth_le",
            "android.hardware.wifi"
        ]
    }
    return config


def main():
    """Main build function"""
    print("=" * 60)
    print("BIMMERAH APK Build Helper")
    print("=" * 60)
    
    # Check requirements
    missing = check_requirements()
    if missing:
        print("\n❌ Missing requirements:")
        for item in missing:
            print(f"  - {item}")
        print("\nTo build APK, install:")
        print("  1. Java Development Kit (JDK 11+)")
        print("  2. Android SDK")
        print("  3. Android NDK")
        return False
    
    # Create configuration
    config = create_apk_config()
    print("\n✅ Configuration created:")
    print(json.dumps(config, indent=2))
    
    print("\n📱 To build the APK manually:")
    print("  1. Install Android tools (see setup guide)")
    print("  2. Run: buildozer android debug")
    print("  3. APK will be in: bin/")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""
Direct APK Installation for Connected ADB Device
Handles installation of BIMMERAH app
"""

import subprocess
import sys
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_adb_devices():
    """Check if any ADB devices are connected"""
    try:
        result = subprocess.run(
            ["adb", "devices", "-l"],
            capture_output=True,
            text=True
        )
        devices = [line.strip() for line in result.stdout.split('\n') 
                  if 'device' in line.lower() and not line.startswith('List')]
        return devices
    except Exception as e:
        logger.error(f"Failed to get ADB devices: {e}")
        return []


def install_apk(apk_path):
    """Install APK on connected device"""
    if not os.path.exists(apk_path):
        logger.error(f"APK not found: {apk_path}")
        return False
    
    try:
        logger.info(f"Installing {apk_path}...")
        result = subprocess.run(
            ["adb", "install", "-r", apk_path],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            logger.info("✓ APK installed successfully")
            return True
        else:
            logger.error(f"Installation failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        logger.error("Installation timed out")
        return False
    except Exception as e:
        logger.error(f"Installation error: {e}")
        return False


def launch_app():
    """Launch the installed app"""
    try:
        logger.info("Launching BIMMERAH app...")
        subprocess.run([
            "adb", "shell", "am", "start",
            "-n", "org.bimmerah.app/.MainActivity"
        ], timeout=10)
        logger.info("✓ App launched")
        return True
    except Exception as e:
        logger.error(f"Failed to launch app: {e}")
        return False


def main():
    logger.info("=" * 60)
    logger.info("BIMMERAH: APK Installation for Connected Device")
    logger.info("=" * 60)
    
    # Check for connected devices
    devices = check_adb_devices()
    if not devices:
        logger.error("No ADB devices found!")
        logger.info("Please ensure:")
        logger.info("1. Mobile device is connected via WiFi ADB")
        logger.info("2. Run: adb connect <device_ip>:5555")
        sys.exit(1)
    
    logger.info(f"Found {len(devices)} connected device(s):")
    for device in devices:
        logger.info(f"  - {device}")
    
    apk_path = "bin/bimmerah-0.1.0-debug.apk"
    
    # Check if APK exists
    if not os.path.exists(apk_path):
        logger.warning(f"APK not found at {apk_path}")
        logger.info("\nNEED TO BUILD APK:")
        logger.info("Unfortunately, buildozer has compatibility issues with Python 3.14")
        logger.info("\nOptions:")
        logger.info("1. Use a cloud build service (EAS, AppVeyor)")
        logger.info("2. Set up Android SDK locally (requires Java + Android SDK)")
        logger.info("3. Switch to Python 3.11 or 3.12 for buildozer compatibility")
        sys.exit(1)
    
    # Install and launch
    if install_apk(apk_path):
        logger.info("\nAPK ready on device!")
        if input("\nLaunch app now? (y/n): ").lower() == 'y':
            launch_app()
    else:
        logger.error("Installation failed")
        sys.exit(1)


if __name__ == "__main__":
    main()

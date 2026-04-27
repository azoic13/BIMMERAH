#!/usr/bin/env python3
"""
Pair, connect, and prepare for installation script
Usage: python pair_and_connect.py <ip> <port> <pairing_code>
Example: python pair_and_connect.py 192.168.1.19 39093 847065
"""

import sys
import logging
from src.core import WiFiManager, VehicleConnection

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Main execution flow: pair → connect → prepare for install"""
    
    # Parse command line arguments
    if len(sys.argv) < 4:
        print("Usage: python pair_and_connect.py <ip> <port> <pairing_code>")
        print("Example: python pair_and_connect.py 192.168.1.19 39093 847065")
        sys.exit(1)
    
    ip = sys.argv[1]
    port = int(sys.argv[2])
    pairing_code = sys.argv[3]
    
    logger.info("=" * 60)
    logger.info("BIMMERAH: Pair, Connect & Install Workflow")
    logger.info("=" * 60)
    
    # Step 1: Initialize managers
    logger.info("\n[1/3] Initializing WiFi and Vehicle managers...")
    wifi = WiFiManager()
    vehicle = VehicleConnection()
    logger.info("✓ Managers initialized")
    
    # Step 2: Pair with the device
    logger.info(f"\n[2/3] Pairing with {ip}:{port} using code {pairing_code}...")
    if wifi.pair(ip, port, pairing_code):
        logger.info("✓ Device paired successfully")
    else:
        logger.error("✗ Pairing failed - aborting")
        sys.exit(1)
    
    # Step 3: Connect to the paired device
    logger.info(f"\n[3/3] Connecting to paired device...")
    if wifi.connect():
        logger.info("✓ Connected to ELM327 adapter")
        logger.info(f"  Device: {wifi.current_device}")
        logger.info(f"  Connected: {wifi.is_connected()}")
    else:
        logger.error("✗ Connection failed - aborting")
        sys.exit(1)
    
    # Step 4: Verify connection and display installation info
    logger.info("\n" + "=" * 60)
    logger.info("READY FOR INSTALLATION")
    logger.info("=" * 60)
    
    if wifi.is_connected():
        logger.info(f"✓ WiFi connected to {ip}:{port}")
        logger.info("\nNext steps:")
        logger.info("1. Run: buildozer android debug")
        logger.info("2. Or run: python build_apk.py")
        logger.info("3. Install generated APK to your Android device")
        logger.info("4. Launch BIMMERAH and select WiFi Connect")
        logger.info("\nYour device pairing details have been saved.")
    else:
        logger.error("✗ Connection verification failed")
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Install BIMMERAH from GitHub Actions APK
Quick steps to download and install the built APK
"""

import subprocess
import os
import sys
import time

def run_command(cmd):
    """Run command and return success status"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode == 0, result.stdout, result.stderr

def main():
    print("=" * 70)
    print(" BIMMERAH: Install from GitHub Actions APK")
    print("=" * 70)
    
    print("\n📋 PREREQUISITES:")
    print("  ✓ APK downloaded from GitHub Actions")
    print("  ✓ Device connected via ADB (already verified)")
    
    print("\n📂 EXPECTED APK LOCATION:")
    apk_path = "bin/bimmerah-0.1.0-debug.apk"
    
    # Check if APK exists
    if os.path.exists(apk_path):
        size = os.path.getsize(apk_path)
        if size > 1000000:  # Should be >1MB for valid APK
            print(f"  ✓ Found: {apk_path} ({size:,} bytes)")
            print("\n🚀 INSTALLATION STEPS:\n")
            
            print("1. UNINSTALL OLD VERSION (if exists)")
            print("   adb uninstall org.bimmerah.app\n")
            
            print("2. INSTALL APK")
            print("   adb install -r bin/bimmerah-0.1.0-debug.apk\n")
            
            print("3. VERIFY INSTALLATION")
            print("   adb shell pm list packages | grep bimmerah\n")
            
            print("4. LAUNCH APP")
            print("   adb shell am start -n org.bimmerah.app/.MainActivity\n")
            
            print("5. VIEW LOGS")
            print("   adb logcat | grep -i bimmerah\n")
            
            print("=" * 70)
            print("\nWould you like to proceed with installation? (y/n): ", end="")
            
        else:
            print(f"  ⚠ Found: {apk_path} but size is only {size} bytes")
            print("  This is the minimal test APK - GitHub Actions build required\n")
            print("NEXT STEPS:")
            print("1. Push code to GitHub")
            print("2. Wait for Actions to build APK")
            print("3. Download artifact")
            print("4. Replace bin/bimmerah-0.1.0-debug.apk")
            print("5. Run this script again")
            return
    else:
        print(f"  ✗ NOT FOUND: {apk_path}")
        print("\nACTION REQUIRED:")
        print("1. Build APK on GitHub Actions")
        print("2. Download the 'bimmerah-apk' artifact")
        print("3. Place it at: bin/bimmerah-0.1.0-debug.apk")
        print("4. Run this script again")
        return
    
    # Ask for confirmation
    response = input()
    if response.lower() != 'y':
        print("Installation cancelled")
        return
    
    print("\n" + "=" * 70)
    print(" INSTALLING...")
    print("=" * 70)
    
    # Step 1: Uninstall
    print("\n[1/4] Uninstalling old version...")
    success, stdout, stderr = run_command("adb uninstall org.bimmerah.app")
    if success or "not installed" in stderr or "Unknown" in stdout:
        print("  ✓ Ready (no previous installation)")
    
    # Step 2: Install
    print("\n[2/4] Installing new APK...")
    success, stdout, stderr = run_command("adb install -r bin/bimmerah-0.1.0-debug.apk")
    if success and ("Success" in stdout or "Success" in stderr):
        print("  ✓ APK installed successfully")
    else:
        print(f"  ✗ Installation failed: {stderr}")
        return
    
    # Step 3: Verify
    print("\n[3/4] Verifying installation...")
    success, stdout, stderr = run_command("adb shell pm list packages | grep bimmerah")
    if "bimmerah" in stdout:
        print("  ✓ App found in installed packages")
    else:
        print("  ⚠ App not found in packages")
    
    # Step 4: Launch
    print("\n[4/4] Launching app...")
    success, stdout, stderr = run_command("adb shell am start -n org.bimmerah.app/.MainActivity")
    if success:
        print("  ✓ App launched")
    else:
        print(f"  ⚠ Could not launch: {stderr}")
    
    print("\n" + "=" * 70)
    print(" ✅ INSTALLATION COMPLETE!")
    print("=" * 70)
    print("\nTroubleshooting:")
    print("  • Check logs: adb logcat")
    print("  • Uninstall: adb uninstall org.bimmerah.app")
    print("  • Reinstall: adb install -r bin/bimmerah-0.1.0-debug.apk")

if __name__ == "__main__":
    main()

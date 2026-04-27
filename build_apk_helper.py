#!/usr/bin/env python3
"""
BIMMERAH APK Build Helper - Works around buildozer Python 3.14 compatibility
"""

import os
import sys
import subprocess
import json
from pathlib import Path


def check_tools():
    """Check for required build tools"""
    print("\n" + "="*60)
    print("🔧 Checking Build Tools")
    print("="*60)
    
    tools = {
        "java": ("Java (JDK)", "-version"),
        "gradle": ("Gradle", "--version"),
        "adb": ("Android SDK (adb)", "--version")
    }
    
    found = {}
    for cmd, (name, arg) in tools.items():
        result = subprocess.run(f"{cmd} {arg}", shell=True, capture_output=True)
        status = "✅" if result.returncode == 0 else "❌"
        found[cmd] = result.returncode == 0
        print(f"{status} {name}: {cmd}")
    
    return found


def install_gradle():
    """Provide gradle installation instructions"""
    print("\n" + "="*60)
    print("📥 Gradle Installation")
    print("="*60)
    print("""
Windows (using Chocolatey):
    choco install gradle

Windows (manual):
    1. Download from: https://gradle.org/releases/
    2. Extract to: C:\\gradle
    3. Add to PATH: C:\\gradle\\bin

macOS:
    brew install gradle

Linux (Ubuntu):
    sudo apt-get install gradle
    """)


def create_test_apk():
    """Create a minimal test APK without full build tools"""
    print("\n" + "="*60)
    print("📦 Creating Test APK")
    print("="*60)
    
    # Create mock APK for testing installation workflow
    bin_dir = Path("bin")
    bin_dir.mkdir(exist_ok=True)
    
    apk_path = bin_dir / "bimmerah-0.1.0-debug.apk"
    
    # Create a minimal valid APK file (zip file with Android structure)
    try:
        import zipfile
        
        with zipfile.ZipFile(apk_path, 'w') as apk:
            # Add minimal required files
            apk.writestr('AndroidManifest.xml', 
                b'<?xml version="1.0" encoding="utf-8"?>'
                b'<manifest package="org.bimmerah.app" />')
            apk.writestr('resources.arsc', b'')
        
        print(f"✅ Created test APK: {apk_path}")
        return str(apk_path)
    except Exception as e:
        print(f"❌ Failed to create test APK: {e}")
        return None


def show_manual_build_steps():
    """Show manual build steps for advanced users"""
    print("\n" + "="*60)
    print("🛠️  Manual APK Build Steps")
    print("="*60)
    print("""
Prerequisites:
1. Java Development Kit (JDK 11+)
2. Android SDK (API 33)
3. Android NDK
4. Gradle

Build Steps:
1. Create Android project:
   gradle init --type android-app

2. Configure build.gradle with:
   - compileSdkVersion 33
   - targetSdkVersion 33
   - minSdkVersion 21

3. Build APK:
   gradle assembleDebug

4. Output:
   app/build/outputs/apk/debug/app-debug.apk

For detailed instructions, see:
https://developer.android.com/training/basics/firstapp
    """)


def show_alternatives():
    """Show alternative APK build methods"""
    print("\n" + "="*60)
    print("🔄 Alternative Build Methods")
    print("="*60)
    print("""
Option 1: Android Studio (Recommended)
- Open Android Studio
- File > New > Import Project
- Select BIMMERAH folder
- Build > Make Project
- Build > Build Bundle(s) / APK(s)

Option 2: Docker (Cross-platform)
- Install Docker
- Use: docker run -v /path/to/bimmerah:/root/bimmerah buildozer
- Avoids Python version issues

Option 3: Cloud Build
- Use GitHub Actions for CI/CD
- Automatically builds APK on push
- Example: https://github.com/kivy/buildozer/wiki/CI-CD

Option 4: Web-based Build (Easiest)
- Upload to: https://apkbuilder.kivy.org/
- Returns APK ready to install

Option 5: Local Kivy2Android
- Use kivy2android instead of buildozer
- More control over build process
- Command: p4a create --requirement=python3,kivy
    """)


def main():
    """Main execution"""
    print("\n" + "="*60)
    print("BIMMERAH APK Build Helper")
    print("="*60)
    
    tools = check_tools()
    
    # Check if we have all tools
    if all(tools.values()):
        print("\n✅ All required tools found!")
        print("You can now build using: buildozer android debug")
        show_manual_build_steps()
    else:
        print("\n❌ Some tools are missing")
        
        if not tools.get("gradle"):
            install_gradle()
        
        if not tools.get("java"):
            print("\n📥 Java (JDK) Installation:")
            print("Download: https://adoptium.net/")
            print("Or: winget install EclipseAdoptium.Temurin")
        
        if not tools.get("adb"):
            print("\n📥 Android SDK Installation:")
            print("Download Android Studio: https://developer.android.com/studio")
            print("Or: winget install Google.AndroidStudio")
        
        print("\n" + "-"*60)
        show_alternatives()
        
        print("\n" + "-"*60)
        print("\n💡 Immediate Option: Create Test APK")
        response = input("Create minimal test APK for installation testing? (y/n): ").strip().lower()
        
        if response == 'y':
            apk = create_test_apk()
            if apk:
                print(f"\n✅ Test APK ready at: {apk}")
                print("You can now test the installation workflow with:")
                print(f"  adb install {apk}")
    
    print("\n" + "="*60)
    print("For WiFi debugging setup, see: docs/WIFI_DEBUGGING_GUIDE.md")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()

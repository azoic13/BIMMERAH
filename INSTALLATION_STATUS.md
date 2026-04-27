# BIMMERAH Installation Guide - Connected Device Ready

## Status
- ✅ **Mobile Device**: Pixel 6 connected at `192.168.1.19:43505`
- ✅ **ADB Connection**: Working
- ⚠️ **APK Build**: Requires setup

## Problem: Buildozer with Python 3.14

Buildozer has compatibility issues with Python 3.14.4 (deprecated urllib imports).

## Solution Options

### Option 1: Use Kivy's Cloud Build Service (EASIEST)
Build APK in the cloud without local Android SDK setup:
```bash
# Install cloud build tools
pip install buildozer

# Or use EAS (Expo Application Services)
pip install eas-cli
```

### Option 2: Temporary - Test App in Development Mode
Since you have ADB connected, test the app wirelessly:

```bash
# Start Python app in debug mode (from dev machine)
python main.py

# Or deploy source via adb
adb push src/ /sdcard/bimmerah/
adb shell "cd /sdcard/bimmerah && python -m main"
```

### Option 3: Install Pre-built APK
If you have a pre-built APK from another source:
```bash
adb install -r path/to/bimmerah.apk
adb shell am start -n org.bimmerah.app/.MainActivity
```

### Option 4: Fix Buildozer Locally (ADVANCED)
Requires Android SDK + Java setup:

**Prerequisites:**
- Java Development Kit (JDK) 17+
- Android SDK (API 33)
- Gradle

**Installation:**
```bash
# Install required build tools
pip install --upgrade buildozer cython

# Set environment variables (Windows PowerShell)
$env:ANDROID_SDK_ROOT = "C:\Android\Sdk"
$env:ANDROID_HOME = "C:\Android\Sdk"

# Build APK
buildozer android debug
buildozer android debug --deploy

# Or install directly
adb install -r bin/bimmerah*.apk
```

## Current Device Info
```
Device: Pixel 6
IP: 192.168.1.19
Port: 43505
Status: Ready for APK installation
```

## Quick Test Commands

Once APK is installed:
```bash
# Launch the app
adb shell am start -n org.bimmerah.app/.MainActivity

# View app logs
adb logcat | grep BIMMERAH

# Check app installation
adb shell pm list packages | grep bimmerah

# Uninstall if needed
adb uninstall org.bimmerah.app
```

## Next Steps

1. **Recommended**: Use Option 1 (Cloud Build) - No local SDK needed
2. **Alternative**: Use Option 4 if you're willing to install Android SDK
3. **Quick Test**: Option 2 for development/debugging

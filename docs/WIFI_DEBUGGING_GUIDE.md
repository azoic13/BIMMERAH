# BIMMERAH WiFi Debugging & Installation Guide

## 📱 WiFi Debugging Setup for Android 12+

This guide shows how to install and test BIMMERAH on your Android device using WiFi debugging (Wireless ADB).

### ✅ Prerequisites

- Android device running Android 12 or newer
- Computer with Windows, macOS, or Linux
- USB cable (only for initial pairing, or skip if you have WiFi already)
- Android SDK Platform Tools (ADB)

---

## 🔧 Step 1: Install Android SDK Tools

### Windows

**Option A: Using Windows Package Manager (Recommended)**
```powershell
winget install Google.AndroidStudio
```

**Option B: Download Android SDK Command Line Tools**
1. Visit: https://developer.android.com/studio#downloads
2. Download "Command line tools"
3. Extract to: `C:\Android\sdk\cmdline-tools`
4. Add to PATH: `C:\Android\sdk\platform-tools`

**Option C: Standalone ADB**
```powershell
# Using Chocolatey
choco install androidstudio

# Or manually download from:
# https://developer.android.com/studio
```

### macOS
```bash
brew install android-platform-tools
# or
brew install android-studio
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-get install android-tools-adb android-tools-fastboot
```

---

## 📲 Step 2: Enable Wireless Debugging on Phone

### Android 12 & 13
1. Open **Settings**
2. Navigate to **System > Developer Options**
   - If not visible: Go to **About** and tap **Build Number** 7 times
3. Enable **"Wireless debugging"**
4. Tap **"Wireless debugging"** option
5. You'll see: **IP address** (e.g., `192.168.1.100`) and **Port** (usually `5555`)

### Android 14+
1. Open **Settings**
2. Navigate to **System > Developer Options**
3. Enable **"Wireless debugging"**
4. Tap **"Wireless debugging"** 
5. Select **"Pair with pairing code"** or **"Pair new device"**
6. Note the **IP address and port**

---

## 🔌 Step 3: Connect via ADB over WiFi

### Using Python Script (Recommended)

**Windows:**
```batch
cd c:\Projects\BIMMERAH
python wifi_debug.py
```

**macOS/Linux:**
```bash
cd ~/Projects/BIMMERAH
python3 wifi_debug.py
```

### Using Batch File (Windows Only)

```batch
cd c:\Projects\BIMMERAH
wifi_debug.bat
```

### Manual ADB Connection

**Get your device IP:**
1. On your phone: Settings > Developer Options > Wireless debugging
2. Note the IP (e.g., `192.168.1.100`)

**Connect from terminal:**

**Windows (PowerShell):**
```powershell
adb connect 192.168.1.100:5555
adb devices
```

**macOS/Linux (Terminal):**
```bash
adb connect 192.168.1.100:5555
adb devices
```

**Expected Output:**
```
List of attached devices
192.168.1.100:5555          device
```

---

## 📦 Step 4: Build APK (If Needed)

If you haven't built the APK yet, you need:

### Prerequisites for Building
- Java Development Kit (JDK 11+)
- Android SDK
- Android NDK

### Build APK
```bash
cd c:\Projects\BIMMERAH

# Activate virtual environment
.venv\Scripts\activate

# Build debug APK
buildozer android debug
```

**Output Location:** `bin/bimmerah-0.1.0-debug.apk`

**Note:** If buildozer fails due to Python version, use Python 3.11 or 3.12 instead of 3.14.

---

## 🚀 Step 5: Install APK on Device

### Using Python Script
```bash
python wifi_debug.py
```
Select "y" to install when prompted.

### Using Batch File (Windows)
```batch
wifi_debug.bat
```

### Manual Installation
```bash
adb install bin/bimmerah-0.1.0-debug.apk
```

**Expected Output:**
```
Success
```

---

## ▶️ Step 6: Run the App

### Using Helper Script
```bash
python wifi_debug.py
# Select "y" to launch app
```

### Manual Launch
```bash
adb shell am start -n org.bimmerah.app/.MainActivity
```

### View Logs
```bash
adb logcat | grep bimmerah
```

---

## 🧪 Testing the App

### Check if App Opened
```bash
adb shell pm list packages | grep bimmerah
```

### View App Data
```bash
adb shell ls /data/data/org.bimmerah.app/
```

### Uninstall App
```bash
adb uninstall org.bimmerah.app
```

### Clear App Data
```bash
adb shell pm clear org.bimmerah.app
```

---

## 🔍 Troubleshooting

### Problem: "ADB not found"

**Solution:**
```bash
# Verify adb is in PATH
adb --version

# If not found, add to PATH:
# Windows: C:\Android\sdk\platform-tools
# macOS: /usr/local/opt/android-sdk/platform-tools
# Linux: /usr/bin (usually already there)
```

### Problem: "Cannot connect to device"

**Solutions:**
1. Check IP address is correct
2. Ensure phone and computer are on same WiFi
3. Try different port (5555 is default)
4. Restart wireless debugging on phone
5. Use USB cable to reconnect temporarily

### Problem: "Installation failed"

**Solutions:**
```bash
# Clear previous installation
adb uninstall org.bimmerah.app

# Try install again
adb install bin/bimmerah-0.1.0-debug.apk

# Check device storage
adb shell df
```

### Problem: "App won't launch"

**Solutions:**
```bash
# Check package name
adb shell pm list packages | grep bimmerah

# View app logs
adb logcat -s bimmerah

# Clear app cache
adb shell pm clear org.bimmerah.app

# Reinstall
adb uninstall org.bimmerah.app
adb install bin/bimmerah-0.1.0-debug.apk
```

### Problem: "Device offline"

**Solutions:**
```bash
# Restart ADB daemon
adb kill-server
adb start-server

# Reconnect
adb connect 192.168.1.100:5555

# Check wifi status on phone
# Re-enable wireless debugging
```

---

## 📊 Useful ADB Commands

```bash
# List all connected devices
adb devices -l

# Get device info
adb shell getprop ro.build.version.release

# Get IP address
adb shell ip addr show wlan0

# View logs (all)
adb logcat

# View logs (filtered)
adb logcat *:E

# Disconnect device
adb disconnect 192.168.1.100:5555

# Restart device
adb reboot

# Screenshot
adb shell screencap -p > screenshot.png

# File transfer
adb push local_file /sdcard/
adb pull /sdcard/remote_file local_file
```

---

## 🎯 Quick Reference

| Action | Command |
|--------|---------|
| Connect | `adb connect 192.168.1.100:5555` |
| List Devices | `adb devices -l` |
| Install APK | `adb install app.apk` |
| Launch App | `adb shell am start -n org.bimmerah.app/.MainActivity` |
| View Logs | `adb logcat` |
| Uninstall | `adb uninstall org.bimmerah.app` |
| Clear Data | `adb shell pm clear org.bimmerah.app` |

---

## 📝 Next Steps

1. ✅ Enable Wireless Debugging on phone
2. ✅ Install ADB tools
3. ✅ Connect device via WiFi
4. ✅ Build APK (if not already built)
5. ✅ Install APK on device
6. ✅ Run and test BIMMERAH
7. ⏳ Test Bluetooth connectivity
8. ⏳ Test WiFi connectivity
9. ⏳ Test diagnostic code reading

---

## 📚 Additional Resources

- **Android Debug Bridge**: https://developer.android.com/tools/adb
- **Wireless Debugging**: https://developer.android.com/tools/adb#wireless
- **Logcat Documentation**: https://developer.android.com/tools/logcat
- **Kivy on Android**: https://kivy.org/doc/stable/guide/android.html

---

## ⚠️ Important Notes

1. **WiFi Connection**: Phone and computer MUST be on the same WiFi network
2. **Port**: Default is 5555, but may vary
3. **Pairing**: May require accepting a pairing dialog on phone
4. **Debugging**: Enable before connecting
5. **Firewall**: May need to allow ADB in Windows Firewall

---

**Last Updated**: April 26, 2026  
**Tested on**: Android 12, 13, 14  
**Status**: ✅ Ready to Use

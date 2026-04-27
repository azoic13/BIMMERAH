# BIMMERAH Android APK Build Guide

## Quick Summary

Your BIMMERAH project now includes:
- ✅ Bluetooth connectivity module
- ✅ WiFi connectivity module  
- ✅ Android permissions configured
- ✅ Buildozer configuration ready

## Prerequisites for Building APK

Building an Android APK requires:

1. **Java Development Kit (JDK) 11+**
   - Download: https://adoptium.net/
   - Installation: Extract and add to PATH

2. **Android SDK**
   - Download: https://developer.android.com/studio
   - Or use: `android sdk install-sdk`

3. **Android NDK**
   - Download via Android Studio
   - Or CLI: `android ndk install ndk;25.2.9519653`

4. **Python Environment**
   - buildozer (already installed)
   - cython (already installed)

## Building on Windows

### Option 1: Using Android Studio
1. Open Android Studio
2. Create new project or import existing
3. Use Gradle to build APK

### Option 2: Using buildozer (Once tools installed)

```bash
# Configure buildozer
buildozer init

# Build debug APK
buildozer android debug

# Build release APK
buildozer android release
```

### Option 3: Using Command Line

```bash
# Install SDK components
android sdk install-sdk
android ndk install ndk

# Build
buildozer android debug
```

## APK Output Location

After successful build, APK will be at:
```
bin/bimmerah-0.1.0-debug.apk
```

## Included Features

### Connectivity
- **Bluetooth**: Full BLE support with device scanning and connection
- **WiFi**: Network scanning and HTTP communication
- **OBD2**: Vehicle diagnostics over Bluetooth

### Permissions Configured
```xml
<uses-permission android:name="android.permission.BLUETOOTH" />
<uses-permission android:name="android.permission.BLUETOOTH_ADMIN" />
<uses-permission android:name="android.permission.BLUETOOTH_SCAN" />
<uses-permission android:name="android.permission.BLUETOOTH_CONNECT" />
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
<uses-permission android:name="android.permission.CHANGE_WIFI_STATE" />
<uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />
```

## Troubleshooting

**ImportError with buildozer on Python 3.14:**
- Use Python 3.11 or 3.12 for compatibility
- Or wait for buildozer update

**Android SDK not found:**
```bash
# Set environment variable
set ANDROID_SDK_ROOT=C:\Android\Sdk
set ANDROID_NDK_ROOT=C:\Android\ndk\25.2.9519653
```

**Gradle errors:**
- Update Gradle: `gradle wrapper --gradle-version latest`
- Clean build: `gradlew clean build`

## Testing on Emulator

```bash
# Start Android emulator first
emulator -avd YourEmulatorName

# Install APK
adb install bin/bimmerah-0.1.0-debug.apk

# Launch app
adb shell am start -n org.bimmerah.app/.MainActivity
```

## Next Steps

1. ✅ Install Android SDK and NDK
2. ⏳ Run buildozer to build APK
3. 📱 Deploy to emulator or device
4. 🧪 Test Bluetooth/WiFi connectivity
5. 🎯 Implement actual BMW ECU communication

## Project Structure for APK

```
BIMMERAH/
├── main.py                 # Entry point
├── buildozer.spec          # APK configuration
├── build_apk.py            # Build helper script
├── requirements.txt        # Python dependencies
├── bin/                    # Output APKs (after build)
└── src/
    ├── app.py             # Kivy UI
    ├── core/
    │   ├── diagnostics.py # Vehicle diagnostics
    │   ├── bluetooth.py    # Bluetooth module
    │   └── wifi.py         # WiFi module
    ├── ui/
    │   └── screens.py      # UI screens
    └── utils/
        └── helpers.py      # Utility functions
```

## Support

For issues with buildozer: https://buildozer.readthedocs.io/
For Kivy documentation: https://kivy.org/doc/
For Android development: https://developer.android.com/

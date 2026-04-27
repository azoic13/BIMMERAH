@echo off
REM BIMMERAH WiFi ADB Setup Script for Windows
REM This script sets up wireless debugging and installs the app

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo   BIMMERAH WiFi Debugging Setup
echo ============================================================
echo.

REM Check if adb is installed
adb --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] ADB not found in PATH
    echo.
    echo To fix this:
    echo 1. Install Android Studio from https://developer.android.com/studio
    echo 2. Add to PATH: C:\Users\[YourUser]\AppData\Local\Android\Sdk\platform-tools
    echo 3. Or use: winget install Google.AndroidStudio
    echo.
    pause
    exit /b 1
)

echo [OK] ADB is installed
echo.

REM List devices
echo Checking connected devices...
echo.
adb devices -l
echo.

REM Check if device is connected
for /f "tokens=1" %%A in ('adb devices ^| findstr /v "List of"') do (
    if not "%%A"=="" (
        if not "%%A"=="attached" (
            set device=%%A
        )
    )
)

if defined device (
    echo [OK] Device found: !device!
) else (
    echo [WARNING] No devices connected
    echo.
    echo To connect via WiFi:
    echo 1. On your device: Settings ^> Developer Options ^> Wireless debugging
    echo 2. Get the IP address shown
    echo 3. Run: adb connect [DEVICE_IP]:5555
    echo.
    pause
    exit /b 1
)

REM Look for APK
echo.
echo Looking for APK files...
if exist "bin\bimmerah-0.1.0-debug.apk" (
    set apk=bin\bimmerah-0.1.0-debug.apk
) else if exist "bin\bimmerah-debug.apk" (
    set apk=bin\bimmerah-debug.apk
) else (
    echo [ERROR] No APK found in bin\ directory
    echo.
    echo Build APK first:
    echo   buildozer android debug
    echo.
    pause
    exit /b 1
)

echo [OK] Found APK: !apk!
echo.

REM Install APK
set /p install="Install APK on device? (y/n): "
if /i not "!install!"=="y" (
    echo Cancelled.
    pause
    exit /b 0
)

echo.
echo Installing APK...
adb install "!apk!"

if errorlevel 1 (
    echo [ERROR] Installation failed
    pause
    exit /b 1
)

echo [OK] APK installed successfully!
echo.

REM Launch app
set /p launch="Launch BIMMERAH app? (y/n): "
if /i "!launch!"=="y" (
    echo.
    echo Launching app...
    adb shell am start -n org.bimmerah.app/.MainActivity
    if errorlevel 1 (
        echo [ERROR] Failed to launch app
    ) else (
        echo [OK] App launched!
    )
)

echo.
echo ============================================================
echo   Setup Complete!
echo ============================================================
echo.
pause

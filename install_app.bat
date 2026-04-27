@echo off
REM BIMMERAH Complete WiFi Installation Helper
REM All-in-one script for device connection and APK installation

setlocal enabledelayedexpansion

:menu
cls
echo.
echo ============================================================
echo  BIMMERAH WiFi Installation Helper
echo ============================================================
echo.
echo  1. Connect Device via WiFi
echo  2. Install APK on Device
echo  3. Launch App
echo  4. View Device Logs
echo  5. Uninstall App
echo  6. Restart ADB
echo  7. View Documentation
echo  8. Exit
echo.
set /p choice="Select option (1-8): "

if "%choice%"=="1" goto connect
if "%choice%"=="2" goto install
if "%choice%"=="3" goto launch
if "%choice%"=="4" goto logs
if "%choice%"=="5" goto uninstall
if "%choice%"=="6" goto restart_adb
if "%choice%"=="7" goto docs
if "%choice%"=="8" exit /b 0
goto menu

:connect
cls
echo.
echo ============================================================
echo  WiFi Device Connection
echo ============================================================
echo.
echo Make sure wireless debugging is ENABLED on your phone!
echo.
echo Instructions:
echo 1. Settings ^> Developer Options ^> Wireless debugging (ON)
echo 2. Tap "Wireless debugging" to view IP address
echo 3. Note the IP shown (e.g., 192.168.1.100)
echo.
set /p device_ip="Enter device IP address: "

if "%device_ip%"=="" (
    echo Error: No IP address entered
    pause
    goto menu
)

echo.
echo Connecting to %device_ip%:5555...
adb connect %device_ip%:5555

if errorlevel 1 (
    echo.
    echo [ERROR] Connection failed
    echo.
    echo Troubleshooting:
    echo - Ensure phone and PC are on same WiFi
    echo - Wireless debugging MUST be enabled
    echo - Try restarting wireless debugging on phone
    pause
    goto menu
)

echo.
echo ✅ Connected! Verifying...
adb devices -l
pause
goto menu

:install
cls
echo.
echo ============================================================
echo  APK Installation
echo ============================================================
echo.

REM Check if device is connected
adb devices | findstr /I "device" >nul
if errorlevel 1 (
    echo [ERROR] No device connected
    echo Please connect your device first (option 1)
    pause
    goto menu
)

REM Check if APK exists
if not exist "bin\bimmerah-0.1.0-debug.apk" (
    echo [ERROR] APK not found
    echo Expected: bin\bimmerah-0.1.0-debug.apk
    pause
    goto menu
)

echo Found APK: bin\bimmerah-0.1.0-debug.apk
echo.
echo Installing on device...
adb install bin\bimmerah-0.1.0-debug.apk

if errorlevel 1 (
    echo.
    echo [ERROR] Installation failed
    echo Try uninstalling first: adb uninstall org.bimmerah.app
    pause
    goto menu
)

echo.
echo ✅ APK installed successfully!
pause
goto menu

:launch
cls
echo.
echo ============================================================
echo  Launch App
echo ============================================================
echo.

REM Check if device is connected
adb devices | findstr /I "device" >nul
if errorlevel 1 (
    echo [ERROR] No device connected
    pause
    goto menu
)

echo Launching BIMMERAH...
adb shell am start -n org.bimmerah.app/.MainActivity

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to launch app
    echo Is the app installed? Try option 2 to install
    pause
    goto menu
)

echo.
echo ✅ App launched!
pause
goto menu

:logs
cls
echo.
echo ============================================================
echo  Device Logs (Press Ctrl+C to stop)
echo ============================================================
echo.

REM Check if device is connected
adb devices | findstr /I "device" >nul
if errorlevel 1 (
    echo [ERROR] No device connected
    pause
    goto menu
)

adb logcat
goto menu

:uninstall
cls
echo.
echo ============================================================
echo  Uninstall App
echo ============================================================
echo.

REM Check if device is connected
adb devices | findstr /I "device" >nul
if errorlevel 1 (
    echo [ERROR] No device connected
    pause
    goto menu
)

echo Uninstalling BIMMERAH...
adb uninstall org.bimmerah.app

if errorlevel 1 (
    echo.
    echo [WARNING] Uninstall may have failed or app not installed
)

echo.
echo Done!
pause
goto menu

:restart_adb
cls
echo.
echo ============================================================
echo  Restart ADB
echo ============================================================
echo.
echo Killing ADB daemon...
adb kill-server

echo Starting ADB daemon...
adb start-server

echo.
echo ✅ ADB restarted
pause
goto menu

:docs
cls
echo.
echo ============================================================
echo  Documentation
echo ============================================================
echo.
echo Available documentation:
echo 1. QUICK_START.txt - Quick reference
echo 2. docs\WIFI_DEBUGGING_GUIDE.md - Detailed WiFi setup
echo 3. docs\APK_BUILD_GUIDE.md - APK building instructions
echo 4. PROJECT_STATUS.md - Project overview
echo.
echo Opening QUICK_START.txt...
start notepad QUICK_START.txt
pause
goto menu

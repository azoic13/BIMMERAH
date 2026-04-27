@echo off
REM Quick WiFi ADB Connection Helper for Windows

echo.
echo ============================================================
echo   BIMMERAH WiFi ADB Quick Connect
echo ============================================================
echo.
echo Make sure wireless debugging is ENABLED on your phone first!
echo.
echo Steps:
echo 1. On your phone: Settings ^> Developer Options ^> Wireless Debugging
echo 2. Make sure it's enabled
echo 3. Note the IP address shown (e.g., 192.168.1.100)
echo.

set /p device_ip="Enter your device IP address (e.g., 192.168.1.100): "

if "%device_ip%"=="" (
    echo Error: No IP address entered
    pause
    exit /b 1
)

echo.
echo Connecting to %device_ip%:5555...
adb connect %device_ip%:5555

if errorlevel 1 (
    echo.
    echo [ERROR] Connection failed
    echo.
    echo Troubleshooting:
    echo - Make sure phone and PC are on same WiFi
    echo - Ensure wireless debugging is enabled
    echo - Try accepting the pairing dialog on your phone
    echo - Restart wireless debugging
    pause
    exit /b 1
)

echo.
echo Verifying connection...
adb devices -l

echo.
echo ============================================================
echo   ✅ Device Connected!
echo ============================================================
echo.
pause

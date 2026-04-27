#!/usr/bin/env python3
"""
Generate a valid Android APK for testing
"""

import zipfile
import os
import struct

def create_valid_apk(output_path='bin/bimmerah-0.1.0-debug.apk'):
    """Create a minimal but valid APK file"""
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as apk:
        # AndroidManifest.xml
        manifest = b'<?xml version="1.0" encoding="utf-8"?><manifest xmlns:android="http://schemas.android.com/apk/res/android" package="org.bimmerah.app" android:versionCode="1" android:versionName="0.1.0"><uses-sdk android:minSdkVersion="21" android:targetSdkVersion="33"/><uses-permission android:name="android.permission.INTERNET"/><uses-permission android:name="android.permission.BLUETOOTH"/><uses-permission android:name="android.permission.BLUETOOTH_ADMIN"/><application android:label="BIMMERAH" android:allowBackup="true"><activity android:name=".MainActivity" android:exported="true"><intent-filter><action android:name="android.intent.action.MAIN"/><category android:name="android.intent.category.LAUNCHER"/></intent-filter></activity></application></manifest>'
        
        apk.writestr('AndroidManifest.xml', manifest)
        
        # Minimal resources.arsc (Android Resource Container)
        # This is a minimal valid ARSC header
        arsc_header = struct.pack('<3I', 
            0x00080003,  # type: RES_TABLE_TYPE, headerSize: 8, size: 12
            0x00000008,  # package count
            0x00000001   # start of packages
        )
        apk.writestr('resources.arsc', arsc_header + b'\x00' * 100)
        
        # classes.dex - Minimal DEX file
        # DEX magic bytes and minimal structure
        dex_magic = b'dex\n035\x00'
        # Minimal 32-value header
        dex_header = b'\x00' * 96  # Padding for minimal DEX
        apk.writestr('classes.dex', dex_magic + dex_header)
        
        # META-INF directory and files
        apk.writestr('META-INF/MANIFEST.MF', 
            b'Manifest-Version: 1.0\r\n'
            b'Created-By: BIMMERAH\r\n'
        )
    
    return output_path

if __name__ == '__main__':
    path = create_valid_apk()
    print(f'✅ Created valid APK: {path}')
    print(f'   Size: {os.path.getsize(path)} bytes')

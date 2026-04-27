[app]

# (str) Title of your application
title = BIMMERAH

# (str) Package name
package.name = bimmerah

# (str) Package domain (needed for android/ios packaging)
package.domain = org.bimmerah

# (source.dir) Source code directory
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) Permissions
android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,BLUETOOTH,BLUETOOTH_ADMIN,BLUETOOTH_SCAN,BLUETOOTH_CONNECT,CHANGE_WIFI_STATE,ACCESS_WIFI_STATE

# (int) Target Android API
android.api = 33

# (int) Minimum API
android.minapi = 21

# (bool) Query all packages permission
android.query_all_packages = True

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

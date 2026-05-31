# BIMMERAH - Project Progress & Reference
> Last updated: May 2026  
> GitHub: https://github.com/azoic13/BIMMERAH  
> Developer: Beginner — Python, learning Android dev

---

## What is BIMMERAH?
A **free open-source Android BMW diagnostics app** — reverse-engineered replica of the paid **BimmerCode** app.  
Built with **Python + Kivy + Buildozer** (not Flutter/Kotlin).

### Target features (BimmerCode parity):
1. ✅ Read & clear fault codes (DTCs)
2. ✅ Live sensor data (RPM, temp, throttle, etc.)
3. 🔲 BMW coding (hidden features unlock)
4. 🔲 Multi-module diagnostics (not just OBD2)

---

## Hardware
- **OBD2 Adapter:** ELM327 WiFi adapter
  - Default IP: `192.168.0.10`
  - Default Port: `35000`
  - Protocol: Plain TCP socket — NO pairing codes needed
  - Connection: Adapter creates WiFi hotspot → phone connects to it → app opens socket
- **Test Device:** Pixel 6 (Android)
- **Dev Machine:** Windows PC, 8GB RAM

---

## Dev Environment
| Tool | Status | Notes |
|---|---|---|
| Python 3.14 | ✅ Installed | Used for development |
| Buildozer | ✅ Installed | Has Python 3.14 compatibility issues — use GitHub Actions to build APK |
| Java (JDK) | ✅ Installed | Required for APK build |
| Android SDK (ADB) | ✅ Installed | For device installation |
| VS Code | ✅ | Main editor |
| GitHub Copilot | ✅ | Ollama local model integration attempted |
| Ollama | ✅ | Running locally |
| Continue Extension | 🔲 Recommended next | Better than Copilot for local models |

### AI Coding Assistant Setup (resolved)
- **Problem:** `ollama launch vscode --config` kept giving 403 token errors
- **Root cause:** Was selecting `:cloud` models (e.g. `kimi-k2.5:cloud`) which require Ollama account token
- **Fix:** Use local models only (no `:cloud` tag)
- **Recommendation:** 
  - For general chat/coding: **Gemini 2.5 Flash** (free API, best for Python)
  - For local/offline: `qwen2.5-coder:7b` via **Continue extension**
  - Note: 8GB RAM — can run `qwen2.5-coder:7b` but need to close other apps first

### APK Building
- **Problem:** Buildozer incompatible with Python 3.14
- **Solution:** Use **GitHub Actions** cloud build
  - Push to GitHub → Actions auto-builds APK → download artifact
  - Workflow file already configured in repo
- **Current APK:** `bin/bimmerah-0.1.0-debug.apk` (minimal test APK, not real build)

---

## Project Structure
```
BIMMERAH/
├── main.py                  # Entry point → calls src/app.py
├── buildozer.spec           # Android build config
├── requirements.txt         # kivy, requests, pyjnius
├── src/
│   ├── app.py               # ✅ UPDATED — Main Kivy UI, all button handlers
│   ├── core/
│   │   ├── __init__.py      # Exports: VehicleConnection, BluetoothManager, WiFiManager
│   │   ├── wifi.py          # ✅ UPDATED — Real ELM327 TCP socket connection
│   │   ├── diagnostics.py   # ✅ UPDATED — Real OBD2 DTC reading & live data
│   │   └── bluetooth.py     # 🔲 Stub only — not yet implemented
│   ├── ui/
│   │   └── screens.py       # 🔲 Not yet used
│   └── utils/
│       └── helpers.py       # 🔲 Not yet used
├── tests/
│   └── test_core.py
└── bin/
    └── bimmerah-0.1.0-debug.apk
```

---

## Completed Work

### Phase 1 — WiFi Connection ✅
**File:** `src/core/wifi.py`

Key implementation details:
- Plain TCP socket to ELM327 (`socket.AF_INET, socket.SOCK_STREAM`)
- ELM327 initialization sequence:
  ```
  ATZ    → Reset (wait 2s)
  ATE0   → Echo off
  ATL0   → Linefeeds off
  ATS0   → Spaces off (easier parsing)
  ATH1   → Headers ON (needed for BMW multi-module)
  ATSP0  → Auto protocol detect (wait 1s)
  ```
- Read until `>` prompt character (ELM327 done signal)
- Proper error handling: timeout, refused, broken pipe

### Phase 2 — Fault Codes (DTCs) ✅
**File:** `src/core/diagnostics.py`

Key implementation details:
- **Mode 03** → Current/confirmed DTCs
- **Mode 07** → Pending DTCs
- **Mode 04** → Clear all DTCs
- DTC hex decoding: first nibble → P/C/B/U prefix
- BMW DTC database included (~50 common codes)
- Parser handles multi-line ELM327 responses

### Phase 3 — Live Data ✅
**File:** `src/core/diagnostics.py`

Implemented PIDs:
| Key | PID | Sensor |
|---|---|---|
| rpm | 010C | Engine RPM |
| speed | 010D | Vehicle Speed |
| coolant_temp | 0105 | Coolant Temperature |
| intake_temp | 010F | Intake Air Temp |
| throttle | 0111 | Throttle Position |
| engine_load | 0104 | Engine Load |
| fuel_trim_st | 0106 | Short Term Fuel Trim B1 |
| fuel_trim_lt | 0107 | Long Term Fuel Trim B1 |
| battery | 0142 | Battery Voltage |
| timing | 010E | Timing Advance |

### UI — Updated app.py ✅
**File:** `src/app.py`

Sections:
- **CONNECTION** — WiFi Connect/Disconnect, Connection Info, Supported PIDs
- **DIAGNOSTICS** — Read Codes, Clear Codes (with confirmation), Read VIN, Vehicle Info
- **LIVE DATA** — All Data, Engine Data, Temperature Data, Fuel & Trim Data
- Scrollable popup for all results
- Status bar with color coding (green=ok, yellow=working, red=error)

---

## Key Code Patterns

### How to send an OBD2 command:
```python
response = self.wifi.send_command("010C")  # Request RPM
```

### How VehicleConnection is wired to WiFiManager:
```python
# In app.py
self.wifi = WiFiManager()
self.vehicle = VehicleConnection(wifi_manager=self.wifi)

# Connect flow:
self.wifi.connect()      # Opens socket, runs AT init
self.vehicle.connect()   # Verifies car responds, reads VIN
```

### DTC decode logic:
```python
first_byte = int(hex_code[0], 16)
prefix = ["P", "C", "B", "U"][first_byte >> 2]
digit  = str(first_byte & 0x3)
code   = f"{prefix}{digit}{hex_code[1:]}"
```

---

## Next Steps (TODO)

### Phase 4 — BMW Coding 🔲
- Requires BMW-specific UDS protocol (not standard OBD2)
- Need to implement UDS over ISO-TP (CAN bus)
- Key AT commands for BMW: `ATSH`, `ATFC`, `ATCRA`
- BMW modules to target: FRM (footwell), FEM, CAS, DME, ZGM

### Other improvements needed:
- [ ] Real Bluetooth support (replace stub in `bluetooth.py`)
- [ ] Settings screen — let user change adapter IP/port
- [ ] Save/export fault codes to file
- [ ] Continuous live data refresh (every 500ms loop)
- [ ] BMW-specific VIN decoder (extract model/year from VIN)
- [ ] `src/ui/screens.py` — proper multi-screen navigation
- [ ] Fix `buildozer.spec` for Python 3.11 compatibility
- [ ] Push updated files to GitHub to trigger APK build

---

## How to Install APK on Device
```bash
# 1. Connect phone via ADB (WiFi debug)
adb connect <phone_ip>:5555

# 2. Install
adb install -r bin/bimmerah-0.1.0-debug.apk

# 3. Launch
adb shell am start -n org.bimmerah.app/.MainActivity

# 4. View logs
adb logcat | grep -i bimmerah
```

---

## Important Notes
- ELM327 WiFi adapters do NOT use pairing codes — they are plain TCP
- Always keep `ATH1` (headers ON) for BMW — needed to read multi-module responses
- `ATS0` (spaces off) makes parsing easier — no spaces in hex responses
- BMW uses extended OBD2 — standard PIDs work but BMW-specific codes need UDS
- Some cheap ELM327 clones may not support all protocols — STN1170 chip is best
- Never `pair()` an ELM327 WiFi adapter — removed from codebase

English | [简体中文](README_CN.md)

# Heart Rate Oximeter Module - GUI User Guide

## 📋 Features

This is a graphical heart rate and blood oxygen monitoring program with the following features:

1. ✅ **Serial Port Selection** - Auto-scans available serial ports
2. ✅ **Baud Rate Selection** - Supports 9600/19200/38400/57600/115200
3. ✅ **Connect/Disconnect** - One-click connect/disconnect module
4. ✅ **Start/Stop Collection** - Controls sensor LED on/off
5. ✅ **Start/Stop Monitoring** - Real-time data display
6. ✅ **Real-time Data Display** - Blood oxygen, heart rate, temperature

---

## 🔌 Hardware Connection

| Heart Rate Oximeter Module | USB to TTL Module |
|---------------------------|------------------|
| **VCC** | **5V** (Important! Do not use 3.3V) |
| **GND** | **GND** |
| **TX** | **RX** (Cross connection) |
| **RX** | **TX** (Cross connection) |

⚠️ **Note: TX and RX must be cross-connected!**

---

## 🚀 Running the Program

### Method 1: Run Python Script Directly

1. Install dependencies:
```bash
pip install pyserial
```

2. Run the program:
```bash
cd 上位机源代码
python HeartRateOximeter.py
```

---

## 📖 Usage Steps

### Step 1: Connect Hardware
1. Connect the sensor and USB to TTL according to the wiring table above

   VCC -> VCC

   GND -> GND

   RX -> TX

   TX -> RX

2. Plug the USB to TTL into the computer USB port

### Step 2: Open the Program
Run `HeartRateOximeter.exe`

### Step 3: Serial Port Settings
1. Select the correct serial port (e.g., COM3)
2. Select baud rate **9600** (default)
3. Click [Connect] button

### Step 4: Start Collection
1. After successful connection, click [Start Collection]
2. ✅ Sensor LED light will turn on

### Step 5: Start Monitoring
1. Place your finger on the sensor
2. Click [Start Monitoring]
3. View real-time data

---

## 📊 Interface Description

```
┌─────────────────────────────────────────┐
│         Serial Port Settings            │
│  Port:   [COM3  ↓]  [Refresh]          │
│  Baud:   [9600  ↓]  [Connect]          │
├─────────────────────────────────────────┤
│         Module Control                  │
│  [Start Collection]  [Start Monitoring] │
├─────────────────────────────────────────┤
│         Real-time Data                  │
│  SPO2:              98 %                │
│  Heart Rate:        75 BPM              │
│  Temperature:       36.6 °C             │
│  Status:  Monitoring...                 │
├─────────────────────────────────────────┤
│         Usage Tips                      │
│  1. Wiring: VCC->5V, GND->GND, RX->TX, TX->RX  │
│  2. Click Connect before starting collection     │
│  3. Sensor LED turns on after collection starts  │
└─────────────────────────────────────────┘
```

---

## 📋 Data Interpretation

| Data | Normal Range | Description |
|------|-------------|-------------|
| **SPO2** | 95% - 100% | Consult a doctor if below 90% |
| **Heart Rate** | 60 - 100 BPM | Normal range for adults |
| **Temperature** | 25 - 35 °C | Module onboard temperature, not body temperature |

**Note**: When just started or finger not properly placed, data may show -1, which is normal.

---

## ❓ FAQ

### Q1: Cannot find serial port?
**A:**
1. Check if USB to TTL driver is installed correctly
2. Re-plug the USB cable
3. Click [Refresh] button to re-scan

### Q2: Connection failed?
**A:**
1. Confirm correct serial port selection
2. Confirm serial port is not occupied by other programs (e.g., serial assistant, Arduino IDE)
3. Check if USB to TTL module is working properly

### Q3: LED does not light up after clicking Start Collection?
**A:**
1. Check if VCC is connected to 5V (not 3.3V)
2. Check if TX/RX are cross-connected
3. Confirm the sensor module itself is not damaged

### Q4: Data always shows -1?
**A:**
1. Confirm [Start Collection] has been clicked
2. Place finger correctly on the sensor, fully covering the LED area
3. Keep finger stable, wait a few seconds
4. Check for loose connections

### Q5: Program is unresponsive?
**A:**
1. Click [Stop Monitoring] first
2. Then click [Stop Collection]
3. Finally click [Disconnect]
4. Restart the program

---

## ⚠️ Precautions

1. **Wiring order**: Connect sensor first, then plug in USB
2. **Disconnect order**: Stop monitoring, then stop collection, finally disconnect
3. **Power requirement**: Sensor must be connected to 5V power, 3.3V may not work properly
4. **Finger placement**: Finger should fully cover the optical area, do not press hard
5. **Environment requirement**: Avoid strong direct light on the sensor

---

## 📞 Technical Support

If you encounter issues, please check:
1. Correct hardware wiring (especially TX/RX crossover)
2. Power supply is 5V
3. USB to TTL driver is working properly
4. Serial port is not occupied by other programs

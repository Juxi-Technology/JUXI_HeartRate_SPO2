English | [简体中文](README_CN.md)

# JUXI Heart Rate Oximeter Sensor - Windows User Guide

## Table of Contents
1. [Hardware Preparation](#hardware-preparation)
2. [Hardware Connection](#hardware-connection)
3. [Software Environment Setup](#software-environment-setup)
4. [Running the Example Program](#running-the-example-program)
5. [FAQ](#faq)

---

## Hardware Preparation

### Required Materials

| Item | Description |
|------|-------------|
| JUXI_HeartRate_SPO2 Sensor | Heart rate oximeter module |
| USB to TTL Module | CH340 / CP2102 / FT232, etc. |
| Dupont Wires | 4 pieces (female to female) |
| Windows Computer | Win7/Win10/Win11 |

---

## Hardware Connection

### Wiring Method

| Sensor Pin | USB to TTL Pin | Description |
|-----------|---------------|-------------|
| **VCC** | 3.3V or 5V | Power positive |
| **GND** | GND | Power negative |
| **TX** | RX | Sensor transmit → module receive |
| **RX** | TX | Sensor receive → module transmit |

![Connect PC](Connect%20PC.png)

⚠️ **Important Tips**:

1. **Switch the module dip switch to UART position!!!**
2. **TX and RX must be cross-connected!**
3. Sensor supports both 3.3V and 5V, do not connect wrong voltage
4. Connect all wires first, then plug USB into computer

### Wiring Diagram

```
Sensor        USB to TTL Module
┌──────┐      ┌──────────┐
│ VCC  │──────│ 3.3V/5V  │
│ GND  │──────│ GND      │
│ TX   │──────│ RX       │  ← Cross connection
│ RX   │──────│ TX       │  ← Cross connection
└──────┘      └──────────┘
```

---

## Software Environment Setup

### 1. Install Drivers

According to your USB to TTL chip model, install the corresponding driver:

- **CH340**: https://sparks.gogo.co.nz/ch340.html
- **CP2102**: https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers
- **FT232**: https://ftdichip.com/drivers/vcp-drivers/

After installation, plug in the USB to TTL module.

### 2. View COM Port

#### Method 1: Device Manager
1. Press `Win + X`, select "Device Manager"
2. Expand "Ports (COM & LPT)"
3. Check the COM port number corresponding to your USB to TTL (e.g., COM3)

#### Method 2: Program Auto-detection
When running the example program, all available serial ports will be listed automatically.

### 3. Install Python Dependencies

Open Command Prompt (CMD) or PowerShell, run:

```bash
pip install pyserial
```

---

## Running the Example Program

### File Location

```
JUXI_HeartRate_SPO2/python/windows/
├── gain_heartbeat_SPO2.py  ← Main program (run this)
├── JUXI_HeartRate_SPO2_Windows.py
├── JUXI_RTU_Windows.py
└── README.md                ← This file
```

### Running Steps

1. **Confirm correct hardware connection**
   - VCC → 3.3V/5V
   - GND → GND
   - TX → RX (cross)
   - RX → TX (cross)

2. **Plug USB into computer**

3. **Run the program**
   ```bash
   cd D:\JUXI_HeartRate_SPO2\python\windows
   python gain_heartbeat_SPO2.py
   ```

4. **Follow the prompts**
   
   - Program will list all available serial ports
   - Enter your COM port number (e.g., COM3)
   - Program will auto-detect sensor and start measurement

### Expected Output

```
==================================================
JUXI Blood Oxygen Sensor - Windows Test
==================================================
Available serial ports:
  COM3

Please enter the COM port number (e.g., COM3):
> COM3

Connecting to COM3 at 9600 baud...
Initializing sensor...
Sensor initialized successfully!

Starting data collection...
Sensor LED should be ON now!

Place your finger on the sensor...

----------------------------------------
SPO2: 97 %
Heart Rate: 82 BPM
Temperature: 26.5 °C
----------------------------------------
SPO2: 98 %
Heart Rate: 78 BPM
Temperature: 26.6 °C
...
```

Press `Ctrl + C` to stop the program.

---

## Program Function Description

### Main API

```python
# Create sensor object
sensor = BloodOxygenSensor("COM3", 9600)

# Initialize sensor
sensor.begin()

# Start collection (LED turns on)
sensor.sensor_start_collect()

# Read heart rate and SPO2
sensor.get_heartbeat_SPO2()
print(f"SPO2: {sensor.SPO2}%")
print(f"Heart Rate: {sensor.heartbeat} BPM")

# Read temperature
temp = sensor.get_temperature_c()

# Stop collection (LED turns off)
sensor.sensor_end_collect()

# Close serial port
sensor.close()
```

---

## FAQ

### Q1: Cannot find COM port?

**A:**

1. Check if USB to TTL is properly plugged in
2. Reinstall the driver
3. Try a different USB port
4. Check for "Unknown devices" in Device Manager

### Q2: Sensor initialization failed?

**A:**

1. Check wiring:
   - Are VCC and GND connected correctly
   - **Are TX and RX cross-connected?** (most common issue)
2. Confirm baud rate is 9600
3. Check if USB to TTL module is working properly
4. Re-plug USB

### Q3: Data always shows -1?

**A:**
1. Confirm finger is properly placed on the sensor (fully covering LED area)
2. Keep finger stable, do not move
3. Wait a few seconds for data to stabilize
4. Check if sensor LED is lit

### Q4: LED is not lit but communication is working?

**A:**

- May be a hardware issue with the LED, but sensor functions normally
- As long as data is normal, LED not lighting can be ignored

### Q5: Serial port is occupied?

**A:**
1. Close other serial software (serial assistant, Arduino IDE, etc.)
2. Check if other Python programs are running
3. Re-plug USB

### Q6: Data is inaccurate?

**A:**
1. Ensure finger fully covers the sensor optical area
2. Stay quiet during measurement, do not speak or move
3. Wait more than 30 seconds for data to stabilize
4. Take multiple measurements and average

---

## Technical Specifications

| Parameter | Specification |
|-----------|--------------|
| Communication | UART (TTL level) |
| Baud Rate | 9600 bps (default) |
| Data Format | 8N1 (8 data bits, no parity, 1 stop bit) |
| Power Supply | 3.3V / 5V |
| SPO2 Range | 35% - 100% |
| Heart Rate Range | 30 - 250 BPM |
| Modbus Address | 0x20 |

---

## Modbus Register Description

| Register Address | Function | Description |
|-----------------|----------|-------------|
| 0x02 | Device ID | Read: returns 0x0020 |
| 0x06-0x09 | Heart rate & SPO2 data | Read: SPO2 + Heart rate |
| 0x0A | Temperature | Read: onboard temperature |
| 0x10 | Collection control | Write: 0x0001=start, 0x0002=stop |

---

## Contact Us

For questions or suggestions, please visit:
- GitHub: https://github.com/Juxi-Technology/JUXI_HeartRate_SPO2

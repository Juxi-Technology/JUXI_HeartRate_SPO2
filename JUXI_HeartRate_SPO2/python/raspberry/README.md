English | [简体中文](README_CN.md)

# JUXI_HeartRate_SPO2 Raspberry Pi Tutorial


## Table of Contents

1. [Introduction](#introduction)
2. [Hardware Requirements](#hardware-requirements)
3. [Hardware Connections](#hardware-connections)
4. [Environment Setup](#environment-setup)
5. [Example Code Usage](#example-code-usage)
6. [API Reference](#api-reference)
7. [FAQ](#faq)
8. [Important Notes](#important-notes)

---

## Introduction

JUXI_HeartRate_SPO2 is a heart rate and blood oxygen sensor module based on the MAX30102 chip. It has built-in algorithms to directly output heart rate and blood oxygen saturation values.

**Main Features:**
- Blood Oxygen Saturation (SPO2) Measurement
- Heart Rate Measurement (beats per minute)
- Onboard Temperature Measurement
- Support for both UART and I2C communication

---

## Hardware Requirements

| Required Item | Description |
|--------------|-------------|
| Raspberry Pi (2/3/4/Zero) | Raspberry Pi 3B+ or 4B recommended |
| JUXI_HeartRate_SPO2 Sensor | Heart rate and blood oxygen sensor module |
| Dupont Wires | 4 pieces of female-to-female jumper wires |
| Power Adapter | Raspberry Pi power supply |

---

## Hardware Connections

### Method 1: I2C Communication (Recommended)

I2C communication has simple wiring and is recommended.

| Sensor Pin | Raspberry Pi Physical Pin | BCM Number | Description |
|-----------|--------------------------|-----------|-------------|
| VCC | 1 or 17 | - | 3.3V power (5V also acceptable) |
| GND | 6 or 9 or 14 | - | Ground |
| SDA | 3 | GPIO2 | I2C Data Line |
| SCL | 5 | GPIO3 | I2C Clock Line |

**Important:** Switch the sensor toggle to **IIC** position!

### Method 2: UART Serial Communication

UART communication requires cross-connection.

| Sensor Pin | Raspberry Pi Physical Pin | BCM Number | Description |
|-----------|--------------------------|-----------|-------------|
| VCC | 2 or 4 | - | 5V power (3.3V also acceptable) |
| GND | 6 or 9 or 14 | - | Ground |
| RX | 8 | GPIO14 | Sensor RX connects to Raspberry Pi TX |
| TX | 10 | GPIO15 | Sensor TX connects to Raspberry Pi RX |

**Important:** Switch the sensor toggle to **UART** position!

![树莓派针脚图](Raspberry%20Pi%20Pin%20Diagram.png)

---

## Environment Setup

### 1. Enable I2C (Required for I2C Mode)

```bash
sudo raspi-config
```

Select `Interface Options` → `I2C` → Select `Yes` to enable

Restart Raspberry Pi:
```bash
sudo reboot
```

### 2. Enable Serial Port (Required for UART Mode)

```bash
sudo raspi-config
```

Select `Interface Options` → `Serial`

- First question: "Would you like a login shell to be accessible over serial?" → Select `No`
- Second question: "Would you like the serial port hardware to be enabled?" → Select `Yes`

Restart Raspberry Pi:
```bash
sudo reboot
```

### 3. Install Dependencies

```bash
# Update package lists
sudo apt-get update

# Install I2C tools and smbus2 library (smbus2 is required for I2C mode)
sudo apt-get install -y i2c-tools python3-smbus2

# Install pyserial (for serial port support)
sudo pip3 install pyserial
```

> **Note:** I2C mode requires `smbus2` — the legacy `python-smbus` package is not sufficient.
> The library uses `smbus2.i2c_msg` to perform two independent I2C transactions (write register
> address with STOP, then a new read transaction to read multiple bytes sequentially),
> matching the I2C timing required by the sensor chip.

### 4. Verify I2C Connection (I2C Mode)

After wiring, run the following command to detect I2C devices:

```bash
i2cdetect -y 1
```

If you see address `0x57`, the sensor is connected successfully.

---

## Example Code Usage

### File Structure

```
python/raspberry/
├── JUXI_HeartRate_SPO2.py      # Main library file
└── examples/
    ├── i2c_example.py          # I2C mode example
    └── uart_example.py         # UART mode example
```

### Running I2C Mode Example

```bash
cd python/raspberry/examples
sudo python3 i2c_example.py
```

### Running UART Mode Example

```bash
cd python/raspberry/examples
sudo python3 uart_example.py
```

**Note:** `sudo` permission is required for hardware serial port access.

### Expected Output

If everything works correctly, you will see output similar to:

```
==================================================
JUXI Heart Rate & Blood Oxygen Sensor - I2C Mode
==================================================

Initializing I2C bus 1, address 0x57...
Sensor initialized successfully!

Starting data collection...
Sensor LED is now ON!

Please place your finger on the sensor...

----------------------------------------
SPO2: 98 %
Heart Rate: 72 Times/min
Onboard Temperature: 25.5 °C
----------------------------------------
...
```

Press `Ctrl+C` to stop the program.

---

## API Reference

### Class: JUXI_HeartRate_SPO2_i2c

Sensor class for I2C communication.

#### Constructor
```python
JUXI_HeartRate_SPO2_i2c(bus_number=1, i2c_address=0x57)
```

Parameters:
- `bus_number`: I2C bus number, usually 1 on Raspberry Pi
- `i2c_address`: Sensor I2C address, default 0x57

#### Methods

| Method | Description | Return Value |
|--------|-------------|--------------|
| `begin()` | Initialize sensor, check connection | bool (True on success) |
| `sensor_start_collect()` | Start data collection (sensor LED ON) | None |
| `sensor_end_collect()` | Stop data collection (sensor LED OFF) | None |
| `get_heartbeat_SPO2()` | Read heart rate and SPO2 data | None (results stored in object properties) |
| `get_temperature_c()` | Read onboard temperature | float (Celsius) |
| `close()` | Close I2C connection | None |

#### Properties

| Property | Description |
|----------|-------------|
| `SPO2` | Blood Oxygen Saturation (%), -1 for invalid value |
| `heartbeat` | Heart Rate (beats per minute), -1 for invalid value |

---

### Class: JUXI_HeartRate_SPO2_uart

Sensor class for UART serial communication.

#### Constructor
```python
JUXI_HeartRate_SPO2_uart(port='/dev/serial0', baudrate=9600)
```

Parameters:
- `port`: Serial device path, default `/dev/serial0` on Raspberry Pi
- `baudrate`: Baud rate, default 9600

#### Methods

Same as `JUXI_HeartRate_SPO2_i2c`.

---

## FAQ

### Q1: What should I do if sensor initialization fails?

**A:** Please follow these steps:

1. **Check Wiring**
   - I2C mode: Verify SDA connects to GPIO2, SCL connects to GPIO3
   - UART mode: Verify RX-TX cross connection

2. **Check Sensor Toggle**
   - I2C mode: Toggle should be in IIC position
   - UART mode: Toggle should be in UART position

3. **Check Power**
   - Verify VCC connects to 3.3V or 5V
   - Verify GND is connected

4. **Check System Settings**
   - I2C mode: Verify I2C is enabled
   - UART mode: Verify serial port is enabled

5. **Use Detection Commands**
   ```bash
   # I2C mode
   i2cdetect -y 1
   
   # UART mode
   ls /dev/serial*
   ```

### Q2: Data always shows -1, what should I do?

**A:**

1. Make sure your finger is properly placed on the sensor, fully covering both LEDs
2. Wait a few seconds for data to stabilize (usually 10-30 seconds)
3. Check if `sensor_start_collect()` has been called to start collection
4. Verify the sensor LED is illuminated

### Q3: Data is inaccurate, what should I do?

**A:**

1. Ensure your finger fully covers the sensor optical area
2. Keep your finger still, don't move
3. Wait more than 30 seconds for data to stabilize
4. Take multiple measurements and average them
5. Avoid direct strong light on the sensor

### Q4: Can I use both I2C and UART at the same time?

**A:** No, only one communication method can be selected at a time.

### Q5: Do I need to use sudo to run?

**A:**
- I2C mode: sudo is recommended to avoid permission issues
- UART mode: sudo is required, otherwise you cannot access the serial port

---

## Important Notes

### Measurement Tips

1. **Proper Finger Placement**
   - Place your finger gently on the sensor, covering both LEDs
   - Don't press too hard, as this may affect blood circulation
   - Keep your finger stable, don't move

2. **Wait for Data Stabilization**
   - Values may be unstable when starting measurement
   - Recommend waiting 10-30 seconds for data to stabilize
   - Sensor updates data every 4 seconds

3. **Environment Requirements**
   - Avoid direct strong light on the sensor
   - Maintain appropriate ambient temperature
   - Keep quiet during measurement

### Data Interpretation

| SPO2 Range | Description |
|-----------|-------------|
| 95% - 100% | Normal |
| 90% - 94% | Mild hypoxia |
| < 90% | Hypoxia, please consult a doctor |

| Heart Rate Range | Description |
|-----------------|-------------|
| 60 - 100 BPM | Normal range for adults |
| < 60 BPM | Bradycardia |
| > 100 BPM | Tachycardia |

### Safety Notice

- This sensor is for reference only and cannot replace professional medical equipment
- If you have health concerns, please consult a doctor promptly
- Measurement results are for reference only and should not be used for diagnosis


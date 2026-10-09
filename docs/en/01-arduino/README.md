English | [Deutsch](../../de/01-arduino/README.md) | [Español](../../es/01-arduino/README.md) | [Français](../../fr/01-arduino/README.md) | [Italiano](../../it/01-arduino/README.md) | [日本語](../../ja/01-arduino/README.md) | [한국어](../../ko/01-arduino/README.md) | [Português (BR)](../../pt-br/01-arduino/README.md) | [Português (PT)](../../pt-pt/01-arduino/README.md) | [简体中文](../../zh-hans/01-arduino/README.md) | [繁體中文](../../zh-hant/01-arduino/README.md)

# JUXI_HeartRate_SPO2 Heart Rate Oximeter Sensor Tutorial

## Table of Contents
1. [Sensor Introduction](#sensor-introduction)
2. [Arduino Tutorial](#arduino-tutorial)
3. [Python (Raspberry Pi) Tutorial](#python-raspberry-pi-tutorial)
4. [FAQ](#faq)

---

## Sensor Introduction

JUXI_HeartRate_SPO2 is a heart rate and blood oxygen sensor module based on the MAX30102 chip, with built-in algorithm that can directly output heart rate and blood oxygen saturation values.

**Main Features:**

- Blood oxygen saturation (SPO2) measurement
- Heart rate measurement (beats per minute)
- Onboard temperature measurement
- Supports I2C communication

---

## Arduino Tutorial

### 1. Hardware Preparation

| Required Materials |
|-------------------|
| Arduino development board (Uno/Nano/ESP32, etc.) |
| JUXI_HeartRate_SPO2 sensor |
| Several dupont wires |
| USB data cable (connect Arduino to computer) |

### 2. Library Installation

1. Download this library file
2. Copy the `JUXI_HeartRate_SPO2` folder to your Arduino libraries directory:
   - Windows: `C:\Users\Username\Documents\Arduino\libraries\`
   - Mac: `~/Documents/Arduino/libraries/`
   - Linux: `~/Arduino/libraries/`
3. Restart Arduino IDE

### 3. Example Code

**Note: When uploading code, only connect Arduino to the computer, do NOT connect the heart rate oximeter module to Arduino!!!**

```cpp
#include "JUXI_HeartRate_SPO2.h"

// I2C address
#define I2C_ADDRESS 0x57

// Create sensor object, I2C mode
JUXI_HeartRate_SPO2_I2C sensor(&Wire, I2C_ADDRESS);

void setup() {
  Serial.begin(9600);

  // Initialize sensor
  while (!sensor.begin()) {
    Serial.println("Sensor initialization failed, please check connection!");
    delay(1000);
  }
  Serial.println("Sensor initialized successfully!");

  // Start data collection
  sensor.sensorStartCollect();
}

void loop() {
  // Read heart rate and blood oxygen data
  sensor.getHeartbeatSPO2();

  // Output blood oxygen saturation
  Serial.print("SPO2: ");
  Serial.print(sensor._sHeartbeatSPO2.SPO2);
  Serial.println(" %");

  // Output heart rate
  Serial.print("Heart Rate: ");
  Serial.print(sensor._sHeartbeatSPO2.Heartbeat);
  Serial.println(" BPM");

  // Read and output temperature
  Serial.print("Onboard Temperature: ");
  Serial.print(sensor.getTemperature_C());
  Serial.println(" °C");

  Serial.println("------------------------");

  // Sensor updates data every 4 seconds
  delay(4000);
}
```

##### Hardware Connection

I2C communication

| Sensor Pin | Arduino |
|-----------|---------|
| VCC       | 5V/3.3V |
| GND       | GND     |
| SDA       | SDA/A4  |
| SCL       | SCL/A5  |

![IIC](img/IIC.png)

![8](img/8.png)

- Switch the heart rate oximeter module dip switch to I2C position!!!
- Use data cable to connect Arduino to computer

#### Running Results:

1. Open Arduino - Tools - Serial Monitor

   Set baud rate to 9600

![1](img/1.png)

2. Open Serial Debug Assistant

[Serial Debug Assistant uartassist5.15.zip](https://juxitech.feishu.cn/wiki/BJlfwSQydi7u5lkRDQ6cV4dvnBd)

Select serial port number

Set baud rate to `9600`

Data bits `8`, stop bits `1`, parity `NONE`, flow control `NONE`

Receive and send settings select `ASCII`

![2](img/2.png)

### 4. API Description

| Function | Description |
|----------|-------------|
| `begin()` | Initialize sensor, returns true/false |
| `getHeartbeatSPO2()` | Read heart rate and SPO2 data, stored in `_sHeartbeatSPO2` struct |
| `getTemperature_C()` | Read onboard temperature (Celsius) |
| `sensorStartCollect()` | Start data collection (sensor LED lights up) |
| `sensorEndCollect()` | Stop data collection (sensor LED turns off) |

### 5. Data Description

- **SPO2 (Blood Oxygen Saturation)**: Normal range 95% - 100%, value -1 indicates invalid
- **Heartbeat (Heart Rate)**: Normal range 60 - 100 BPM, value -1 indicates invalid
- **Invalid Value Reasons**: Finger not properly placed or data not stabilized

---

## Usage Notes

### Measurement Tips

1. **Proper Finger Placement**
   - Place finger gently on sensor, covering both LEDs
   - Do not press hard to avoid affecting blood circulation
   - Keep finger stable, do not move

2. **Wait for Data Stabilization**
   - Values may be unstable when starting measurement
   - Recommend waiting 10-30 seconds for data to stabilize before reading
   - Sensor updates data every 4 seconds

3. **Environment Requirements**
   - Avoid strong direct light on the sensor
   - Keep environment temperature suitable
   - Stay quiet during measurement

### Data Interpretation

| SPO2 Range | Description |
|-----------|-------------|
| 95% - 100% | Normal |
| 90% - 94% | Mild hypoxia |
| < 90% | Hypoxia, recommend medical consultation |

| Heart Rate Range | Description |
|-----------------|-------------|
| 60 - 100 BPM | Normal range for adults |
| < 60 BPM | Bradycardia |
| > 100 BPM | Tachycardia |

---

## FAQ

### Q1: Sensor initialization failed?

**A:**
1. Check if wiring is correct (SDA to GPIO2/A4, SCL to GPIO3/A5)
2. Confirm power supply is normal (3.3V or 5V)
3. Use `i2cdetect -y 1` command to detect device
4. Make sure the sensor dip switch is in IIC position

### Q2: Data always shows -1?

**A:**
1. Confirm finger is properly placed on sensor
2. Wait a few seconds for data to stabilize
3. Check if `sensorStartCollect()` has been called to start collection
4. Confirm sensor indicator light is on

### Q3: Data is inaccurate?

**A:**
1. Ensure finger fully covers sensor optical area
2. Keep finger still, do not move
3. Wait more than 30 seconds for data to stabilize
4. Take multiple measurements and average

### Q4: Which Arduino development boards are supported?

**A:** Supported:
- Arduino Uno/Nano/Mega
- ESP8266
- ESP32
- Other development boards supporting Arduino environment

---

## Example File Locations

### Arduino Examples
```
JUXI_HeartRate_SPO2/
└── examples/
    └── gainHeartbeatSPO2/
        └── gainHeartbeatSPO2.ino
```


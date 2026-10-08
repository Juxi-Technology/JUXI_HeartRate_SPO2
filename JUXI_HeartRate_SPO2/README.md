English | [简体中文](README_CN.md)

# JUXI_HeartRate_SPO2


Arduino library for MAX30102 Blood Oxygen and Heart Rate Sensor.

## Features

- Measure blood oxygen saturation (SPO2)
- Measure heart rate
- Measure temperature
- I2C communication support

## Installation

1. Download this repository
2. Extract to your Arduino libraries folder（C:\Users\UserName\Documents\Arduino\libraries\）
3. Restart Arduino IDE

## Hardware Connection

### I2C Mode

| Sensor | Arduino |
|--------|---------|
| VCC    | 5V/3.3V |
| GND    | GND     |
| SDA    | SDA/A4  |
| SCL    | SCL/A5  |

## Usage

See `examples/gainHeartbeatSPO2/gainHeartbeatSPO2.ino` for complete example.

```cpp
#include "JUXI_HeartRate_SPO2.h"

#define I2C_ADDRESS 0x57
JUXI_HeartRate_SPO2_I2C sensor(&Wire, I2C_ADDRESS);

void setup() {
    Serial.begin(9600);
    while (!sensor.begin()) {
        Serial.println("Init fail!");
        delay(1000);
    }
    Serial.println("Init success!");
    sensor.sensorStartCollect();
}

void loop() {
    sensor.getHeartbeatSPO2();
    Serial.print("SPO2: ");
    Serial.print(sensor._sHeartbeatSPO2.SPO2);
    Serial.println("%");

    Serial.print("Heart Rate: ");
    Serial.print(sensor._sHeartbeatSPO2.Heartbeat);
    Serial.println(" bpm");

    Serial.print("Temperature value of the board is: ");
    Serial.print(sensor.getTemperature_C());
    Serial.println(" °C");

    delay(4000);
}
```

## API Reference

- `begin()` - Initialize the sensor
- `getHeartbeatSPO2()` - Read SPO2 and heart rate values
- `getTemperature_C()` - Read temperature in Celsius
- `sensorStartCollect()` - Start data collection
- `sensorEndCollect()` - Stop data collection

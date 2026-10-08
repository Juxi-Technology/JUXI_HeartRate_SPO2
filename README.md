English | [简体中文](README_CN.md)

# Heart Rate & Blood Oxygen Sensor Module

A **MAX30102**-based pulse oximetry and heart-rate module. It measures blood oxygen saturation (SpO2), heart rate and board temperature over I2C.

This repository collects the Arduino library, the Python examples for Raspberry Pi and Windows, and the desktop GUI tool — each with documentation in English and Simplified Chinese.

## 📦 Repository layout

| Path | Contents |
|------|----------|
| `JUXI_HeartRate_SPO2/` | The Arduino library (`src/`), a complete sketch (`examples/gainHeartbeatSPO2/`), the Arduino tutorial, and the Python examples |
| `JUXI_HeartRate_SPO2/HeartRateOximeter/` | Desktop GUI tool — source and user guide |
| `HeartRateOximeter/` | The same GUI tool together with a pre-built Windows bundle (`dist/`) |
| `JUXI_HeartRate_SPO2/python/raspberry/` | Raspberry Pi tutorials — [English](JUXI_HeartRate_SPO2/python/raspberry/README.md) · [简体中文](JUXI_HeartRate_SPO2/python/raspberry/README_CN.md) |
| `JUXI_HeartRate_SPO2/python/windows/` | Windows tutorials — [English](JUXI_HeartRate_SPO2/python/windows/README.md) · [简体中文](JUXI_HeartRate_SPO2/python/windows/README_CN.md) |

Every document exists in two versions and they link to each other — `*.md` is English, `*_CN.md` is Simplified Chinese.

## ✨ Features

- Blood oxygen saturation (SpO2)
- Heart rate
- Board temperature
- I2C interface

## 🔌 Hardware connection

### Sensor to Arduino (I2C mode)

| Sensor | Arduino |
|--------|---------|
| VCC | 5V / 3.3V |
| GND | GND |
| SDA | SDA / A4 |
| SCL | SCL / A5 |

### Sensor to a USB-to-TTL adapter (serial mode)

| Sensor | USB-to-TTL |
|--------|------------|
| VCC | **5V** (not 3.3V) |
| GND | GND |
| TX | RX (crossed) |
| RX | TX (crossed) |

TX and RX must be crossed.

## 🚀 Quick start

**Arduino** — copy `JUXI_HeartRate_SPO2/` into your Arduino `libraries` folder, restart the IDE, then open `examples/gainHeartbeatSPO2/gainHeartbeatSPO2.ino`. See the [library README](JUXI_HeartRate_SPO2/README.md).

**Raspberry Pi / Windows** — see the platform tutorials linked above.

**Desktop GUI tool** — run `HeartRateOximeter/dist/HeartRateOximeter/HeartRateOximeter.exe` on Windows, or run the Python source directly. See the [GUI user guide](HeartRateOximeter/README.md).

## 📐 Typical readings

| Reading | Normal range | Note |
|---------|--------------|------|
| SpO2 | 95 % – 100 % | Below 90 % warrants medical attention |
| Heart rate | 60 – 100 bpm | Adult resting range |
| Temperature | 25 – 35 °C | On-board sensor temperature, not body temperature |

Values of `-1` right after start-up, or when a finger is not properly placed, are normal.

## 📄 License

The MAX30102 driver and sample code are provided as-is for use with this module.

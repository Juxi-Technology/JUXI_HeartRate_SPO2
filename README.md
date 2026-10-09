English | [简体中文](README_CN.md)

# Heart Rate & Blood Oxygen Sensor Module

A **MAX30102**-based pulse oximetry and heart-rate module. It measures blood oxygen saturation (SpO2), heart rate and board temperature over I2C.

This repository collects the Arduino library, the Python examples for Raspberry Pi and Windows, and the desktop GUI tool — The tutorials under `docs/` are available in 11 languages.

## 📦 Repository layout

| Path | Contents |
|------|----------|
| `docs/<lang>/` | Tutorials — the same four guides in each language tree. Images are stored only under `docs/en/`; every other language links to them. |
| `docs/<lang>/01-arduino/` | Arduino tutorial |
| `docs/<lang>/02-raspberry-pi/` | Raspberry Pi tutorial |
| `docs/<lang>/03-windows/` | Windows tutorial |
| `docs/<lang>/04-gui-tool/` | Desktop GUI tool user guide |
| `JUXI_HeartRate_SPO2/` | The Arduino library (`src/`), a complete sketch (`examples/gainHeartbeatSPO2/`), and the Python examples |
| `HeartRateOximeter/` | Desktop GUI tool — source and a pre-built Windows bundle (`dist/`) |

The tutorials are available in 11 languages — the same four guides in each folder:

| Language | Folder |
|----------|--------|
| English | [`docs/en/`](docs/en/) |
| Deutsch | [`docs/de/`](docs/de/) |
| Español | [`docs/es/`](docs/es/) |
| Français | [`docs/fr/`](docs/fr/) |
| Italiano | [`docs/it/`](docs/it/) |
| 日本語 | [`docs/ja/`](docs/ja/) |
| 한국어 | [`docs/ko/`](docs/ko/) |
| Português (BR) | [`docs/pt-br/`](docs/pt-br/) |
| Português (PT) | [`docs/pt-pt/`](docs/pt-pt/) |
| 简体中文 | [`docs/zh-hans/`](docs/zh-hans/) |
| 繁體中文 | [`docs/zh-hant/`](docs/zh-hant/) |


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

**Desktop GUI tool** — run `HeartRateOximeter/dist/HeartRateOximeter/HeartRateOximeter.exe` on Windows, or run the Python source directly. See the [GUI user guide](docs/en/04-gui-tool/README.md).

## 📐 Typical readings

| Reading | Normal range | Note |
|---------|--------------|------|
| SpO2 | 95 % – 100 % | Below 90 % warrants medical attention |
| Heart rate | 60 – 100 bpm | Adult resting range |
| Temperature | 25 – 35 °C | On-board sensor temperature, not body temperature |

Values of `-1` right after start-up, or when a finger is not properly placed, are normal.

## 📄 License

The MAX30102 driver and sample code are provided as-is for use with this module.

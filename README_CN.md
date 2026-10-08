[English](README.md) | 简体中文

# 心率血氧监测模块

基于 **MAX30102** 的心率血氧监测模块，可通过 I2C 测量血氧饱和度（SpO2）、心率和板载温度。

本仓库汇集了 Arduino 库、树莓派与 Windows 的 Python 例程，以及桌面图形化上位机工具——文档均提供中英双语版本。

## 📦 仓库结构

| 路径 | 内容 |
|------|------|
| `JUXI_HeartRate_SPO2/` | Arduino 库（`src/`）、完整示例（`examples/gainHeartbeatSPO2/`）、Arduino 教程，以及 Python 例程 |
| `JUXI_HeartRate_SPO2/HeartRateOximeter/` | 桌面图形化上位机——源码与使用说明 |
| `HeartRateOximeter/` | 同一个上位机工具，另外附带打包好的 Windows 版本（`dist/`） |
| `JUXI_HeartRate_SPO2/python/raspberry/` | 树莓派教程——[English](JUXI_HeartRate_SPO2/python/raspberry/README.md) · [简体中文](JUXI_HeartRate_SPO2/python/raspberry/README_CN.md) |
| `JUXI_HeartRate_SPO2/python/windows/` | Windows 教程——[English](JUXI_HeartRate_SPO2/python/windows/README.md) · [简体中文](JUXI_HeartRate_SPO2/python/windows/README_CN.md) |

每份文档都有中英两个版本并互相跳转——`*.md` 是英文，`*_CN.md` 是简体中文。

## ✨ 功能特性

- 血氧饱和度（SpO2）
- 心率
- 板载温度
- I2C 通讯

## 🔌 硬件连接

### 传感器接 Arduino（I2C 模式）

| 传感器 | Arduino |
|--------|---------|
| VCC | 5V / 3.3V |
| GND | GND |
| SDA | SDA / A4 |
| SCL | SCL / A5 |

### 传感器接 USB 转 TTL（串口模式）

| 传感器 | USB 转 TTL |
|--------|------------|
| VCC | **5V**（不要接 3.3V） |
| GND | GND |
| TX | RX（交叉） |
| RX | TX（交叉） |

**TX 与 RX 必须交叉连接。**

## 🚀 快速开始

**Arduino** —— 把 `JUXI_HeartRate_SPO2/` 复制到 Arduino 的 `libraries` 目录，重启 IDE，然后打开 `examples/gainHeartbeatSPO2/gainHeartbeatSPO2.ino`。详见[库说明](JUXI_HeartRate_SPO2/README_CN.md)。

**树莓派 / Windows** —— 见上表对应的平台教程。

**桌面上位机** —— 在 Windows 上运行 `HeartRateOximeter/dist/HeartRateOximeter/HeartRateOximeter.exe`，或直接运行 Python 源码。详见[上位机使用说明](HeartRateOximeter/README_CN.md)。

## 📐 数据参考范围

| 数据 | 正常范围 | 说明 |
|------|----------|------|
| 血氧 SpO2 | 95% – 100% | 低于 90% 建议就医 |
| 心率 | 60 – 100 bpm | 成人静息范围 |
| 温度 | 25 – 35 °C | 板载传感器温度，非体温 |

刚启动或手指未放好时显示 `-1` 属于正常现象。

## 📄 许可

MAX30102 驱动与示例代码按现状提供，供配合本模块使用。

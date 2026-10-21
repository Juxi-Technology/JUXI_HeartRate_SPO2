[English](README.md) | 简体中文

# 心率血氧监测模块

基于 **MAX30102** 的心率血氧监测模块，可通过 I2C 测量血氧饱和度（SpO2）、心率和板载温度。

本仓库汇集了 Arduino 库、树莓派与 Windows 的 Python 例程、桌面图形化上位机，以及它的网页版——`docs/` 下的教程提供 11 种语言版本。

## 📦 仓库结构

| 路径 | 内容 |
|------|------|
| `docs/<语言>/` | 教程——各语言目录内容一致。**图片只存放在 `docs/en/` 下**，其他语言引用它们。 |
| `docs/<语言>/01-arduino/` | Arduino 教程 |
| `docs/<语言>/02-raspberry-pi/` | 树莓派教程 |
| `docs/<语言>/03-windows/` | Windows 教程 |
| `docs/<语言>/04-gui-tool/` | 上位机使用说明 |
| `docs/index.html`、`docs/assets/` | 网页版上位机与教程阅读页，发布在 GitHub Pages 上 |
| `JUXI_HeartRate_SPO2/` | Arduino 库（`src/`）、完整示例（`examples/gainHeartbeatSPO2/`），以及 Python 例程 |
| `HeartRateOximeter/` | 桌面图形化上位机——源码，另外附带打包好的 Windows 版本（`dist/`） |

教程提供 11 种语言版本，各语言目录内容一致：

| 语言 | 目录 |
|------|------|
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

**桌面上位机** —— 在 Windows 上运行 `HeartRateOximeter/dist/HeartRateOximeter.exe`，或直接运行 Python 源码。详见[上位机使用说明](docs/zh-hans/04-gui-tool/README.md)。

**网页版** —— 打开下一节的链接即可，无需安装。

## 🌐 网页版（免安装）

同一套上位机界面也能直接在浏览器里跑，通过 Web Serial API 和模块通信——不需要 Python 和 `.exe`，Windows、macOS、Linux 都能用。

**https://juxi-technology.github.io/JUXI_HeartRate_SPO2/**

1. 用 USB 转 TTL 接好模块并插上电脑（CH340、CP2102、FT232 等驱动需先安装）。
2. 用**桌面版 Chrome、Edge 或 Opera** 打开链接。Safari 和 Firefox 没有实现 Web Serial，打不开串口。
3. 点「连接串口」，在浏览器自带的弹窗里选择 USB 串口设备。
4. 点「启动采集」（模块 LED 点亮），再点「开始监测」。

它和桌面上位机走同一套 Modbus RTU 协议（地址 `0x20`、9600 波特率），读数完全一致。「使用文档」页签里就是同样的 11 语言教程。两个限制：页面每次都要联网加载；浏览器一次只授权给页面一个串口设备。

## 📐 数据参考范围

| 数据 | 正常范围 | 说明 |
|------|----------|------|
| 血氧 SpO2 | 95% – 100% | 低于 90% 建议就医 |
| 心率 | 60 – 100 bpm | 成人静息范围 |
| 温度 | 25 – 35 °C | 板载传感器温度，非体温 |

刚启动或手指未放好时显示 `-1` 属于正常现象。

## 📄 许可

MAX30102 驱动与示例代码按现状提供，供配合本模块使用。

[English](../../en/03-windows/README.md) | [Deutsch](../../de/03-windows/README.md) | [Español](../../es/03-windows/README.md) | [Français](../../fr/03-windows/README.md) | [Italiano](../../it/03-windows/README.md) | [日本語](../../ja/03-windows/README.md) | [한국어](../../ko/03-windows/README.md) | [Português (BR)](../../pt-br/03-windows/README.md) | [Português (PT)](../../pt-pt/03-windows/README.md) | [简体中文](../../zh-hans/03-windows/README.md) | 繁體中文

# JUXI 心率血氧感測器 - Windows 使用指南

## 目錄
1. [硬體準備](#硬體準備)
2. [硬體連接](#硬體連接)
3. [軟體環境設定](#軟體環境設定)
4. [執行範例程式](#執行範例程式)
5. [常見問題](#常見問題)

---

## 硬體準備

### 所需材料
| 材料 | 說明 |
|------|------|
| JUXI_HeartRate_SPO2 感測器 | 心率血氧模組 |
| USB轉TTL模組 | CH340 / CP2102 / FT232 等 |
| 杜邦線 | 4根（母對母） |
| Windows 電腦 | Win7/Win10/Win11 |

---

## 硬體連接

### 接線方式

| 感測器接腳 | USB轉TTL接腳 | 說明 |
|-----------|-------------|------|
| **VCC** | 3.3V 或 5V | 電源正極 |
| **GND** | GND | 電源負極 |
| **TX** | RX | 感測器傳送 → 模組接收 |
| **RX** | TX | 感測器接收 → 模組傳送 |

![Connect PC](../../en/03-windows/Connect%20PC.png)

⚠️ **重要提示**：

1. **模組撥片撥動到UART！！！**
2. **TX 和 RX 必須交叉連接！**
3. 感測器支援 3.3V 和 5V，不要接錯電壓
4. 先接好所有線，再插入USB到電腦

### 接線示意圖
```
传感器        USB转TTL模块
┌──────┐      ┌──────────┐
│ VCC  │──────│ 3.3V/5V  │
│ GND  │──────│ GND      │
│ TX   │──────│ RX       │  ← 交叉连接
│ RX   │──────│ TX       │  ← 交叉连接
└──────┘      └──────────┘
```

---

## 軟體環境設定

### 1. 安裝驅動程式

根據你的USB轉TTL晶片型號，安裝對應的驅動程式：

- **CH340**: https://sparks.gogo.co.nz/ch340.html
- **CP2102**: https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers
- **FT232**: https://ftdichip.com/drivers/vcp-drivers/

安裝完成後，插入USB轉TTL模組。

### 2. 查看COM埠

#### 方法一：裝置管理員
1. 按 `Win + X`，選擇"裝置管理員"
2. 展開"埠 (COM 和 LPT)"
3. 查看你的USB轉TTL對應的COM埠號（如 COM3）

#### 方法二：程式自動偵測
執行範例程式時，會自動列出所有可用的序列埠。

### 3. 安裝Python相依套件

開啟命令提示字元（CMD）或PowerShell，執行：

```bash
pip install pyserial
```

---

## 執行範例程式

### 檔案位置
```
JUXI_HeartRate_SPO2/python/windows/
├── gain_heartbeat_SPO2.py  ← 主程序（直接运行这个）
├── JUXI_HeartRate_SPO2_Windows.py
├── JUXI_RTU_Windows.py
└── README_Windows.md        ← 本文件
```

### 執行步驟

1. **確認硬體連接正確**
   - VCC → 3.3V/5V
   - GND → GND
   - TX → RX（交叉）
   - RX → TX（交叉）

2. **插入USB到電腦**

3. **執行程式**
   ```bash
   cd D:\JUXI_HeartRate_SPO2\python\windows
   python gain_heartbeat_SPO2.py
   ```

4. **依照提示操作**
   
   - 程式會列出所有可用的序列埠
   - 輸入你的COM埠號（如 COM3）
   - 程式自動偵測感測器並開始測量

### 預期輸出

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
SPO2 (血氧): 97 %
Heart Rate (心率): 82 BPM
Temperature (温度): 26.5 °C
----------------------------------------
SPO2 (血氧): 98 %
Heart Rate (心率): 78 BPM
Temperature (温度): 26.6 °C
...
```

按 `Ctrl + C` 停止程式。

---

## 程式功能說明

### 主要API

```python
# 创建传感器对象
sensor = BloodOxygenSensor("COM3", 9600)

# 初始化传感器
sensor.begin()

# 开始采集（LED亮起）
sensor.sensor_start_collect()

# 读取心率血氧
sensor.get_heartbeat_SPO2()
print(f"SPO2: {sensor.SPO2}%")
print(f"Heart Rate: {sensor.heartbeat} BPM")

# 读取温度
temp = sensor.get_temperature_c()

# 停止采集（LED熄灭）
sensor.sensor_end_collect()

# 关闭串口
sensor.close()
```

---

## 常見問題

### Q1: 找不到COM埠怎麼辦？

**A:**

1. 檢查USB轉TTL是否插好
2. 重新安裝驅動程式
3. 換一個USB埠試試
4. 在裝置管理員中查看是否有"未知裝置"

### Q2: 感測器初始化失敗怎麼辦？

**A:**

1. 檢查接線：
   - VCC 和 GND 是否接對
   - **TX 和 RX 是否交叉連接**（最常見問題）
2. 確認鮑率是 9600
3. 檢查USB轉TTL模組是否正常運作
4. 重新插拔USB

### Q3: 資料一直顯示 -1 怎麼辦？

**A:**
1. 確認手指正確放在感測器上（完全覆蓋LED區域）
2. 保持手指穩定，不要移動
3. 等待幾秒鐘讓資料穩定
4. 檢查感測器LED是否亮起

### Q4: LED燈不亮但通訊正常？

**A:**

- 可能是LED燈硬體問題，但感測器功能正常
- 只要資料正常，可以忽略LED不亮的問題

### Q5: 序列埠被佔用怎麼辦？

**A:**
1. 關閉其他序列埠軟體（序列埠助手、Arduino IDE等）
2. 檢查是否有其他Python程式正在執行
3. 重新插拔USB

### Q6: 資料不準確怎麼辦？

**A:**
1. 確保手指完全覆蓋感測器光學區域
2. 測量時保持安靜，不要說話或移動
3. 等待30秒以上讓資料穩定
4. 多次測量取平均值

---

## 技術規格

| 參數 | 規格 |
|-----|------|
| 通訊方式 | UART (TTL電平) |
| 鮑率 | 9600 bps（預設） |
| 資料格式 | 8N1 (8資料位, 無校驗, 1停止位) |
| 供電電壓 | 3.3V / 5V |
| SPO2測量範圍 | 35% - 100% |
| 心率測量範圍 | 30 - 250 BPM |
| Modbus設備位址 | 0x20 |

---

## Modbus 暫存器說明

| 暫存器位址 | 功能 | 說明 |
|-----------|------|------|
| 0x02 | 設備ID | 讀：傳回 0x0020 |
| 0x06-0x09 | 心率血氧資料 | 讀：SPO2 + 心率 |
| 0x0A | 溫度 | 讀：板載溫度 |
| 0x10 | 採集控制 | 寫：0x0001=開始, 0x0002=停止 |

---

## 聯絡我們

如有問題或建議，請造訪：
- GitHub: https://github.com/Juxi-Technology/JUXI_HeartRate_SPO2

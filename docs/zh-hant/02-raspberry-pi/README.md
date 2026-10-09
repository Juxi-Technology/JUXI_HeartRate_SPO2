[English](../../en/02-raspberry-pi/README.md) | [Deutsch](../../de/02-raspberry-pi/README.md) | [Español](../../es/02-raspberry-pi/README.md) | [Français](../../fr/02-raspberry-pi/README.md) | [Italiano](../../it/02-raspberry-pi/README.md) | [日本語](../../ja/02-raspberry-pi/README.md) | [한국어](../../ko/02-raspberry-pi/README.md) | [Português (BR)](../../pt-br/02-raspberry-pi/README.md) | [Português (PT)](../../pt-pt/02-raspberry-pi/README.md) | [简体中文](../../zh-hans/02-raspberry-pi/README.md) | 繁體中文

# JUXI_HeartRate_SPO2 树莓派使用教學


## 目錄

1. [專案簡介](#專案簡介)
2. [硬體準備](#硬體準備)
3. [硬體連接](#硬體連接)
4. [環境設定](#環境設定)
5. [範例程式碼使用](#範例程式碼使用)
6. [API 參考](#api-參考)
7. [常見問題](#常見問題)
8. [注意事項](#注意事項)

---

## 專案簡介

JUXI_HeartRate_SPO2 是一款基於 MAX30102 晶片的心率血氧感測器模組，內建演算法可直接輸出心率和血氧飽和度數值。

**主要功能：**
- 血氧飽和度（SPO2）測量
- 心率測量（次/分鐘）
- 板載溫度測量
- 支援 UART 和 I2C 兩種通訊方式

---

## 硬體準備

| 所需材料 | 說明 |
|---------|------|
| 树莓派（2/3/4/Zero 均可） | 推薦使用树莓派 3B+ 或 4B |
| JUXI_HeartRate_SPO2 感測器 | 心率血氧感測器模組 |
| 杜邦線若干 | 母對母杜邦線 4 根 |
| 電源適配器 | 树莓派專用電源 |

---

## 硬體連接

### 方式一：I2C 通訊（推薦）

I2C 通訊接線簡單，推薦使用。

| 感測器接腳 | 树莓派物理接腳 | BCM 編號 | 說明 |
|-----------|---------------|---------|------|
| VCC | 1 或 17 | - | 3.3V 電源（也可接 5V） |
| GND | 6 或 9 或 14 | - | 接地 |
| SDA | 3 | GPIO2 | I2C 資料線 |
| SCL | 5 | GPIO3 | I2C 時脈線 |

**重要：** 將感測器上的撥片撥動到 **IIC** 位置！

### 方式二：UART 序列埠通訊

UART 通訊需要交叉連接。

| 感測器接腳 | 树莓派物理接腳 | BCM 編號 | 說明 |
|-----------|---------------|---------|------|
| VCC | 2 或 4 | - | 5V 電源（也可接 3.3V） |
| GND | 6 或 9 或 14 | - | 接地 |
| RX | 8 | GPIO14 | 感測器 RX 接树莓派 TX |
| TX | 10 | GPIO15 | 感測器 TX 接树莓派 RX |

**重要：** 將感測器上的撥片撥動到 **UART** 位置！

![Raspberry Pi Pin Diagram](../../en/02-raspberry-pi/Raspberry%20Pi%20Pin%20Diagram.png)

---

## 環境設定

### 1. 啟用 I2C（I2C 模式需要）

```bash
sudo raspi-config
```

選擇 `Interface Options` → `I2C` → 選擇 `Yes` 啟用

重新啟動树莓派：
```bash
sudo reboot
```

### 2. 啟用序列埠（UART 模式需要）

```bash
sudo raspi-config
```

選擇 `Interface Options` → `Serial`

- 第一個問題："Would you like a login shell to be accessible over serial?" → 選擇 `No`
- 第二個問題："Would you like the serial port hardware to be enabled?" → 選擇 `Yes`

重新啟動树莓派：
```bash
sudo reboot
```

### 3. 安裝相依函式庫

```bash
# 更新软件源
sudo apt-get update

# 安装 I2C 工具和 smbus2 库（I2C 模式必须使用 smbus2）
sudo apt-get install -y i2c-tools python3-smbus2

# 安装 pyserial（串口支持）
sudo pip3 install pyserial
```

> **注意：** I2C 模式必須安裝 `smbus2`，不能使用舊版 `python-smbus`。
> 函式庫內部使用 `smbus2.i2c_msg` 實現獨立的兩步 I2C 交易（先寫暫存器位址並傳送 STOP，
> 再開啟新的讀交易連續讀取多位元組），以匹配感測器晶片的 I2C 時序要求。

### 4. 驗證 I2C 連接（I2C 模式）

接線完成後，執行以下命令檢測 I2C 設備：

```bash
i2cdetect -y 1
```

如果看到位址 `0x57`，表示感測器連接成功。

---

## 範例程式碼使用

### 檔案結構

```
python/raspberry/
├── JUXI_HeartRate_SPO2.py      # 主库文件
└── examples/
    ├── i2c_example.py          # I2C 模式示例
    └── uart_example.py         # UART 模式示例
```

### 執行 I2C 模式範例

```bash
cd python/raspberry/examples
sudo python3 i2c_example.py
```

### 執行 UART 模式範例

```bash
cd python/raspberry/examples
sudo python3 uart_example.py
```

**注意：** 使用硬體序列埠時需要 `sudo` 權限。

### 執行結果

如果一切正常，你會看到類似以下的輸出：

```
==================================================
JUXI 心率血氧传感器 - I2C 模式
==================================================

正在初始化 I2C 总线 1，地址 0x57...
传感器初始化成功！

开始数据采集...
传感器 LED 已亮起！

请将手指放在传感器上...

----------------------------------------
血氧饱和度: 98 %
心率: 72 次/分钟
板载温度: 25.5 ℃
----------------------------------------
...
```

按 `Ctrl+C` 停止程式。

---

## API 參考

### 類別：JUXI_HeartRate_SPO2_i2c

I2C 通訊方式的感測器類別。

#### 建構函式
```python
JUXI_HeartRate_SPO2_i2c(bus_number=1, i2c_address=0x57)
```

參數：
- `bus_number`: I2C 匯流排號，树莓派通常為 1
- `i2c_address`: 感測器 I2C 位址，預設 0x57

#### 方法

| 方法 | 說明 | 傳回值 |
|-----|------|--------|
| `begin()` | 初始化感測器，檢測連接 | bool (成功傳回 True) |
| `sensor_start_collect()` | 開始資料採集（感測器亮燈） | 無 |
| `sensor_end_collect()` | 停止資料採集（感測器關燈） | 無 |
| `get_heartbeat_SPO2()` | 讀取心率和血氧資料 | 無（結果儲存在物件屬性中） |
| `get_temperature_c()` | 讀取板載溫度 | float (攝氏度) |
| `close()` | 關閉 I2C 連接 | 無 |

#### 屬性

| 屬性 | 說明 |
|-----|------|
| `SPO2` | 血氧飽和度（%），無效值為 -1 |
| `heartbeat` | 心率（次/分鐘），無效值為 -1 |

---

### 類別：JUXI_HeartRate_SPO2_uart

UART 序列埠通訊方式的感測器類別。

#### 建構函式
```python
JUXI_HeartRate_SPO2_uart(port='/dev/serial0', baudrate=9600)
```

參數：
- `port`: 序列埠設備路徑，树莓派預設為 `/dev/serial0`
- `baudrate`: 鮑率，預設 9600

#### 方法

與 `JUXI_HeartRate_SPO2_i2c` 相同。

---

## 常見問題

### Q1: 感測器初始化失敗怎麼辦？

**A:** 請按以下步驟檢查：

1. **檢查接線**
   - I2C 模式：確認 SDA 接 GPIO2，SCL 接 GPIO3
   - UART 模式：確認 RX-TX 交叉連接

2. **檢查感測器撥片**
   - I2C 模式：撥片應在 IIC 位置
   - UART 模式：撥片應在 UART 位置

3. **檢查電源**
   - 確認 VCC 接 3.3V 或 5V
   - 確認 GND 已連接

4. **檢查系統設定**
   - I2C 模式：確認 I2C 已啟用
   - UART 模式：確認序列埠已啟用

5. **使用檢測命令**
   ```bash
   # I2C 模式
   i2cdetect -y 1
   
   # UART 模式
   ls /dev/serial*
   ```

### Q2: 資料一直顯示 -1 怎麼辦？

**A:**

1. 確認手指已正確放置在感測器上，完全覆蓋兩個 LED 燈
2. 等待幾秒鐘讓資料穩定（通常需要 10-30 秒）
3. 檢查是否已呼叫 `sensor_start_collect()` 開啟採集
4. 確認感測器指示燈是否亮起

### Q3: 資料不準確怎麼辦？

**A:**

1. 確保手指完全覆蓋感測器光學區域
2. 保持手指靜止，不要移動
3. 等待 30 秒以上讓資料穩定
4. 多次測量取平均值
5. 避免強光直射感測器

### Q4: I2C 和 UART 可以同時使用嗎？

**A:** 不可以，同一時間只能選擇一種通訊方式。

### Q5: 需要使用 sudo 執行嗎？

**A:**
- I2C 模式：建議使用 sudo，避免權限問題
- UART 模式：必須使用 sudo，否則無法存取序列埠

---

## 注意事項

### 測量技巧

1. **正確放置手指**
   - 將手指輕輕放在感測器上，覆蓋兩個 LED 燈
   - 不要用力按壓，以免影響血液循環
   - 保持手指穩定，不要移動

2. **等待資料穩定**
   - 剛開始測量時，數值可能不穩定
   - 建議等待 10-30 秒，待資料穩定後再讀取
   - 感測器每 4 秒更新一次資料

3. **環境要求**
   - 避免強光直射感測器
   - 保持環境溫度適宜
   - 測量時保持安靜

### 資料解讀

| SPO2 範圍 | 說明 |
|----------|------|
| 95% - 100% | 正常 |
| 90% - 94% | 輕度低氧 |
| < 90% | 低氧，建議就醫 |

| 心率範圍 | 說明 |
|---------|------|
| 60 - 100 次/分 | 成人正常範圍 |
| < 60 次/分 | 心動過緩 |
| > 100 次/分 | 心動過速 |

### 安全提示

- 本感測器僅供參考，不能替代專業醫療設備
- 如有健康問題，請及時就醫
- 測量結果僅作參考，不做診斷依據

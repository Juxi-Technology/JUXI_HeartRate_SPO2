[English](../../en/03-windows/README.md) | [Deutsch](../../de/03-windows/README.md) | [Español](../../es/03-windows/README.md) | [Français](../../fr/03-windows/README.md) | [Italiano](../../it/03-windows/README.md) | 日本語 | [한국어](../../ko/03-windows/README.md) | [Português (BR)](../../pt-br/03-windows/README.md) | [Português (PT)](../../pt-pt/03-windows/README.md) | [简体中文](../../zh-hans/03-windows/README.md) | [繁體中文](../../zh-hant/03-windows/README.md)

# JUXI 心拍血中酸素センサー - Windows ユーザーガイド

## 目次
1. [ハードウェアの準備](#ハードウェアの準備)
2. [ハードウェア接続](#ハードウェア接続)
3. [ソフトウェア環境のセットアップ](#ソフトウェア環境のセットアップ)
4. [サンプルプログラムの実行](#サンプルプログラムの実行)
5. [FAQ](#faq)

---

## ハードウェアの準備

### 必要なもの

| 項目 | 説明 |
|------|-------------|
| JUXI_HeartRate_SPO2 センサー | 心拍血中酸素モジュール |
| USB-TTL モジュール | CH340 / CP2102 / FT232 など |
| ジャンパーワイヤー | 4 本（メス-メス） |
| Windows パソコン | Win7/Win10/Win11 |

---

## ハードウェア接続

### 配線方法

| センサー側ピン | USB-TTL 側ピン | 説明 |
|-----------|---------------|-------------|
| **VCC** | 3.3V または 5V | 電源プラス |
| **GND** | GND | 電源マイナス |
| **TX** | RX | センサーの送信 → モジュールの受信 |
| **RX** | TX | センサーの受信 → モジュールの送信 |

![Connect PC](../../en/03-windows/Connect%20PC.png)

⚠️ **重要なヒント**：

1. **モジュールのディップスイッチを UART の位置に切り替えてください！！！**
2. **TX と RX は必ずクロス接続してください！**
3. センサーは 3.3V と 5V の両方に対応しています。誤った電圧を接続しないでください
4. 先にすべての配線を行い、その後で USB をパソコンに接続してください

### 配線図

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

## ソフトウェア環境のセットアップ

### 1. ドライバーのインストール

お使いの USB-TTL チップの型番に応じて、対応するドライバーをインストールしてください：

- **CH340**: https://sparks.gogo.co.nz/ch340.html
- **CP2102**: https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers
- **FT232**: https://ftdichip.com/drivers/vcp-drivers/

インストール後、USB-TTL モジュールを接続してください。

### 2. COM ポートの確認

#### 方法 1：デバイスマネージャー
1. `Win + X` を押し、「デバイスマネージャー」を選択します
2. 「ポート (COM と LPT)」を展開します
3. USB-TTL に対応する COM ポート番号を確認します（例：COM3）

#### 方法 2：プログラムによる自動検出
サンプルプログラムを実行すると、使用可能なすべてのシリアルポートが自動的に一覧表示されます。

### 3. Python 依存関係のインストール

コマンドプロンプト（CMD）または PowerShell を開き、次を実行します：

```bash
pip install pyserial
```

---

## サンプルプログラムの実行

### ファイルの場所

```
JUXI_HeartRate_SPO2/python/windows/
├── gain_heartbeat_SPO2.py  ← Main program (run this)
├── JUXI_HeartRate_SPO2_Windows.py
├── JUXI_RTU_Windows.py
└── README.md                ← This file
```

### 実行手順

1. **ハードウェア接続が正しいことを確認する**
   - VCC → 3.3V/5V
   - GND → GND
   - TX → RX（クロス）
   - RX → TX（クロス）

2. **USB をパソコンに接続する**

3. **プログラムを実行する**
   ```bash
   cd D:\JUXI_HeartRate_SPO2\python\windows
   python gain_heartbeat_SPO2.py
   ```

4. **画面の指示に従う**
   
   - プログラムが使用可能なすべてのシリアルポートを一覧表示します
   - COM ポート番号を入力します（例：COM3）
   - プログラムがセンサーを自動検出し、測定を開始します

### 期待される出力

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

`Ctrl + C` を押すとプログラムを停止します。

---

## プログラムの機能説明

### 主要 API

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

### Q1: COM ポートが見つかりませんか？

**A:**

1. USB-TTL が正しく接続されているか確認してください
2. ドライバーを再インストールしてください
3. 別の USB ポートを試してください
4. デバイスマネージャーで「不明なデバイス」がないか確認してください

### Q2: センサーの初期化に失敗しますか？

**A:**

1. 配線を確認してください：
   - VCC と GND が正しく接続されているか
   - **TX と RX がクロス接続されていますか？**（最もよくある問題です）
2. ボーレートが 9600 であることを確認してください
3. USB-TTL モジュールが正常に動作しているか確認してください
4. USB を再接続してください

### Q3: データが常に -1 と表示されますか？

**A:**
1. 指がセンサーに正しく置かれていることを確認してください（LED 領域を完全に覆う）
2. 指を動かさず、安定させてください
3. データが安定するまで数秒待ちます
4. センサーの LED が点灯しているか確認してください

### Q4: LED は点灯していませんが、通信は機能していますか？

**A:**

- LED のハードウェア的な問題の可能性がありますが、センサーは正常に機能しています
- データが正常であれば、LED が点灯しないことは無視できます

### Q5: シリアルポートが使用中ですか？

**A:**
1. 他のシリアルソフトウェアを閉じてください（シリアルアシスタント、Arduino IDE など）
2. 他の Python プログラムが実行されていないか確認してください
3. USB を再接続してください

### Q6: データが正確ではありませんか？

**A:**
1. 指がセンサーの光学領域を完全に覆っていることを確認してください
2. 測定中は静かにし、話したり動いたりしないでください
3. データが安定するまで 30 秒以上待ちます
4. 複数回測定して平均を取ります

---

## 技術仕様

| パラメーター | 仕様 |
|-----------|--------------|
| 通信 | UART（TTL レベル） |
| ボーレート | 9600 bps（デフォルト） |
| データ形式 | 8N1（データビット 8、パリティなし、ストップビット 1） |
| 電源 | 3.3V / 5V |
| SPO2 範囲 | 35% - 100% |
| 心拍数範囲 | 30 - 250 BPM |
| Modbus アドレス | 0x20 |

---

## Modbus レジスタの説明

| レジスタアドレス | 機能 | 説明 |
|-----------------|----------|-------------|
| 0x02 | デバイス ID | 読み取り：0x0020 を返します |
| 0x06-0x09 | 心拍数 & SPO2 データ | 読み取り：SPO2 + 心拍数 |
| 0x0A | 温度 | 読み取り：基板温度 |
| 0x10 | 収集制御 | 書き込み：0x0001=開始、0x0002=停止 |

---

## お問い合わせ

ご質問やご提案がある場合は、次をご覧ください：
- GitHub: https://github.com/Juxi-Technology/JUXI_HeartRate_SPO2

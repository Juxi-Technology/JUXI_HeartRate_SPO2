[English](../../en/01-arduino/README.md) | [Deutsch](../../de/01-arduino/README.md) | [Español](../../es/01-arduino/README.md) | [Français](../../fr/01-arduino/README.md) | [Italiano](../../it/01-arduino/README.md) | 日本語 | [한국어](../../ko/01-arduino/README.md) | [Português (BR)](../../pt-br/01-arduino/README.md) | [Português (PT)](../../pt-pt/01-arduino/README.md) | [简体中文](../../zh-hans/01-arduino/README.md) | [繁體中文](../../zh-hant/01-arduino/README.md)

# JUXI_HeartRate_SPO2 心拍・血中酸素センサー使用チュートリアル

## 目次
1. [センサー紹介](#センサー紹介)
2. [Arduino チュートリアル](#arduino-チュートリアル)
3. [Python (Raspberry Pi) チュートリアル](#python-raspberry-pi-チュートリアル)
4. [FAQ](#faq)

---

## センサー紹介

JUXI_HeartRate_SPO2 は、MAX30102 チップを採用した心拍・血中酸素センサーモジュールです。内蔵アルゴリズムにより、心拍数と血中酸素飽和度の値を直接出力できます。

**主な機能：**

- 血中酸素飽和度（SPO2）の測定
- 心拍数の測定（1 分あたりの拍数）
- 基板温度の測定
- I2C 通信に対応

---

## Arduino チュートリアル

### 1. ハードウェアの準備

| 必要なもの |
|-------------------|
| Arduino 開発ボード（Uno/Nano/ESP32 など） |
| JUXI_HeartRate_SPO2 センサー |
| ジャンパーワイヤー（数本） |
| USB データケーブル（Arduino をパソコンに接続） |

### 2. ライブラリのインストール

1. このライブラリファイルをダウンロードします
2. `JUXI_HeartRate_SPO2` フォルダーを Arduino のライブラリフォルダーにコピーします：
   - Windows: `C:\Users\Username\Documents\Arduino\libraries\`
   - Mac: `~/Documents/Arduino/libraries/`
   - Linux: `~/Arduino/libraries/`
3. Arduino IDE を再起動します

### 3. サンプルコード

**注意：コードを書き込む際は、Arduino のみをパソコンに接続し、心拍血中酸素モジュールを Arduino に接続しないでください！！！**

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

##### ハードウェア接続

I2C 通信

| センサー側ピン | Arduino |
|-----------|---------|
| VCC       | 5V/3.3V |
| GND       | GND     |
| SDA       | SDA/A4  |
| SCL       | SCL/A5  |

![IIC](../../en/01-arduino/img/IIC.png)

![8](../../en/01-arduino/img/8.png)

- 心拍血中酸素モジュールのディップスイッチを I2C の位置に切り替えてください！！！
- データケーブルで Arduino をパソコンに接続します

#### 実行結果：

1. Arduino を開く - ツール - シリアルモニタ

   ボーレートを 9600 に設定

![1](../../en/01-arduino/img/1.png)

2. シリアルデバッグアシスタントを開く

[Serial Debug Assistant uartassist5.15.zip](https://juxitech.feishu.cn/wiki/BJlfwSQydi7u5lkRDQ6cV4dvnBd)

シリアルポート番号を選択

ボーレートを `9600` に設定

データビット `8`、ストップビット `1`、パリティ `NONE`、フロー制御 `NONE`

受信設定と送信設定は `ASCII` を選択

![2](../../en/01-arduino/img/2.png)

### 4. API の説明

| 関数 | 説明 |
|----------|-------------|
| `begin()` | センサーを初期化し、true/false を返します |
| `getHeartbeatSPO2()` | 心拍と SPO2 のデータを読み取り、`_sHeartbeatSPO2` 構造体に格納します |
| `getTemperature_C()` | 基板温度を読み取ります（摂氏） |
| `sensorStartCollect()` | データ収集を開始します（センサー LED が点灯） |
| `sensorEndCollect()` | データ収集を停止します（センサー LED が消灯） |

### 5. データの説明

- **SPO2（血中酸素飽和度）**：正常範囲は 95% - 100%、値 -1 は無効を示します
- **Heartbeat（心拍数）**：正常範囲は 60 - 100 BPM、値 -1 は無効を示します
- **無効値の原因**：指が正しく置かれていない、またはデータが安定していない

---

## 使用上の注意

### 測定のコツ

1. **指を正しく置く**
   - 指をセンサーにそっと置き、2 つの LED を覆います
   - 血行に影響を与えないよう、強く押さえないでください
   - 指を動かさず、安定させてください

2. **データが安定するまで待つ**
   - 測定を始めた直後は値が不安定になることがあります
   - データが安定するまで 10～30 秒待ってから読み取ることをおすすめします
   - センサーは 4 秒ごとにデータを更新します

3. **環境の条件**
   - センサーへの強い直射光を避けてください
   - 周囲の温度を適切に保ってください
   - 測定中は静かにしてください

### データの見方

| SPO2 範囲 | 説明 |
|-----------|-------------|
| 95% - 100% | 正常 |
| 90% - 94% | 軽度の低酸素 |
| < 90% | 低酸素、受診をおすすめします |

| 心拍数範囲 | 説明 |
|-----------------|-------------|
| 60 - 100 BPM | 成人の正常範囲 |
| < 60 BPM | 徐脈 |
| > 100 BPM | 頻脈 |

---

## FAQ

### Q1: センサーの初期化に失敗しますか？

**A:**
1. 配線が正しいか確認してください（SDA は GPIO2/A4、SCL は GPIO3/A5）
2. 電源が正常か確認してください（3.3V または 5V）
3. `i2cdetect -y 1` コマンドでデバイスを検出します
4. センサーのディップスイッチが IIC の位置にあることを確認してください

### Q2: データが常に -1 と表示されますか？

**A:**
1. 指がセンサーに正しく置かれていることを確認してください
2. データが安定するまで数秒待ちます
3. `sensorStartCollect()` を呼び出して収集を開始したか確認してください
4. センサーのインジケーターランプが点灯していることを確認してください

### Q3: データが正確ではありませんか？

**A:**
1. 指がセンサーの光学領域を完全に覆っていることを確認してください
2. 指を動かさず、静止させてください
3. データが安定するまで 30 秒以上待ちます
4. 複数回測定して平均を取ります

### Q4: 対応している Arduino 開発ボードはどれですか？

**A:** 対応：
- Arduino Uno/Nano/Mega
- ESP8266
- ESP32
- Arduino 環境に対応したその他の開発ボード

---

## サンプルファイルの場所

### Arduino サンプル
```
JUXI_HeartRate_SPO2/
└── examples/
    └── gainHeartbeatSPO2/
        └── gainHeartbeatSPO2.ino
```

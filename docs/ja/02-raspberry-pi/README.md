[English](../../en/02-raspberry-pi/README.md) | [Deutsch](../../de/02-raspberry-pi/README.md) | [Español](../../es/02-raspberry-pi/README.md) | [Français](../../fr/02-raspberry-pi/README.md) | [Italiano](../../it/02-raspberry-pi/README.md) | 日本語 | [한국어](../../ko/02-raspberry-pi/README.md) | [Português (BR)](../../pt-br/02-raspberry-pi/README.md) | [Português (PT)](../../pt-pt/02-raspberry-pi/README.md) | [简体中文](../../zh-hans/02-raspberry-pi/README.md) | [繁體中文](../../zh-hant/02-raspberry-pi/README.md)

# JUXI_HeartRate_SPO2 Raspberry Pi チュートリアル


## 目次

1. [はじめに](#はじめに)
2. [必要なハードウェア](#必要なハードウェア)
3. [ハードウェア接続](#ハードウェア接続)
4. [環境のセットアップ](#環境のセットアップ)
5. [サンプルコードの使い方](#サンプルコードの使い方)
6. [API リファレンス](#api-リファレンス)
7. [FAQ](#faq)
8. [重要な注意事項](#重要な注意事項)

---

## はじめに

JUXI_HeartRate_SPO2 は、MAX30102 チップを採用した心拍・血中酸素センサーモジュールです。内蔵アルゴリズムにより、心拍数と血中酸素飽和度の値を直接出力します。

**主な機能：**
- 血中酸素飽和度（SPO2）の測定
- 心拍数の測定（1 分あたりの拍数）
- 基板温度の測定
- UART と I2C の両方の通信に対応

---

## 必要なハードウェア

| 必要なもの | 説明 |
|--------------|-------------|
| Raspberry Pi (2/3/4/Zero) | Raspberry Pi 3B+ または 4B を推奨 |
| JUXI_HeartRate_SPO2 センサー | 心拍・血中酸素センサーモジュール |
| ジャンパーワイヤー | メス-メスのジャンパーワイヤー 4 本 |
| 電源アダプター | Raspberry Pi 用の電源 |

---

## ハードウェア接続

### 方法 1：I2C 通信（推奨）

I2C 通信は配線が簡単で、推奨されます。

| センサー側ピン | Raspberry Pi の物理ピン | BCM 番号 | 説明 |
|-----------|--------------------------|-----------|-------------|
| VCC | 1 または 17 | - | 3.3V 電源（5V でも可） |
| GND | 6 または 9 または 14 | - | グラウンド |
| SDA | 3 | GPIO2 | I2C データライン |
| SCL | 5 | GPIO3 | I2C クロックライン |

**重要：** センサーの切り替えスイッチを **IIC** の位置にしてください！

### 方法 2：UART シリアル通信

UART 通信にはクロス接続が必要です。

| センサー側ピン | Raspberry Pi の物理ピン | BCM 番号 | 説明 |
|-----------|--------------------------|-----------|-------------|
| VCC | 2 または 4 | - | 5V 電源（3.3V でも可） |
| GND | 6 または 9 または 14 | - | グラウンド |
| RX | 8 | GPIO14 | センサーの RX を Raspberry Pi の TX に接続 |
| TX | 10 | GPIO15 | センサーの TX を Raspberry Pi の RX に接続 |

**重要：** センサーの切り替えスイッチを **UART** の位置にしてください！

![树莓派针脚图](../../en/02-raspberry-pi/Raspberry%20Pi%20Pin%20Diagram.png)

---

## 環境のセットアップ

### 1. I2C を有効化（I2C モードで必要）

```bash
sudo raspi-config
```

`Interface Options` → `I2C` → `Yes` を選択して有効化します

Raspberry Pi を再起動します：
```bash
sudo reboot
```

### 2. シリアルポートを有効化（UART モードで必要）

```bash
sudo raspi-config
```

`Interface Options` → `Serial` を選択します

- 1 つ目の質問："Would you like a login shell to be accessible over serial?" → `No` を選択
- 2 つ目の質問："Would you like the serial port hardware to be enabled?" → `Yes` を選択

Raspberry Pi を再起動します：
```bash
sudo reboot
```

### 3. 依存関係のインストール

```bash
# Update package lists
sudo apt-get update

# Install I2C tools and smbus2 library (smbus2 is required for I2C mode)
sudo apt-get install -y i2c-tools python3-smbus2

# Install pyserial (for serial port support)
sudo pip3 install pyserial
```

> **注意：** I2C モードには `smbus2` が必要です。従来の `python-smbus` パッケージでは不十分です。
> このライブラリは `smbus2.i2c_msg` を使用して 2 つの独立した I2C トランザクションを実行します（STOP 付きで
> レジスタアドレスを書き込み、その後、新しい読み取りトランザクションで複数バイトを順次読み取る）。
> これはセンサーチップが要求する I2C タイミングに一致します。

### 4. I2C 接続の確認（I2C モード）

配線後、次のコマンドを実行して I2C デバイスを検出します：

```bash
i2cdetect -y 1
```

アドレス `0x57` が表示されれば、センサーは正常に接続されています。

---

## サンプルコードの使い方

### ファイル構成

```
python/raspberry/
├── JUXI_HeartRate_SPO2.py      # Main library file
└── examples/
    ├── i2c_example.py          # I2C mode example
    └── uart_example.py         # UART mode example
```

### I2C モードのサンプルを実行

```bash
cd python/raspberry/examples
sudo python3 i2c_example.py
```

### UART モードのサンプルを実行

```bash
cd python/raspberry/examples
sudo python3 uart_example.py
```

**注意：** ハードウェアシリアルポートにアクセスするには `sudo` 権限が必要です。

### 期待される出力

すべてが正常に動作すると、次のような出力が表示されます：

```
==================================================
JUXI Heart Rate & Blood Oxygen Sensor - I2C Mode
==================================================

Initializing I2C bus 1, address 0x57...
Sensor initialized successfully!

Starting data collection...
Sensor LED is now ON!

Please place your finger on the sensor...

----------------------------------------
SPO2: 98 %
Heart Rate: 72 Times/min
Onboard Temperature: 25.5 °C
----------------------------------------
...
```

`Ctrl+C` を押すとプログラムを停止します。

---

## API リファレンス

### クラス: JUXI_HeartRate_SPO2_i2c

I2C 通信用のセンサークラスです。

#### コンストラクター
```python
JUXI_HeartRate_SPO2_i2c(bus_number=1, i2c_address=0x57)
```

パラメーター：
- `bus_number`: I2C バス番号。Raspberry Pi では通常 1 です
- `i2c_address`: センサーの I2C アドレス。デフォルトは 0x57 です

#### メソッド

| メソッド | 説明 | 戻り値 |
|--------|-------------|--------------|
| `begin()` | センサーを初期化し、接続を確認します | bool（成功時は True） |
| `sensor_start_collect()` | データ収集を開始します（センサー LED 点灯） | None |
| `sensor_end_collect()` | データ収集を停止します（センサー LED 消灯） | None |
| `get_heartbeat_SPO2()` | 心拍と SPO2 のデータを読み取ります | None（結果はオブジェクトのプロパティに格納されます） |
| `get_temperature_c()` | 基板温度を読み取ります | float（摂氏） |
| `close()` | I2C 接続を閉じます | None |

#### プロパティ

| プロパティ | 説明 |
|----------|-------------|
| `SPO2` | 血中酸素飽和度（%）、無効値の場合は -1 |
| `heartbeat` | 心拍数（1 分あたりの拍数）、無効値の場合は -1 |

---

### クラス: JUXI_HeartRate_SPO2_uart

UART シリアル通信用のセンサークラスです。

#### コンストラクター
```python
JUXI_HeartRate_SPO2_uart(port='/dev/serial0', baudrate=9600)
```

パラメーター：
- `port`: シリアルデバイスのパス。Raspberry Pi ではデフォルトで `/dev/serial0` です
- `baudrate`: ボーレート。デフォルトは 9600 です

#### メソッド

`JUXI_HeartRate_SPO2_i2c` と同じです。

---

## FAQ

### Q1: センサーの初期化に失敗した場合はどうすればよいですか？

**A:** 次の手順に従ってください：

1. **配線を確認する**
   - I2C モード：SDA が GPIO2 に、SCL が GPIO3 に接続されているか確認します
   - UART モード：RX-TX がクロス接続されているか確認します

2. **センサーのスイッチを確認する**
   - I2C モード：スイッチが IIC の位置にある必要があります
   - UART モード：スイッチが UART の位置にある必要があります

3. **電源を確認する**
   - VCC が 3.3V または 5V に接続されているか確認します
   - GND が接続されているか確認します

4. **システム設定を確認する**
   - I2C モード：I2C が有効になっているか確認します
   - UART モード：シリアルポートが有効になっているか確認します

5. **検出コマンドを使用する**
   ```bash
   # I2C mode
   i2cdetect -y 1
   
   # UART mode
   ls /dev/serial*
   ```

### Q2: データが常に -1 と表示される場合はどうすればよいですか？

**A:**

1. 指がセンサーに正しく置かれ、2 つの LED を完全に覆っていることを確認してください
2. データが安定するまで数秒待ちます（通常 10～30 秒）
3. `sensor_start_collect()` を呼び出して収集を開始したか確認してください
4. センサーの LED が点灯していることを確認してください

### Q3: データが正確でない場合はどうすればよいですか？

**A:**

1. 指がセンサーの光学領域を完全に覆っていることを確認してください
2. 指を動かさず、静止させてください
3. データが安定するまで 30 秒以上待ちます
4. 複数回測定して平均を取ります
5. センサーへの強い直射光を避けてください

### Q4: I2C と UART を同時に使用できますか？

**A:** いいえ、同時に選択できる通信方式は 1 つだけです。

### Q5: 実行に sudo は必要ですか？

**A:**
- I2C モード：権限の問題を避けるため、sudo の使用を推奨します
- UART モード：sudo が必要です。そうしないとシリアルポートにアクセスできません

---

## 重要な注意事項

### 測定のコツ

1. **指を正しく置く**
   - 指をセンサーにそっと置き、2 つの LED を覆います
   - 血行に影響を与える可能性があるため、強く押さないでください
   - 指を動かさず、安定させてください

2. **データが安定するまで待つ**
   - 測定を始めた直後は値が不安定になることがあります
   - データが安定するまで 10～30 秒待つことをおすすめします
   - センサーは 4 秒ごとにデータを更新します

3. **環境の条件**
   - センサーへの強い直射光を避けてください
   - 適切な周囲温度を保ってください
   - 測定中は静かにしてください

### データの見方

| SPO2 範囲 | 説明 |
|-----------|-------------|
| 95% - 100% | 正常 |
| 90% - 94% | 軽度の低酸素 |
| < 90% | 低酸素、医師に相談してください |

| 心拍数範囲 | 説明 |
|-----------------|-------------|
| 60 - 100 BPM | 成人の正常範囲 |
| < 60 BPM | 徐脈 |
| > 100 BPM | 頻脈 |

### 安全に関する注意

- このセンサーは参考用であり、専門の医療機器の代わりにはなりません
- 健康上の懸念がある場合は、速やかに医師に相談してください
- 測定結果は参考用であり、診断に使用しないでください

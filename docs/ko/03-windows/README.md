[English](../../en/03-windows/README.md) | [Deutsch](../../de/03-windows/README.md) | [Español](../../es/03-windows/README.md) | [Français](../../fr/03-windows/README.md) | [Italiano](../../it/03-windows/README.md) | [日本語](../../ja/03-windows/README.md) | 한국어 | [Português (BR)](../../pt-br/03-windows/README.md) | [Português (PT)](../../pt-pt/03-windows/README.md) | [简体中文](../../zh-hans/03-windows/README.md) | [繁體中文](../../zh-hant/03-windows/README.md)

# JUXI 심박수·혈중산소 센서 - Windows 사용자 가이드

## 목차
1. [하드웨어 준비](#하드웨어-준비)
2. [하드웨어 연결](#하드웨어-연결)
3. [소프트웨어 환경 설정](#소프트웨어-환경-설정)
4. [예제 프로그램 실행](#예제-프로그램-실행)
5. [FAQ](#faq)

---

## 하드웨어 준비

### 준비물

| 항목 | 설명 |
|------|-------------|
| JUXI_HeartRate_SPO2 센서 | 심박수·혈중산소 모듈 |
| USB to TTL 모듈 | CH340 / CP2102 / FT232 등 |
| 점퍼 와이어 | 4개 (암-암) |
| Windows 컴퓨터 | Win7/Win10/Win11 |

---

## 하드웨어 연결

### 배선 방법

| 센서 핀 | USB to TTL 핀 | 설명 |
|-----------|---------------|-------------|
| **VCC** | 3.3V 또는 5V | 전원 양극 |
| **GND** | GND | 전원 음극 |
| **TX** | RX | 센서 송신 → 모듈 수신 |
| **RX** | TX | 센서 수신 → 모듈 송신 |

![Connect PC](../../en/03-windows/Connect%20PC.png)

⚠️ **중요 안내**:

1. **모듈의 DIP 스위치를 UART 위치로 전환하십시오!!!**
2. **TX와 RX는 반드시 교차 연결해야 합니다!**
3. 센서는 3.3V와 5V를 모두 지원하므로 전압을 잘못 연결하지 마십시오
4. 모든 배선을 먼저 연결한 다음 USB를 컴퓨터에 꽂습니다

### 배선도

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

## 소프트웨어 환경 설정

### 1. 드라이버 설치

USB to TTL 칩 모델에 따라 해당 드라이버를 설치합니다:

- **CH340**: https://sparks.gogo.co.nz/ch340.html
- **CP2102**: https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers
- **FT232**: https://ftdichip.com/drivers/vcp-drivers/

설치 후 USB to TTL 모듈을 꽂습니다.

### 2. COM 포트 확인

#### 방법 1: 장치 관리자
1. `Win + X`를 누르고 "장치 관리자"를 선택합니다
2. "포트(COM 및 LPT)"를 펼칩니다
3. USB to TTL에 해당하는 COM 포트 번호를 확인합니다(예: COM3)

#### 방법 2: 프로그램 자동 감지
예제 프로그램을 실행하면 사용 가능한 모든 시리얼 포트가 자동으로 나열됩니다.

### 3. Python 종속성 설치

명령 프롬프트(CMD) 또는 PowerShell을 열고 실행합니다:

```bash
pip install pyserial
```

---

## 예제 프로그램 실행

### 파일 위치

```
JUXI_HeartRate_SPO2/python/windows/
├── gain_heartbeat_SPO2.py  ← Main program (run this)
├── JUXI_HeartRate_SPO2_Windows.py
├── JUXI_RTU_Windows.py
└── README.md                ← This file
```

### 실행 단계

1. **하드웨어 연결이 올바른지 확인합니다**
   - VCC → 3.3V/5V
   - GND → GND
   - TX → RX (교차)
   - RX → TX (교차)

2. **USB를 컴퓨터에 꽂습니다**

3. **프로그램을 실행합니다**
   ```bash
   cd D:\JUXI_HeartRate_SPO2\python\windows
   python gain_heartbeat_SPO2.py
   ```

4. **안내에 따릅니다**
   
   - 프로그램이 사용 가능한 모든 시리얼 포트를 나열합니다
   - COM 포트 번호를 입력합니다(예: COM3)
   - 프로그램이 센서를 자동으로 감지하고 측정을 시작합니다

### 예상 출력

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

`Ctrl + C`를 눌러 프로그램을 중지합니다.

---

## 프로그램 기능 설명

### 주요 API

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

### Q1: COM 포트를 찾을 수 없나요?

**A:**

1. USB to TTL이 제대로 꽂혔는지 확인합니다
2. 드라이버를 다시 설치합니다
3. 다른 USB 포트를 시도합니다
4. 장치 관리자에서 "알 수 없는 장치"가 있는지 확인합니다

### Q2: 센서 초기화에 실패하나요?

**A:**

1. 배선을 확인합니다:
   - VCC와 GND가 올바르게 연결되었는지
   - **TX와 RX가 교차 연결되었는지?** (가장 흔한 문제)
2. 보드레이트가 9600인지 확인합니다
3. USB to TTL 모듈이 정상적으로 동작하는지 확인합니다
4. USB를 다시 꽂습니다

### Q3: 데이터가 항상 -1로 표시되나요?

**A:**
1. 손가락이 센서 위에 제대로 놓였는지 확인합니다(LED 영역을 완전히 덮음)
2. 손가락을 움직이지 않고 안정적으로 유지합니다
3. 데이터가 안정화될 때까지 몇 초 기다립니다
4. 센서 LED가 켜져 있는지 확인합니다

### Q4: LED는 켜지지 않지만 통신은 정상인가요?

**A:**

- LED에 하드웨어 문제가 있을 수 있지만 센서는 정상적으로 동작합니다
- 데이터가 정상이라면 LED가 켜지지 않는 것은 무시해도 됩니다

### Q5: 시리얼 포트가 점유되어 있나요?

**A:**
1. 다른 시리얼 소프트웨어를 닫습니다(시리얼 어시스턴트, Arduino IDE 등)
2. 다른 Python 프로그램이 실행 중인지 확인합니다
3. USB를 다시 꽂습니다

### Q6: 데이터가 부정확한가요?

**A:**
1. 손가락이 센서의 광학 영역을 완전히 덮는지 확인합니다
2. 측정 중에는 조용히 유지하고 말하거나 움직이지 않습니다
3. 데이터가 안정화될 때까지 30초 이상 기다립니다
4. 여러 번 측정하여 평균을 냅니다

---

## 기술 사양

| 매개변수 | 사양 |
|-----------|--------------|
| 통신 | UART (TTL 레벨) |
| 보드레이트 | 9600 bps (기본) |
| 데이터 형식 | 8N1 (데이터 비트 8, 패리티 없음, 정지 비트 1) |
| 전원 | 3.3V / 5V |
| SPO2 범위 | 35% - 100% |
| 심박수 범위 | 30 - 250 BPM |
| Modbus 주소 | 0x20 |

---

## Modbus 레지스터 설명

| 레지스터 주소 | 기능 | 설명 |
|-----------------|----------|-------------|
| 0x02 | 장치 ID | 읽기: 0x0020 반환 |
| 0x06-0x09 | 심박수 및 SPO2 데이터 | 읽기: SPO2 + 심박수 |
| 0x0A | 온도 | 읽기: 온보드 온도 |
| 0x10 | 수집 제어 | 쓰기: 0x0001=시작, 0x0002=중지 |

---

## 문의하기

질문이나 제안이 있으시면 다음을 방문해 주십시오:
- GitHub: https://github.com/Juxi-Technology/JUXI_HeartRate_SPO2

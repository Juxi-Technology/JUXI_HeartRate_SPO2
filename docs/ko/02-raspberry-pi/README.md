[English](../../en/02-raspberry-pi/README.md) | [Deutsch](../../de/02-raspberry-pi/README.md) | [Español](../../es/02-raspberry-pi/README.md) | [Français](../../fr/02-raspberry-pi/README.md) | [Italiano](../../it/02-raspberry-pi/README.md) | [日本語](../../ja/02-raspberry-pi/README.md) | 한국어 | [Português (BR)](../../pt-br/02-raspberry-pi/README.md) | [Português (PT)](../../pt-pt/02-raspberry-pi/README.md) | [简体中文](../../zh-hans/02-raspberry-pi/README.md) | [繁體中文](../../zh-hant/02-raspberry-pi/README.md)

# JUXI_HeartRate_SPO2 라즈베리 파이 튜토리얼


## 목차

1. [소개](#소개)
2. [하드웨어 요구 사항](#하드웨어-요구-사항)
3. [하드웨어 연결](#하드웨어-연결)
4. [환경 설정](#환경-설정)
5. [예제 코드 사용](#예제-코드-사용)
6. [API 레퍼런스](#api-레퍼런스)
7. [FAQ](#faq)
8. [중요 사항](#중요-사항)

---

## 소개

JUXI_HeartRate_SPO2는 MAX30102 칩을 기반으로 한 심박수·혈중산소 센서 모듈입니다. 내장 알고리즘을 통해 심박수와 혈중산소 포화도 값을 직접 출력합니다.

**주요 특징:**
- 혈중산소 포화도(SPO2) 측정
- 심박수 측정(분당 박동수)
- 온보드 온도 측정
- UART 및 I2C 통신 모두 지원

---

## 하드웨어 요구 사항

| 필요 항목 | 설명 |
|--------------|-------------|
| 라즈베리 파이 (2/3/4/Zero) | Raspberry Pi 3B+ 또는 4B 권장 |
| JUXI_HeartRate_SPO2 센서 | 심박수·혈중산소 센서 모듈 |
| 점퍼 와이어 | 암-암 점퍼 와이어 4개 |
| 전원 어댑터 | 라즈베리 파이 전원 공급 장치 |

---

## 하드웨어 연결

### 방법 1: I2C 통신 (권장)

I2C 통신은 배선이 간단하여 권장합니다.

| 센서 핀 | 라즈베리 파이 물리 핀 | BCM 번호 | 설명 |
|-----------|--------------------------|-----------|-------------|
| VCC | 1 또는 17 | - | 3.3V 전원 (5V도 가능) |
| GND | 6 또는 9 또는 14 | - | 접지 |
| SDA | 3 | GPIO2 | I2C 데이터 라인 |
| SCL | 5 | GPIO3 | I2C 클록 라인 |

**중요:** 센서 토글을 **IIC** 위치로 전환하십시오!

### 방법 2: UART 시리얼 통신

UART 통신은 교차 연결이 필요합니다.

| 센서 핀 | 라즈베리 파이 물리 핀 | BCM 번호 | 설명 |
|-----------|--------------------------|-----------|-------------|
| VCC | 2 또는 4 | - | 5V 전원 (3.3V도 가능) |
| GND | 6 또는 9 또는 14 | - | 접지 |
| RX | 8 | GPIO14 | 센서 RX는 라즈베리 파이 TX에 연결 |
| TX | 10 | GPIO15 | 센서 TX는 라즈베리 파이 RX에 연결 |

**중요:** 센서 토글을 **UART** 위치로 전환하십시오!

![树莓派针脚图](../../en/02-raspberry-pi/Raspberry%20Pi%20Pin%20Diagram.png)

---

## 환경 설정

### 1. I2C 활성화 (I2C 모드에 필요)

```bash
sudo raspi-config
```

`Interface Options` → `I2C` → `Yes`를 선택하여 활성화합니다

라즈베리 파이 재시작:
```bash
sudo reboot
```

### 2. 시리얼 포트 활성화 (UART 모드에 필요)

```bash
sudo raspi-config
```

`Interface Options` → `Serial`을 선택합니다

- 첫 번째 질문: "Would you like a login shell to be accessible over serial?" → `No`를 선택합니다
- 두 번째 질문: "Would you like the serial port hardware to be enabled?" → `Yes`를 선택합니다

라즈베리 파이 재시작:
```bash
sudo reboot
```

### 3. 종속성 설치

```bash
# Update package lists
sudo apt-get update

# Install I2C tools and smbus2 library (smbus2 is required for I2C mode)
sudo apt-get install -y i2c-tools python3-smbus2

# Install pyserial (for serial port support)
sudo pip3 install pyserial
```

> **참고:** I2C 모드에는 `smbus2`가 필요합니다 — 레거시 `python-smbus` 패키지로는 충분하지 않습니다.
> 라이브러리는 `smbus2.i2c_msg`를 사용하여 두 개의 독립적인 I2C 트랜잭션을 수행합니다(레지스터 주소를 STOP과 함께
> 기록한 후, 새로운 읽기 트랜잭션으로 여러 바이트를 순차적으로 읽음). 이는 센서 칩이 요구하는 I2C 타이밍과 일치합니다.

### 4. I2C 연결 확인 (I2C 모드)

배선 후 다음 명령을 실행하여 I2C 장치를 탐지합니다:

```bash
i2cdetect -y 1
```

주소 `0x57`이 표시되면 센서가 성공적으로 연결된 것입니다.

---

## 예제 코드 사용

### 파일 구조

```
python/raspberry/
├── JUXI_HeartRate_SPO2.py      # Main library file
└── examples/
    ├── i2c_example.py          # I2C mode example
    └── uart_example.py         # UART mode example
```

### I2C 모드 예제 실행

```bash
cd python/raspberry/examples
sudo python3 i2c_example.py
```

### UART 모드 예제 실행

```bash
cd python/raspberry/examples
sudo python3 uart_example.py
```

**참고:** 하드웨어 시리얼 포트에 접근하려면 `sudo` 권한이 필요합니다.

### 예상 출력

모든 것이 정상적으로 동작하면 다음과 유사한 출력이 표시됩니다:

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

`Ctrl+C`를 눌러 프로그램을 중지합니다.

---

## API 레퍼런스

### 클래스: JUXI_HeartRate_SPO2_i2c

I2C 통신용 센서 클래스입니다.

#### 생성자
```python
JUXI_HeartRate_SPO2_i2c(bus_number=1, i2c_address=0x57)
```

매개변수:
- `bus_number`: I2C 버스 번호로, 라즈베리 파이에서는 보통 1입니다
- `i2c_address`: 센서 I2C 주소로, 기본값은 0x57입니다

#### 메서드

| 메서드 | 설명 | 반환 값 |
|--------|-------------|--------------|
| `begin()` | 센서를 초기화하고 연결을 확인합니다 | bool (성공 시 True) |
| `sensor_start_collect()` | 데이터 수집을 시작합니다(센서 LED 점등) | None |
| `sensor_end_collect()` | 데이터 수집을 중지합니다(센서 LED 소등) | None |
| `get_heartbeat_SPO2()` | 심박수와 SPO2 데이터를 읽습니다 | None (결과는 객체 속성에 저장됨) |
| `get_temperature_c()` | 온보드 온도를 읽습니다 | float (섭씨) |
| `close()` | I2C 연결을 닫습니다 | None |

#### 속성

| 속성 | 설명 |
|----------|-------------|
| `SPO2` | 혈중산소 포화도(%), -1은 유효하지 않은 값입니다 |
| `heartbeat` | 심박수(분당 박동수), -1은 유효하지 않은 값입니다 |

---

### 클래스: JUXI_HeartRate_SPO2_uart

UART 시리얼 통신용 센서 클래스입니다.

#### 생성자
```python
JUXI_HeartRate_SPO2_uart(port='/dev/serial0', baudrate=9600)
```

매개변수:
- `port`: 시리얼 장치 경로로, 라즈베리 파이에서는 기본값이 `/dev/serial0`입니다
- `baudrate`: 보드레이트로, 기본값은 9600입니다

#### 메서드

`JUXI_HeartRate_SPO2_i2c`와 동일합니다.

---

## FAQ

### Q1: 센서 초기화에 실패하면 어떻게 해야 하나요?

**A:** 다음 단계를 따라 주십시오:

1. **배선 확인**
   - I2C 모드: SDA가 GPIO2에, SCL이 GPIO3에 연결되었는지 확인합니다
   - UART 모드: RX-TX 교차 연결을 확인합니다

2. **센서 토글 확인**
   - I2C 모드: 토글이 IIC 위치에 있어야 합니다
   - UART 모드: 토글이 UART 위치에 있어야 합니다

3. **전원 확인**
   - VCC가 3.3V 또는 5V에 연결되었는지 확인합니다
   - GND가 연결되었는지 확인합니다

4. **시스템 설정 확인**
   - I2C 모드: I2C가 활성화되었는지 확인합니다
   - UART 모드: 시리얼 포트가 활성화되었는지 확인합니다

5. **탐지 명령 사용**
   ```bash
   # I2C mode
   i2cdetect -y 1
   
   # UART mode
   ls /dev/serial*
   ```

### Q2: 데이터가 항상 -1로 표시되는데 어떻게 해야 하나요?

**A:**

1. 손가락이 센서 위에 제대로 놓여 두 개의 LED를 완전히 덮고 있는지 확인합니다
2. 데이터가 안정화될 때까지 몇 초 기다립니다(보통 10-30초)
3. 수집을 시작하기 위해 `sensor_start_collect()`를 호출했는지 확인합니다
4. 센서 LED가 켜져 있는지 확인합니다

### Q3: 데이터가 부정확한데 어떻게 해야 하나요?

**A:**

1. 손가락이 센서의 광학 영역을 완전히 덮는지 확인합니다
2. 손가락을 움직이지 않고 안정적으로 유지합니다
3. 데이터가 안정화될 때까지 30초 이상 기다립니다
4. 여러 번 측정하여 평균을 냅니다
5. 센서에 강한 직사광이 비치지 않도록 합니다

### Q4: I2C와 UART를 동시에 사용할 수 있나요?

**A:** 아니요, 한 번에 하나의 통신 방식만 선택할 수 있습니다.

### Q5: 실행하려면 sudo를 사용해야 하나요?

**A:**
- I2C 모드: 권한 문제를 피하기 위해 sudo를 권장합니다
- UART 모드: sudo가 필요하며, 그렇지 않으면 시리얼 포트에 접근할 수 없습니다

---

## 중요 사항

### 측정 팁

1. **올바른 손가락 위치**
   - 손가락을 센서 위에 부드럽게 올리고 두 개의 LED를 덮습니다
   - 혈액 순환에 영향을 줄 수 있으므로 너무 세게 누르지 않습니다
   - 손가락을 안정적으로 유지하고 움직이지 않습니다

2. **데이터 안정화 대기**
   - 측정을 시작할 때 값이 불안정할 수 있습니다
   - 데이터가 안정화될 때까지 10-30초 기다리는 것을 권장합니다
   - 센서는 4초마다 데이터를 갱신합니다

3. **환경 요구 사항**
   - 센서에 강한 직사광이 비치지 않도록 합니다
   - 적절한 주변 온도를 유지합니다
   - 측정 중에는 조용히 유지합니다

### 데이터 해석

| SPO2 범위 | 설명 |
|-----------|-------------|
| 95% - 100% | 정상 |
| 90% - 94% | 경증 저산소증 |
| < 90% | 저산소증, 의사와 상담하십시오 |

| 심박수 범위 | 설명 |
|-----------------|-------------|
| 60 - 100 BPM | 성인의 정상 범위 |
| < 60 BPM | 서맥 |
| > 100 BPM | 빈맥 |

### 안전 주의사항

- 이 센서는 참고용이며 전문 의료 장비를 대체할 수 없습니다
- 건강에 우려가 있으면 즉시 의사와 상담하십시오
- 측정 결과는 참고용이며 진단에 사용해서는 안 됩니다

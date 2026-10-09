[English](../../en/01-arduino/README.md) | [Deutsch](../../de/01-arduino/README.md) | [Español](../../es/01-arduino/README.md) | [Français](../../fr/01-arduino/README.md) | [Italiano](../../it/01-arduino/README.md) | [日本語](../../ja/01-arduino/README.md) | 한국어 | [Português (BR)](../../pt-br/01-arduino/README.md) | [Português (PT)](../../pt-pt/01-arduino/README.md) | [简体中文](../../zh-hans/01-arduino/README.md) | [繁體中文](../../zh-hant/01-arduino/README.md)

# JUXI_HeartRate_SPO2 심박수·혈중산소 센서 튜토리얼

## 목차
1. [센서 소개](#센서-소개)
2. [아두이노 튜토리얼](#아두이노-튜토리얼)
3. [Python (라즈베리 파이) 튜토리얼](#python-라즈베리-파이-튜토리얼)
4. [FAQ](#faq)

---

## 센서 소개

JUXI_HeartRate_SPO2는 MAX30102 칩을 기반으로 한 심박수·혈중산소 센서 모듈로, 내장 알고리즘이 심박수와 혈중산소 포화도 값을 직접 출력할 수 있습니다.

**주요 특징:**

- 혈중산소 포화도(SPO2) 측정
- 심박수 측정(분당 박동수)
- 온보드 온도 측정
- I2C 통신 지원

---

## 아두이노 튜토리얼

### 1. 하드웨어 준비

| 준비물 |
|-------------------|
| 아두이노 개발 보드 (Uno/Nano/ESP32 등) |
| JUXI_HeartRate_SPO2 센서 |
| 점퍼 와이어 여러 개 |
| USB 데이터 케이블 (아두이노와 컴퓨터 연결) |

### 2. 라이브러리 설치

1. 이 라이브러리 파일을 다운로드합니다
2. `JUXI_HeartRate_SPO2` 폴더를 아두이노 라이브러리 디렉터리에 복사합니다:
   - Windows: `C:\Users\Username\Documents\Arduino\libraries\`
   - Mac: `~/Documents/Arduino/libraries/`
   - Linux: `~/Arduino/libraries/`
3. 아두이노 IDE를 재시작합니다

### 3. 예제 코드

**주의: 코드를 업로드할 때는 아두이노만 컴퓨터에 연결하고, 심박수·혈중산소 모듈은 아두이노에 연결하지 마십시오!!!**

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

##### 하드웨어 연결

I2C 통신

| 센서 핀 | 아두이노 |
|-----------|---------|
| VCC       | 5V/3.3V |
| GND       | GND     |
| SDA       | SDA/A4  |
| SCL       | SCL/A5  |

![IIC](../../en/01-arduino/img/IIC.png)

![8](../../en/01-arduino/img/8.png)

- 심박수·혈중산소 모듈의 DIP 스위치를 I2C 위치로 전환하십시오!!!
- 데이터 케이블로 아두이노와 컴퓨터를 연결합니다

#### 실행 결과:

1. 아두이노 - 도구 - 시리얼 모니터를 엽니다

   보드레이트를 9600으로 설정합니다

![1](../../en/01-arduino/img/1.png)

2. 시리얼 디버그 어시스턴트를 엽니다

[Serial Debug Assistant uartassist5.15.zip](https://juxitech.feishu.cn/wiki/BJlfwSQydi7u5lkRDQ6cV4dvnBd)

시리얼 포트 번호를 선택합니다

보드레이트를 `9600`으로 설정합니다

데이터 비트 `8`, 정지 비트 `1`, 패리티 `NONE`, 흐름 제어 `NONE`

수신 및 송신 설정에서 `ASCII`를 선택합니다

![2](../../en/01-arduino/img/2.png)

### 4. API 설명

| 함수 | 설명 |
|----------|-------------|
| `begin()` | 센서를 초기화하며, true/false를 반환합니다 |
| `getHeartbeatSPO2()` | 심박수와 SPO2 데이터를 읽으며, `_sHeartbeatSPO2` 구조체에 저장됩니다 |
| `getTemperature_C()` | 온보드 온도를 읽습니다(섭씨) |
| `sensorStartCollect()` | 데이터 수집을 시작합니다(센서 LED 점등) |
| `sensorEndCollect()` | 데이터 수집을 중지합니다(센서 LED 소등) |

### 5. 데이터 설명

- **SPO2(혈중산소 포화도)**: 정상 범위 95% - 100%, 값 -1은 유효하지 않음을 나타냅니다
- **Heartbeat(심박수)**: 정상 범위 60 - 100 BPM, 값 -1은 유효하지 않음을 나타냅니다
- **유효하지 않은 값의 원인**: 손가락이 제대로 놓이지 않았거나 데이터가 안정되지 않음

---

## 사용 참고 사항

### 측정 팁

1. **올바른 손가락 위치**
   - 손가락을 센서 위에 부드럽게 올리고 두 개의 LED를 모두 덮습니다
   - 혈액 순환에 영향을 주지 않도록 세게 누르지 않습니다
   - 손가락을 안정적으로 유지하고 움직이지 않습니다

2. **데이터 안정화 대기**
   - 측정을 시작할 때 값이 불안정할 수 있습니다
   - 데이터가 안정화될 때까지 10~30초 기다린 후 읽는 것을 권장합니다
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
| < 90% | 저산소증, 의료 상담 권장 |

| 심박수 범위 | 설명 |
|-----------------|-------------|
| 60 - 100 BPM | 성인의 정상 범위 |
| < 60 BPM | 서맥 |
| > 100 BPM | 빈맥 |

---

## FAQ

### Q1: 센서 초기화에 실패하나요?

**A:**
1. 배선이 올바른지 확인합니다(SDA는 GPIO2/A4, SCL은 GPIO3/A5)
2. 전원 공급이 정상인지 확인합니다(3.3V 또는 5V)
3. `i2cdetect -y 1` 명령으로 장치를 탐지합니다
4. 센서의 DIP 스위치가 IIC 위치에 있는지 확인합니다

### Q2: 데이터가 항상 -1로 표시되나요?

**A:**
1. 손가락이 센서 위에 제대로 놓였는지 확인합니다
2. 데이터가 안정화될 때까지 몇 초 기다립니다
3. 수집을 시작하기 위해 `sensorStartCollect()`를 호출했는지 확인합니다
4. 센서 표시등이 켜져 있는지 확인합니다

### Q3: 데이터가 부정확한가요?

**A:**
1. 손가락이 센서의 광학 영역을 완전히 덮는지 확인합니다
2. 손가락을 움직이지 않고 안정적으로 유지합니다
3. 데이터가 안정화될 때까지 30초 이상 기다립니다
4. 여러 번 측정하여 평균을 냅니다

### Q4: 어떤 아두이노 개발 보드가 지원되나요?

**A:** 지원 대상:
- Arduino Uno/Nano/Mega
- ESP8266
- ESP32
- 아두이노 환경을 지원하는 기타 개발 보드

---

## 예제 파일 위치

### 아두이노 예제
```
JUXI_HeartRate_SPO2/
└── examples/
    └── gainHeartbeatSPO2/
        └── gainHeartbeatSPO2.ino
```

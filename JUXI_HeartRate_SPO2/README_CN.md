[English](README.md) | 简体中文

# JUXI_HeartRate_SPO2


MAX30102 血氧心率传感器 Arduino 库

## 功能特性

- 测量血氧饱和度（SPO2）
- 测量心率
- 测量温度
- 支持 I2C 通信

## 安装方法

1. 下载本库
2. 解压到Arduino libraries文件夹
3. 重启Arduino IDE

## 硬件连接

### I2C 模式

| 传感器 | Arduino |
|--------|---------|
| VCC    | 5V/3.3V |
| GND    | GND     |
| SDA    | SDA/A4  |
| SCL    | SCL/A5  |

## 使用方法

完整示例请查看 `examples/gainHeartbeatSPO2/gainHeartbeatSPO2.ino`

```cpp
#include "JUXI_HeartRate_SPO2.h"

#define I2C_ADDRESS 0x57
JUXI_HeartRate_SPO2_I2C sensor(&Wire, I2C_ADDRESS);

void setup() {
    Serial.begin(9600);
    while (!sensor.begin()) {
        Serial.println("初始化失败！");
        delay(1000);
    }
    Serial.println("初始化成功！");
    sensor.sensorStartCollect();
}

void loop() {
    sensor.getHeartbeatSPO2();
    Serial.print("血氧: ");
    Serial.print(sensor._sHeartbeatSPO2.SPO2);
    Serial.println("%");

    Serial.print("心率: ");
    Serial.print(sensor._sHeartbeatSPO2.Heartbeat);
    Serial.println(" 次/分");

    Serial.print("板载温度: ");
    Serial.print(sensor.getTemperature_C());
    Serial.println(" ℃");

    delay(4000);
}
```

## API参考

- `begin()` - 初始化传感器
- `getHeartbeatSPO2()` - 读取血氧和心率值
- `getTemperature_C()` - 读取温度（摄氏度）
- `sensorStartCollect()` - 开始数据采集
- `sensorEndCollect()` - 停止数据采集

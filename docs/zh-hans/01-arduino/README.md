[English](../../en/01-arduino/README.md) | [Deutsch](../../de/01-arduino/README.md) | [Español](../../es/01-arduino/README.md) | [Français](../../fr/01-arduino/README.md) | [Italiano](../../it/01-arduino/README.md) | [日本語](../../ja/01-arduino/README.md) | [한국어](../../ko/01-arduino/README.md) | [Português (BR)](../../pt-br/01-arduino/README.md) | [Português (PT)](../../pt-pt/01-arduino/README.md) | 简体中文 | [繁體中文](../../zh-hant/01-arduino/README.md)

# JUXI_HeartRate_SPO2 心率血氧传感器使用教程

## 目录
1. [传感器简介](#传感器简介)
2. [Arduino 使用教程](#arduino-使用教程)
3. [Python (树莓派) 使用教程](#python-树莓派-使用教程)
4. [常见问题](#常见问题)

---

## 传感器简介

JUXI_HeartRate_SPO2 是一款基于 MAX30102 芯片的心率血氧传感器模块，内置算法可直接输出心率和血氧饱和度数值。

**主要功能：**

- 血氧饱和度（SPO2）测量
- 心率测量（次/分钟）
- 板载温度测量
- 支持 I2C 通信方式

---

## Arduino 使用教程

### 1. 硬件准备

| 所需材料 |
|---------|
| Arduino 开发板（Uno/Nano/ESP32等） |
| JUXI_HeartRate_SPO2 传感器 |
| 杜邦线若干 |
| USB数据线（Arduino连接到电脑上） |

### 2. 库安装

1. 下载本库文件
2. 将 `JUXI_HeartRate_SPO2` 文件夹复制到 Arduino 库目录：
   - Windows: `C:\Users\用户名\Documents\Arduino\libraries\`
   - Mac: `~/Documents/Arduino/libraries/`
   - Linux: `~/Arduino/libraries/`
3. 重启 Arduino IDE

### 3. 示例代码

**注意上传代码时，只连接Arduino 到电脑上，Arduino不连接心率血氧监测模块！！！**

```cpp
#include "JUXI_HeartRate_SPO2.h"

// I2C 地址
#define I2C_ADDRESS 0x57

// 创建传感器对象，I2C模式
JUXI_HeartRate_SPO2_I2C sensor(&Wire, I2C_ADDRESS);

void setup() {
  Serial.begin(9600);

  // 初始化传感器
  while (!sensor.begin()) {
    Serial.println("传感器初始化失败，请检查连接！");
    delay(1000);
  }
  Serial.println("传感器初始化成功！");

  // 启动数据采集
  sensor.sensorStartCollect();
}

void loop() {
  // 读取心率和血氧数据
  sensor.getHeartbeatSPO2();

  // 输出血氧饱和度
  Serial.print("血氧饱和度: ");
  Serial.print(sensor._sHeartbeatSPO2.SPO2);
  Serial.println(" %");

  // 输出心率
  Serial.print("心率: ");
  Serial.print(sensor._sHeartbeatSPO2.Heartbeat);
  Serial.println(" 次/分钟");

  // 读取并输出温度
  Serial.print("板载温度: ");
  Serial.print(sensor.getTemperature_C());
  Serial.println(" ℃");

  Serial.println("------------------------");

  // 传感器每4秒更新一次数据
  delay(4000);
}
```

##### 硬件连接

I2C 通信

| 传感器引脚 | Arduino |
| ---------- | ------- |
| VCC        | 5V/3.3V |
| GND        | GND     |
| SDA        | SDA/A4  |
| SCL        | SCL/A5  |

![IIC](../../en/01-arduino/img/IIC.png)

![8](../../en/01-arduino/img/8.png)

- 将心率血氧监测模块拨片拨动到IIC！！！
- 使用数据线将Arduino连接到电脑上

#### 运行结果：

1、打开 Arduino-工具-串口监视器

​	设置波特率为9600

![1](../../en/01-arduino/img/1.png)

2、打开串口调试助手

[串口调试助手uartassist5.15.zip](https://juxitech.feishu.cn/wiki/BJlfwSQydi7u5lkRDQ6cV4dvnBd)

选择串口号

设置波特率为`9600`

数据位`8`，停止位`1`，校验位`NONE`，流控制`NONE`

接受设置和发送设置选择`ASCII`

![2](../../en/01-arduino/img/2.png)

### 4. API 说明

| 函数 | 说明 |
|-----|------|
| `begin()` | 初始化传感器，返回 true/false |
| `getHeartbeatSPO2()` | 读取心率和血氧数据，存储在 `_sHeartbeatSPO2` 结构体中 |
| `getTemperature_C()` | 读取板载温度（摄氏度） |
| `sensorStartCollect()` | 开始数据采集（传感器亮灯） |
| `sensorEndCollect()` | 停止数据采集（传感器关灯） |

### 5. 数据说明

- **SPO2（血氧饱和度）**: 正常范围 95% - 100%，值为 -1 表示无效
- **Heartbeat（心率）**: 正常范围 60 - 100 次/分钟，值为 -1 表示无效
- **无效值原因**: 手指未放置好或数据未稳定

---

## 使用注意事项

### 测量技巧

1. **正确放置手指**
   - 将手指轻轻放在传感器上，覆盖两个LED灯
   - 不要用力按压，以免影响血液循环
   - 保持手指稳定，不要移动

2. **等待数据稳定**
   - 刚开始测量时，数值可能不稳定
   - 建议等待 10-30 秒，待数据稳定后再读取
   - 传感器每 4 秒更新一次数据

3. **环境要求**
   - 避免强光直射传感器
   - 保持环境温度适宜
   - 测量时保持安静

### 数据解读

| SPO2 范围 | 说明 |
|----------|------|
| 95% - 100% | 正常 |
| 90% - 94% | 轻度低氧 |
| < 90% | 低氧，建议就医 |

| 心率范围 | 说明 |
|---------|------|
| 60 - 100 次/分 | 成人正常范围 |
| < 60 次/分 | 心动过缓 |
| > 100 次/分 | 心动过速 |

---

## 常见问题

### Q1: 传感器初始化失败怎么办？

**A:**

1. 检查接线是否正确（SDA接GPIO2/A4，SCL接GPIO3/A5）
2. 确认电源是否正常（3.3V或5V）
3. 使用 `i2cdetect -y 1` 命令检测设备
4. 确认传感器拨片在 IIC 位置

### Q2: 数据一直显示 -1 怎么办？

**A:**
1. 确认手指已正确放置在传感器上
2. 等待几秒钟让数据稳定
3. 检查是否已调用 `sensorStartCollect()` 开启采集
4. 确认传感器指示灯是否亮起

### Q3: 数据不准确怎么办？

**A:**
1. 确保手指完全覆盖传感器光学区域
2. 保持手指静止，不要移动
3. 等待 30 秒以上让数据稳定
4. 多次测量取平均值

### Q4: 传感器支持哪些 Arduino 开发板？

**A:** 支持：
- Arduino Uno/Nano/Mega
- ESP8266
- ESP32
- 其他支持 Arduino 环境的开发板

---

## 示例文件位置

### Arduino 示例
```
JUXI_HeartRate_SPO2/
└── examples/
    └── gainHeartbeatSPO2/
        └── gainHeartbeatSPO2.ino
```




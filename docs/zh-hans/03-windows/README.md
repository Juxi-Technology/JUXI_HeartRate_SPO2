[English](../../en/03-windows/README.md) | [Deutsch](../../de/03-windows/README.md) | [Español](../../es/03-windows/README.md) | [Français](../../fr/03-windows/README.md) | [Italiano](../../it/03-windows/README.md) | [日本語](../../ja/03-windows/README.md) | [한국어](../../ko/03-windows/README.md) | [Português (BR)](../../pt-br/03-windows/README.md) | [Português (PT)](../../pt-pt/03-windows/README.md) | 简体中文 | [繁體中文](../../zh-hant/03-windows/README.md)

# JUXI 心率血氧传感器 - Windows 使用指南

## 目录
1. [硬件准备](#硬件准备)
2. [硬件连接](#硬件连接)
3. [软件环境配置](#软件环境配置)
4. [运行示例程序](#运行示例程序)
5. [常见问题](#常见问题)

---

## 硬件准备

### 所需材料
| 材料 | 说明 |
|------|------|
| JUXI_HeartRate_SPO2 传感器 | 心率血氧模块 |
| USB转TTL模块 | CH340 / CP2102 / FT232 等 |
| 杜邦线 | 4根（母对母） |
| Windows 电脑 | Win7/Win10/Win11 |

---

## 硬件连接

### 接线方式

| 传感器引脚 | USB转TTL引脚 | 说明 |
|-----------|-------------|------|
| **VCC** | 3.3V 或 5V | 电源正极 |
| **GND** | GND | 电源负极 |
| **TX** | RX | 传感器发送 → 模块接收 |
| **RX** | TX | 传感器接收 → 模块发送 |

![Connect PC](../../en/03-windows/Connect%20PC.png)

⚠️ **重要提示**：

1. **模块拨片拨动到UART！！！**
2. **TX 和 RX 必须交叉连接！**
3. 传感器支持 3.3V 和 5V，不要接错电压
4. 先接好所有线，再插入USB到电脑

### 接线示意图
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

## 软件环境配置

### 1. 安装驱动

根据你的USB转TTL芯片型号，安装对应的驱动：

- **CH340**: https://sparks.gogo.co.nz/ch340.html
- **CP2102**: https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers
- **FT232**: https://ftdichip.com/drivers/vcp-drivers/

安装完成后，插入USB转TTL模块。

### 2. 查看COM端口

#### 方法一：设备管理器
1. 按 `Win + X`，选择"设备管理器"
2. 展开"端口 (COM 和 LPT)"
3. 查看你的USB转TTL对应的COM口号（如 COM3）

#### 方法二：程序自动检测
运行示例程序时，会自动列出所有可用串口。

### 3. 安装Python依赖

打开命令提示符（CMD）或PowerShell，运行：

```bash
pip install pyserial
```

---

## 运行示例程序

### 文件位置
```
JUXI_HeartRate_SPO2/python/windows/
├── gain_heartbeat_SPO2.py  ← 主程序（直接运行这个）
├── JUXI_HeartRate_SPO2_Windows.py
├── JUXI_RTU_Windows.py
└── README_Windows.md        ← 本文件
```

### 运行步骤

1. **确认硬件连接正确**
   - VCC → 3.3V/5V
   - GND → GND
   - TX → RX（交叉）
   - RX → TX（交叉）

2. **插入USB到电脑**

3. **运行程序**
   ```bash
   cd D:\JUXI_HeartRate_SPO2\python\windows
   python gain_heartbeat_SPO2.py
   ```

4. **按照提示操作**
   
   - 程序会列出所有可用串口
   - 输入你的COM口号（如 COM3）
   - 程序自动检测传感器并开始测量

### 预期输出

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

按 `Ctrl + C` 停止程序。

---

## 程序功能说明

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

## 常见问题

### Q1: 找不到COM端口怎么办？

**A:**

1. 检查USB转TTL是否插好
2. 重新安装驱动程序
3. 换一个USB口试试
4. 在设备管理器中查看是否有"未知设备"

### Q2: 传感器初始化失败怎么办？

**A:**

1. 检查接线：
   - VCC 和 GND 是否接对
   - **TX 和 RX 是否交叉连接**（最常见问题）
2. 确认波特率是 9600
3. 检查USB转TTL模块是否正常工作
4. 重新插拔USB

### Q3: 数据一直显示 -1 怎么办？

**A:**
1. 确认手指正确放在传感器上（完全覆盖LED区域）
2. 保持手指稳定，不要移动
3. 等待几秒钟让数据稳定
4. 检查传感器LED是否亮起

### Q4: LED灯不亮但通信正常？

**A:**

- 可能是LED灯硬件问题，但传感器功能正常
- 只要数据正常，可以忽略LED不亮问题

### Q5: 串口被占用怎么办？

**A:**
1. 关闭其他串口软件（串口助手、Arduino IDE等）
2. 检查是否有其他Python程序正在运行
3. 重新插拔USB

### Q6: 数据不准确怎么办？

**A:**
1. 确保手指完全覆盖传感器光学区域
2. 测量时保持安静，不要说话或移动
3. 等待30秒以上让数据稳定
4. 多次测量取平均值

---

## 技术规格

| 参数 | 规格 |
|-----|------|
| 通信方式 | UART (TTL电平) |
| 波特率 | 9600 bps（默认） |
| 数据格式 | 8N1 (8数据位, 无校验, 1停止位) |
| 供电电压 | 3.3V / 5V |
| SPO2测量范围 | 35% - 100% |
| 心率测量范围 | 30 - 250 BPM |
| Modbus设备地址 | 0x20 |

---

## Modbus 寄存器说明

| 寄存器地址 | 功能 | 说明 |
|-----------|------|------|
| 0x02 | 设备ID | 读：返回 0x0020 |
| 0x06-0x09 | 心率血氧数据 | 读：SPO2 + 心率 |
| 0x0A | 温度 | 读：板载温度 |
| 0x10 | 采集控制 | 写：0x0001=开始, 0x0002=停止 |

---

## 联系我们

如有问题或建议，请访问：
- GitHub: https://github.com/Juxi-Technology/JUXI_HeartRate_SPO2

[English](README.md) | 简体中文

# JUXI_HeartRate_SPO2 树莓派使用教程


## 目录

1. [项目简介](#项目简介)
2. [硬件准备](#硬件准备)
3. [硬件连接](#硬件连接)
4. [环境配置](#环境配置)
5. [示例代码使用](#示例代码使用)
6. [API 参考](#api-参考)
7. [常见问题](#常见问题)
8. [注意事项](#注意事项)

---

## 项目简介

JUXI_HeartRate_SPO2 是一款基于 MAX30102 芯片的心率血氧传感器模块，内置算法可直接输出心率和血氧饱和度数值。

**主要功能：**
- 血氧饱和度（SPO2）测量
- 心率测量（次/分钟）
- 板载温度测量
- 支持 UART 和 I2C 两种通信方式

---

## 硬件准备

| 所需材料 | 说明 |
|---------|------|
| 树莓派（2/3/4/Zero 均可） | 推荐使用树莓派 3B+ 或 4B |
| JUXI_HeartRate_SPO2 传感器 | 心率血氧传感器模块 |
| 杜邦线若干 | 母对母杜邦线 4 根 |
| 电源适配器 | 树莓派专用电源 |

---

## 硬件连接

### 方式一：I2C 通信（推荐）

I2C 通信接线简单，推荐使用。

| 传感器引脚 | 树莓派物理引脚 | BCM 编号 | 说明 |
|-----------|---------------|---------|------|
| VCC | 1 或 17 | - | 3.3V 电源（也可接 5V） |
| GND | 6 或 9 或 14 | - | 接地 |
| SDA | 3 | GPIO2 | I2C 数据线 |
| SCL | 5 | GPIO3 | I2C 时钟线 |

**重要：** 将传感器上的拨片拨动到 **IIC** 位置！

### 方式二：UART 串口通信

UART 通信需要交叉连接。

| 传感器引脚 | 树莓派物理引脚 | BCM 编号 | 说明 |
|-----------|---------------|---------|------|
| VCC | 2 或 4 | - | 5V 电源（也可接 3.3V） |
| GND | 6 或 9 或 14 | - | 接地 |
| RX | 8 | GPIO14 | 传感器 RX 接树莓派 TX |
| TX | 10 | GPIO15 | 传感器 TX 接树莓派 RX |

**重要：** 将传感器上的拨片拨动到 **UART** 位置！

![Raspberry Pi Pin Diagram](Raspberry%20Pi%20Pin%20Diagram.png)

---

## 环境配置

### 1. 启用 I2C（I2C 模式需要）

```bash
sudo raspi-config
```

选择 `Interface Options` → `I2C` → 选择 `Yes` 启用

重启树莓派：
```bash
sudo reboot
```

### 2. 启用串口（UART 模式需要）

```bash
sudo raspi-config
```

选择 `Interface Options` → `Serial`

- 第一个问题："Would you like a login shell to be accessible over serial?" → 选择 `No`
- 第二个问题："Would you like the serial port hardware to be enabled?" → 选择 `Yes`

重启树莓派：
```bash
sudo reboot
```

### 3. 安装依赖库

```bash
# 更新软件源
sudo apt-get update

# 安装 I2C 工具和 smbus2 库（I2C 模式必须使用 smbus2）
sudo apt-get install -y i2c-tools python3-smbus2

# 安装 pyserial（串口支持）
sudo pip3 install pyserial
```

> **注意：** I2C 模式必须安装 `smbus2`，不能使用旧版 `python-smbus`。
> 库内部使用 `smbus2.i2c_msg` 实现独立的两步 I2C 事务（先写寄存器地址并发送 STOP，
> 再开启新的读事务连续读取多字节），以匹配传感器芯片的 I2C 时序要求。

### 4. 验证 I2C 连接（I2C 模式）

接线完成后，运行以下命令检测 I2C 设备：

```bash
i2cdetect -y 1
```

如果看到地址 `0x57`，说明传感器连接成功。

---

## 示例代码使用

### 文件结构

```
python/raspberry/
├── JUXI_HeartRate_SPO2.py      # 主库文件
└── examples/
    ├── i2c_example.py          # I2C 模式示例
    └── uart_example.py         # UART 模式示例
```

### 运行 I2C 模式示例

```bash
cd python/raspberry/examples
sudo python3 i2c_example.py
```

### 运行 UART 模式示例

```bash
cd python/raspberry/examples
sudo python3 uart_example.py
```

**注意：** 使用硬件串口时需要 `sudo` 权限。

### 运行结果

如果一切正常，你会看到类似以下的输出：

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

按 `Ctrl+C` 停止程序。

---

## API 参考

### 类：JUXI_HeartRate_SPO2_i2c

I2C 通信方式的传感器类。

#### 构造函数
```python
JUXI_HeartRate_SPO2_i2c(bus_number=1, i2c_address=0x57)
```

参数：
- `bus_number`: I2C 总线号，树莓派通常为 1
- `i2c_address`: 传感器 I2C 地址，默认 0x57

#### 方法

| 方法 | 说明 | 返回值 |
|-----|------|--------|
| `begin()` | 初始化传感器，检测连接 | bool (成功返回 True) |
| `sensor_start_collect()` | 开始数据采集（传感器亮灯） | 无 |
| `sensor_end_collect()` | 停止数据采集（传感器关灯） | 无 |
| `get_heartbeat_SPO2()` | 读取心率和血氧数据 | 无（结果存储在对象属性中） |
| `get_temperature_c()` | 读取板载温度 | float (摄氏度) |
| `close()` | 关闭 I2C 连接 | 无 |

#### 属性

| 属性 | 说明 |
|-----|------|
| `SPO2` | 血氧饱和度（%），无效值为 -1 |
| `heartbeat` | 心率（次/分钟），无效值为 -1 |

---

### 类：JUXI_HeartRate_SPO2_uart

UART 串口通信方式的传感器类。

#### 构造函数
```python
JUXI_HeartRate_SPO2_uart(port='/dev/serial0', baudrate=9600)
```

参数：
- `port`: 串口设备路径，树莓派默认为 `/dev/serial0`
- `baudrate`: 波特率，默认 9600

#### 方法

与 `JUXI_HeartRate_SPO2_i2c` 相同。

---

## 常见问题

### Q1: 传感器初始化失败怎么办？

**A:** 请按以下步骤检查：

1. **检查接线**
   - I2C 模式：确认 SDA 接 GPIO2，SCL 接 GPIO3
   - UART 模式：确认 RX-TX 交叉连接

2. **检查传感器拨片**
   - I2C 模式：拨片应在 IIC 位置
   - UART 模式：拨片应在 UART 位置

3. **检查电源**
   - 确认 VCC 接 3.3V 或 5V
   - 确认 GND 已连接

4. **检查系统设置**
   - I2C 模式：确认 I2C 已启用
   - UART 模式：确认串口已启用

5. **使用检测命令**
   ```bash
   # I2C 模式
   i2cdetect -y 1
   
   # UART 模式
   ls /dev/serial*
   ```

### Q2: 数据一直显示 -1 怎么办？

**A:**

1. 确认手指已正确放置在传感器上，完全覆盖两个 LED 灯
2. 等待几秒钟让数据稳定（通常需要 10-30 秒）
3. 检查是否已调用 `sensor_start_collect()` 开启采集
4. 确认传感器指示灯是否亮起

### Q3: 数据不准确怎么办？

**A:**

1. 确保手指完全覆盖传感器光学区域
2. 保持手指静止，不要移动
3. 等待 30 秒以上让数据稳定
4. 多次测量取平均值
5. 避免强光直射传感器

### Q4: I2C 和 UART 可以同时使用吗？

**A:** 不可以，同一时间只能选择一种通信方式。

### Q5: 需要使用 sudo 运行吗？

**A:**
- I2C 模式：建议使用 sudo，避免权限问题
- UART 模式：必须使用 sudo，否则无法访问串口

---

## 注意事项

### 测量技巧

1. **正确放置手指**
   - 将手指轻轻放在传感器上，覆盖两个 LED 灯
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

### 安全提示

- 本传感器仅供参考，不能替代专业医疗设备
- 如有健康问题，请及时就医
- 测量结果仅作参考，不做诊断依据

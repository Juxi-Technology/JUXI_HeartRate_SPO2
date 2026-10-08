# -*- coding: utf-8 -*-
"""
JUXI 心率血氧传感器 - I2C 模式示例
树莓派 Python 示例代码
"""

import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from JUXI_HeartRate_SPO2 import JUXI_HeartRate_SPO2_i2c

I2C_BUS = 0x01
I2C_ADDRESS = 0x57

def setup():
    print("=" * 50)
    print("JUXI 心率血氧传感器 - I2C 模式")
    print("=" * 50)
    print()
    
    print(f"正在初始化 I2C 总线 {I2C_BUS}，地址 0x{I2C_ADDRESS:02X}...")
    
    try:
        sensor = JUXI_HeartRate_SPO2_i2c(I2C_BUS, I2C_ADDRESS)
    except ImportError as e:
        print(f"错误: {e}")
        print("请运行: sudo apt-get install -y python3-smbus2")
        sys.exit(1)
    
    while not sensor.begin():
        print("传感器初始化失败，请检查连接！")
        print("请检查:")
        print("  1. I2C 是否已启用 (sudo raspi-config -> Interface Options -> I2C)")
        print("  2. 接线是否正确 (SDA -> GPIO2, SCL -> GPIO3)")
        print("  3. 传感器拨片是否拨到 IIC 位置")
        print("  4. 电源是否正常 (3.3V 或 5V)")
        time.sleep(2)
    
    print("传感器初始化成功！")
    print()
    print("开始数据采集...")
    sensor.sensor_start_collect()
    print("传感器 LED 已亮起！")
    print()
    print("请将手指放在传感器上...")
    print()
    time.sleep(2)
    
    return sensor

def loop(sensor):
    sensor.get_heartbeat_SPO2()
    temp = sensor.get_temperature_c()
    
    print("-" * 40)
    print(f"血氧饱和度: {sensor.SPO2} %")
    print(f"心率: {sensor.heartbeat} 次/分钟")
    print(f"板载温度: {temp:.1f} ℃")
    
    time.sleep(4)

def main():
    sensor = None
    try:
        sensor = setup()
        while True:
            loop(sensor)
    except KeyboardInterrupt:
        print("\n\n正在停止...")
        if sensor:
            sensor.sensor_end_collect()
            sensor.close()
        print("传感器已关闭。")
    except Exception as e:
        print(f"\n发生错误: {e}")
        if sensor:
            sensor.close()

if __name__ == "__main__":
    main()

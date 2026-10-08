# -*- coding: utf-8 -*-
"""
JUXI 心率血氧传感器 - UART 模式示例
树莓派 Python 示例代码
"""

import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from JUXI_HeartRate_SPO2 import JUXI_HeartRate_SPO2_uart

UART_PORT = '/dev/serial0'
BAUD_RATE = 9600

def setup():
    print("=" * 50)
    print("JUXI 心率血氧传感器 - UART 模式")
    print("=" * 50)
    print()
    
    print(f"正在连接串口 {UART_PORT}，波特率 {BAUD_RATE}...")
    
    try:
        sensor = JUXI_HeartRate_SPO2_uart(UART_PORT, BAUD_RATE)
    except ImportError as e:
        print(f"错误: {e}")
        print("请运行: sudo pip3 install pyserial")
        sys.exit(1)
    
    while not sensor.begin():
        print("传感器初始化失败，请检查连接！")
        print("请检查:")
        print("  1. 串口是否已启用 (sudo raspi-config -> Interface Options -> Serial)")
        print("  2. 接线是否正确 (RX-TX 交叉连接)")
        print("  3. 传感器拨片是否拨到 UART 位置")
        print("  4. 电源是否正常 (3.3V 或 5V)")
        print("  5. 是否使用 sudo 运行程序")
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

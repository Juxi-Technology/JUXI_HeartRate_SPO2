# -*- coding: utf-8 -*-
"""
JUXI_HeartRate_SPO2 - 树莓派心率血氧传感器库
支持 I2C 和 UART 两种通信方式
"""

import time
import struct

try:
    import smbus2 as smbus
except ImportError:
    try:
        import smbus
    except ImportError:
        smbus = None

try:
    import serial
except ImportError:
    serial = None


def calculate_crc(data):
    """
    计算 Modbus CRC16 校验码
    """
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for i in range(8):
            if (crc & 0x0001) != 0:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return ((crc & 0x00FF) << 8) | ((crc & 0xFF00) >> 8)


class JUXI_HeartRate_SPO2_Base:
    """
    传感器基类，定义通用接口
    """

    def __init__(self):
        self.dev_addr = 0x20
        self.SPO2 = -1
        self.heartbeat = -1
        self._is_collecting = False

    def begin(self):
        """
        初始化传感器
        返回 True 表示成功
        """
        raise NotImplementedError("子类必须实现此方法")

    def sensor_start_collect(self):
        """
        开始数据采集（传感器亮灯）
        """
        raise NotImplementedError("子类必须实现此方法")

    def sensor_end_collect(self):
        """
        停止数据采集（传感器关灯）
        """
        raise NotImplementedError("子类必须实现此方法")

    def get_heartbeat_SPO2(self):
        """
        读取心率和血氧数据
        结果存储在 self.SPO2 和 self.heartbeat 中
        """
        raise NotImplementedError("子类必须实现此方法")

    def get_temperature_c(self):
        """
        读取板载温度（摄氏度）
        """
        raise NotImplementedError("子类必须实现此方法")


class JUXI_HeartRate_SPO2_i2c(JUXI_HeartRate_SPO2_Base):
    """
    I2C 通信方式的传感器类
    """

    def __init__(self, bus_number=1, i2c_address=0x57):
        """
        初始化 I2C 传感器
        参数:
            bus_number: I2C 总线号，树莓派通常为 1
            i2c_address: 传感器 I2C 地址，默认 0x57
        """
        super().__init__()
        if smbus is None:
            raise ImportError("请先安装 smbus2 库: sudo pip3 install smbus2")

        self.bus_number = bus_number
        self.i2c_address = i2c_address
        self.bus = None

    def begin(self):
        """
        初始化 I2C 连接并检测传感器
        """
        try:
            self.bus = smbus.SMBus(self.bus_number)
            time.sleep(0.1)
            # 只要能打开 I2C 总线就认为初始化成功
            return True
        except Exception as e:
            print(f"I2C 初始化失败: {e}")
            return False

    def _write_reg(self, reg_addr, data_buf):
        """
        写寄存器
        参数:
            reg_addr: 寄存器地址（8位）
            data_buf: 要写入的数据列表
        """
        try:
            self.bus.write_i2c_block_data(self.i2c_address, reg_addr, data_buf)
            time.sleep(0.05)
        except Exception as e:
            print(f"写寄存器错误: {e}")

    def _read_reg(self, reg_addr, length):
        """
        读寄存器
        参数:
            reg_addr: 寄存器地址（8位）
            length: 要读取的字节数
        返回: 读取的数据列表
        """
        try:
            from smbus2 import i2c_msg

            self.bus.write_byte(self.i2c_address, reg_addr)

            read_msg = i2c_msg.read(self.i2c_address, length)
            self.bus.i2c_rdwr(read_msg)
            data = list(read_msg)

            return data
        except Exception as e:
            print(f"读寄存器错误: {e}")
            return []

    def sensor_start_collect(self):
        """
        开始数据采集
        """
        data_buf = [0x00, 0x01]
        self._write_reg(0x20, data_buf)
        self._is_collecting = True
        time.sleep(0.1)

    def sensor_end_collect(self):
        """
        停止数据采集
        """
        data_buf = [0x00, 0x02]
        self._write_reg(0x20, data_buf)
        self._is_collecting = False
        time.sleep(0.1)

    def get_heartbeat_SPO2(self):
        """
        读取心率和血氧数据
        """
        data = self._read_reg(0x0C, 8)

        if len(data) >= 6:
            self.SPO2 = data[0]
            if self.SPO2 == 0:
                self.SPO2 = -1

            # 心率: data[2]-data[5] (4字节大端模式)
            self.heartbeat = (data[2] << 24) | (data[3] << 16) | (data[4] << 8) | data[5]
            if self.heartbeat == 0:
                self.heartbeat = -1

    def get_temperature_c(self):
        """
        读取温度（摄氏度）
        """
        data = self._read_reg(0x14, 2)

        if len(data) >= 2:
            temperature = data[0] + data[1] / 100.0
            return temperature
        return 0.0

    def close(self):
        """
        关闭 I2C 连接
        """
        if self.bus:
            self.bus.close()


class JUXI_HeartRate_SPO2_uart(JUXI_HeartRate_SPO2_Base):
    """
    UART 串口通信方式的传感器类
    """

    def __init__(self, port='/dev/serial0', baudrate=9600):
        """
        初始化 UART 传感器
        参数:
            port: 串口设备路径，树莓派默认为 /dev/serial0
            baudrate: 波特率，默认 9600
        """
        super().__init__()
        if serial is None:
            raise ImportError("请先安装 pyserial 库: sudo pip3 install pyserial")

        self.port = port
        self.baudrate = baudrate
        self.ser = None

    def begin(self):
        """
        初始化串口连接并检测传感器
        """
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=0.5
            )
            time.sleep(0.1)
            return self._read_test()
        except Exception as e:
            print(f"UART 初始化失败: {e}")
            return False

    def _send_command(self, cmd):
        """
        发送命令
        """
        self.ser.reset_input_buffer()
        self.ser.write(bytes(cmd))
        time.sleep(0.05)

    def _read_response(self, expected_bytes=32):
        """
        读取响应
        """
        response = []
        t = time.time()
        while len(response) < expected_bytes and (time.time() - t) < 0.3:
            if self.ser.in_waiting:
                response.append(self.ser.read(1)[0])
            else:
                time.sleep(0.01)
        return response

    def _read_test(self):
        """
        测试读取
        """
        cmd = [self.dev_addr, 0x03, 0x00, 0x02, 0x00, 0x01]
        crc = calculate_crc(cmd)
        cmd.extend([(crc >> 8) & 0xFF, crc & 0xFF])
        self._send_command(cmd)
        resp = self._read_response(7)

        return len(resp) >= 7 and resp[0] == self.dev_addr and resp[1] == 0x03

    def sensor_start_collect(self):
        """
        开始数据采集
        """
        cmd = [self.dev_addr, 0x10, 0x00, 0x10, 0x00, 0x01, 0x02, 0x00, 0x01]
        crc = calculate_crc(cmd)
        cmd.extend([(crc >> 8) & 0xFF, crc & 0xFF])
        self._send_command(cmd)
        self._is_collecting = True
        time.sleep(0.1)

    def sensor_end_collect(self):
        """
        停止数据采集
        """
        cmd = [self.dev_addr, 0x10, 0x00, 0x10, 0x00, 0x01, 0x02, 0x00, 0x02]
        crc = calculate_crc(cmd)
        cmd.extend([(crc >> 8) & 0xFF, crc & 0xFF])
        self._send_command(cmd)
        self._is_collecting = False
        time.sleep(0.1)

    def get_heartbeat_SPO2(self):
        """
        读取心率和血氧数据
        """
        cmd = [self.dev_addr, 0x03, 0x00, 0x06, 0x00, 0x04]
        crc = calculate_crc(cmd)
        cmd.extend([(crc >> 8) & 0xFF, crc & 0xFF])
        self._send_command(cmd)
        resp = self._read_response(13)

        if len(resp) >= 11 and resp[0] == self.dev_addr and resp[1] == 0x03:
            self.SPO2 = resp[3]
            if self.SPO2 == 0:
                self.SPO2 = -1

            self.heartbeat = (resp[5] << 24) | (resp[6] << 16) | (resp[7] << 8) | resp[8]
            if self.heartbeat == 0:
                self.heartbeat = -1

    def get_temperature_c(self):
        """
        读取温度（摄氏度）
        """
        cmd = [self.dev_addr, 0x03, 0x00, 0x0A, 0x00, 0x01]
        crc = calculate_crc(cmd)
        cmd.extend([(crc >> 8) & 0xFF, crc & 0xFF])
        self._send_command(cmd)
        resp = self._read_response(7)

        if len(resp) >= 7 and resp[0] == self.dev_addr and resp[1] == 0x03:
            temperature = resp[3] + resp[4] / 100.0
            return temperature
        return 0.0

    def close(self):
        """
        关闭串口
        """
        if self.ser and self.ser.is_open:
            self.ser.close()
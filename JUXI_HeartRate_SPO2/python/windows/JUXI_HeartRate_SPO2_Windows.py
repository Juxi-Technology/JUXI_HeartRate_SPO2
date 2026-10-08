import serial
import time
import math
from JUXI_RTU_Windows import JUXI_RTU

DEVICE_ADDRESS = 0x20

class JUXI_HeartRate_SPO2(JUXI_RTU):
  SPO2 = 0
  heartbeat = 0
  
  BAUT_RATE_1200 = 0 
  BAUT_RATE_2400 = 1
  BAUT_RATE_9600 = 3
  BAUT_RATE_19200 = 5
  BAUT_RATE_38400 = 6 
  BAUT_RATE_57600 = 7
  BAUT_RATE_115200 = 8   
    
  def __init__(self, port, Baud=9600):
    super(JUXI_HeartRate_SPO2, self).__init__(port, Baud, 8, 'N', 1)

  def begin(self):
    rbuf = self.read_holding_registers(DEVICE_ADDRESS, 0x02, 1)
    if rbuf[0] == 0 and len(rbuf) >= 3:
      if ((rbuf[1] << 8) | rbuf[2]) == 0x0020:
        return True
    return False

  def sensor_start_collect(self):
    self.write_holding_registers(DEVICE_ADDRESS, 0x08, [0x00, 0x01])
    time.sleep(0.1)
    
  def sensor_end_collect(self):
    self.write_holding_registers(DEVICE_ADDRESS, 0x08, [0x00, 0x02])
    time.sleep(0.1)

  def get_heartbeat_SPO2(self):
    rbuf = self.read_holding_registers(DEVICE_ADDRESS, 0x03, 4)
    if rbuf[0] == 0 and len(rbuf) >= 9:
      self.SPO2 = rbuf[1]
      if self.SPO2 == 0:
        self.SPO2 = -1
      self.heartbeat = (rbuf[4] << 24) | (rbuf[5] << 16) | (rbuf[6] << 8) | rbuf[7]
      if self.heartbeat == 0:
        self.heartbeat = -1

  def get_temperature_c(self):
    rbuf = self.read_holding_registers(DEVICE_ADDRESS, 0x05, 1)
    if rbuf[0] == 0 and len(rbuf) >= 4:
      Temperature = rbuf[1] + rbuf[2] / 100.0
      return Temperature
    return 0

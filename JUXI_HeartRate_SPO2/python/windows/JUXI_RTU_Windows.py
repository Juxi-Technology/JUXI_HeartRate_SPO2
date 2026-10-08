import sys
import serial
import time
import serial.tools.list_ports

class JUXI_RTU(object):
  
  _packet_header = {"id": 0, "cmd": 1, "cs": 0}
  
  eRTU_EXCEPTION_ILLEGAL_FUNCTION     = 0x01
  eRTU_EXCEPTION_ILLEGAL_DATA_ADDRESS = 0x02
  eRTU_EXCEPTION_ILLEGAL_DATA_VALUE   = 0x03
  eRTU_EXCEPTION_SLAVE_FAILURE        = 0x04
  eRTU_EXCEPTION_CRC_ERROR            = 0x08
  eRTU_RECV_ERROR                     = 0x09
  eRTU_MEMORY_ERROR                   = 0x0A
  eRTU_ID_ERROR                       = 0x0B
  
  eCMD_READ_COILS           = 0x01
  eCMD_READ_DISCRETE        = 0x02
  eCMD_READ_HOLDING         = 0x03
  eCMD_WRITE_COILS          = 0x05
  eCMD_WRITE_HOLDING        = 0x06
  eCMD_WRITE_MULTI_COILS    = 0x0F
  eCMD_WRITE_MULTI_HOLDING  = 0x10
  
  @staticmethod
  def list_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]
  
  def __init__(self, port, baud, bits=8, parity='N', stopbit=1):
    self._port = port
    self._baud = baud
    self._bits = bits
    self._parity = parity
    self._stopbit = stopbit
    parity_map = {'N': serial.PARITY_NONE, 'E': serial.PARITY_EVEN, 'O': serial.PARITY_ODD}
    self._ser = serial.Serial(
        port=port,
        baudrate=baud,
        bytesize=bits,
        parity=parity_map.get(parity, serial.PARITY_NONE),
        stopbits=stopbit,
        timeout=0.5
    )

  def _calculate_crc(self, data):
    crc = 0xFFFF
    length = len(data)
    pos = 0
    while pos < length:
      crc ^= (data[pos] | 0x0000)
      i = 8
      while i != 0:
        if (crc & 0x0001) != 0:
          crc = (crc >> 1) & 0xFFFF
          crc ^= 0xA001
        else:
          crc = (crc >> 1) & 0xFFFF
        i -= 1
      pos += 1
    crc = (((crc & 0x00FF) << 8) | ((crc & 0xFF00) >> 8)) & 0xFFFF
    return crc

  def _clear_recv_buffer(self):
    remain = self._ser.in_waiting
    while remain:
      self._ser.read(remain)
      remain = self._ser.in_waiting

  def _packed(self, id, cmd, l):
    length = 4 + len(l)
    package = [0] * length
    package[0] = id
    package[1] = cmd
    package[2:length-2] = l

    crc = self._calculate_crc(package[:len(package)-2])
    package[length-2] = (crc >> 8) & 0xFF
    package[length-1] = crc & 0xFF
    
    return package

  def _send_package(self, l):
    self._clear_recv_buffer()
    if len(l):
      self._ser.write(bytes(l))

  def read_holding_registers(self, id, reg, size):
    l = [(reg >> 8) & 0xFF, (reg & 0xFF), (size >> 8) & 0xFF, size & 0xFF]
    if id > 0xF7:
      print("device addr error.")
      return [self.eRTU_ID_ERROR]
    l = self._packed(id, self.eCMD_READ_HOLDING, l)
    self._send_package(l)
    
    time.sleep(0.05)
    
    package = []
    head = [0] * 4
    index = 0
    t = time.time()
    remain = 0
    expected_length = 5 + size * 2 + 2
    
    while len(package) < expected_length:
      if self._ser.in_waiting:
        data = self._ser.read(1)
        package.append(data[0])
        t = time.time()
      if time.time() - t > 0.2:
        break
    
    if len(package) >= 5:
      if package[0] == id and package[1] == self.eCMD_READ_HOLDING:
        crc = ((package[-2] << 8) | package[-1]) & 0xFFFF
        calc_crc = self._calculate_crc(package[:-2])
        if crc == calc_crc:
          result = [0] + package[3:-2]
          return result
    
    return [self.eRTU_RECV_ERROR]

  def write_holding_register(self, id, reg, val):
    l = [(reg >> 8) & 0xFF, (reg & 0xFF), (val >> 8) & 0xFF, (val & 0xFF)]
    if id > 0xF7:
      print("device addr error.")
      return 0
    l = self._packed(id, self.eCMD_WRITE_HOLDING, l)
    self._send_package(l)
    return 0

  def write_holding_registers(self, id, reg, data):
    size = len(data) >> 1
    l = [(reg >> 8) & 0xFF, (reg & 0xFF), ((size >> 8) & 0xFF), (size & 0xFF), size * 2] + data
    if id > 0xF7:
      print("device addr error.")
      return 0
    l = self._packed(id, self.eCMD_WRITE_MULTI_HOLDING, l)
    self._send_package(l)
    return 0

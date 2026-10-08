#include "JUXI_HeartRate_SPO2.h"

void JUXI_HeartRate_SPO2::getHeartbeatSPO2(void)
{
  uint8_t rbuf[8];
  readReg(0x0C, rbuf, 8);
  _sHeartbeatSPO2.SPO2 = rbuf[0];
  if (_sHeartbeatSPO2.SPO2 == 0)
  {
    _sHeartbeatSPO2.SPO2 = -1;
  }
  _sHeartbeatSPO2.Heartbeat = ((uint32_t)rbuf[2] << 24) | ((uint32_t)rbuf[3] << 16) | ((uint32_t)rbuf[4] << 8) | ((uint32_t)rbuf[5]);
  if (_sHeartbeatSPO2.Heartbeat == 0)
  {
    _sHeartbeatSPO2.Heartbeat = -1;
  }
}

float JUXI_HeartRate_SPO2::getTemperature_C(void)
{
  uint8_t temp_buf[2];
  readReg(0x14, temp_buf, 2);
  float Temperature = temp_buf[0] * 1.0 + temp_buf[1] / 100.0;
  return Temperature;
}

void JUXI_HeartRate_SPO2::sensorStartCollect(void)
{
  uint8_t wbuf[2] = {0, 1};
  writeReg(0x20, wbuf, 2);
}

void JUXI_HeartRate_SPO2::sensorEndCollect(void)
{
  uint8_t wbuf[2] = {0, 2};
  writeReg(0x20, wbuf, 2);
}

JUXI_HeartRate_SPO2_I2C::JUXI_HeartRate_SPO2_I2C(TwoWire *pWire, uint8_t addr)
{
  _pWire = pWire;
  this->_I2C_addr = addr;
}

bool JUXI_HeartRate_SPO2_I2C::begin(void)
{
  _pWire->begin();
  _pWire->beginTransmission(_I2C_addr);
  if (_pWire->endTransmission() == 0)
  {
    return true;
  }
  else
  {
    return false;
  }
}

void JUXI_HeartRate_SPO2_I2C::writeReg(uint16_t reg_addr, uint8_t *data_buf, uint8_t len)
{
  _pWire->beginTransmission(this->_I2C_addr);
  _pWire->write(reg_addr);
  for (uint8_t i = 0; i < len; i++)
  {
    _pWire->write(data_buf[i]);
  }
  _pWire->endTransmission();
}

int16_t JUXI_HeartRate_SPO2_I2C::readReg(uint16_t reg_addr, uint8_t *data_buf, uint8_t len)
{
  int i = 0;
  _pWire->beginTransmission(this->_I2C_addr);
  _pWire->write(reg_addr);
  if (_pWire->endTransmission() != 0)
  {
    return -1;
  }
  _pWire->requestFrom((uint8_t)this->_I2C_addr, (uint8_t)len);
  while (_pWire->available())
  {
    data_buf[i++] = _pWire->read();
  }
  return len;
}

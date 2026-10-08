#ifndef __JUXI_HeartRate_SPO2_H__
#define __JUXI_HeartRate_SPO2_H__
#include "Arduino.h"
#include <Wire.h>

// Open this macro to see the program running in detail
#define ENABLE_DBG

#ifdef ENABLE_DBG
#define DBG(...)                 \
  {                              \
    Serial.print("[");           \
    Serial.print(__FUNCTION__);  \
    Serial.print("(): ");        \
    Serial.print(__LINE__);      \
    Serial.print(" ] ");         \
    Serial.println(__VA_ARGS__); \
  } 
#else
#define DBG(...)
#endif

class JUXI_HeartRate_SPO2
{
  public:
    /**
     * @struct sHeartbeatSPO2
     * @brief The struct for storing heart rate and oxygen saturation
     */
    typedef struct
    {
      int SPO2;
      int Heartbeat;
    } sHeartbeatSPO2;

    JUXI_HeartRate_SPO2(void){};
    ~JUXI_HeartRate_SPO2(void){};

    /**
     * @fn getHeartbeatSPO2
     * @brief Get heart rate and oxygen saturation and store them into the struct sHeartbeatSPO2
     */
    void getHeartbeatSPO2(void);

    /**
     * @fn getTemperature_C
     * @brief Get the sensor board temp
     * @return The current onboard temp (unit: ℃)
     */
    float getTemperature_C(void);

    /**
     * @fn sensorStartCollect
     * @brief Data collecting starts
     */
    void sensorStartCollect(void);

    /**
     * @fn sensorEndCollect
     * @brief Data collecting stops
     */
    void sensorEndCollect(void);
    sHeartbeatSPO2 _sHeartbeatSPO2;

  protected:
    /**
     * @fn writeReg
     * @brief Write data to the specified register of the sensor
     * @param reg_addr Register address to be written
     * @param data_buf Data to be written to register
     * @param len Length of data to be written
     */
    virtual void writeReg(uint16_t reg_addr, uint8_t *data_buf, uint8_t len) = 0;

    /**
     * @fn readReg
     * @brief Get the data with specified length from the specified sensor
     * @param reg_addr Register address to be read
     * @param data_buf The position storing the register data to be read
     * @param len Length of the data to be read
     */
    virtual int16_t readReg(uint16_t reg_addr, uint8_t *data_buf, uint8_t len) = 0;
};

class JUXI_HeartRate_SPO2_I2C : public JUXI_HeartRate_SPO2
{
  public:
    JUXI_HeartRate_SPO2_I2C(TwoWire *pWire = &Wire, uint8_t addr = 0x57);
    ~JUXI_HeartRate_SPO2_I2C(){};
    bool begin();
  protected:
    void writeReg(uint16_t reg_addr, uint8_t *data_buf, uint8_t len);
    int16_t readReg(uint16_t reg_addr, uint8_t *data_buf, uint8_t len);
  private:
    TwoWire *_pWire;
    uint8_t _I2C_addr;
};

#endif

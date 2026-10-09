[English](../../en/01-arduino/README.md) | [Deutsch](../../de/01-arduino/README.md) | Español | [Français](../../fr/01-arduino/README.md) | [Italiano](../../it/01-arduino/README.md) | [日本語](../../ja/01-arduino/README.md) | [한국어](../../ko/01-arduino/README.md) | [Português (BR)](../../pt-br/01-arduino/README.md) | [Português (PT)](../../pt-pt/01-arduino/README.md) | [简体中文](../../zh-hans/01-arduino/README.md) | [繁體中文](../../zh-hant/01-arduino/README.md)

# Tutorial del sensor de oxímetro de pulso JUXI_HeartRate_SPO2

## Índice
1. [Introducción al sensor](#sensor-introduction)
2. [Tutorial de Arduino](#arduino-tutorial)
3. [Tutorial de Python (Raspberry Pi)](#python-raspberry-pi-tutorial)
4. [Preguntas frecuentes](#faq)

---

## Introducción al sensor

JUXI_HeartRate_SPO2 es un módulo sensor de ritmo cardíaco y oxígeno en sangre basado en el chip MAX30102, con algoritmo integrado capaz de entregar directamente los valores de ritmo cardíaco y saturación de oxígeno en sangre.

**Características principales:**

- Medición de la saturación de oxígeno en sangre (SPO2)
- Medición del ritmo cardíaco (latidos por minuto)
- Medición de la temperatura a bordo
- Compatible con comunicación I2C

---

## Tutorial de Arduino

### 1. Preparación del hardware

| Materiales necesarios |
|-------------------|
| Placa de desarrollo Arduino (Uno/Nano/ESP32, etc.) |
| Sensor JUXI_HeartRate_SPO2 |
| Varios cables dupont |
| Cable de datos USB (para conectar el Arduino al PC) |

### 2. Instalación de la biblioteca

1. Descarga este archivo de biblioteca
2. Copia la carpeta `JUXI_HeartRate_SPO2` en tu directorio de bibliotecas de Arduino:
   - Windows: `C:\Users\Username\Documents\Arduino\libraries\`
   - Mac: `~/Documents/Arduino/libraries/`
   - Linux: `~/Arduino/libraries/`
3. Reinicia el Arduino IDE

### 3. Código de ejemplo

**Nota: al subir el código, conecta únicamente el Arduino al PC, ¡NO conectes el módulo de oxímetro de pulso al Arduino!**

```cpp
#include "JUXI_HeartRate_SPO2.h"

// I2C address
#define I2C_ADDRESS 0x57

// Create sensor object, I2C mode
JUXI_HeartRate_SPO2_I2C sensor(&Wire, I2C_ADDRESS);

void setup() {
  Serial.begin(9600);

  // Initialize sensor
  while (!sensor.begin()) {
    Serial.println("Sensor initialization failed, please check connection!");
    delay(1000);
  }
  Serial.println("Sensor initialized successfully!");

  // Start data collection
  sensor.sensorStartCollect();
}

void loop() {
  // Read heart rate and blood oxygen data
  sensor.getHeartbeatSPO2();

  // Output blood oxygen saturation
  Serial.print("SPO2: ");
  Serial.print(sensor._sHeartbeatSPO2.SPO2);
  Serial.println(" %");

  // Output heart rate
  Serial.print("Heart Rate: ");
  Serial.print(sensor._sHeartbeatSPO2.Heartbeat);
  Serial.println(" BPM");

  // Read and output temperature
  Serial.print("Onboard Temperature: ");
  Serial.print(sensor.getTemperature_C());
  Serial.println(" °C");

  Serial.println("------------------------");

  // Sensor updates data every 4 seconds
  delay(4000);
}
```

##### Conexión de hardware

Comunicación I2C

| Pin del sensor | Arduino |
|-----------|---------|
| VCC       | 5V/3.3V |
| GND       | GND     |
| SDA       | SDA/A4  |
| SCL       | SCL/A5  |

![IIC](../../en/01-arduino/img/IIC.png)

![8](../../en/01-arduino/img/8.png)

- ¡Cambia el interruptor DIP del módulo de oxímetro de pulso a la posición I2C!
- Usa el cable de datos para conectar el Arduino al PC

#### Resultados de ejecución:

1. Abre Arduino - Herramientas - Monitor Serie

   Configura la velocidad en baudios a 9600

![1](../../en/01-arduino/img/1.png)

2. Abre Serial Debug Assistant

[Serial Debug Assistant uartassist5.15.zip](https://juxitech.feishu.cn/wiki/BJlfwSQydi7u5lkRDQ6cV4dvnBd)

Selecciona el número de puerto serie

Configura la velocidad en baudios a `9600`

Bits de datos `8`, bits de parada `1`, paridad `NONE`, control de flujo `NONE`

En la configuración de recepción y envío, selecciona `ASCII`

![2](../../en/01-arduino/img/2.png)

### 4. Descripción de la API

| Función | Descripción |
|----------|-------------|
| `begin()` | Inicializa el sensor, devuelve true/false |
| `getHeartbeatSPO2()` | Lee los datos de ritmo cardíaco y SPO2, almacenados en la estructura `_sHeartbeatSPO2` |
| `getTemperature_C()` | Lee la temperatura a bordo (Celsius) |
| `sensorStartCollect()` | Inicia la recolección de datos (el LED del sensor se enciende) |
| `sensorEndCollect()` | Detiene la recolección de datos (el LED del sensor se apaga) |

### 5. Descripción de los datos

- **SPO2 (saturación de oxígeno en sangre)**: Rango normal 95 % - 100 %, el valor -1 indica dato no válido
- **Heartbeat (ritmo cardíaco)**: Rango normal 60 - 100 BPM, el valor -1 indica dato no válido
- **Motivos de valores no válidos**: Dedo mal colocado o datos sin estabilizar

---

## Notas de uso

### Consejos de medición

1. **Colocación correcta del dedo**
   - Coloca el dedo suavemente sobre el sensor, cubriendo ambos LED
   - No presiones con fuerza para no afectar la circulación sanguínea
   - Mantén el dedo estable, no lo muevas

2. **Espera a que los datos se estabilicen**
   - Los valores pueden ser inestables al iniciar la medición
   - Se recomienda esperar de 10 a 30 segundos para que los datos se estabilicen antes de leerlos
   - El sensor actualiza los datos cada 4 segundos

3. **Condiciones del entorno**
   - Evita la luz directa intensa sobre el sensor
   - Mantén una temperatura ambiente adecuada
   - Permanece en silencio durante la medición

### Interpretación de los datos

| Rango de SPO2 | Descripción |
|-----------|-------------|
| 95 % - 100 % | Normal |
| 90 % - 94 % | Hipoxia leve |
| < 90 % | Hipoxia, se recomienda consultar a un médico |

| Rango de ritmo cardíaco | Descripción |
|-----------------|-------------|
| 60 - 100 BPM | Rango normal en adultos |
| < 60 BPM | Bradicardia |
| > 100 BPM | Taquicardia |

---

## Preguntas frecuentes

### P1: ¿Falla la inicialización del sensor?

**R:**
1. Comprueba si el cableado es correcto (SDA a GPIO2/A4, SCL a GPIO3/A5)
2. Confirma que la alimentación sea normal (3.3V o 5V)
3. Usa el comando `i2cdetect -y 1` para detectar el dispositivo
4. Asegúrate de que el interruptor DIP del sensor esté en la posición IIC

### P2: ¿Los datos siempre muestran -1?

**R:**
1. Confirma que el dedo esté bien colocado sobre el sensor
2. Espera unos segundos para que los datos se estabilicen
3. Comprueba si se ha llamado a `sensorStartCollect()` para iniciar la recolección
4. Confirma que la luz indicadora del sensor esté encendida

### P3: ¿Los datos son imprecisos?

**R:**
1. Asegúrate de que el dedo cubra por completo el área óptica del sensor
2. Mantén el dedo quieto, no lo muevas
3. Espera más de 30 segundos para que los datos se estabilicen
4. Realiza varias mediciones y promedia

### P4: ¿Qué placas de desarrollo Arduino son compatibles?

**R:** Compatibles:
- Arduino Uno/Nano/Mega
- ESP8266
- ESP32
- Otras placas de desarrollo compatibles con el entorno Arduino

---

## Ubicación de los archivos de ejemplo

### Ejemplos de Arduino
```
JUXI_HeartRate_SPO2/
└── examples/
    └── gainHeartbeatSPO2/
        └── gainHeartbeatSPO2.ino
```

[English](../../en/02-raspberry-pi/README.md) | [Deutsch](../../de/02-raspberry-pi/README.md) | Español | [Français](../../fr/02-raspberry-pi/README.md) | [Italiano](../../it/02-raspberry-pi/README.md) | [日本語](../../ja/02-raspberry-pi/README.md) | [한국어](../../ko/02-raspberry-pi/README.md) | [Português (BR)](../../pt-br/02-raspberry-pi/README.md) | [Português (PT)](../../pt-pt/02-raspberry-pi/README.md) | [简体中文](../../zh-hans/02-raspberry-pi/README.md) | [繁體中文](../../zh-hant/02-raspberry-pi/README.md)

# Tutorial de Raspberry Pi para JUXI_HeartRate_SPO2


## Índice

1. [Introducción](#introduction)
2. [Requisitos de hardware](#hardware-requirements)
3. [Conexiones de hardware](#hardware-connections)
4. [Configuración del entorno](#environment-setup)
5. [Uso del código de ejemplo](#example-code-usage)
6. [Referencia de la API](#api-reference)
7. [Preguntas frecuentes](#faq)
8. [Notas importantes](#important-notes)

---

## Introducción

JUXI_HeartRate_SPO2 es un módulo sensor de ritmo cardíaco y oxígeno en sangre basado en el chip MAX30102. Incluye algoritmos integrados que entregan directamente los valores de ritmo cardíaco y saturación de oxígeno en sangre.

**Características principales:**
- Medición de la saturación de oxígeno en sangre (SPO2)
- Medición del ritmo cardíaco (latidos por minuto)
- Medición de la temperatura a bordo
- Compatible con comunicación UART e I2C

---

## Requisitos de hardware

| Elemento necesario | Descripción |
|--------------|-------------|
| Raspberry Pi (2/3/4/Zero) | Se recomienda Raspberry Pi 3B+ o 4B |
| Sensor JUXI_HeartRate_SPO2 | Módulo sensor de ritmo cardíaco y oxígeno en sangre |
| Cables dupont | 4 cables puente hembra-hembra |
| Adaptador de alimentación | Fuente de alimentación para Raspberry Pi |

---

## Conexiones de hardware

### Método 1: Comunicación I2C (recomendado)

La comunicación I2C tiene un cableado sencillo y es la recomendada.

| Pin del sensor | Pin físico de la Raspberry Pi | Número BCM | Descripción |
|-----------|--------------------------|-----------|-------------|
| VCC | 1 o 17 | - | Alimentación de 3.3V (también se acepta 5V) |
| GND | 6 o 9 o 14 | - | Tierra |
| SDA | 3 | GPIO2 | Línea de datos I2C |
| SCL | 5 | GPIO3 | Línea de reloj I2C |

**Importante:** ¡Cambia el interruptor del sensor a la posición **IIC**!

### Método 2: Comunicación serie UART

La comunicación UART requiere conexión cruzada.

| Pin del sensor | Pin físico de la Raspberry Pi | Número BCM | Descripción |
|-----------|--------------------------|-----------|-------------|
| VCC | 2 o 4 | - | Alimentación de 5V (también se acepta 3.3V) |
| GND | 6 o 9 o 14 | - | Tierra |
| RX | 8 | GPIO14 | El RX del sensor se conecta al TX de la Raspberry Pi |
| TX | 10 | GPIO15 | El TX del sensor se conecta al RX de la Raspberry Pi |

**Importante:** ¡Cambia el interruptor del sensor a la posición **UART**!

![diagrama de pines de Raspberry Pi](../../en/02-raspberry-pi/Raspberry%20Pi%20Pin%20Diagram.png)

---

## Configuración del entorno

### 1. Habilitar I2C (necesario para el modo I2C)

```bash
sudo raspi-config
```

Selecciona `Interface Options` → `I2C` → Selecciona `Yes` para habilitarlo

Reinicia la Raspberry Pi:
```bash
sudo reboot
```

### 2. Habilitar el puerto serie (necesario para el modo UART)

```bash
sudo raspi-config
```

Selecciona `Interface Options` → `Serial`

- Primera pregunta: "Would you like a login shell to be accessible over serial?" → Selecciona `No`
- Segunda pregunta: "Would you like the serial port hardware to be enabled?" → Selecciona `Yes`

Reinicia la Raspberry Pi:
```bash
sudo reboot
```

### 3. Instalar dependencias

```bash
# Update package lists
sudo apt-get update

# Install I2C tools and smbus2 library (smbus2 is required for I2C mode)
sudo apt-get install -y i2c-tools python3-smbus2

# Install pyserial (for serial port support)
sudo pip3 install pyserial
```

> **Nota:** El modo I2C requiere `smbus2`; el paquete heredado `python-smbus` no es suficiente.
> La biblioteca usa `smbus2.i2c_msg` para realizar dos transacciones I2C independientes (escribir la
> dirección del registro con STOP y luego una nueva transacción de lectura para leer varios bytes de
> forma secuencial), en consonancia con la temporización I2C que requiere el chip del sensor.

### 4. Verificar la conexión I2C (modo I2C)

Después del cableado, ejecuta el siguiente comando para detectar dispositivos I2C:

```bash
i2cdetect -y 1
```

Si ves la dirección `0x57`, el sensor se ha conectado correctamente.

---

## Uso del código de ejemplo

### Estructura de archivos

```
python/raspberry/
├── JUXI_HeartRate_SPO2.py      # Main library file
└── examples/
    ├── i2c_example.py          # I2C mode example
    └── uart_example.py         # UART mode example
```

### Ejecutar el ejemplo del modo I2C

```bash
cd python/raspberry/examples
sudo python3 i2c_example.py
```

### Ejecutar el ejemplo del modo UART

```bash
cd python/raspberry/examples
sudo python3 uart_example.py
```

**Nota:** Se requiere permiso `sudo` para acceder al puerto serie de hardware.

### Salida esperada

Si todo funciona correctamente, verás una salida similar a:

```
==================================================
JUXI Heart Rate & Blood Oxygen Sensor - I2C Mode
==================================================

Initializing I2C bus 1, address 0x57...
Sensor initialized successfully!

Starting data collection...
Sensor LED is now ON!

Please place your finger on the sensor...

----------------------------------------
SPO2: 98 %
Heart Rate: 72 Times/min
Onboard Temperature: 25.5 °C
----------------------------------------
...
```

Pulsa `Ctrl+C` para detener el programa.

---

## Referencia de la API

### Clase: JUXI_HeartRate_SPO2_i2c

Clase de sensor para comunicación I2C.

#### Constructor
```python
JUXI_HeartRate_SPO2_i2c(bus_number=1, i2c_address=0x57)
```

Parámetros:
- `bus_number`: número del bus I2C, normalmente 1 en la Raspberry Pi
- `i2c_address`: dirección I2C del sensor, por defecto 0x57

#### Métodos

| Método | Descripción | Valor de retorno |
|--------|-------------|--------------|
| `begin()` | Inicializa el sensor y comprueba la conexión | bool (True si tiene éxito) |
| `sensor_start_collect()` | Inicia la recolección de datos (LED del sensor encendido) | None |
| `sensor_end_collect()` | Detiene la recolección de datos (LED del sensor apagado) | None |
| `get_heartbeat_SPO2()` | Lee los datos de ritmo cardíaco y SPO2 | None (los resultados se guardan en las propiedades del objeto) |
| `get_temperature_c()` | Lee la temperatura a bordo | float (Celsius) |
| `close()` | Cierra la conexión I2C | None |

#### Propiedades

| Propiedad | Descripción |
|----------|-------------|
| `SPO2` | Saturación de oxígeno en sangre (%), -1 para valor no válido |
| `heartbeat` | Ritmo cardíaco (latidos por minuto), -1 para valor no válido |

---

### Clase: JUXI_HeartRate_SPO2_uart

Clase de sensor para comunicación serie UART.

#### Constructor
```python
JUXI_HeartRate_SPO2_uart(port='/dev/serial0', baudrate=9600)
```

Parámetros:
- `port`: ruta del dispositivo serie, por defecto `/dev/serial0` en la Raspberry Pi
- `baudrate`: velocidad en baudios, por defecto 9600

#### Métodos

Igual que `JUXI_HeartRate_SPO2_i2c`.

---

## Preguntas frecuentes

### P1: ¿Qué debo hacer si falla la inicialización del sensor?

**R:** Sigue estos pasos:

1. **Comprueba el cableado**
   - Modo I2C: Verifica que SDA se conecte a GPIO2 y SCL a GPIO3
   - Modo UART: Verifica la conexión cruzada RX-TX

2. **Comprueba el interruptor del sensor**
   - Modo I2C: el interruptor debe estar en la posición IIC
   - Modo UART: el interruptor debe estar en la posición UART

3. **Comprueba la alimentación**
   - Verifica que VCC se conecte a 3.3V o 5V
   - Verifica que GND esté conectado

4. **Comprueba la configuración del sistema**
   - Modo I2C: Verifica que I2C esté habilitado
   - Modo UART: Verifica que el puerto serie esté habilitado

5. **Usa los comandos de detección**
   ```bash
   # I2C mode
   i2cdetect -y 1
   
   # UART mode
   ls /dev/serial*
   ```

### P2: Los datos siempre muestran -1, ¿qué debo hacer?

**R:**

1. Asegúrate de que el dedo esté bien colocado sobre el sensor, cubriendo por completo ambos LED
2. Espera unos segundos para que los datos se estabilicen (normalmente de 10 a 30 segundos)
3. Comprueba si se ha llamado a `sensor_start_collect()` para iniciar la recolección
4. Verifica que el LED del sensor esté encendido

### P3: Los datos son imprecisos, ¿qué debo hacer?

**R:**

1. Asegúrate de que el dedo cubra por completo el área óptica del sensor
2. Mantén el dedo quieto, no lo muevas
3. Espera más de 30 segundos para que los datos se estabilicen
4. Realiza varias mediciones y promedia
5. Evita la luz directa intensa sobre el sensor

### P4: ¿Puedo usar I2C y UART al mismo tiempo?

**R:** No, solo se puede seleccionar un método de comunicación a la vez.

### P5: ¿Necesito usar sudo para ejecutarlo?

**R:**
- Modo I2C: se recomienda usar sudo para evitar problemas de permisos
- Modo UART: sudo es obligatorio; de lo contrario, no podrás acceder al puerto serie

---

## Notas importantes

### Consejos de medición

1. **Colocación correcta del dedo**
   - Coloca el dedo suavemente sobre el sensor, cubriendo ambos LED
   - No presiones con demasiada fuerza, ya que puede afectar la circulación sanguínea
   - Mantén el dedo estable, no lo muevas

2. **Espera a que los datos se estabilicen**
   - Los valores pueden ser inestables al iniciar la medición
   - Se recomienda esperar de 10 a 30 segundos para que los datos se estabilicen
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
| < 90 % | Hipoxia, consulta a un médico |

| Rango de ritmo cardíaco | Descripción |
|-----------------|-------------|
| 60 - 100 BPM | Rango normal en adultos |
| < 60 BPM | Bradicardia |
| > 100 BPM | Taquicardia |

### Aviso de seguridad

- Este sensor es solo de referencia y no puede sustituir equipos médicos profesionales
- Si tienes problemas de salud, consulta a un médico cuanto antes
- Los resultados de medición son solo de referencia y no deben usarse para diagnóstico

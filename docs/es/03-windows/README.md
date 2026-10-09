[English](../../en/03-windows/README.md) | [Deutsch](../../de/03-windows/README.md) | Español | [Français](../../fr/03-windows/README.md) | [Italiano](../../it/03-windows/README.md) | [日本語](../../ja/03-windows/README.md) | [한국어](../../ko/03-windows/README.md) | [Português (BR)](../../pt-br/03-windows/README.md) | [Português (PT)](../../pt-pt/03-windows/README.md) | [简体中文](../../zh-hans/03-windows/README.md) | [繁體中文](../../zh-hant/03-windows/README.md)

# Sensor de oxímetro de pulso JUXI - Guía de usuario para Windows

## Índice
1. [Preparación del hardware](#hardware-preparation)
2. [Conexión del hardware](#hardware-connection)
3. [Configuración del entorno de software](#software-environment-setup)
4. [Ejecutar el programa de ejemplo](#running-the-example-program)
5. [Preguntas frecuentes](#faq)

---

## Preparación del hardware

### Materiales necesarios

| Elemento | Descripción |
|------|-------------|
| Sensor JUXI_HeartRate_SPO2 | Módulo de oxímetro de pulso |
| Módulo USB a TTL | CH340 / CP2102 / FT232, etc. |
| Cables dupont | 4 unidades (hembra a hembra) |
| PC con Windows | Win7/Win10/Win11 |

---

## Conexión del hardware

### Método de cableado

| Pin del sensor | Pin del USB a TTL | Descripción |
|-----------|---------------|-------------|
| **VCC** | 3.3V o 5V | Positivo de alimentación |
| **GND** | GND | Negativo de alimentación |
| **TX** | RX | Transmisión del sensor → recepción del módulo |
| **RX** | TX | Recepción del sensor → transmisión del módulo |

![Connect PC](../../en/03-windows/Connect%20PC.png)

⚠️ **Consejos importantes**:

1. **¡Cambia el interruptor DIP del módulo a la posición UART!**
2. **¡TX y RX deben conectarse de forma cruzada!**
3. El sensor admite tanto 3.3V como 5V; no conectes un voltaje incorrecto
4. Conecta todos los cables primero y luego enchufa el USB al PC

### Diagrama de cableado

```
Sensor        USB to TTL Module
┌──────┐      ┌──────────┐
│ VCC  │──────│ 3.3V/5V  │
│ GND  │──────│ GND      │
│ TX   │──────│ RX       │  ← Cross connection
│ RX   │──────│ TX       │  ← Cross connection
└──────┘      └──────────┘
```

---

## Configuración del entorno de software

### 1. Instalar los controladores

Según el modelo de chip de tu módulo USB a TTL, instala el controlador correspondiente:

- **CH340**: https://sparks.gogo.co.nz/ch340.html
- **CP2102**: https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers
- **FT232**: https://ftdichip.com/drivers/vcp-drivers/

Después de la instalación, enchufa el módulo USB a TTL.

### 2. Ver el puerto COM

#### Método 1: Administrador de dispositivos
1. Pulsa `Win + X` y selecciona "Administrador de dispositivos"
2. Expande "Puertos (COM y LPT)"
3. Consulta el número de puerto COM correspondiente a tu USB a TTL (por ejemplo, COM3)

#### Método 2: Detección automática del programa
Al ejecutar el programa de ejemplo, se listarán automáticamente todos los puertos serie disponibles.

### 3. Instalar las dependencias de Python

Abre el Símbolo del sistema (CMD) o PowerShell y ejecuta:

```bash
pip install pyserial
```

---

## Ejecutar el programa de ejemplo

### Ubicación de los archivos

```
JUXI_HeartRate_SPO2/python/windows/
├── gain_heartbeat_SPO2.py  ← Main program (run this)
├── JUXI_HeartRate_SPO2_Windows.py
├── JUXI_RTU_Windows.py
└── README.md                ← This file
```

### Pasos de ejecución

1. **Confirma que la conexión de hardware sea correcta**
   - VCC → 3.3V/5V
   - GND → GND
   - TX → RX (cruzado)
   - RX → TX (cruzado)

2. **Enchufa el USB al PC**

3. **Ejecuta el programa**
   ```bash
   cd D:\JUXI_HeartRate_SPO2\python\windows
   python gain_heartbeat_SPO2.py
   ```

4. **Sigue las indicaciones**
   
   - El programa listará todos los puertos serie disponibles
   - Introduce el número de puerto COM (por ejemplo, COM3)
   - El programa detectará automáticamente el sensor e iniciará la medición

### Salida esperada

```
==================================================
JUXI Blood Oxygen Sensor - Windows Test
==================================================
Available serial ports:
  COM3

Please enter the COM port number (e.g., COM3):
> COM3

Connecting to COM3 at 9600 baud...
Initializing sensor...
Sensor initialized successfully!

Starting data collection...
Sensor LED should be ON now!

Place your finger on the sensor...

----------------------------------------
SPO2: 97 %
Heart Rate: 82 BPM
Temperature: 26.5 °C
----------------------------------------
SPO2: 98 %
Heart Rate: 78 BPM
Temperature: 26.6 °C
...
```

Pulsa `Ctrl + C` para detener el programa.

---

## Descripción de las funciones del programa

### API principal

```python
# Create sensor object
sensor = BloodOxygenSensor("COM3", 9600)

# Initialize sensor
sensor.begin()

# Start collection (LED turns on)
sensor.sensor_start_collect()

# Read heart rate and SPO2
sensor.get_heartbeat_SPO2()
print(f"SPO2: {sensor.SPO2}%")
print(f"Heart Rate: {sensor.heartbeat} BPM")

# Read temperature
temp = sensor.get_temperature_c()

# Stop collection (LED turns off)
sensor.sensor_end_collect()

# Close serial port
sensor.close()
```

---

## Preguntas frecuentes

### P1: ¿No se encuentra el puerto COM?

**R:**

1. Comprueba si el USB a TTL está bien enchufado
2. Reinstala el controlador
3. Prueba con otro puerto USB
4. Busca "Dispositivos desconocidos" en el Administrador de dispositivos

### P2: ¿Falla la inicialización del sensor?

**R:**

1. Comprueba el cableado:
   - ¿Están VCC y GND conectados correctamente?
   - **¿Están TX y RX conectados de forma cruzada?** (el problema más común)
2. Confirma que la velocidad en baudios sea 9600
3. Comprueba si el módulo USB a TTL funciona correctamente
4. Vuelve a enchufar el USB

### P3: ¿Los datos siempre muestran -1?

**R:**
1. Confirma que el dedo esté bien colocado sobre el sensor (cubriendo por completo el área del LED)
2. Mantén el dedo estable, no lo muevas
3. Espera unos segundos para que los datos se estabilicen
4. Comprueba si el LED del sensor está encendido

### P4: ¿El LED no se enciende pero la comunicación funciona?

**R:**

- Puede ser un problema de hardware del LED, pero el sensor funciona con normalidad
- Mientras los datos sean correctos, se puede ignorar que el LED no se encienda

### P5: ¿El puerto serie está ocupado?

**R:**
1. Cierra otro software serie (asistente serie, Arduino IDE, etc.)
2. Comprueba si hay otros programas de Python en ejecución
3. Vuelve a enchufar el USB

### P6: ¿Los datos son imprecisos?

**R:**
1. Asegúrate de que el dedo cubra por completo el área óptica del sensor
2. Permanece en silencio durante la medición, no hables ni te muevas
3. Espera más de 30 segundos para que los datos se estabilicen
4. Realiza varias mediciones y promedia

---

## Especificaciones técnicas

| Parámetro | Especificación |
|-----------|--------------|
| Comunicación | UART (nivel TTL) |
| Velocidad en baudios | 9600 bps (por defecto) |
| Formato de datos | 8N1 (8 bits de datos, sin paridad, 1 bit de parada) |
| Alimentación | 3.3V / 5V |
| Rango de SPO2 | 35 % - 100 % |
| Rango de ritmo cardíaco | 30 - 250 BPM |
| Dirección Modbus | 0x20 |

---

## Descripción de los registros Modbus

| Dirección del registro | Función | Descripción |
|-----------------|----------|-------------|
| 0x02 | ID del dispositivo | Lectura: devuelve 0x0020 |
| 0x06-0x09 | Datos de ritmo cardíaco y SPO2 | Lectura: SPO2 + ritmo cardíaco |
| 0x0A | Temperatura | Lectura: temperatura a bordo |
| 0x10 | Control de recolección | Escritura: 0x0001=iniciar, 0x0002=detener |

---

## Contáctanos

Si tienes preguntas o sugerencias, visita:
- GitHub: https://github.com/Juxi-Technology/JUXI_HeartRate_SPO2

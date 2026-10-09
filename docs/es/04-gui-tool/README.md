[English](../../en/04-gui-tool/README.md) | [Deutsch](../../de/04-gui-tool/README.md) | Español | [Français](../../fr/04-gui-tool/README.md) | [Italiano](../../it/04-gui-tool/README.md) | [日本語](../../ja/04-gui-tool/README.md) | [한국어](../../ko/04-gui-tool/README.md) | [Português (BR)](../../pt-br/04-gui-tool/README.md) | [Português (PT)](../../pt-pt/04-gui-tool/README.md) | [简体中文](../../zh-hans/04-gui-tool/README.md) | [繁體中文](../../zh-hant/04-gui-tool/README.md)

# Módulo de oxímetro de pulso - Guía de usuario de la GUI

## 📋 Características

Este es un programa gráfico de monitoreo de ritmo cardíaco y oxígeno en sangre con las siguientes características:

1. ✅ **Selección de puerto serie** - Escanea automáticamente los puertos serie disponibles
2. ✅ **Selección de velocidad en baudios** - Admite 9600/19200/38400/57600/115200
3. ✅ **Conectar/Desconectar** - Conecta y desconecta el módulo con un clic
4. ✅ **Iniciar/Detener recolección** - Controla el encendido y apagado del LED del sensor
5. ✅ **Iniciar/Detener monitoreo** - Visualización de datos en tiempo real
6. ✅ **Visualización de datos en tiempo real** - Oxígeno en sangre, ritmo cardíaco, temperatura
7. ✅ **Cambio entre inglés / chino** - Cambia el idioma de la interfaz en cualquier momento; el inglés es el predeterminado

---

## 🔌 Conexión de hardware

| Módulo de oxímetro de pulso | Módulo USB a TTL |
|---------------------------|------------------|
| **VCC** | **5V** (¡Importante! No usar 3.3V) |
| **GND** | **GND** |
| **TX** | **RX** (conexión cruzada) |
| **RX** | **TX** (conexión cruzada) |

⚠️ **Nota: ¡TX y RX deben conectarse de forma cruzada!**

---

## 🚀 Ejecutar el programa

### Método 1: Ejecutar el script de Python directamente

1. Instala las dependencias:
```bash
pip install pyserial
```

2. Ejecuta el programa:
```bash
cd 上位机源代码
python HeartRateOximeter.py
```

---

## 📖 Pasos de uso

### Paso 1: Conectar el hardware
1. Conecta el sensor y el USB a TTL según la tabla de cableado anterior

   VCC -> VCC

   GND -> GND

   RX -> TX

   TX -> RX

2. Enchufa el USB a TTL en un puerto USB del PC

### Paso 2: Abrir el programa
Ejecuta `HeartRateOximeter.exe`

### Paso 3: Configuración del puerto serie
1. Selecciona el puerto serie correcto (por ejemplo, COM3)
2. Selecciona la velocidad en baudios **9600** (por defecto)
3. Haz clic en el botón [Connect]

### Paso 4: Iniciar la recolección
1. Después de conectar correctamente, haz clic en [Start Collection]
2. ✅ El LED del sensor se encenderá

### Paso 5: Iniciar el monitoreo
1. Coloca el dedo sobre el sensor
2. Haz clic en [Start Monitoring]
3. Consulta los datos en tiempo real

---

## 📊 Descripción de la interfaz

```
┌─────────────────────────────────────────┐
│  Language:               [English ↓]    │
├─────────────────────────────────────────┤
│         Serial Port Settings            │
│  Port:   [COM3  ↓]  [Refresh]          │
│  Baud:   [9600  ↓]  [Connect]          │
├─────────────────────────────────────────┤
│         Module Control                  │
│  [Start Collection]  [Start Monitoring] │
├─────────────────────────────────────────┤
│         Real-time Data                  │
│  SPO2:              98 %                │
│  Heart Rate:        75 BPM              │
│  Temperature:       36.6 °C             │
│  Status:  Monitoring...                 │
├─────────────────────────────────────────┤
│         Usage Tips                      │
│  1. Wiring: VCC->5V, GND->GND, RX->TX, TX->RX  │
│  2. Click Connect before starting collection     │
│  3. Sensor LED turns on after collection starts  │
└─────────────────────────────────────────┘
```

**Cambio de idioma**: el menú desplegable situado en la parte superior de la ventana cambia la interfaz entre inglés y 中文. El programa se inicia en inglés.

---

## 📋 Interpretación de los datos

| Dato | Rango normal | Descripción |
|------|-------------|-------------|
| **SPO2** | 95 % - 100 % | Consulta a un médico si está por debajo del 90 % |
| **Ritmo cardíaco** | 60 - 100 BPM | Rango normal en adultos |
| **Temperatura** | 25 - 35 °C | Temperatura a bordo del módulo, no temperatura corporal |

**Nota**: Justo al iniciar o si el dedo no está bien colocado, los datos pueden mostrar -1, lo cual es normal.

---

## ❓ Preguntas frecuentes

### P1: ¿No se encuentra el puerto serie?
**R:**
1. Comprueba si el controlador del USB a TTL está instalado correctamente
2. Vuelve a enchufar el cable USB
3. Haz clic en el botón [Refresh] para volver a escanear

### P2: ¿Falla la conexión?
**R:**
1. Confirma que hayas seleccionado el puerto serie correcto
2. Confirma que el puerto serie no esté ocupado por otro programa (por ejemplo, un asistente serie o el Arduino IDE)
3. Comprueba si el módulo USB a TTL funciona correctamente

### P3: ¿El LED no se enciende después de hacer clic en Start Collection?
**R:**
1. Comprueba si VCC está conectado a 5V (no a 3.3V)
2. Comprueba si TX/RX están conectados de forma cruzada
3. Confirma que el propio módulo sensor no esté dañado

### P4: ¿Los datos siempre muestran -1?
**R:**
1. Confirma que se haya hecho clic en [Start Collection]
2. Coloca el dedo correctamente sobre el sensor, cubriendo por completo el área del LED
3. Mantén el dedo estable y espera unos segundos
4. Comprueba si hay conexiones flojas

### P5: ¿El programa no responde?
**R:**
1. Haz clic primero en [Stop Monitoring]
2. Luego haz clic en [Stop Collection]
3. Por último, haz clic en [Disconnect]
4. Reinicia el programa

---

## ⚠️ Precauciones

1. **Orden de conexión**: conecta primero el sensor y luego enchufa el USB
2. **Orden de desconexión**: detén el monitoreo, luego detén la recolección y por último desconecta
3. **Requisito de alimentación**: el sensor debe conectarse a una alimentación de 5V; con 3.3V puede no funcionar correctamente
4. **Colocación del dedo**: el dedo debe cubrir por completo el área óptica, no presiones con fuerza
5. **Requisito del entorno**: evita la luz directa intensa sobre el sensor

---

## 📞 Soporte técnico

Si encuentras problemas, comprueba lo siguiente:
1. Cableado de hardware correcto (especialmente el cruce de TX/RX)
2. La alimentación es de 5V
3. El controlador del USB a TTL funciona correctamente
4. El puerto serie no está ocupado por otros programas

[English](../../en/01-arduino/README.md) | Deutsch | [Español](../../es/01-arduino/README.md) | [Français](../../fr/01-arduino/README.md) | [Italiano](../../it/01-arduino/README.md) | [日本語](../../ja/01-arduino/README.md) | [한국어](../../ko/01-arduino/README.md) | [Português (BR)](../../pt-br/01-arduino/README.md) | [Português (PT)](../../pt-pt/01-arduino/README.md) | [简体中文](../../zh-hans/01-arduino/README.md) | [繁體中文](../../zh-hant/01-arduino/README.md)

# JUXI_HeartRate_SPO2 Sensor-Tutorial für Herzfrequenz und Blutsauerstoff

## Inhaltsverzeichnis
1. [Einführung in den Sensor](#einführung-in-den-sensor)
2. [Arduino-Tutorial](#arduino-tutorial)
3. [Python-Tutorial (Raspberry Pi)](#python-tutorial-raspberry-pi)
4. [FAQ](#faq)

---

## Einführung in den Sensor

JUXI_HeartRate_SPO2 ist ein Herzfrequenz- und Blutsauerstoff-Sensormodul auf Basis des MAX30102-Chips mit integriertem Algorithmus, der Herzfrequenz und Blutsauerstoffsättigung direkt ausgeben kann.

**Hauptmerkmale:**

- Messung der Blutsauerstoffsättigung (SPO2)
- Herzfrequenzmessung (Schläge pro Minute)
- Integrierte Temperaturmessung
- Unterstützt I2C-Kommunikation

---

## Arduino-Tutorial

### 1. Hardware-Vorbereitung

| Benötigtes Material |
|---------------------|
| Arduino-Entwicklungsboard (Uno/Nano/ESP32 usw.) |
| JUXI_HeartRate_SPO2 Sensor |
| Mehrere Dupont-Kabel |
| USB-Datenkabel (Arduino mit Computer verbinden) |

### 2. Installation der Bibliothek

1. Diese Bibliotheksdatei herunterladen
2. Den Ordner `JUXI_HeartRate_SPO2` in Ihr Arduino-Bibliotheksverzeichnis kopieren:
   - Windows: `C:\Users\Username\Documents\Arduino\libraries\`
   - Mac: `~/Documents/Arduino/libraries/`
   - Linux: `~/Arduino/libraries/`
3. Arduino IDE neu starten

### 3. Beispielcode

**Hinweis: Beim Hochladen des Codes darf nur der Arduino mit dem Computer verbunden werden, NICHT das Herzfrequenz-Oximeter-Modul mit dem Arduino verbinden!!!**

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

##### Hardwareanschluss

I2C-Kommunikation

| Sensor-Pin | Arduino |
|-----------|---------|
| VCC       | 5V/3.3V |
| GND       | GND     |
| SDA       | SDA/A4  |
| SCL       | SCL/A5  |

![IIC](../../en/01-arduino/img/IIC.png)

![8](../../en/01-arduino/img/8.png)

- Den DIP-Schalter des Herzfrequenz-Oximeter-Moduls auf die Position I2C stellen!!!
- Mit dem Datenkabel den Arduino mit dem Computer verbinden

#### Ausgabeergebnisse:

1. Arduino öffnen - Werkzeuge - Serieller Monitor

   Baudrate auf 9600 einstellen

![1](../../en/01-arduino/img/1.png)

2. Seriellen Debug-Assistenten öffnen

[Serial Debug Assistant uartassist5.15.zip](https://juxitech.feishu.cn/wiki/BJlfwSQydi7u5lkRDQ6cV4dvnBd)

Serielle Portnummer auswählen

Baudrate auf `9600` einstellen

Datenbits `8`, Stoppbits `1`, Parität `NONE`, Flusskontrolle `NONE`

Empfangs- und Sendeeinstellungen auf `ASCII` setzen

![2](../../en/01-arduino/img/2.png)

### 4. API-Beschreibung

| Funktion | Beschreibung |
|----------|-------------|
| `begin()` | Sensor initialisieren, gibt true/false zurück |
| `getHeartbeatSPO2()` | Herzfrequenz- und SPO2-Daten lesen, gespeichert in der Struktur `_sHeartbeatSPO2` |
| `getTemperature_C()` | Integrierte Temperatur lesen (Celsius) |
| `sensorStartCollect()` | Datenerfassung starten (Sensor-LED leuchtet auf) |
| `sensorEndCollect()` | Datenerfassung stoppen (Sensor-LED erlischt) |

### 5. Datenbeschreibung

- **SPO2 (Blutsauerstoffsättigung)**: Normalbereich 95% - 100%, Wert -1 bedeutet ungültig
- **Heartbeat (Herzfrequenz)**: Normalbereich 60 - 100 BPM, Wert -1 bedeutet ungültig
- **Gründe für ungültige Werte**: Finger nicht richtig aufgelegt oder Daten noch nicht stabil

---

## Verwendungshinweise

### Messtipps

1. **Finger richtig auflegen**
   - Den Finger sanft auf den Sensor legen, sodass beide LEDs bedeckt sind
   - Nicht fest drücken, um die Blutzirkulation nicht zu beeinträchtigen
   - Den Finger ruhig halten, nicht bewegen

2. **Auf Stabilisierung der Daten warten**
   - Die Werte können zu Beginn der Messung instabil sein
   - Es wird empfohlen, 10–30 Sekunden zu warten, bis sich die Daten stabilisiert haben, bevor Werte abgelesen werden
   - Der Sensor aktualisiert die Daten alle 4 Sekunden

3. **Umgebungsanforderungen**
   - Starkes direktes Licht auf den Sensor vermeiden
   - Eine geeignete Umgebungstemperatur einhalten
   - Während der Messung ruhig bleiben

### Interpretation der Daten

| SPO2-Bereich | Beschreibung |
|-----------|-------------|
| 95% - 100% | Normal |
| 90% - 94% | Leichte Hypoxie |
| < 90% | Hypoxie, ärztliche Beratung empfohlen |

| Herzfrequenzbereich | Beschreibung |
|-----------------|-------------|
| 60 - 100 BPM | Normalbereich für Erwachsene |
| < 60 BPM | Bradykardie |
| > 100 BPM | Tachykardie |

---

## FAQ

### Frage 1: Sensorinitialisierung fehlgeschlagen?

**Antwort:**
1. Prüfen, ob die Verkabelung korrekt ist (SDA an GPIO2/A4, SCL an GPIO3/A5)
2. Sicherstellen, dass die Stromversorgung in Ordnung ist (3,3V oder 5V)
3. Mit dem Befehl `i2cdetect -y 1` nach Geräten suchen
4. Sicherstellen, dass der DIP-Schalter des Sensors auf der Position IIC steht

### Frage 2: Die Daten zeigen immer -1 an?

**Antwort:**
1. Sicherstellen, dass der Finger richtig auf dem Sensor liegt
2. Einige Sekunden warten, bis sich die Daten stabilisiert haben
3. Prüfen, ob `sensorStartCollect()` aufgerufen wurde, um die Erfassung zu starten
4. Sicherstellen, dass die Kontrollleuchte des Sensors leuchtet

### Frage 3: Die Daten sind ungenau?

**Antwort:**
1. Sicherstellen, dass der Finger den optischen Bereich des Sensors vollständig bedeckt
2. Den Finger ruhig halten, nicht bewegen
3. Mehr als 30 Sekunden warten, bis sich die Daten stabilisiert haben
4. Mehrere Messungen durchführen und den Mittelwert bilden

### Frage 4: Welche Arduino-Entwicklungsboards werden unterstützt?

**Antwort:** Unterstützt werden:
- Arduino Uno/Nano/Mega
- ESP8266
- ESP32
- Andere Entwicklungsboards, die die Arduino-Umgebung unterstützen

---

## Speicherorte der Beispieldateien

### Arduino-Beispiele
```
JUXI_HeartRate_SPO2/
└── examples/
    └── gainHeartbeatSPO2/
        └── gainHeartbeatSPO2.ino
```


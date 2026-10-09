[English](../../en/02-raspberry-pi/README.md) | Deutsch | [Español](../../es/02-raspberry-pi/README.md) | [Français](../../fr/02-raspberry-pi/README.md) | [Italiano](../../it/02-raspberry-pi/README.md) | [日本語](../../ja/02-raspberry-pi/README.md) | [한국어](../../ko/02-raspberry-pi/README.md) | [Português (BR)](../../pt-br/02-raspberry-pi/README.md) | [Português (PT)](../../pt-pt/02-raspberry-pi/README.md) | [简体中文](../../zh-hans/02-raspberry-pi/README.md) | [繁體中文](../../zh-hant/02-raspberry-pi/README.md)

# JUXI_HeartRate_SPO2 Raspberry-Pi-Tutorial


## Inhaltsverzeichnis

1. [Einführung](#einführung)
2. [Hardware-Anforderungen](#hardware-anforderungen)
3. [Hardware-Anschlüsse](#hardware-anschlüsse)
4. [Einrichtung der Umgebung](#einrichtung-der-umgebung)
5. [Verwendung des Beispielcodes](#verwendung-des-beispielcodes)
6. [API-Referenz](#api-referenz)
7. [FAQ](#faq)
8. [Wichtige Hinweise](#wichtige-hinweise)

---

## Einführung

JUXI_HeartRate_SPO2 ist ein Herzfrequenz- und Blutsauerstoff-Sensormodul auf Basis des MAX30102-Chips. Es verfügt über integrierte Algorithmen, die Herzfrequenz und Blutsauerstoffsättigung direkt ausgeben.

**Hauptmerkmale:**
- Messung der Blutsauerstoffsättigung (SPO2)
- Herzfrequenzmessung (Schläge pro Minute)
- Integrierte Temperaturmessung
- Unterstützung sowohl für UART- als auch I2C-Kommunikation

---

## Hardware-Anforderungen

| Benötigtes Element | Beschreibung |
|--------------|-------------|
| Raspberry Pi (2/3/4/Zero) | Raspberry Pi 3B+ oder 4B empfohlen |
| JUXI_HeartRate_SPO2 Sensor | Herzfrequenz- und Blutsauerstoff-Sensormodul |
| Dupont-Kabel | 4 Stück Buchse-zu-Buchse-Jumperkabel |
| Netzteil | Stromversorgung für den Raspberry Pi |

---

## Hardware-Anschlüsse

### Methode 1: I2C-Kommunikation (empfohlen)

Die I2C-Kommunikation erfordert eine einfache Verkabelung und wird empfohlen.

| Sensor-Pin | Physischer Pin des Raspberry Pi | BCM-Nummer | Beschreibung |
|-----------|--------------------------|-----------|-------------|
| VCC | 1 oder 17 | - | 3,3V-Stromversorgung (5V ebenfalls möglich) |
| GND | 6 oder 9 oder 14 | - | Masse |
| SDA | 3 | GPIO2 | I2C-Datenleitung |
| SCL | 5 | GPIO3 | I2C-Taktleitung |

**Wichtig:** Den Schalter des Sensors auf die Position **IIC** stellen!

### Methode 2: UART-serieller Anschluss

Die UART-Kommunikation erfordert eine Kreuzverbindung.

| Sensor-Pin | Physischer Pin des Raspberry Pi | BCM-Nummer | Beschreibung |
|-----------|--------------------------|-----------|-------------|
| VCC | 2 oder 4 | - | 5V-Stromversorgung (3,3V ebenfalls möglich) |
| GND | 6 oder 9 oder 14 | - | Masse |
| RX | 8 | GPIO14 | Sensor-RX wird mit Raspberry-Pi-TX verbunden |
| TX | 10 | GPIO15 | Sensor-TX wird mit Raspberry-Pi-RX verbunden |

**Wichtig:** Den Schalter des Sensors auf die Position **UART** stellen!

![树莓派针脚图](../../en/02-raspberry-pi/Raspberry%20Pi%20Pin%20Diagram.png)

---

## Einrichtung der Umgebung

### 1. I2C aktivieren (erforderlich für den I2C-Modus)

```bash
sudo raspi-config
```

`Interface Options` → `I2C` → `Yes` wählen, um zu aktivieren

Raspberry Pi neu starten:
```bash
sudo reboot
```

### 2. Seriellen Port aktivieren (erforderlich für den UART-Modus)

```bash
sudo raspi-config
```

`Interface Options` → `Serial` auswählen

- Erste Frage: "Would you like a login shell to be accessible over serial?" → `No` wählen
- Zweite Frage: "Would you like the serial port hardware to be enabled?" → `Yes` wählen

Raspberry Pi neu starten:
```bash
sudo reboot
```

### 3. Abhängigkeiten installieren

```bash
# Update package lists
sudo apt-get update

# Install I2C tools and smbus2 library (smbus2 is required for I2C mode)
sudo apt-get install -y i2c-tools python3-smbus2

# Install pyserial (for serial port support)
sudo pip3 install pyserial
```

> **Hinweis:** Der I2C-Modus erfordert `smbus2` — das alte Paket `python-smbus` ist nicht ausreichend.
> Die Bibliothek verwendet `smbus2.i2c_msg`, um zwei unabhängige I2C-Transaktionen durchzuführen (Schreiben der Registeradresse mit STOP, dann eine neue Lese-Transaktion, um mehrere Bytes nacheinander zu lesen),
> was dem vom Sensorchip geforderten I2C-Timing entspricht.

### 4. I2C-Verbindung überprüfen (I2C-Modus)

Nach dem Verkabeln führen Sie den folgenden Befehl aus, um I2C-Geräte zu erkennen:

```bash
i2cdetect -y 1
```

Wenn Sie die Adresse `0x57` sehen, ist der Sensor erfolgreich verbunden.

---

## Verwendung des Beispielcodes

### Dateistruktur

```
python/raspberry/
├── JUXI_HeartRate_SPO2.py      # Main library file
└── examples/
    ├── i2c_example.py          # I2C mode example
    └── uart_example.py         # UART mode example
```

### I2C-Modus-Beispiel ausführen

```bash
cd python/raspberry/examples
sudo python3 i2c_example.py
```

### UART-Modus-Beispiel ausführen

```bash
cd python/raspberry/examples
sudo python3 uart_example.py
```

**Hinweis:** Für den Zugriff auf den hardware-seriellen Port sind `sudo`-Rechte erforderlich.

### Erwartete Ausgabe

Wenn alles korrekt funktioniert, sehen Sie eine Ausgabe ähnlich wie:

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

Drücken Sie `Ctrl+C`, um das Programm zu beenden.

---

## API-Referenz

### Klasse: JUXI_HeartRate_SPO2_i2c

Sensor-Klasse für die I2C-Kommunikation.

#### Konstruktor
```python
JUXI_HeartRate_SPO2_i2c(bus_number=1, i2c_address=0x57)
```

Parameter:
- `bus_number`: I2C-Busnummer, auf dem Raspberry Pi normalerweise 1
- `i2c_address`: I2C-Adresse des Sensors, Standard 0x57

#### Methoden

| Methode | Beschreibung | Rückgabewert |
|--------|-------------|--------------|
| `begin()` | Sensor initialisieren, Verbindung prüfen | bool (True bei Erfolg) |
| `sensor_start_collect()` | Datenerfassung starten (Sensor-LED an) | None |
| `sensor_end_collect()` | Datenerfassung stoppen (Sensor-LED aus) | None |
| `get_heartbeat_SPO2()` | Herzfrequenz- und SPO2-Daten lesen | None (Ergebnisse werden in den Objekteigenschaften gespeichert) |
| `get_temperature_c()` | Integrierte Temperatur lesen | float (Celsius) |
| `close()` | I2C-Verbindung schließen | None |

#### Eigenschaften

| Eigenschaft | Beschreibung |
|----------|-------------|
| `SPO2` | Blutsauerstoffsättigung (%), -1 bei ungültigem Wert |
| `heartbeat` | Herzfrequenz (Schläge pro Minute), -1 bei ungültigem Wert |

---

### Klasse: JUXI_HeartRate_SPO2_uart

Sensor-Klasse für die UART-serielle Kommunikation.

#### Konstruktor
```python
JUXI_HeartRate_SPO2_uart(port='/dev/serial0', baudrate=9600)
```

Parameter:
- `port`: Pfad des seriellen Geräts, Standard `/dev/serial0` auf dem Raspberry Pi
- `baudrate`: Baudrate, Standard 9600

#### Methoden

Wie bei `JUXI_HeartRate_SPO2_i2c`.

---

## FAQ

### Frage 1: Was soll ich tun, wenn die Sensorinitialisierung fehlschlägt?

**Antwort:** Bitte befolgen Sie diese Schritte:

1. **Verkabelung prüfen**
   - I2C-Modus: Prüfen Sie, ob SDA mit GPIO2 und SCL mit GPIO3 verbunden ist
   - UART-Modus: Prüfen Sie die RX-TX-Kreuzverbindung

2. **Sensor-Schalter prüfen**
   - I2C-Modus: Der Schalter sollte auf der Position IIC stehen
   - UART-Modus: Der Schalter sollte auf der Position UART stehen

3. **Stromversorgung prüfen**
   - Prüfen Sie, ob VCC mit 3,3V oder 5V verbunden ist
   - Prüfen Sie, ob GND angeschlossen ist

4. **Systemeinstellungen prüfen**
   - I2C-Modus: Prüfen Sie, ob I2C aktiviert ist
   - UART-Modus: Prüfen Sie, ob der serielle Port aktiviert ist

5. **Erkennungsbefehle verwenden**
   ```bash
   # I2C mode
   i2cdetect -y 1
   
   # UART mode
   ls /dev/serial*
   ```

### Frage 2: Die Daten zeigen immer -1 an, was soll ich tun?

**Antwort:**

1. Stellen Sie sicher, dass Ihr Finger richtig auf dem Sensor liegt und beide LEDs vollständig bedeckt sind
2. Warten Sie einige Sekunden, bis sich die Daten stabilisiert haben (normalerweise 10–30 Sekunden)
3. Prüfen Sie, ob `sensor_start_collect()` aufgerufen wurde, um die Erfassung zu starten
4. Vergewissern Sie sich, dass die Sensor-LED leuchtet

### Frage 3: Die Daten sind ungenau, was soll ich tun?

**Antwort:**

1. Stellen Sie sicher, dass Ihr Finger den optischen Bereich des Sensors vollständig bedeckt
2. Halten Sie Ihren Finger ruhig, bewegen Sie ihn nicht
3. Warten Sie mehr als 30 Sekunden, bis sich die Daten stabilisiert haben
4. Führen Sie mehrere Messungen durch und bilden Sie den Mittelwert
5. Vermeiden Sie direktes starkes Licht auf dem Sensor

### Frage 4: Kann ich I2C und UART gleichzeitig verwenden?

**Antwort:** Nein, es kann jeweils nur eine Kommunikationsmethode gewählt werden.

### Frage 5: Muss ich zum Ausführen sudo verwenden?

**Antwort:**
- I2C-Modus: sudo wird empfohlen, um Berechtigungsprobleme zu vermeiden
- UART-Modus: sudo ist erforderlich, da sonst kein Zugriff auf den seriellen Port möglich ist

---

## Wichtige Hinweise

### Messtipps

1. **Finger richtig auflegen**
   - Legen Sie Ihren Finger sanft auf den Sensor, sodass beide LEDs bedeckt sind
   - Drücken Sie nicht zu fest, da dies die Blutzirkulation beeinträchtigen kann
   - Halten Sie Ihren Finger ruhig, bewegen Sie ihn nicht

2. **Auf Stabilisierung der Daten warten**
   - Die Werte können zu Beginn der Messung instabil sein
   - Es wird empfohlen, 10–30 Sekunden zu warten, bis sich die Daten stabilisiert haben
   - Der Sensor aktualisiert die Daten alle 4 Sekunden

3. **Umgebungsanforderungen**
   - Vermeiden Sie direktes starkes Licht auf dem Sensor
   - Halten Sie eine angemessene Umgebungstemperatur ein
   - Bleiben Sie während der Messung ruhig

### Interpretation der Daten

| SPO2-Bereich | Beschreibung |
|-----------|-------------|
| 95% - 100% | Normal |
| 90% - 94% | Leichte Hypoxie |
| < 90% | Hypoxie, bitte einen Arzt konsultieren |

| Herzfrequenzbereich | Beschreibung |
|-----------------|-------------|
| 60 - 100 BPM | Normalbereich für Erwachsene |
| < 60 BPM | Bradykardie |
| > 100 BPM | Tachykardie |

### Sicherheitshinweis

- Dieser Sensor dient nur als Referenz und kann keine professionelle medizinische Ausrüstung ersetzen
- Bei gesundheitlichen Bedenken wenden Sie sich bitte umgehend an einen Arzt
- Die Messergebnisse dienen nur als Referenz und sollten nicht zur Diagnose verwendet werden


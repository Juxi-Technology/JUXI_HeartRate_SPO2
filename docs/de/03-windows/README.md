[English](../../en/03-windows/README.md) | Deutsch | [Español](../../es/03-windows/README.md) | [Français](../../fr/03-windows/README.md) | [Italiano](../../it/03-windows/README.md) | [日本語](../../ja/03-windows/README.md) | [한국어](../../ko/03-windows/README.md) | [Português (BR)](../../pt-br/03-windows/README.md) | [Português (PT)](../../pt-pt/03-windows/README.md) | [简体中文](../../zh-hans/03-windows/README.md) | [繁體中文](../../zh-hant/03-windows/README.md)

# JUXI Herzfrequenz-Oximeter-Sensor - Benutzerhandbuch für Windows

## Inhaltsverzeichnis
1. [Hardware-Vorbereitung](#hardware-vorbereitung)
2. [Hardware-Anschluss](#hardware-anschluss)
3. [Einrichtung der Softwareumgebung](#einrichtung-der-softwareumgebung)
4. [Ausführen des Beispielprogramms](#ausführen-des-beispielprogramms)
5. [FAQ](#faq)

---

## Hardware-Vorbereitung

### Benötigtes Material

| Element | Beschreibung |
|------|-------------|
| JUXI_HeartRate_SPO2 Sensor | Herzfrequenz-Oximeter-Modul |
| USB-zu-TTL-Modul | CH340 / CP2102 / FT232 usw. |
| Dupont-Kabel | 4 Stück (Buchse zu Buchse) |
| Windows-Computer | Win7/Win10/Win11 |

---

## Hardware-Anschluss

### Verkabelungsmethode

| Sensor-Pin | USB-zu-TTL-Pin | Beschreibung |
|-----------|---------------|-------------|
| **VCC** | 3.3V oder 5V | Pluspol der Stromversorgung |
| **GND** | GND | Minuspol der Stromversorgung |
| **TX** | RX | Sensor sendet → Modul empfängt |
| **RX** | TX | Sensor empfängt → Modul sendet |

![Connect PC](../../en/03-windows/Connect%20PC.png)

⚠️ **Wichtige Hinweise**:

1. **Den DIP-Schalter des Moduls auf die Position UART stellen!!!**
2. **TX und RX müssen kreuzweise verbunden werden!**
3. Der Sensor unterstützt sowohl 3,3V als auch 5V, schließen Sie keine falsche Spannung an
4. Verbinden Sie zuerst alle Kabel und stecken Sie dann den USB-Stecker in den Computer

### Verkabelungsdiagramm

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

## Einrichtung der Softwareumgebung

### 1. Treiber installieren

Installieren Sie je nach Chiptyp Ihres USB-zu-TTL-Moduls den passenden Treiber:

- **CH340**: https://sparks.gogo.co.nz/ch340.html
- **CP2102**: https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers
- **FT232**: https://ftdichip.com/drivers/vcp-drivers/

Stecken Sie nach der Installation das USB-zu-TTL-Modul ein.

### 2. COM-Port anzeigen

#### Methode 1: Geräte-Manager
1. Drücken Sie `Win + X`, wählen Sie "Geräte-Manager"
2. Erweitern Sie "Anschlüsse (COM & LPT)"
3. Prüfen Sie die COM-Portnummer, die Ihrem USB-zu-TTL entspricht (z. B. COM3)

#### Methode 2: Automatische Erkennung durch das Programm
Beim Ausführen des Beispielprogramms werden automatisch alle verfügbaren seriellen Ports aufgelistet.

### 3. Python-Abhängigkeiten installieren

Öffnen Sie die Eingabeaufforderung (CMD) oder PowerShell und führen Sie aus:

```bash
pip install pyserial
```

---

## Ausführen des Beispielprogramms

### Dateispeicherort

```
JUXI_HeartRate_SPO2/python/windows/
├── gain_heartbeat_SPO2.py  ← Main program (run this)
├── JUXI_HeartRate_SPO2_Windows.py
├── JUXI_RTU_Windows.py
└── README.md                ← This file
```

### Ausführungsschritte

1. **Korrekte Hardware-Verbindung sicherstellen**
   - VCC → 3.3V/5V
   - GND → GND
   - TX → RX (gekreuzt)
   - RX → TX (gekreuzt)

2. **USB in den Computer einstecken**

3. **Programm ausführen**
   ```bash
   cd D:\JUXI_HeartRate_SPO2\python\windows
   python gain_heartbeat_SPO2.py
   ```

4. **Den Anweisungen folgen**
   
   - Das Programm listet alle verfügbaren seriellen Ports auf
   - Geben Sie Ihre COM-Portnummer ein (z. B. COM3)
   - Das Programm erkennt den Sensor automatisch und startet die Messung

### Erwartete Ausgabe

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

Drücken Sie `Ctrl + C`, um das Programm zu beenden.

---

## Beschreibung der Programmfunktionen

### Haupt-API

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

## FAQ

### Frage 1: COM-Port wird nicht gefunden?

**Antwort:**

1. Prüfen Sie, ob das USB-zu-TTL ordnungsgemäß eingesteckt ist
2. Installieren Sie den Treiber neu
3. Probieren Sie einen anderen USB-Anschluss
4. Prüfen Sie im Geräte-Manager auf "Unbekannte Geräte"

### Frage 2: Sensorinitialisierung fehlgeschlagen?

**Antwort:**

1. Prüfen Sie die Verkabelung:
   - Sind VCC und GND korrekt angeschlossen
   - **Sind TX und RX kreuzweise verbunden?** (häufigstes Problem)
2. Stellen Sie sicher, dass die Baudrate 9600 beträgt
3. Prüfen Sie, ob das USB-zu-TTL-Modul ordnungsgemäß funktioniert
4. Stecken Sie den USB-Stecker erneut ein

### Frage 3: Die Daten zeigen immer -1 an?

**Antwort:**
1. Stellen Sie sicher, dass der Finger richtig auf dem Sensor liegt (LED-Bereich vollständig bedeckt)
2. Halten Sie den Finger ruhig, bewegen Sie ihn nicht
3. Warten Sie einige Sekunden, bis sich die Daten stabilisiert haben
4. Prüfen Sie, ob die Sensor-LED leuchtet

### Frage 4: Die LED leuchtet nicht, aber die Kommunikation funktioniert?

**Antwort:**

- Möglicherweise liegt ein Hardwareproblem mit der LED vor, aber der Sensor funktioniert normal
- Solange die Daten normal sind, kann die nicht leuchtende LED ignoriert werden

### Frage 5: Der serielle Port ist belegt?

**Antwort:**
1. Schließen Sie andere serielle Software (serieller Assistent, Arduino IDE usw.)
2. Prüfen Sie, ob andere Python-Programme laufen
3. Stecken Sie den USB-Stecker erneut ein

### Frage 6: Die Daten sind ungenau?

**Antwort:**
1. Stellen Sie sicher, dass der Finger den optischen Bereich des Sensors vollständig bedeckt
2. Bleiben Sie während der Messung ruhig, sprechen oder bewegen Sie sich nicht
3. Warten Sie mehr als 30 Sekunden, bis sich die Daten stabilisiert haben
4. Führen Sie mehrere Messungen durch und bilden Sie den Mittelwert

---

## Technische Spezifikationen

| Parameter | Spezifikation |
|-----------|--------------|
| Kommunikation | UART (TTL-Pegel) |
| Baudrate | 9600 bps (Standard) |
| Datenformat | 8N1 (8 Datenbits, keine Parität, 1 Stoppbit) |
| Stromversorgung | 3.3V / 5V |
| SPO2-Bereich | 35% - 100% |
| Herzfrequenzbereich | 30 - 250 BPM |
| Modbus-Adresse | 0x20 |

---

## Beschreibung der Modbus-Register

| Registeradresse | Funktion | Beschreibung |
|-----------------|----------|-------------|
| 0x02 | Geräte-ID | Lesen: gibt 0x0020 zurück |
| 0x06-0x09 | Herzfrequenz- & SPO2-Daten | Lesen: SPO2 + Herzfrequenz |
| 0x0A | Temperatur | Lesen: integrierte Temperatur |
| 0x10 | Erfassungssteuerung | Schreiben: 0x0001=Start, 0x0002=Stopp |

---

## Kontakt

Bei Fragen oder Anregungen besuchen Sie bitte:
- GitHub: https://github.com/Juxi-Technology/JUXI_HeartRate_SPO2

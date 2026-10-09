[English](../../en/04-gui-tool/README.md) | Deutsch | [Español](../../es/04-gui-tool/README.md) | [Français](../../fr/04-gui-tool/README.md) | [Italiano](../../it/04-gui-tool/README.md) | [日本語](../../ja/04-gui-tool/README.md) | [한국어](../../ko/04-gui-tool/README.md) | [Português (BR)](../../pt-br/04-gui-tool/README.md) | [Português (PT)](../../pt-pt/04-gui-tool/README.md) | [简体中文](../../zh-hans/04-gui-tool/README.md) | [繁體中文](../../zh-hant/04-gui-tool/README.md)

# Herzfrequenz-Oximeter-Modul - Benutzerhandbuch für die GUI

## 📋 Funktionen

Dies ist ein grafisches Programm zur Überwachung von Herzfrequenz und Blutsauerstoff mit folgenden Funktionen:

1. ✅ **Auswahl des seriellen Ports** - Scannt verfügbare serielle Ports automatisch
2. ✅ **Auswahl der Baudrate** - Unterstützt 9600/19200/38400/57600/115200
3. ✅ **Verbinden/Trennen** - Modul mit einem Klick verbinden/trennen
4. ✅ **Erfassung starten/stoppen** - Steuert das Ein-/Ausschalten der Sensor-LED
5. ✅ **Überwachung starten/stoppen** - Echtzeitanzeige der Daten
6. ✅ **Echtzeitanzeige der Daten** - Blutsauerstoff, Herzfrequenz, Temperatur
7. ✅ **Umschalten zwischen Englisch / Chinesisch** - Die Sprache der Oberfläche jederzeit umschalten; Englisch ist die Standardeinstellung

---

## 🔌 Hardware-Anschluss

| Herzfrequenz-Oximeter-Modul | USB-zu-TTL-Modul |
|---------------------------|------------------|
| **VCC** | **5V** (Wichtig! Nicht 3.3V verwenden) |
| **GND** | **GND** |
| **TX** | **RX** (Kreuzverbindung) |
| **RX** | **TX** (Kreuzverbindung) |

⚠️ **Hinweis: TX und RX müssen kreuzweise verbunden werden!**

---

## 🚀 Programm ausführen

### Methode 1: Python-Skript direkt ausführen

1. Abhängigkeiten installieren:
```bash
pip install pyserial
```

2. Programm ausführen:
```bash
cd 上位机源代码
python HeartRateOximeter.py
```

---

## 📖 Verwendungsschritte

### Schritt 1: Hardware verbinden
1. Verbinden Sie den Sensor und das USB-zu-TTL gemäß der obigen Verkabelungstabelle

   VCC -> VCC

   GND -> GND

   RX -> TX

   TX -> RX

2. Stecken Sie das USB-zu-TTL in einen USB-Anschluss des Computers

### Schritt 2: Programm öffnen
Führen Sie `HeartRateOximeter.exe` aus

### Schritt 3: Seriellen Port einstellen
1. Wählen Sie den richtigen seriellen Port (z. B. COM3)
2. Wählen Sie die Baudrate **9600** (Standard)
3. Klicken Sie auf die Schaltfläche [Verbinden]

### Schritt 4: Erfassung starten
1. Klicken Sie nach erfolgreicher Verbindung auf [Erfassung starten]
2. ✅ Die Sensor-LED leuchtet auf

### Schritt 5: Überwachung starten
1. Legen Sie Ihren Finger auf den Sensor
2. Klicken Sie auf [Überwachung starten]
3. Sehen Sie sich die Echtzeitdaten an

---

## 📊 Beschreibung der Oberfläche

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

**Sprachumschaltung**: Das Dropdown-Menü oben im Fenster schaltet die Oberfläche zwischen Englisch und 中文 um. Das Programm startet auf Englisch.

---

## 📋 Interpretation der Daten

| Daten | Normalbereich | Beschreibung |
|------|-------------|-------------|
| **SPO2** | 95% - 100% | Bei unter 90% einen Arzt konsultieren |
| **Herzfrequenz** | 60 - 100 BPM | Normalbereich für Erwachsene |
| **Temperatur** | 25 - 35 °C | Integrierte Temperatur des Moduls, nicht Körpertemperatur |

**Hinweis**: Wenn gerade gestartet oder der Finger nicht richtig aufgelegt wurde, können die Daten -1 anzeigen; das ist normal.

---

## ❓ FAQ

### Frage 1: Serieller Port wird nicht gefunden?
**Antwort:**
1. Prüfen Sie, ob der USB-zu-TTL-Treiber korrekt installiert ist
2. Stecken Sie das USB-Kabel erneut ein
3. Klicken Sie auf die Schaltfläche [Aktualisieren], um erneut zu scannen

### Frage 2: Verbindung fehlgeschlagen?
**Antwort:**
1. Stellen Sie sicher, dass der richtige serielle Port gewählt ist
2. Stellen Sie sicher, dass der serielle Port nicht von anderen Programmen belegt ist (z. B. serieller Assistent, Arduino IDE)
3. Prüfen Sie, ob das USB-zu-TTL-Modul ordnungsgemäß funktioniert

### Frage 3: Die LED leuchtet nach dem Klick auf Start Collection nicht auf?
**Antwort:**
1. Prüfen Sie, ob VCC mit 5V verbunden ist (nicht 3.3V)
2. Prüfen Sie, ob TX/RX kreuzweise verbunden sind
3. Stellen Sie sicher, dass das Sensormodul selbst nicht beschädigt ist

### Frage 4: Die Daten zeigen immer -1 an?
**Antwort:**
1. Vergewissern Sie sich, dass [Erfassung starten] angeklickt wurde
2. Legen Sie den Finger korrekt auf den Sensor, sodass der LED-Bereich vollständig bedeckt ist
3. Halten Sie den Finger ruhig und warten Sie einige Sekunden
4. Prüfen Sie auf lose Verbindungen

### Frage 5: Das Programm reagiert nicht?
**Antwort:**
1. Klicken Sie zuerst auf [Überwachung stoppen]
2. Klicken Sie dann auf [Erfassung stoppen]
3. Klicken Sie schließlich auf [Trennen]
4. Starten Sie das Programm neu

---

## ⚠️ Vorsichtsmaßnahmen

1. **Reihenfolge der Verkabelung**: Zuerst den Sensor anschließen, dann den USB-Stecker einstecken
2. **Reihenfolge beim Trennen**: Zuerst die Überwachung stoppen, dann die Erfassung stoppen, schließlich trennen
3. **Stromversorgung**: Der Sensor muss an 5V angeschlossen werden, 3.3V funktioniert möglicherweise nicht ordnungsgemäß
4. **Fingerposition**: Der Finger sollte den optischen Bereich vollständig bedecken, nicht fest drücken
5. **Umgebungsanforderung**: Direktes starkes Licht auf dem Sensor vermeiden

---

## 📞 Technischer Support

Bei Problemen prüfen Sie bitte:
1. Korrekte Hardware-Verkabelung (insbesondere TX/RX-Überkreuzung)
2. Stromversorgung beträgt 5V
3. Der USB-zu-TTL-Treiber funktioniert ordnungsgemäß
4. Der serielle Port ist nicht von anderen Programmen belegt

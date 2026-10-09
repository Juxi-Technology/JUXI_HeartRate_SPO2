[English](../../en/03-windows/README.md) | [Deutsch](../../de/03-windows/README.md) | [Español](../../es/03-windows/README.md) | [Français](../../fr/03-windows/README.md) | Italiano | [日本語](../../ja/03-windows/README.md) | [한국어](../../ko/03-windows/README.md) | [Português (BR)](../../pt-br/03-windows/README.md) | [Português (PT)](../../pt-pt/03-windows/README.md) | [简体中文](../../zh-hans/03-windows/README.md) | [繁體中文](../../zh-hant/03-windows/README.md)

# Sensore ossimetro per frequenza cardiaca JUXI - Guida utente Windows

## Indice
1. [Preparazione hardware](#hardware-preparation)
2. [Collegamento hardware](#hardware-connection)
3. [Configurazione dell'ambiente software](#software-environment-setup)
4. [Esecuzione del programma di esempio](#running-the-example-program)
5. [FAQ](#faq)

---

## Preparazione hardware

### Materiale necessario

| Elemento | Descrizione |
|------|-------------|
| Sensore JUXI_HeartRate_SPO2 | Modulo ossimetro per frequenza cardiaca |
| Modulo USB-TTL | CH340 / CP2102 / FT232, ecc. |
| Cavetti Dupont | 4 pezzi (femmina-femmina) |
| Computer Windows | Win7/Win10/Win11 |

---

## Collegamento hardware

### Metodo di cablaggio

| Pin del sensore | Pin USB-TTL | Descrizione |
|-----------|---------------|-------------|
| **VCC** | 3.3V o 5V | Alimentazione positiva |
| **GND** | GND | Alimentazione negativa |
| **TX** | RX | Trasmissione del sensore → ricezione del modulo |
| **RX** | TX | Ricezione del sensore → trasmissione del modulo |

![Connect PC](../../en/03-windows/Connect%20PC.png)

⚠️ **Suggerimenti importanti**:

1. **Porta l'interruttore DIP del modulo in posizione UART!!!**
2. **TX e RX devono essere collegati in modo incrociato!**
3. Il sensore supporta sia 3.3V sia 5V, non collegare una tensione errata
4. Collega prima tutti i fili, poi inserisci l'USB nel computer

### Schema di cablaggio

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

## Configurazione dell'ambiente software

### 1. Installare i driver

In base al modello di chip del tuo adattatore USB-TTL, installa il driver corrispondente:

- **CH340**: https://sparks.gogo.co.nz/ch340.html
- **CP2102**: https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers
- **FT232**: https://ftdichip.com/drivers/vcp-drivers/

Dopo l'installazione, inserisci il modulo USB-TTL.

### 2. Visualizzare la porta COM

#### Metodo 1: Gestione dispositivi
1. Premi `Win + X`, seleziona "Gestione dispositivi"
2. Espandi "Porte (COM e LPT)"
3. Controlla il numero della porta COM corrispondente al tuo USB-TTL (ad esempio COM3)

#### Metodo 2: rilevamento automatico del programma
Quando si esegue il programma di esempio, tutte le porte seriali disponibili vengono elencate automaticamente.

### 3. Installare le dipendenze Python

Apri il Prompt dei comandi (CMD) o PowerShell ed esegui:

```bash
pip install pyserial
```

---

## Esecuzione del programma di esempio

### Posizione dei file

```
JUXI_HeartRate_SPO2/python/windows/
├── gain_heartbeat_SPO2.py  ← Main program (run this)
├── JUXI_HeartRate_SPO2_Windows.py
├── JUXI_RTU_Windows.py
└── README.md                ← This file
```

### Passaggi di esecuzione

1. **Verifica il corretto collegamento hardware**
   - VCC → 3.3V/5V
   - GND → GND
   - TX → RX (incrociato)
   - RX → TX (incrociato)

2. **Inserisci l'USB nel computer**

3. **Esegui il programma**
   ```bash
   cd D:\JUXI_HeartRate_SPO2\python\windows
   python gain_heartbeat_SPO2.py
   ```

4. **Segui le istruzioni**
   
   - Il programma elencherà tutte le porte seriali disponibili
   - Inserisci il numero della tua porta COM (ad esempio COM3)
   - Il programma rileverà automaticamente il sensore e avvierà la misurazione

### Output previsto

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

Premi `Ctrl + C` per fermare il programma.

---

## Descrizione delle funzioni del programma

### API principali

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

### D1: Non riesco a trovare la porta COM?

**R:**

1. Verifica che l'USB-TTL sia inserito correttamente
2. Reinstalla il driver
3. Prova un'altra porta USB
4. Controlla la presenza di "Dispositivi sconosciuti" nella Gestione dispositivi

### D2: Inizializzazione del sensore non riuscita?

**R:**

1. Controlla il cablaggio:
   - VCC e GND sono collegati correttamente?
   - **TX e RX sono collegati in modo incrociato?** (problema più comune)
2. Verifica che la velocità di trasmissione (baud rate) sia 9600
3. Verifica che il modulo USB-TTL funzioni correttamente
4. Reinserisci l'USB

### D3: I dati mostrano sempre -1?

**R:**
1. Verifica che il dito sia posizionato correttamente sul sensore (coprendo completamente l'area del LED)
2. Mantieni il dito fermo, non muoverlo
3. Attendi qualche secondo affinché i dati si stabilizzino
4. Verifica che il LED del sensore sia acceso

### D4: Il LED non è acceso ma la comunicazione funziona?

**R:**

- Potrebbe essere un problema hardware del LED, ma il sensore funziona normalmente
- Finché i dati sono normali, il LED non acceso può essere ignorato

### D5: La porta seriale è occupata?

**R:**
1. Chiudi gli altri software seriali (assistente seriale, Arduino IDE, ecc.)
2. Verifica se sono in esecuzione altri programmi Python
3. Reinserisci l'USB

### D6: I dati non sono accurati?

**R:**
1. Assicurati che il dito copra completamente l'area ottica del sensore
2. Rimani in silenzio durante la misurazione, non parlare né muoverti
3. Attendi più di 30 secondi affinché i dati si stabilizzino
4. Effettua più misurazioni e calcola la media

---

## Specifiche tecniche

| Parametro | Specifica |
|-----------|--------------|
| Comunicazione | UART (livello TTL) |
| Velocità di trasmissione | 9600 bps (predefinita) |
| Formato dati | 8N1 (8 bit di dati, nessuna parità, 1 bit di stop) |
| Alimentazione | 3.3V / 5V |
| Intervallo SPO2 | 35% - 100% |
| Intervallo di frequenza cardiaca | 30 - 250 BPM |
| Indirizzo Modbus | 0x20 |

---

## Descrizione dei registri Modbus

| Indirizzo del registro | Funzione | Descrizione |
|-----------------|----------|-------------|
| 0x02 | ID dispositivo | Lettura: restituisce 0x0020 |
| 0x06-0x09 | Dati di frequenza cardiaca e SPO2 | Lettura: SPO2 + frequenza cardiaca |
| 0x0A | Temperatura | Lettura: temperatura a bordo |
| 0x10 | Controllo raccolta | Scrittura: 0x0001=avvia, 0x0002=arresta |

---

## Contattaci

Per domande o suggerimenti, visita:
- GitHub: https://github.com/Juxi-Technology/JUXI_HeartRate_SPO2

[English](../../en/02-raspberry-pi/README.md) | [Deutsch](../../de/02-raspberry-pi/README.md) | [Español](../../es/02-raspberry-pi/README.md) | [Français](../../fr/02-raspberry-pi/README.md) | Italiano | [日本語](../../ja/02-raspberry-pi/README.md) | [한국어](../../ko/02-raspberry-pi/README.md) | [Português (BR)](../../pt-br/02-raspberry-pi/README.md) | [Português (PT)](../../pt-pt/02-raspberry-pi/README.md) | [简体中文](../../zh-hans/02-raspberry-pi/README.md) | [繁體中文](../../zh-hant/02-raspberry-pi/README.md)

# Tutorial JUXI_HeartRate_SPO2 per Raspberry Pi


## Indice

1. [Introduzione](#introduction)
2. [Requisiti hardware](#hardware-requirements)
3. [Collegamenti hardware](#hardware-connections)
4. [Configurazione dell'ambiente](#environment-setup)
5. [Utilizzo del codice di esempio](#example-code-usage)
6. [Riferimento API](#api-reference)
7. [FAQ](#faq)
8. [Note importanti](#important-notes)

---

## Introduzione

JUXI_HeartRate_SPO2 è un modulo sensore per la frequenza cardiaca e la saturazione dell'ossigeno nel sangue, basato sul chip MAX30102. Dispone di algoritmi integrati che restituiscono direttamente i valori di frequenza cardiaca e saturazione dell'ossigeno.

**Caratteristiche principali:**
- Misurazione della saturazione dell'ossigeno (SPO2)
- Misurazione della frequenza cardiaca (battiti al minuto)
- Misurazione della temperatura a bordo
- Supporto alla comunicazione sia UART sia I2C

---

## Requisiti hardware

| Elemento necessario | Descrizione |
|--------------|-------------|
| Raspberry Pi (2/3/4/Zero) | Consigliati Raspberry Pi 3B+ o 4B |
| Sensore JUXI_HeartRate_SPO2 | Modulo sensore per frequenza cardiaca e saturazione dell'ossigeno |
| Cavetti Dupont | 4 cavetti jumper femmina-femmina |
| Alimentatore | Alimentatore per Raspberry Pi |

---

## Collegamenti hardware

### Metodo 1: comunicazione I2C (consigliato)

La comunicazione I2C ha un cablaggio semplice ed è quella consigliata.

| Pin del sensore | Pin fisico del Raspberry Pi | Numero BCM | Descrizione |
|-----------|--------------------------|-----------|-------------|
| VCC | 1 o 17 | - | Alimentazione 3.3V (anche 5V è accettabile) |
| GND | 6 o 9 o 14 | - | Massa |
| SDA | 3 | GPIO2 | Linea dati I2C |
| SCL | 5 | GPIO3 | Linea di clock I2C |

**Importante:** porta l'interruttore del sensore in posizione **IIC**!

### Metodo 2: comunicazione seriale UART

La comunicazione UART richiede un collegamento incrociato.

| Pin del sensore | Pin fisico del Raspberry Pi | Numero BCM | Descrizione |
|-----------|--------------------------|-----------|-------------|
| VCC | 2 o 4 | - | Alimentazione 5V (anche 3.3V è accettabile) |
| GND | 6 o 9 o 14 | - | Massa |
| RX | 8 | GPIO14 | L'RX del sensore si collega al TX del Raspberry Pi |
| TX | 10 | GPIO15 | Il TX del sensore si collega all'RX del Raspberry Pi |

**Importante:** porta l'interruttore del sensore in posizione **UART**!

![树莓派针脚图](../../en/02-raspberry-pi/Raspberry%20Pi%20Pin%20Diagram.png)

---

## Configurazione dell'ambiente

### 1. Abilitare I2C (necessario per la modalità I2C)

```bash
sudo raspi-config
```

Seleziona `Interface Options` → `I2C` → Seleziona `Yes` per abilitare

Riavvia il Raspberry Pi:
```bash
sudo reboot
```

### 2. Abilitare la porta seriale (necessario per la modalità UART)

```bash
sudo raspi-config
```

Seleziona `Interface Options` → `Serial`

- Prima domanda: "Would you like a login shell to be accessible over serial?" → Seleziona `No`
- Seconda domanda: "Would you like the serial port hardware to be enabled?" → Seleziona `Yes`

Riavvia il Raspberry Pi:
```bash
sudo reboot
```

### 3. Installare le dipendenze

```bash
# Update package lists
sudo apt-get update

# Install I2C tools and smbus2 library (smbus2 is required for I2C mode)
sudo apt-get install -y i2c-tools python3-smbus2

# Install pyserial (for serial port support)
sudo pip3 install pyserial
```

> **Nota:** la modalità I2C richiede `smbus2` — il pacchetto legacy `python-smbus` non è sufficiente.
> La libreria usa `smbus2.i2c_msg` per eseguire due transazioni I2C indipendenti (scrittura dell'indirizzo
> del registro con STOP, poi una nuova transazione di lettura per leggere più byte in sequenza),
> rispettando la temporizzazione I2C richiesta dal chip del sensore.

### 4. Verificare la connessione I2C (modalità I2C)

Dopo il cablaggio, esegui il seguente comando per rilevare i dispositivi I2C:

```bash
i2cdetect -y 1
```

Se visualizzi l'indirizzo `0x57`, il sensore è collegato correttamente.

---

## Utilizzo del codice di esempio

### Struttura dei file

```
python/raspberry/
├── JUXI_HeartRate_SPO2.py      # Main library file
└── examples/
    ├── i2c_example.py          # I2C mode example
    └── uart_example.py         # UART mode example
```

### Esecuzione dell'esempio in modalità I2C

```bash
cd python/raspberry/examples
sudo python3 i2c_example.py
```

### Esecuzione dell'esempio in modalità UART

```bash
cd python/raspberry/examples
sudo python3 uart_example.py
```

**Nota:** per accedere alla porta seriale hardware è necessario il permesso `sudo`.

### Output previsto

Se tutto funziona correttamente, vedrai un output simile a:

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

Premi `Ctrl+C` per fermare il programma.

---

## Riferimento API

### Classe: JUXI_HeartRate_SPO2_i2c

Classe del sensore per la comunicazione I2C.

#### Costruttore
```python
JUXI_HeartRate_SPO2_i2c(bus_number=1, i2c_address=0x57)
```

Parametri:
- `bus_number`: numero del bus I2C, di solito 1 su Raspberry Pi
- `i2c_address`: indirizzo I2C del sensore, predefinito 0x57

#### Metodi

| Metodo | Descrizione | Valore restituito |
|--------|-------------|--------------|
| `begin()` | Inizializza il sensore, verifica la connessione | bool (True in caso di successo) |
| `sensor_start_collect()` | Avvia la raccolta dati (LED del sensore ON) | None |
| `sensor_end_collect()` | Arresta la raccolta dati (LED del sensore OFF) | None |
| `get_heartbeat_SPO2()` | Legge i dati di frequenza cardiaca e SPO2 | None (i risultati sono memorizzati nelle proprietà dell'oggetto) |
| `get_temperature_c()` | Legge la temperatura a bordo | float (Celsius) |
| `close()` | Chiude la connessione I2C | None |

#### Proprietà

| Proprietà | Descrizione |
|----------|-------------|
| `SPO2` | Saturazione dell'ossigeno (%), -1 per valore non valido |
| `heartbeat` | Frequenza cardiaca (battiti al minuto), -1 per valore non valido |

---

### Classe: JUXI_HeartRate_SPO2_uart

Classe del sensore per la comunicazione seriale UART.

#### Costruttore
```python
JUXI_HeartRate_SPO2_uart(port='/dev/serial0', baudrate=9600)
```

Parametri:
- `port`: percorso del dispositivo seriale, predefinito `/dev/serial0` su Raspberry Pi
- `baudrate`: velocità di trasmissione, predefinita 9600

#### Metodi

Uguali a `JUXI_HeartRate_SPO2_i2c`.

---

## FAQ

### D1: Cosa devo fare se l'inizializzazione del sensore non riesce?

**R:** Segui questi passaggi:

1. **Verifica il cablaggio**
   - Modalità I2C: verifica che SDA sia collegato a GPIO2 e SCL a GPIO3
   - Modalità UART: verifica il collegamento incrociato RX-TX

2. **Verifica l'interruttore del sensore**
   - Modalità I2C: l'interruttore deve essere in posizione IIC
   - Modalità UART: l'interruttore deve essere in posizione UART

3. **Verifica l'alimentazione**
   - Verifica che VCC sia collegato a 3.3V o 5V
   - Verifica che GND sia collegato

4. **Verifica le impostazioni di sistema**
   - Modalità I2C: verifica che I2C sia abilitato
   - Modalità UART: verifica che la porta seriale sia abilitata

5. **Usa i comandi di rilevamento**
   ```bash
   # I2C mode
   i2cdetect -y 1
   
   # UART mode
   ls /dev/serial*
   ```

### D2: I dati mostrano sempre -1, cosa devo fare?

**R:**

1. Assicurati che il dito sia posizionato correttamente sul sensore, coprendo completamente entrambi i LED
2. Attendi qualche secondo affinché i dati si stabilizzino (di solito 10-30 secondi)
3. Verifica che sia stata chiamata `sensor_start_collect()` per avviare la raccolta
4. Verifica che il LED del sensore sia acceso

### D3: I dati non sono accurati, cosa devo fare?

**R:**

1. Assicurati che il dito copra completamente l'area ottica del sensore
2. Mantieni il dito fermo, non muoverlo
3. Attendi più di 30 secondi affinché i dati si stabilizzino
4. Effettua più misurazioni e calcola la media
5. Evita luce diretta intensa sul sensore

### D4: Posso usare I2C e UART contemporaneamente?

**R:** No, è possibile selezionare una sola modalità di comunicazione alla volta.

### D5: Devo usare sudo per eseguire il programma?

**R:**
- Modalità I2C: si consiglia sudo per evitare problemi di autorizzazione
- Modalità UART: sudo è necessario, altrimenti non è possibile accedere alla porta seriale

---

## Note importanti

### Consigli per la misurazione

1. **Corretto posizionamento del dito**
   - Appoggia delicatamente il dito sul sensore, coprendo entrambi i LED
   - Non premere troppo forte, poiché ciò può compromettere la circolazione sanguigna
   - Mantieni il dito fermo, non muoverlo

2. **Attendere la stabilizzazione dei dati**
   - I valori possono essere instabili all'inizio della misurazione
   - Si consiglia di attendere 10-30 secondi affinché i dati si stabilizzino
   - Il sensore aggiorna i dati ogni 4 secondi

3. **Requisiti ambientali**
   - Evita luce diretta intensa sul sensore
   - Mantieni una temperatura ambiente adeguata
   - Rimani in silenzio durante la misurazione

### Interpretazione dei dati

| Intervallo SPO2 | Descrizione |
|-----------|-------------|
| 95% - 100% | Normale |
| 90% - 94% | Ipossia lieve |
| < 90% | Ipossia, consultare un medico |

| Intervallo di frequenza cardiaca | Descrizione |
|-----------------|-------------|
| 60 - 100 BPM | Intervallo normale per gli adulti |
| < 60 BPM | Bradicardia |
| > 100 BPM | Tachicardia |

### Avvertenza di sicurezza

- Questo sensore è solo a scopo indicativo e non può sostituire le apparecchiature mediche professionali
- In caso di problemi di salute, consultare tempestivamente un medico
- I risultati delle misurazioni sono solo indicativi e non devono essere utilizzati per la diagnosi

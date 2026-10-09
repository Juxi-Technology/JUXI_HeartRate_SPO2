[English](../../en/01-arduino/README.md) | [Deutsch](../../de/01-arduino/README.md) | [Español](../../es/01-arduino/README.md) | [Français](../../fr/01-arduino/README.md) | Italiano | [日本語](../../ja/01-arduino/README.md) | [한국어](../../ko/01-arduino/README.md) | [Português (BR)](../../pt-br/01-arduino/README.md) | [Português (PT)](../../pt-pt/01-arduino/README.md) | [简体中文](../../zh-hans/01-arduino/README.md) | [繁體中文](../../zh-hant/01-arduino/README.md)

# Tutorial del sensore di frequenza cardiaca e ossimetro JUXI_HeartRate_SPO2

## Indice
1. [Introduzione al sensore](#sensor-introduction)
2. [Tutorial Arduino](#arduino-tutorial)
3. [Tutorial Python (Raspberry Pi)](#python-raspberry-pi-tutorial)
4. [FAQ](#faq)

---

## Introduzione al sensore

JUXI_HeartRate_SPO2 è un modulo sensore per la frequenza cardiaca e la saturazione dell'ossigeno nel sangue, basato sul chip MAX30102, con un algoritmo integrato in grado di restituire direttamente i valori di frequenza cardiaca e saturazione dell'ossigeno.

**Caratteristiche principali:**

- Misurazione della saturazione dell'ossigeno (SPO2)
- Misurazione della frequenza cardiaca (battiti al minuto)
- Misurazione della temperatura a bordo
- Supporta la comunicazione I2C

---

## Tutorial Arduino

### 1. Preparazione hardware

| Materiale necessario |
|-------------------|
| Scheda di sviluppo Arduino (Uno/Nano/ESP32, ecc.) |
| Sensore JUXI_HeartRate_SPO2 |
| Cavetti dupont |
| Cavo dati USB (per collegare Arduino al computer) |

### 2. Installazione della libreria

1. Scarica questo file di libreria
2. Copia la cartella `JUXI_HeartRate_SPO2` nella directory delle librerie di Arduino:
   - Windows: `C:\Users\Username\Documents\Arduino\libraries\`
   - Mac: `~/Documents/Arduino/libraries/`
   - Linux: `~/Arduino/libraries/`
3. Riavvia l'Arduino IDE

### 3. Codice di esempio

**Nota: durante l'upload del codice, collega al computer solo Arduino, NON collegare il modulo ossimetro ad Arduino!!!**

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

##### Collegamento hardware

Comunicazione I2C

| Pin del sensore | Arduino |
|-----------|---------|
| VCC       | 5V/3.3V |
| GND       | GND     |
| SDA       | SDA/A4  |
| SCL       | SCL/A5  |

![IIC](../../en/01-arduino/img/IIC.png)

![8](../../en/01-arduino/img/8.png)

- Porta l'interruttore DIP del modulo ossimetro in posizione I2C!!!
- Usa il cavo dati per collegare Arduino al computer

#### Risultati dell'esecuzione:

1. Apri Arduino - Strumenti - Monitor seriale

   Imposta la velocità di trasmissione (baud rate) a 9600

![1](../../en/01-arduino/img/1.png)

2. Apri Serial Debug Assistant

[Serial Debug Assistant uartassist5.15.zip](https://juxitech.feishu.cn/wiki/BJlfwSQydi7u5lkRDQ6cV4dvnBd)

Seleziona il numero della porta seriale

Imposta la velocità di trasmissione (baud rate) a `9600`

Bit di dati `8`, bit di stop `1`, parità `NONE`, controllo di flusso `NONE`

Nelle impostazioni di ricezione e trasmissione seleziona `ASCII`

![2](../../en/01-arduino/img/2.png)

### 4. Descrizione delle API

| Funzione | Descrizione |
|----------|-------------|
| `begin()` | Inizializza il sensore, restituisce true/false |
| `getHeartbeatSPO2()` | Legge i dati di frequenza cardiaca e SPO2, memorizzati nella struttura `_sHeartbeatSPO2` |
| `getTemperature_C()` | Legge la temperatura a bordo (Celsius) |
| `sensorStartCollect()` | Avvia la raccolta dati (il LED del sensore si accende) |
| `sensorEndCollect()` | Arresta la raccolta dati (il LED del sensore si spegne) |

### 5. Descrizione dei dati

- **SPO2 (saturazione dell'ossigeno)**: intervallo normale 95% - 100%, il valore -1 indica un dato non valido
- **Heartbeat (frequenza cardiaca)**: intervallo normale 60 - 100 BPM, il valore -1 indica un dato non valido
- **Cause dei valori non validi**: dito posizionato in modo scorretto o dati non ancora stabilizzati

---

## Note d'uso

### Consigli per la misurazione

1. **Corretto posizionamento del dito**
   - Appoggia delicatamente il dito sul sensore, coprendo entrambi i LED
   - Non premere con forza per non compromettere la circolazione sanguigna
   - Mantieni il dito fermo, senza muoverlo

2. **Attendere la stabilizzazione dei dati**
   - I valori possono essere instabili all'inizio della misurazione
   - Si consiglia di attendere 10-30 secondi affinché i dati si stabilizzino prima di leggerli
   - Il sensore aggiorna i dati ogni 4 secondi

3. **Requisiti ambientali**
   - Evita luce diretta intensa sul sensore
   - Mantieni una temperatura ambiente adeguata
   - Rimani fermo e in silenzio durante la misurazione

### Interpretazione dei dati

| Intervallo SPO2 | Descrizione |
|-----------|-------------|
| 95% - 100% | Normale |
| 90% - 94% | Ipossia lieve |
| < 90% | Ipossia, si consiglia una consulenza medica |

| Intervallo di frequenza cardiaca | Descrizione |
|-----------------|-------------|
| 60 - 100 BPM | Intervallo normale per gli adulti |
| < 60 BPM | Bradicardia |
| > 100 BPM | Tachicardia |

---

## FAQ

### D1: Inizializzazione del sensore non riuscita?

**R:**
1. Verifica che il cablaggio sia corretto (SDA su GPIO2/A4, SCL su GPIO3/A5)
2. Verifica che l'alimentazione sia regolare (3.3V o 5V)
3. Usa il comando `i2cdetect -y 1` per rilevare il dispositivo
4. Assicurati che l'interruttore DIP del sensore sia in posizione IIC

### D2: I dati mostrano sempre -1?

**R:**
1. Verifica che il dito sia posizionato correttamente sul sensore
2. Attendi qualche secondo affinché i dati si stabilizzino
3. Verifica che sia stata chiamata `sensorStartCollect()` per avviare la raccolta
4. Verifica che la spia del sensore sia accesa

### D3: I dati non sono accurati?

**R:**
1. Assicurati che il dito copra completamente l'area ottica del sensore
2. Mantieni il dito fermo, senza muoverlo
3. Attendi più di 30 secondi affinché i dati si stabilizzino
4. Effettua più misurazioni e calcola la media

### D4: Quali schede di sviluppo Arduino sono supportate?

**R:** Supportate:
- Arduino Uno/Nano/Mega
- ESP8266
- ESP32
- Altre schede di sviluppo che supportano l'ambiente Arduino

---

## Posizione dei file di esempio

### Esempi Arduino
```
JUXI_HeartRate_SPO2/
└── examples/
    └── gainHeartbeatSPO2/
        └── gainHeartbeatSPO2.ino
```

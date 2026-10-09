[English](../../en/04-gui-tool/README.md) | [Deutsch](../../de/04-gui-tool/README.md) | [Español](../../es/04-gui-tool/README.md) | [Français](../../fr/04-gui-tool/README.md) | Italiano | [日本語](../../ja/04-gui-tool/README.md) | [한국어](../../ko/04-gui-tool/README.md) | [Português (BR)](../../pt-br/04-gui-tool/README.md) | [Português (PT)](../../pt-pt/04-gui-tool/README.md) | [简体中文](../../zh-hans/04-gui-tool/README.md) | [繁體中文](../../zh-hant/04-gui-tool/README.md)

# Modulo ossimetro per frequenza cardiaca - Guida utente dell'interfaccia grafica

## 📋 Caratteristiche

Questo è un programma grafico per il monitoraggio della frequenza cardiaca e della saturazione dell'ossigeno con le seguenti funzionalità:

1. ✅ **Selezione della porta seriale** - Scansione automatica delle porte seriali disponibili
2. ✅ **Selezione della velocità di trasmissione (baud rate)** - Supporta 9600/19200/38400/57600/115200
3. ✅ **Connetti/Disconnetti** - Connessione e disconnessione del modulo con un clic
4. ✅ **Avvia/Arresta raccolta** - Controlla l'accensione/spegnimento del LED del sensore
5. ✅ **Avvia/Arresta monitoraggio** - Visualizzazione dei dati in tempo reale
6. ✅ **Visualizzazione dei dati in tempo reale** - Saturazione dell'ossigeno, frequenza cardiaca, temperatura
7. ✅ **Commutazione inglese / cinese** - Cambia la lingua dell'interfaccia in qualsiasi momento; l'inglese è la lingua predefinita

---

## 🔌 Collegamento hardware

| Modulo ossimetro per frequenza cardiaca | Modulo USB-TTL |
|---------------------------|------------------|
| **VCC** | **5V** (Importante! Non usare 3.3V) |
| **GND** | **GND** |
| **TX** | **RX** (Collegamento incrociato) |
| **RX** | **TX** (Collegamento incrociato) |

⚠️ **Nota: TX e RX devono essere collegati in modo incrociato!**

---

## 🚀 Esecuzione del programma

### Metodo 1: esecuzione diretta dello script Python

1. Installa le dipendenze:
```bash
pip install pyserial
```

2. Esegui il programma:
```bash
cd 上位机源代码
python HeartRateOximeter.py
```

---

## 📖 Passaggi di utilizzo

### Passaggio 1: collegare l'hardware
1. Collega il sensore e l'USB-TTL secondo la tabella di cablaggio sopra

   VCC -> VCC

   GND -> GND

   RX -> TX

   TX -> RX

2. Inserisci l'USB-TTL nella porta USB del computer

### Passaggio 2: aprire il programma
Esegui `HeartRateOximeter.exe`

### Passaggio 3: impostazioni della porta seriale
1. Seleziona la porta seriale corretta (ad esempio COM3)
2. Seleziona la velocità di trasmissione **9600** (predefinita)
3. Fai clic sul pulsante [Connetti]

### Passaggio 4: avviare la raccolta
1. Dopo una connessione riuscita, fai clic su [Avvia raccolta]
2. ✅ Il LED del sensore si accenderà

### Passaggio 5: avviare il monitoraggio
1. Appoggia il dito sul sensore
2. Fai clic su [Avvia monitoraggio]
3. Visualizza i dati in tempo reale

---

## 📊 Descrizione dell'interfaccia

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

**Commutazione della lingua**: il menu a discesa nella parte superiore della finestra permette di passare l'interfaccia tra l'inglese e il cinese. Il programma si avvia in inglese.

---

## 📋 Interpretazione dei dati

| Dato | Intervallo normale | Descrizione |
|------|-------------|-------------|
| **SPO2** | 95% - 100% | Consultare un medico se inferiore al 90% |
| **Frequenza cardiaca** | 60 - 100 BPM | Intervallo normale per gli adulti |
| **Temperatura** | 25 - 35 °C | Temperatura a bordo del modulo, non temperatura corporea |

**Nota**: quando il programma è appena avviato o il dito non è posizionato correttamente, i dati possono mostrare -1, il che è normale.

---

## ❓ FAQ

### D1: Non riesco a trovare la porta seriale?
**R:**
1. Verifica che il driver del modulo USB-TTL sia installato correttamente
2. Reinserisci il cavo USB
3. Fai clic sul pulsante [Aggiorna] per ripetere la scansione

### D2: Connessione non riuscita?
**R:**
1. Verifica che la selezione della porta seriale sia corretta
2. Verifica che la porta seriale non sia occupata da altri programmi (ad esempio assistente seriale, Arduino IDE)
3. Verifica che il modulo USB-TTL funzioni correttamente

### D3: Il LED non si accende dopo aver fatto clic su Avvia raccolta?
**R:**
1. Verifica che VCC sia collegato a 5V (non a 3.3V)
2. Verifica che TX/RX siano collegati in modo incrociato
3. Verifica che il modulo sensore stesso non sia danneggiato

### D4: I dati mostrano sempre -1?
**R:**
1. Verifica che sia stato fatto clic su [Avvia raccolta]
2. Posiziona correttamente il dito sul sensore, coprendo completamente l'area del LED
3. Mantieni il dito fermo, attendi qualche secondo
4. Controlla che i collegamenti non siano allentati

### D5: Il programma non risponde?
**R:**
1. Fai clic prima su [Arresta monitoraggio]
2. Poi fai clic su [Arresta raccolta]
3. Infine fai clic su [Disconnetti]
4. Riavvia il programma

---

## ⚠️ Precauzioni

1. **Ordine di cablaggio**: collega prima il sensore, poi inserisci l'USB
2. **Ordine di disconnessione**: arresta il monitoraggio, poi la raccolta, infine disconnetti
3. **Requisiti di alimentazione**: il sensore deve essere collegato a un'alimentazione da 5V, con 3.3V potrebbe non funzionare correttamente
4. **Posizionamento del dito**: il dito deve coprire completamente l'area ottica, non premere con forza
5. **Requisiti ambientali**: evita luce diretta intensa sul sensore

---

## 📞 Supporto tecnico

In caso di problemi, verifica:
1. Il corretto cablaggio dell'hardware (in particolare l'incrocio TX/RX)
2. Che l'alimentazione sia a 5V
3. Che il driver del modulo USB-TTL funzioni correttamente
4. Che la porta seriale non sia occupata da altri programmi

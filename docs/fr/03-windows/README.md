[English](../../en/03-windows/README.md) | [Deutsch](../../de/03-windows/README.md) | [Español](../../es/03-windows/README.md) | Français | [Italiano](../../it/03-windows/README.md) | [日本語](../../ja/03-windows/README.md) | [한국어](../../ko/03-windows/README.md) | [Português (BR)](../../pt-br/03-windows/README.md) | [Português (PT)](../../pt-pt/03-windows/README.md) | [简体中文](../../zh-hans/03-windows/README.md) | [繁體中文](../../zh-hant/03-windows/README.md)

# Capteur oxymètre de pouls JUXI - Guide d'utilisation Windows

## Table des matières
1. [Préparation du matériel](#hardware-preparation)
2. [Connexion matérielle](#hardware-connection)
3. [Configuration de l'environnement logiciel](#software-environment-setup)
4. [Exécution du programme d'exemple](#running-the-example-program)
5. [FAQ](#faq)

---

## Préparation du matériel

### Matériel requis

| Élément | Description |
|------|-------------|
| Capteur JUXI_HeartRate_SPO2 | Module oxymètre de pouls |
| Module USB vers TTL | CH340 / CP2102 / FT232, etc. |
| Câbles Dupont | 4 pièces (femelle-femelle) |
| Ordinateur Windows | Win7/Win10/Win11 |

---

## Connexion matérielle

### Méthode de câblage

| Broche du capteur | Broche du module USB vers TTL | Description |
|-----------|---------------|-------------|
| **VCC** | 3.3V ou 5V | Pôle positif de l'alimentation |
| **GND** | GND | Pôle négatif de l'alimentation |
| **TX** | RX | Émission du capteur → réception du module |
| **RX** | TX | Réception du capteur → émission du module |

![Connexion au PC](../../en/03-windows/Connect%20PC.png)

⚠️ **Conseils importants** :

1. **Placez le commutateur DIP du module en position UART !!!**
2. **Les broches TX et RX doivent être croisées !**
3. Le capteur accepte aussi bien 3.3V que 5V, ne vous trompez pas de tension
4. Câblez toutes les liaisons d'abord, puis branchez l'USB sur l'ordinateur

### Schéma de câblage

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

## Configuration de l'environnement logiciel

### 1. Installer les pilotes

Selon le modèle de puce de votre module USB vers TTL, installez le pilote correspondant :

- **CH340** : https://sparks.gogo.co.nz/ch340.html
- **CP2102** : https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers
- **FT232** : https://ftdichip.com/drivers/vcp-drivers/

Après l'installation, branchez le module USB vers TTL.

### 2. Identifier le port COM

#### Méthode 1 : Gestionnaire de périphériques
1. Appuyez sur `Win + X`, sélectionnez « Gestionnaire de périphériques »
2. Développez « Ports (COM et LPT) »
3. Notez le numéro de port COM correspondant à votre module USB vers TTL (par exemple COM3)

#### Méthode 2 : détection automatique par le programme
Lors de l'exécution du programme d'exemple, tous les ports série disponibles sont listés automatiquement.

### 3. Installer les dépendances Python

Ouvrez l'invite de commandes (CMD) ou PowerShell, puis exécutez :

```bash
pip install pyserial
```

---

## Exécution du programme d'exemple

### Emplacement des fichiers

```
JUXI_HeartRate_SPO2/python/windows/
├── gain_heartbeat_SPO2.py  ← Main program (run this)
├── JUXI_HeartRate_SPO2_Windows.py
├── JUXI_RTU_Windows.py
└── README.md                ← This file
```

### Étapes d'exécution

1. **Vérifiez que le câblage est correct**
   - VCC → 3.3V/5V
   - GND → GND
   - TX → RX (croisé)
   - RX → TX (croisé)

2. **Branchez l'USB sur l'ordinateur**

3. **Lancez le programme**
   ```bash
   cd D:\JUXI_HeartRate_SPO2\python\windows
   python gain_heartbeat_SPO2.py
   ```

4. **Suivez les invites**
   
   - Le programme liste tous les ports série disponibles
   - Saisissez votre numéro de port COM (par exemple COM3)
   - Le programme détecte automatiquement le capteur et démarre la mesure

### Sortie attendue

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

Appuyez sur `Ctrl + C` pour arrêter le programme.

---

## Description des fonctions du programme

### API principale

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

### Q1 : Le port COM est introuvable ?

**R :**

1. Vérifiez que le module USB vers TTL est correctement branché
2. Réinstallez le pilote
3. Essayez un autre port USB
4. Recherchez les « Périphériques inconnus » dans le Gestionnaire de périphériques

### Q2 : L'initialisation du capteur échoue ?

**R :**

1. Vérifiez le câblage :
   - VCC et GND sont-ils correctement reliés ?
   - **Les broches TX et RX sont-elles croisées ?** (cause la plus fréquente)
2. Vérifiez que le débit en bauds est bien 9600
3. Vérifiez que le module USB vers TTL fonctionne correctement
4. Rebranchez l'USB

### Q3 : Les données affichent toujours -1 ?

**R :**
1. Vérifiez que le doigt est correctement posé sur le capteur (en couvrant entièrement la zone des LED)
2. Gardez le doigt immobile, ne bougez pas
3. Attendez quelques secondes que les données se stabilisent
4. Vérifiez que la LED du capteur est allumée

### Q4 : La LED ne s'allume pas alors que la communication fonctionne ?

**R :**

- Il peut s'agir d'un problème matériel de la LED, mais le capteur fonctionne normalement
- Tant que les données sont normales, une LED éteinte peut être ignorée

### Q5 : Le port série est occupé ?

**R :**
1. Fermez les autres logiciels série (assistant série, IDE Arduino, etc.)
2. Vérifiez si d'autres programmes Python sont en cours d'exécution
3. Rebranchez l'USB

### Q6 : Les données sont imprécises ?

**R :**
1. Assurez-vous que le doigt couvre entièrement la zone optique du capteur
2. Restez calme pendant la mesure, ne parlez pas et ne bougez pas
3. Attendez plus de 30 secondes que les données se stabilisent
4. Effectuez plusieurs mesures et faites la moyenne

---

## Spécifications techniques

| Paramètre | Spécification |
|-----------|--------------|
| Communication | UART (niveau TTL) |
| Débit en bauds | 9600 bps (par défaut) |
| Format des données | 8N1 (8 bits de données, sans parité, 1 bit d'arrêt) |
| Alimentation | 3.3V / 5V |
| Plage SPO2 | 35% - 100% |
| Plage de fréquence cardiaque | 30 - 250 BPM |
| Adresse Modbus | 0x20 |

---

## Description des registres Modbus

| Adresse du registre | Fonction | Description |
|-----------------|----------|-------------|
| 0x02 | ID de l'appareil | Lecture : renvoie 0x0020 |
| 0x06-0x09 | Données de fréquence cardiaque et de SPO2 | Lecture : SPO2 + fréquence cardiaque |
| 0x0A | Température | Lecture : température intégrée |
| 0x10 | Commande d'acquisition | Écriture : 0x0001=démarrage, 0x0002=arrêt |

---

## Nous contacter

Pour toute question ou suggestion, rendez-vous sur :
- GitHub : https://github.com/Juxi-Technology/JUXI_HeartRate_SPO2

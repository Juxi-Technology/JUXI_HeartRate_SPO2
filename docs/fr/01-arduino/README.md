[English](../../en/01-arduino/README.md) | [Deutsch](../../de/01-arduino/README.md) | [Español](../../es/01-arduino/README.md) | Français | [Italiano](../../it/01-arduino/README.md) | [日本語](../../ja/01-arduino/README.md) | [한국어](../../ko/01-arduino/README.md) | [Português (BR)](../../pt-br/01-arduino/README.md) | [Português (PT)](../../pt-pt/01-arduino/README.md) | [简体中文](../../zh-hans/01-arduino/README.md) | [繁體中文](../../zh-hant/01-arduino/README.md)

# Tutoriel du capteur oxymètre de pouls JUXI_HeartRate_SPO2

## Table des matières
1. [Présentation du capteur](#sensor-introduction)
2. [Tutoriel Arduino](#arduino-tutorial)
3. [Tutoriel Python (Raspberry Pi)](#python-raspberry-pi-tutorial)
4. [FAQ](#faq)

---

## Présentation du capteur

JUXI_HeartRate_SPO2 est un module capteur de fréquence cardiaque et de saturation en oxygène du sang (SpO2) basé sur la puce MAX30102. Il embarque un algorithme capable de fournir directement les valeurs de fréquence cardiaque et de saturation en oxygène.

**Caractéristiques principales :**

- Mesure de la saturation en oxygène du sang (SPO2)
- Mesure de la fréquence cardiaque (battements par minute)
- Mesure de la température intégrée
- Prise en charge de la communication I2C

---

## Tutoriel Arduino

### 1. Préparation du matériel

| Matériel requis |
|-------------------|
| Carte de développement Arduino (Uno/Nano/ESP32, etc.) |
| Capteur JUXI_HeartRate_SPO2 |
| Quelques câbles Dupont |
| Câble de données USB (pour relier l'Arduino à l'ordinateur) |

### 2. Installation de la bibliothèque

1. Téléchargez le fichier de cette bibliothèque
2. Copiez le dossier `JUXI_HeartRate_SPO2` dans le répertoire des bibliothèques Arduino :
   - Windows : `C:\Users\Username\Documents\Arduino\libraries\`
   - Mac : `~/Documents/Arduino/libraries/`
   - Linux : `~/Arduino/libraries/`
3. Redémarrez l'IDE Arduino

### 3. Exemple de code

**Remarque : lors du téléversement du code, reliez uniquement l'Arduino à l'ordinateur ; ne connectez PAS le module oxymètre de pouls à l'Arduino !!!**

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

##### Connexion matérielle

Communication I2C

| Broche du capteur | Arduino |
|-----------|---------|
| VCC       | 5V/3.3V |
| GND       | GND     |
| SDA       | SDA/A4  |
| SCL       | SCL/A5  |

![IIC](../../en/01-arduino/img/IIC.png)

![8](../../en/01-arduino/img/8.png)

- Placez le commutateur DIP du module oxymètre de pouls en position I2C !!!
- Utilisez le câble de données pour relier l'Arduino à l'ordinateur

#### Résultats d'exécution :

1. Ouvrez Arduino - Outils - Moniteur série

   Réglez le débit en bauds sur 9600

![1](../../en/01-arduino/img/1.png)

2. Ouvrez l'assistant de débogage série

[Serial Debug Assistant uartassist5.15.zip](https://juxitech.feishu.cn/wiki/BJlfwSQydi7u5lkRDQ6cV4dvnBd)

Sélectionnez le numéro de port série

Réglez le débit en bauds sur `9600`

Bits de données `8`, bits d'arrêt `1`, parité `NONE`, contrôle de flux `NONE`

Pour les paramètres de réception et d'émission, sélectionnez `ASCII`

![2](../../en/01-arduino/img/2.png)

### 4. Description de l'API

| Fonction | Description |
|----------|-------------|
| `begin()` | Initialise le capteur, renvoie true/false |
| `getHeartbeatSPO2()` | Lit les données de fréquence cardiaque et de SPO2, stockées dans la structure `_sHeartbeatSPO2` |
| `getTemperature_C()` | Lit la température intégrée (en degrés Celsius) |
| `sensorStartCollect()` | Démarre l'acquisition des données (la LED du capteur s'allume) |
| `sensorEndCollect()` | Arrête l'acquisition des données (la LED du capteur s'éteint) |

### 5. Description des données

- **SPO2 (saturation en oxygène du sang)** : plage normale 95% - 100%, la valeur -1 indique une mesure invalide
- **Heartbeat (fréquence cardiaque)** : plage normale 60 - 100 BPM, la valeur -1 indique une mesure invalide
- **Causes d'une valeur invalide** : doigt mal positionné ou données non stabilisées

---

## Remarques d'utilisation

### Conseils de mesure

1. **Bonne position du doigt**
   - Posez le doigt délicatement sur le capteur, en couvrant les deux LED
   - N'appuyez pas fort, afin de ne pas perturber la circulation sanguine
   - Gardez le doigt immobile, ne bougez pas

2. **Attendre la stabilisation des données**
   - Les valeurs peuvent être instables au début de la mesure
   - Il est conseillé d'attendre 10 à 30 secondes que les données se stabilisent avant de les lire
   - Le capteur actualise les données toutes les 4 secondes

3. **Conditions ambiantes**
   - Évitez toute lumière forte directe sur le capteur
   - Maintenez une température ambiante adaptée
   - Restez calme pendant la mesure

### Interprétation des données

| Plage SPO2 | Description |
|-----------|-------------|
| 95% - 100% | Normal |
| 90% - 94% | Hypoxie légère |
| < 90% | Hypoxie, consultez un médecin |

| Plage de fréquence cardiaque | Description |
|-----------------|-------------|
| 60 - 100 BPM | Plage normale chez l'adulte |
| < 60 BPM | Bradycardie |
| > 100 BPM | Tachycardie |

---

## FAQ

### Q1 : L'initialisation du capteur échoue ?

**R :**
1. Vérifiez que le câblage est correct (SDA sur GPIO2/A4, SCL sur GPIO3/A5)
2. Vérifiez que l'alimentation est correcte (3.3V ou 5V)
3. Utilisez la commande `i2cdetect -y 1` pour détecter le périphérique
4. Assurez-vous que le commutateur DIP du capteur est en position IIC

### Q2 : Les données affichent toujours -1 ?

**R :**
1. Vérifiez que le doigt est correctement posé sur le capteur
2. Attendez quelques secondes que les données se stabilisent
3. Vérifiez que `sensorStartCollect()` a bien été appelée pour démarrer l'acquisition
4. Vérifiez que le voyant du capteur est allumé

### Q3 : Les données sont imprécises ?

**R :**
1. Assurez-vous que le doigt couvre entièrement la zone optique du capteur
2. Gardez le doigt immobile, ne bougez pas
3. Attendez plus de 30 secondes que les données se stabilisent
4. Effectuez plusieurs mesures et faites la moyenne

### Q4 : Quelles cartes de développement Arduino sont prises en charge ?

**R :** Cartes prises en charge :
- Arduino Uno/Nano/Mega
- ESP8266
- ESP32
- Autres cartes de développement compatibles avec l'environnement Arduino

---

## Emplacement des fichiers d'exemple

### Exemples Arduino
```
JUXI_HeartRate_SPO2/
└── examples/
    └── gainHeartbeatSPO2/
        └── gainHeartbeatSPO2.ino
```


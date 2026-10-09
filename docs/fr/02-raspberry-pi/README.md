[English](../../en/02-raspberry-pi/README.md) | [Deutsch](../../de/02-raspberry-pi/README.md) | [Español](../../es/02-raspberry-pi/README.md) | Français | [Italiano](../../it/02-raspberry-pi/README.md) | [日本語](../../ja/02-raspberry-pi/README.md) | [한국어](../../ko/02-raspberry-pi/README.md) | [Português (BR)](../../pt-br/02-raspberry-pi/README.md) | [Português (PT)](../../pt-pt/02-raspberry-pi/README.md) | [简体中文](../../zh-hans/02-raspberry-pi/README.md) | [繁體中文](../../zh-hant/02-raspberry-pi/README.md)

# Tutoriel Raspberry Pi pour JUXI_HeartRate_SPO2


## Table des matières

1. [Présentation](#introduction)
2. [Matériel requis](#hardware-requirements)
3. [Connexions matérielles](#hardware-connections)
4. [Configuration de l'environnement](#environment-setup)
5. [Utilisation de l'exemple de code](#example-code-usage)
6. [Référence de l'API](#api-reference)
7. [FAQ](#faq)
8. [Remarques importantes](#important-notes)

---

## Présentation

JUXI_HeartRate_SPO2 est un module capteur de fréquence cardiaque et de saturation en oxygène du sang basé sur la puce MAX30102. Il embarque des algorithmes capables de fournir directement les valeurs de fréquence cardiaque et de saturation en oxygène.

**Caractéristiques principales :**
- Mesure de la saturation en oxygène du sang (SPO2)
- Mesure de la fréquence cardiaque (battements par minute)
- Mesure de la température intégrée
- Prise en charge des communications UART et I2C

---

## Matériel requis

| Élément requis | Description |
|--------------|-------------|
| Raspberry Pi (2/3/4/Zero) | Raspberry Pi 3B+ ou 4B recommandé |
| Capteur JUXI_HeartRate_SPO2 | Module capteur de fréquence cardiaque et de saturation en oxygène |
| Câbles Dupont | 4 câbles de liaison femelle-femelle |
| Adaptateur secteur | Alimentation pour Raspberry Pi |

---

## Connexions matérielles

### Méthode 1 : communication I2C (recommandée)

La communication I2C se câble simplement et est recommandée.

| Broche du capteur | Broche physique du Raspberry Pi | Numéro BCM | Description |
|-----------|--------------------------|-----------|-------------|
| VCC | 1 ou 17 | - | Alimentation 3.3V (5V également possible) |
| GND | 6 ou 9 ou 14 | - | Masse |
| SDA | 3 | GPIO2 | Ligne de données I2C |
| SCL | 5 | GPIO3 | Ligne d'horloge I2C |

**Important :** placez le commutateur du capteur en position **IIC** !

### Méthode 2 : communication série UART

La communication UART nécessite un croisement des liaisons.

| Broche du capteur | Broche physique du Raspberry Pi | Numéro BCM | Description |
|-----------|--------------------------|-----------|-------------|
| VCC | 2 ou 4 | - | Alimentation 5V (3.3V également possible) |
| GND | 6 ou 9 ou 14 | - | Masse |
| RX | 8 | GPIO14 | Le RX du capteur se relie au TX du Raspberry Pi |
| TX | 10 | GPIO15 | Le TX du capteur se relie au RX du Raspberry Pi |

**Important :** placez le commutateur du capteur en position **UART** !

![Schéma des broches du Raspberry Pi](../../en/02-raspberry-pi/Raspberry%20Pi%20Pin%20Diagram.png)

---

## Configuration de l'environnement

### 1. Activer I2C (nécessaire en mode I2C)

```bash
sudo raspi-config
```

Sélectionnez `Interface Options` → `I2C` → choisissez `Yes` pour activer

Redémarrez le Raspberry Pi :
```bash
sudo reboot
```

### 2. Activer le port série (nécessaire en mode UART)

```bash
sudo raspi-config
```

Sélectionnez `Interface Options` → `Serial`

- Première question : « Would you like a login shell to be accessible over serial? » → sélectionnez `No`
- Deuxième question : « Would you like the serial port hardware to be enabled? » → sélectionnez `Yes`

Redémarrez le Raspberry Pi :
```bash
sudo reboot
```

### 3. Installer les dépendances

```bash
# Update package lists
sudo apt-get update

# Install I2C tools and smbus2 library (smbus2 is required for I2C mode)
sudo apt-get install -y i2c-tools python3-smbus2

# Install pyserial (for serial port support)
sudo pip3 install pyserial
```

> **Remarque :** le mode I2C nécessite `smbus2` — le paquet historique `python-smbus` ne suffit pas.
> La bibliothèque utilise `smbus2.i2c_msg` pour effectuer deux transactions I2C indépendantes (écriture de
> l'adresse de registre avec STOP, puis une nouvelle transaction de lecture pour lire plusieurs octets en séquence),
> conformément au timing I2C requis par la puce du capteur.

### 4. Vérifier la connexion I2C (mode I2C)

Après le câblage, exécutez la commande suivante pour détecter les périphériques I2C :

```bash
i2cdetect -y 1
```

Si l'adresse `0x57` apparaît, le capteur est correctement connecté.

---

## Utilisation de l'exemple de code

### Arborescence des fichiers

```
python/raspberry/
├── JUXI_HeartRate_SPO2.py      # Main library file
└── examples/
    ├── i2c_example.py          # I2C mode example
    └── uart_example.py         # UART mode example
```

### Exécution de l'exemple en mode I2C

```bash
cd python/raspberry/examples
sudo python3 i2c_example.py
```

### Exécution de l'exemple en mode UART

```bash
cd python/raspberry/examples
sudo python3 uart_example.py
```

**Remarque :** les droits `sudo` sont nécessaires pour accéder au port série matériel.

### Sortie attendue

Si tout fonctionne correctement, vous obtiendrez une sortie semblable à :

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

Appuyez sur `Ctrl+C` pour arrêter le programme.

---

## Référence de l'API

### Classe : JUXI_HeartRate_SPO2_i2c

Classe du capteur pour la communication I2C.

#### Constructeur
```python
JUXI_HeartRate_SPO2_i2c(bus_number=1, i2c_address=0x57)
```

Paramètres :
- `bus_number` : numéro du bus I2C, généralement 1 sur Raspberry Pi
- `i2c_address` : adresse I2C du capteur, 0x57 par défaut

#### Méthodes

| Méthode | Description | Valeur de retour |
|--------|-------------|--------------|
| `begin()` | Initialise le capteur et vérifie la connexion | bool (True en cas de succès) |
| `sensor_start_collect()` | Démarre l'acquisition des données (LED du capteur allumée) | None |
| `sensor_end_collect()` | Arrête l'acquisition des données (LED du capteur éteinte) | None |
| `get_heartbeat_SPO2()` | Lit les données de fréquence cardiaque et de SPO2 | None (résultats stockés dans les propriétés de l'objet) |
| `get_temperature_c()` | Lit la température intégrée | float (Celsius) |
| `close()` | Ferme la connexion I2C | None |

#### Propriétés

| Propriété | Description |
|----------|-------------|
| `SPO2` | Saturation en oxygène du sang (%), -1 pour une valeur invalide |
| `heartbeat` | Fréquence cardiaque (battements par minute), -1 pour une valeur invalide |

---

### Classe : JUXI_HeartRate_SPO2_uart

Classe du capteur pour la communication série UART.

#### Constructeur
```python
JUXI_HeartRate_SPO2_uart(port='/dev/serial0', baudrate=9600)
```

Paramètres :
- `port` : chemin du périphérique série, `/dev/serial0` par défaut sur Raspberry Pi
- `baudrate` : débit en bauds, 9600 par défaut

#### Méthodes

Identiques à celles de `JUXI_HeartRate_SPO2_i2c`.

---

## FAQ

### Q1 : Que faire si l'initialisation du capteur échoue ?

**R :** suivez ces étapes :

1. **Vérifier le câblage**
   - Mode I2C : vérifiez que SDA est relié à GPIO2 et SCL à GPIO3
   - Mode UART : vérifiez le croisement RX-TX

2. **Vérifier le commutateur du capteur**
   - Mode I2C : le commutateur doit être en position IIC
   - Mode UART : le commutateur doit être en position UART

3. **Vérifier l'alimentation**
   - Vérifiez que VCC est relié à 3.3V ou 5V
   - Vérifiez que GND est relié

4. **Vérifier les paramètres système**
   - Mode I2C : vérifiez que I2C est activé
   - Mode UART : vérifiez que le port série est activé

5. **Utiliser les commandes de détection**
   ```bash
   # I2C mode
   i2cdetect -y 1
   
   # UART mode
   ls /dev/serial*
   ```

### Q2 : Les données affichent toujours -1, que faire ?

**R :**

1. Assurez-vous que votre doigt est correctement posé sur le capteur et couvre entièrement les deux LED
2. Attendez quelques secondes que les données se stabilisent (généralement 10 à 30 secondes)
3. Vérifiez que `sensor_start_collect()` a bien été appelée pour démarrer l'acquisition
4. Vérifiez que la LED du capteur est allumée

### Q3 : Les données sont imprécises, que faire ?

**R :**

1. Assurez-vous que votre doigt couvre entièrement la zone optique du capteur
2. Gardez le doigt immobile, ne bougez pas
3. Attendez plus de 30 secondes que les données se stabilisent
4. Effectuez plusieurs mesures et faites-en la moyenne
5. Évitez toute lumière forte directe sur le capteur

### Q4 : Puis-je utiliser I2C et UART en même temps ?

**R :** non, un seul mode de communication peut être sélectionné à la fois.

### Q5 : Faut-il utiliser sudo pour exécuter le programme ?

**R :**
- Mode I2C : `sudo` est recommandé pour éviter les problèmes de permissions
- Mode UART : `sudo` est obligatoire, sinon le port série est inaccessible

---

## Remarques importantes

### Conseils de mesure

1. **Bonne position du doigt**
   - Posez votre doigt délicatement sur le capteur, en couvrant les deux LED
   - N'appuyez pas trop fort, cela peut perturber la circulation sanguine
   - Gardez le doigt immobile, ne bougez pas

2. **Attendre la stabilisation des données**
   - Les valeurs peuvent être instables au début de la mesure
   - Il est conseillé d'attendre 10 à 30 secondes que les données se stabilisent
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

### Avertissement de sécurité

- Ce capteur est fourni à titre indicatif uniquement et ne remplace pas un équipement médical professionnel
- En cas de problème de santé, consultez rapidement un médecin
- Les résultats de mesure sont indicatifs et ne doivent pas servir au diagnostic


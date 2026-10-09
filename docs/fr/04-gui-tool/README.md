[English](../../en/04-gui-tool/README.md) | [Deutsch](../../de/04-gui-tool/README.md) | [Español](../../es/04-gui-tool/README.md) | Français | [Italiano](../../it/04-gui-tool/README.md) | [日本語](../../ja/04-gui-tool/README.md) | [한국어](../../ko/04-gui-tool/README.md) | [Português (BR)](../../pt-br/04-gui-tool/README.md) | [Português (PT)](../../pt-pt/04-gui-tool/README.md) | [简体中文](../../zh-hans/04-gui-tool/README.md) | [繁體中文](../../zh-hant/04-gui-tool/README.md)

# Module oxymètre de pouls - Guide d'utilisation de l'interface graphique

## 📋 Fonctionnalités

Ceci est un programme graphique de surveillance de la fréquence cardiaque et de la saturation en oxygène du sang, qui offre les fonctionnalités suivantes :

1. ✅ **Sélection du port série** - Détecte automatiquement les ports série disponibles
2. ✅ **Sélection du débit en bauds** - Prend en charge 9600/19200/38400/57600/115200
3. ✅ **Connexion/Déconnexion** - Connexion et déconnexion du module en un clic
4. ✅ **Démarrer/Arrêter l'acquisition** - Contrôle l'allumage et l'extinction de la LED du capteur
5. ✅ **Démarrer/Arrêter la surveillance** - Affichage des données en temps réel
6. ✅ **Affichage des données en temps réel** - Saturation en oxygène, fréquence cardiaque, température
7. ✅ **Bascule anglais / chinois** - Changez la langue de l'interface à tout moment ; l'anglais est la langue par défaut

---

## 🔌 Connexion matérielle

| Module oxymètre de pouls | Module USB vers TTL |
|---------------------------|------------------|
| **VCC** | **5V** (Important ! N'utilisez pas 3.3V) |
| **GND** | **GND** |
| **TX** | **RX** (liaisons croisées) |
| **RX** | **TX** (liaisons croisées) |

⚠️ **Remarque : les broches TX et RX doivent être croisées !**

---

## 🚀 Exécution du programme

### Méthode 1 : exécuter directement le script Python

1. Installez les dépendances :
```bash
pip install pyserial
```

2. Lancez le programme :
```bash
cd 上位机源代码
python HeartRateOximeter.py
```

---

## 📖 Étapes d'utilisation

### Étape 1 : connecter le matériel
1. Reliez le capteur et le module USB vers TTL conformément au tableau de câblage ci-dessus

   VCC -> VCC

   GND -> GND

   RX -> TX

   TX -> RX

2. Branchez le module USB vers TTL sur un port USB de l'ordinateur

### Étape 2 : ouvrir le programme
Lancez `HeartRateOximeter.exe`

### Étape 3 : configurer le port série
1. Sélectionnez le bon port série (par exemple COM3)
2. Sélectionnez le débit en bauds **9600** (par défaut)
3. Cliquez sur le bouton [Connect]

### Étape 4 : démarrer l'acquisition
1. Une fois la connexion réussie, cliquez sur [Start Collection]
2. ✅ La LED du capteur s'allume

### Étape 5 : démarrer la surveillance
1. Posez votre doigt sur le capteur
2. Cliquez sur [Start Monitoring]
3. Consultez les données en temps réel

---

## 📊 Description de l'interface

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

**Sélecteur de langue** : la liste déroulante en haut de la fenêtre permet de basculer l'interface entre l'anglais et le 中文. Le programme démarre en anglais.

---

## 📋 Interprétation des données

| Donnée | Plage normale | Description |
|------|-------------|-------------|
| **SPO2** | 95% - 100% | Consultez un médecin si la valeur est inférieure à 90% |
| **Fréquence cardiaque** | 60 - 100 BPM | Plage normale chez l'adulte |
| **Température** | 25 - 35 °C | Température intégrée au module, et non température corporelle |

**Remarque** : au démarrage ou si le doigt est mal placé, les données peuvent afficher -1, ce qui est normal.

---

## ❓ FAQ

### Q1 : Le port série est introuvable ?
**R :**
1. Vérifiez que le pilote du module USB vers TTL est correctement installé
2. Rebranchez le câble USB
3. Cliquez sur le bouton [Refresh] pour relancer la détection

### Q2 : La connexion a échoué ?
**R :**
1. Vérifiez que le bon port série est sélectionné
2. Vérifiez que le port série n'est pas utilisé par d'autres programmes (par exemple un assistant série ou l'IDE Arduino)
3. Vérifiez que le module USB vers TTL fonctionne correctement

### Q3 : La LED ne s'allume pas après avoir cliqué sur Start Collection ?
**R :**
1. Vérifiez que VCC est bien relié à 5V (et non à 3.3V)
2. Vérifiez que TX et RX sont croisés
3. Vérifiez que le module capteur lui-même n'est pas endommagé

### Q4 : Les données affichent toujours -1 ?
**R :**
1. Vérifiez que [Start Collection] a bien été cliqué
2. Posez correctement le doigt sur le capteur, en couvrant entièrement la zone des LED
3. Gardez le doigt immobile et attendez quelques secondes
4. Vérifiez qu'aucune connexion n'est desserrée

### Q5 : Le programme ne répond plus ?
**R :**
1. Cliquez d'abord sur [Stop Monitoring]
2. Cliquez ensuite sur [Stop Collection]
3. Cliquez enfin sur [Disconnect]
4. Redémarrez le programme

---

## ⚠️ Précautions

1. **Ordre de câblage** : connectez d'abord le capteur, puis branchez l'USB
2. **Ordre de déconnexion** : arrêtez la surveillance, puis l'acquisition, et enfin déconnectez
3. **Alimentation requise** : le capteur doit être alimenté en 5V ; le 3.3V peut ne pas fonctionner correctement
4. **Position du doigt** : le doigt doit couvrir entièrement la zone optique, sans appuyer fort
5. **Environnement** : évitez toute lumière forte directe sur le capteur

---

## 📞 Support technique

En cas de problème, vérifiez les points suivants :
1. Le câblage matériel (en particulier le croisement TX/RX)
2. L'alimentation en 5V
3. Le bon fonctionnement du pilote USB vers TTL
4. Que le port série ne soit pas occupé par d'autres programmes

# Projet Météo Coopérative

Détection de risques climatiques (gel, sécheresse) pour une coopérative agricole, à partir des prévisions météo par zone.

## Fonctionnement

Le programme lit une liste de zones (départements/villes françaises), interroge l'API Open-Meteo pour chacune, détecte les risques de gel et de sécheresse, et génère un fichier récapitulatif des alertes.

## Installation

```bash
pip3 install requests
```

## Lancement

```bash
python3 main.py
```

Le rapport est généré dans `output/alertes.csv`.

## Structure du projet

- `meteo.py` : appel à l'API Open-Meteo
- `zones.py` : gestion des zones (lecture/ajout/suppression/modification)
- `risque.py` : détection des risques (gel/sécheresse)
- `main.py` : orchestration du programme
- `data/zones.json` : données des zones de la coopérative
- `output/alertes.csv` : rapport généré à chaque exécution

## Choix des zones

Les 5 zones présentes dans `data/zones.json` (Amiens, Bordeaux, Marseille, Strasbourg, Tours) sont des données de démonstration représentant différentes régions climatiques de France. Chaque zone correspond à un département où sont regroupés plusieurs des 30 exploitants de la coopérative.

## Ajouter une nouvelle zone

Deux méthodes possibles :

**1. Directement dans le fichier** `data/zones.json`, en ajoutant un nouvel objet avec un id unique :
```json
{
  "id": 6,
  "nom": "Nom de la zone",
  "departement": "Département",
  "ville": "Ville",
  "latitude": 00.0000,
  "longitude": 0.0000
}
```

**2. Via la fonction `ajouter_zone()`** dans `zones.py`, qui calcule automatiquement l'id :
```python
from zones import ajouter_zone
ajouter_zone("Nom", "Département", "Ville", latitude, longitude)
```

## Choix de l'API

Open-Meteo a été choisie car elle est 100% gratuite, sans clé API ni inscription requise (jusqu'à 10 000 appels/jour), contrairement à OpenWeatherMap (clé API requise) ou l'API Météo-France (inscription et souscription nécessaires).

## Améliorations possibles

- Interface web pour la coopérative
- Envoi automatique d'alertes par email
- Détection d'autres risques climatiques (grêle, vent fort)
- Ajout de zones via ligne de commande (argparse)
- Historisation des alertes pour analyse de tendances